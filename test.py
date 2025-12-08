files_to_create = ['accounts','customers','products','plants','contracts','users','orders','order_lines','shipments','invoices','usage_metrics','quality_incidents','oee_metrics','support_tickets','agent_runs','signals','churn_risk_assessments','rca_analysis','churn_briefs','email_drafts','crm_activities','recommendations','llm_prompts','vector_index_metadata','agent_memory']

for file_name in files_to_create:
    class_name = ''.join(word.capitalize() for word in file_name.split('_'))
    base_file_content = f'''from flask import request, Blueprint, jsonify
from database import SessionLocal
from models.base_model import {class_name}

{file_name}_bp = Blueprint("{file_name}", __name__)

@{file_name}_bp.route("/{file_name}", methods=["GET"])
def get_{file_name}():
    db = SessionLocal()
    data = [run.to_dict() for run in db.query({class_name}).all()]
    db.close()
    return jsonify(data), 200

'''

    with open(f"routes/{file_name}_routes.py", "w") as file:
        file.write(base_file_content)