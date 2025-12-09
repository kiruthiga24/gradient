import uuid
import logging
import psycopg2
from datetime import datetime

# =========================
# CONFIGURE LOGGING
# =========================
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s'
)

# =========================
# DATABASE CONNECTION
# =========================
DB_CONFIG = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'admin@123',
    'host': 'localhost',
}

def get_db_connection():
    return psycopg2.connect(
        dbname=DB_CONFIG['dbname'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        host=DB_CONFIG['host']
    )

# =========================
# AGENT RUN HANDLING
# =========================
def create_agent_run():
    agent_run_id = uuid.uuid4()
    logging.info(f"Creating new agent_run entry: {agent_run_id}")

    conn = get_db_connection()
    cur = conn.cursor()

    # Insert only into the required column; run_timestamp has default now()
    cur.execute("""
        INSERT INTO agent_runs (agent_run_id)
        VALUES (%s)
    """, (str(agent_run_id),))  # convert UUID to string

    conn.commit()
    cur.close()
    conn.close()

    logging.info(f"✔️ Agent run created successfully: {agent_run_id}")
    return str(agent_run_id)

# =========================
# SIGNAL INSERTION
# =========================
def insert_signals(signals):
    logging.info(f"Inserting {len(signals)} signals...")

    agent_run_id = create_agent_run()

    conn = get_db_connection()
    cur = conn.cursor()

    for s in signals:
        sql = """
            INSERT INTO signals (
                signal_id,
                agent_run_id,
                account_id,
                signal_type,
                signal_strength
            ) 
            VALUES (%s, %s, %s, %s, %s)
        """

        params = (
            str(uuid.uuid4()),       # signal_id as string
            agent_run_id,            # already string
            str(s['account_id']),    # convert UUID to string
            s['signal_type'],
            s['signal_strength']
        )

        logging.debug(f"Executing INSERT: {params}")
        cur.execute(sql, params)

    conn.commit()
    cur.close()
    conn.close()

    logging.info("✔️ All signals inserted successfully!")

# =========================
# EXAMPLE USAGE
# =========================
def get_existing_account_ids():
    """Fetch all account_ids from accounts table"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT account_id FROM accounts")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    # Return as list of strings
    return [str(r[0]) for r in rows]

if __name__ == "__main__":
    existing_accounts = get_existing_account_ids()
    if len(existing_accounts) < 2:
        raise Exception("Not enough accounts in 'accounts' table for sample signals!")

    # Use actual existing account_ids
    sample_signals = [
        {
            "account_id": existing_accounts[0],
            "signal_type": "buy",
            "signal_strength": 0.85
        },
        {
            "account_id": existing_accounts[1],
            "signal_type": "sell",
            "signal_strength": 0.42
        }
    ]

    insert_signals(sample_signals)

