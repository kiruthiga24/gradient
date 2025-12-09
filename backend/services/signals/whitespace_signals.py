from sqlalchemy import func
from models.base_model import Signals, Orders, OrderLines, Products
from ..utils.base import normalize

def detect_whitespace(db, agent_run_id):
    rows = db.query(
        Orders.account_id,
        Products.product_category
    ).join(OrderLines, Orders.order_id == OrderLines.order_id)\
     .join(Products, Products.product_id == OrderLines.product_id).all()

    grouped = {}
    for acct, cat in rows:
        if cat:
            grouped.setdefault(acct, set()).add(cat)

    cat_pop = db.query(Products.product_category).all()
    cat_counts = {}
    for (c,) in cat_pop:
        cat_counts[c] = cat_counts.get(c, 0) + 1

    results = []
    popular = sorted(cat_counts, key=lambda x: -cat_counts[x])

    for acct, owned in grouped.items():
        missing = [c for c in popular if c not in owned][:3]
        if missing:
            results.append(Signals(
                agent_run_id=agent_run_id,
                account_id=acct,
                signal_type="cross_sell_whitespace",
                signal_strength=normalize(len(missing)/3),
                extras={"missing_categories": missing}
            ))

    db.add_all(results)
    db.commit()
    return results
