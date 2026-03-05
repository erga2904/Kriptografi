"""
Challenge Mode API Routes — generate challenges, check answers, leaderboard.
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.extensions import db
from app.models import ChallengeScore
from app.blueprints.challenges.services import (
    generate_challenge,
    check_answer,
    get_leaderboard,
    CHALLENGES,
)

challenges_bp = Blueprint("challenges", __name__)


@challenges_bp.route("/list", methods=["GET"])
def list_challenges():
    result = {}
    for cid, ch in CHALLENGES.items():
        result[cid] = {
            "name": ch.get("title", cid),
            "difficulty": ch["difficulty"],
            "description": ch["description"],
            "points": ch["points"],
        }
    return jsonify(result)


@challenges_bp.route("/generate", methods=["POST"])
def generate():
    data = request.get_json(silent=True) or {}
    challenge_id = data.get("challenge_id", "caesar_easy_1")
    safe_challenge, plaintext = generate_challenge(challenge_id)
    return jsonify(safe_challenge)


@challenges_bp.route("/check", methods=["POST"])
def check():
    data = request.get_json(silent=True) or {}
    user_answer = data.get("answer", "")
    correct_answer = data.get("correct_answer", "")
    challenge_id = data.get("challenge_id", "")
    time_seconds = data.get("time_seconds", 0)
    hints_used = data.get("hints_used", 0)

    result = check_answer(user_answer, correct_answer)

    if result["correct"] and challenge_id in CHALLENGES:
        ch = CHALLENGES[challenge_id]
        base_points = ch["points"]
        penalty = hints_used * (base_points * 0.15)
        time_bonus = max(0, 30 - time_seconds) * 2
        score = max(0, int(base_points - penalty + time_bonus))

        username = "Anonim"
        user_id = None
        if current_user.is_authenticated:
            username = current_user.username
            user_id = current_user.id

        entry = ChallengeScore(
            challenge_id=challenge_id,
            difficulty=ch["difficulty"],
            username=username,
            hints_used=hints_used,
            time_seconds=time_seconds,
            solved=True,
        )
        entry.score = score
        if user_id:
            entry.user_id = user_id
        db.session.add(entry)
        db.session.commit()

        result["score"] = score
        result["base_points"] = base_points

    return jsonify(result)


@challenges_bp.route("/leaderboard", methods=["GET"])
def leaderboard():
    limit = request.args.get("limit", 20, type=int)
    return jsonify(get_leaderboard(limit))
