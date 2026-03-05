"""
Benchmark API Routes — performance comparison of algorithms.
"""
from flask import Blueprint, request, jsonify
from app.blueprints.benchmark.services import run_benchmark

benchmark_bp = Blueprint("benchmark", __name__)


@benchmark_bp.route("/run", methods=["POST"])
def run():
    data = request.get_json(silent=True) or {}

    text_sizes = data.get("text_sizes", [100, 500, 1000, 5000])
    iterations = int(data.get("iterations", 3))
    iterations = max(1, min(iterations, 20))

    # Validate text sizes
    if not isinstance(text_sizes, list):
        text_sizes = [100, 500, 1000, 5000]
    text_sizes = [max(10, min(int(s), 50000)) for s in text_sizes[:8]]

    result = run_benchmark(text_sizes, iterations)
    return jsonify(result)
