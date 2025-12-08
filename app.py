from flask import Flask
from routes.health import test_bp
from routes.accounts_routes import accounts_bp
from routes.customers_routes import customers_bp
from routes.products_routes import products_bp
from routes.plants_routes import plants_bp
from routes.contracts_routes import contracts_bp
from routes.users_routes import users_bp
from routes.orders_routes import orders_bp
from routes.order_lines_routes import order_lines_bp
from routes.shipments_routes import shipments_bp
from routes.invoices_routes import invoices_bp
from routes.usage_metrics_routes import usage_metrics_bp
from routes.quality_incidents_routes import quality_incidents_bp
from routes.oee_metrics_routes import oee_metrics_bp
from routes.support_tickets_routes import support_tickets_bp
from routes.agent_runs_routes import agent_runs_bp
from routes.signals_routes import signals_bp
# from routes.churn_routes import churn_bp
# from routes.expansion_routes import expansion_bp
# from routes.quality_routes import quality_bp
# from routes.shipment_routes import shipment_bp
# from routes.qbr_routes import qbr_bp

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(test_bp)
app.register_blueprint(accounts_bp)
app.register_blueprint(customers_bp)
app.register_blueprint(products_bp)
app.register_blueprint(plants_bp)
app.register_blueprint(contracts_bp)
app.register_blueprint(users_bp)
app.register_blueprint(orders_bp)
app.register_blueprint(order_lines_bp)
app.register_blueprint(shipments_bp)
app.register_blueprint(invoices_bp)
app.register_blueprint(usage_metrics_bp)
app.register_blueprint(quality_incidents_bp)
app.register_blueprint(oee_metrics_bp)
app.register_blueprint(support_tickets_bp)
app.register_blueprint(agent_runs_bp)
app.register_blueprint(signals_bp)
# app.register_blueprint(churn_bp)
# app.register_blueprint(expansion_bp)
# app.register_blueprint(quality_bp)
# app.register_blueprint(shipment_bp)
# app.register_blueprint(qbr_bp)

if __name__ == "__main__":
    app.run(port=5000, debug=True)        # Backend runs here
