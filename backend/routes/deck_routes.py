from flask import Blueprint, request, send_file, jsonify
from utils.logger import logger
from utils.deck_generator import *
import uuid
import os

deck_bp = Blueprint("ppt", __name__)

@deck_bp.route("/agent/action/download-deck", methods=["POST"])
def generate_ppt():
    logger.info("Received request to generate DECK")

    # content = request.json.get("content")
    content = request.get_json()
    if not content:
        return jsonify({"error": "content is required"}), 400

    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    decks_dir = os.path.join(BASE_DIR, "generated_decks")
    os.makedirs(decks_dir, exist_ok=True)

    file_name = f"deck_{uuid.uuid4()}.pptx"
    file_path = os.path.join("generated_decks", file_name)


    os.makedirs("generated_decks", exist_ok=True)

    output = generate_deck(content, file_path)

    return send_file(
        output, 
        as_attachment=True,
        mimetype="application/vnd.openxmlformats-officedocument.presentationml.presentation"
    )