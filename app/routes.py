from flask import Blueprint, request, jsonify
from app.utils import run_pipeline

bp = Blueprint('routes', __name__)

@bp.route("/start", methods=["POST"])
def start_pipeline():
    try:
        run_pipeline()
        return jsonify({"status": "done"})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)})
