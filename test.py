files_to_create = ['accounts','customers','products','plants','contracts','users','orders','order_lines','shipments','invoices','usage_metrics','quality_incidents','oee_metrics','support_tickets','agent_runs','signals','churn_risk_assessments','rca_analysis','churn_briefs','email_drafts','crm_activities','recommendations','llm_prompts','vector_index_metadata','agent_memory']

for file_name in files_to_create:
    base_file_content = f'''from flask import request, Blueprint, jsonify
from backend.models.base_model import fetch_all, insert_record

{file_name}_bp = Blueprint("{file_name}", __name__)

@{file_name}_bp.route("/{file_name}", methods=["GET"])
def get_{file_name}():
    data = fetch_all("{file_name}")
    return jsonify(data), 200

@{file_name}_bp.route("/{file_name}", methods=["POST"])
def create_{file_name}():
    data = request.json
    created = insert_record("{file_name}", data)
    return jsonify({{"status": "success", "inserted": created}}), 201
    

'''

    with open(f"routes/{file_name}_routes.py", "w") as file:
        file.write(base_file_content)