files_to_create = ["customers","products","plants","contracts","users","orders","order_lines","shipments","invoices","usage_metrics","quality_incidents","oee_metrics","support_tickets","agent_runs","signals"]

for file_name in files_to_create:
    base_file_content = f'''from flask import Blueprint, jsonify
from backend.models.base_model import fetch_all

{file_name}_bp = Blueprint("{file_name}", __name__)

@{file_name}_bp.route("/{file_name}", methods=["GET"])
def get_accounts():
    data = fetch_all("{file_name}")
    return jsonify(data), 200
'''

    with open(f"routes/{file_name}_routes.py", "w") as file:
        file.write(base_file_content)