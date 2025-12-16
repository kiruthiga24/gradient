from flask import Flask, request, jsonify
from flask_cors import CORS
import traceback
from orchestrator import LLMOrchestrator

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Initialize orchestrator once at startup
orchestrator = LLMOrchestrator()

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "LLM Orchestrator"})

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON payload received"}), 400

        # Extract required fields with defaults
        account_name = data.get("account_name")
        signals = data.get("signals")
        raw_tables = data.get("raw_tables", {})
        summary_stats = data.get("summary_stats", {})
        business_rules = data.get("business_rules", {})

        # Validate required fields
        if not account_name:
            return jsonify({"error": "Missing required field: account_name"}), 400
        if not signals:
            return jsonify({"error": "Missing required field: signals"}), 400

        # Run full pipeline
        result = orchestrator.run_pipeline(data)
        
        return jsonify({
            "success": True,
            "data": result,
            "account_name": account_name
        })

    except Exception as e:
        print(f"Error in /analyze: {str(e)}")
        traceback.print_exc()
        return jsonify({
            "success": False, 
            "error": str(e)
        }), 500

@app.route("/docs", methods=["GET"])
def docs():
    """API documentation endpoint"""
    return jsonify({
        "endpoints": {
            "/health": "GET - Health check",
            "/analyze": {
                "method": "POST",
                "payload": {
                    "account_name": "str (required)",
                    "signals": "list (required)", 
                    "raw_tables": "dict (optional)",
                    "summary_stats": "dict (optional)",
                    "business_rules": "dict (optional)"
                },
                "response": {
                    "rca": "dict",
                    "brief": "dict", 
                    "actions": "dict",
                    "email": "dict"
                }
            }
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
