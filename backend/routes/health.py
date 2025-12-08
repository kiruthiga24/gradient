from flask import Blueprint, jsonify
test_bp = Blueprint('test', __name__)

@test_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "Backend Running"}), 200
