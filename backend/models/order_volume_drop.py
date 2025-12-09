#!/usr/bin/env python3
import os
import uuid
import logging
from datetime import datetime, timedelta
import json
import math
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

load_dotenv()



# detection windows
RECENT_DAYS = 30
BASELINE_DAYS = 90
ORDER_DROP_THRESHOLD = 0.25  # 25% drop triggers signal

# logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


# -------------------------
# DB helpers
# -------------------------
def get_conn():
    # Directly pass credentials to psycopg2.connect
    return psycopg2.connect(
        host='localhost',
        port=5432,
        dbname='postgres',
        user='postgres',
        password='admin@123'
    )


def fetch_table(conn, sql, params=None):
    return pd.read_sql(sql, conn, params=params)


def now_ts():
    return datetime.utcnow()


def uid():
    return str(uuid.uuid4())


def normalize_score(value, min_val=0.0, max_val=1.0):
    if math.isnan(value) or value is None:
        return 0.0
    v = float(value)
    if v <= min_val:
        return 0.0
    if v >= max_val:
        return 1.0
    return (v - min_val) / (max_val - min_val)


# -------------------------
# Signal detection
# -------------------------
def detect_order_volume_drop(conn, agent_run_id):
    logging.info("Detecting order volume drops...")
    sql = f"""
    SELECT account_id,
           order_date,
           SUM(total_amount) AS daily_amount
    FROM orders
    WHERE order_date >= CURRENT_DATE - INTERVAL '{BASELINE_DAYS} days'
    GROUP BY account_id, order_date
    """
    df = fetch_table(conn, sql)
    if df.empty:
        logging.info("No orders found in baseline window.")
        return []

    results = []
    for account_id, g in df.groupby("account_id"):
        baseline_cutoff = (datetime.utcnow().date() - timedelta(days=RECENT_DAYS))
        baseline_df = g[g["order_date"] < baseline_cutoff]
        recent_df = g[g["order_date"] >= baseline_cutoff]
        baseline_avg = baseline_df["daily_amount"].mean() if not baseline_df.empty else g["daily_amount"].mean()
        recent_avg = recent_df["daily_amount"].mean() if not recent_df.empty else 0.0

        drop_pct = max(0.0, (baseline_avg - recent_avg) / baseline_avg) if baseline_avg else 0.0
        strength = normalize_score(drop_pct)
        extras = {"baseline_avg": float(baseline_avg or 0.0), "recent_avg": float(recent_avg or 0.0), "drop_pct": drop_pct}

        if drop_pct >= ORDER_DROP_THRESHOLD:
            results.append({
                "signal_id": uid(),
                "agent_run_id": agent_run_id,
                "account_id": account_id,
                "signal_type": "order_volume_drop",
                "signal_strength": round(strength, 4),
                "detected_at": now_ts(),
                "extras": json.dumps(extras)
            })

    logging.info("Order volume detection complete: %d signals", len(results))
    return results


# -------------------------
# DB write helpers
# -------------------------
def insert_signals(conn, signals_rows):
    if not signals_rows:
        return
    cols = ("signal_id", "agent_run_id", "account_id", "signal_type", "signal_strength", "detected_at", "extras")
    values = [[r[c] for c in cols] for r in signals_rows]
    insert_sql = f"INSERT INTO signals ({', '.join(cols)}) VALUES %s"
    with conn.cursor() as cur:
        execute_values(cur, insert_sql, values)
    conn.commit()
    logging.info("Inserted %d signals", len(signals_rows))


def insert_agent_run(conn, run_id, run_type="scheduled", status="completed"):
    sql = "INSERT INTO agent_runs (agent_run_id, run_timestamp, run_type, status) VALUES (%s, %s, %s, %s)"
    with conn.cursor() as cur:
        cur.execute(sql, (run_id, now_ts(), run_type, status))
    conn.commit()


def insert_churn_assessments(conn, signals_rows):
    churn_types = {"order_volume_drop"}
    rows = []
    for s in signals_rows:
        if s["signal_type"] in churn_types:
            risk_score = float(s["signal_strength"])
            risk_level = "High" if risk_score >= 0.7 else ("Medium" if risk_score >= 0.4 else "Low")
            rows.append((
                uid(),
                s["signal_id"],
                s["account_id"],
                round(risk_score, 4),
                risk_level,
                now_ts()
            ))
    if not rows:
        return
    insert_sql = """
    INSERT INTO churn_risk_assessments (assessment_id, signal_id, account_id, risk_score, risk_level, assessed_at)
    VALUES %s
    """
    with conn.cursor() as cur:
        execute_values(cur, insert_sql, rows)
    conn.commit()
    logging.info("Inserted %d churn assessments", len(rows))


# -------------------------
# Main orchestration
# -------------------------
def run_all_signals():
    conn = get_conn()
    run_id = uid()
    logging.info("Starting agent run %s", run_id)
    try:
        insert_agent_run(conn, run_id, run_type="scheduled", status="running")
        all_signals = detect_order_volume_drop(conn, run_id)
        insert_signals(conn, all_signals)
        insert_churn_assessments(conn, all_signals)

        with conn.cursor() as cur:
            cur.execute(
                "UPDATE agent_runs SET status = %s WHERE agent_run_id = %s",
                ("completed", run_id)
            )
        conn.commit()

    except Exception as e:
        logging.exception("Agent run failed: %s", str(e))
        conn.rollback()  # <-- reset failed transaction

        with conn.cursor() as cur:
            cur.execute(
                "UPDATE agent_runs SET status = %s WHERE agent_run_id = %s",
                ("failed", run_id)
            )
        conn.commit()

    finally:
        conn.close()




if __name__ == "__main__":
    run_all_signals()
