from flask import Blueprint, jsonify, request, send_from_directory
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request, get_jwt
from app.tasks.export_csv import export_user_quiz_details
from functools import wraps
import os
from app import limiter
from app import cache
from datetime import datetime, timezone
from app.model.models import *

user = Blueprint('user', __name__)

def user_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            claims = get_jwt()
            identity = get_jwt_identity()

            if claims.get("role") != "user":
                return jsonify({"msg": "Users only!"}), 403
        except Exception as e:
            print("JWT Error:", e)
            return jsonify({"msg": "Invalid or missing token"}), 401
        return fn(*args, **kwargs)
    return wrapper

# -------- USER INFO --------

@user.get('/info')
@user_required
def get_user_info():
    try:
        user_id = get_jwt_identity()
        user_obj = User.query.get(user_id)

        if not user_obj:
            return jsonify({'msg': 'User not found'}), 404

        return jsonify({
            'id': user_obj.id,
            'email': user_obj.email,
            'full_name': user_obj.full_name,
            'qualification': user_obj.qualification,
            'dob': user_obj.dob.strftime('%Y-%m-%d') if user_obj.dob else None,
            'role': user_obj.role}), 201

    except Exception as e:
        return jsonify({'msg': 'Server error'}), 500

# -------- DASHBOARD --------

@user.get('/dashboard')
@user_required
@cache.cached(timeout=60)
def user_dashboard():
    quizzes = Quiz.query.all()
    return jsonify([{
        "id": quiz.id,
        "chapter": quiz.chapter.name,
        "subject": quiz.chapter.subject.name,
        "date_of_quiz": quiz.date_of_quiz.isoformat(),
        "remarks": quiz.remarks,
        "duration": quiz.time_duration,
        "questionCount": len(quiz.questions)} for quiz in quizzes]), 201

# -------- ATTEMPTING --------

@cache.memoize(timeout=60)
def get_questions(quiz_id, progress):
    return Question.query.filter_by(quiz_id=quiz_id).offset(progress).first()

@user.get('/attempt_quiz/<int:quiz_id>')
@user_required
@limiter.limit("10 per minute", key_func=lambda: get_jwt_identity()) 
def get_quiz_question(quiz_id):
    user_id = get_jwt_identity()
    progress = request.args.get('progress', default=0, type=int)
    question = get_questions(quiz_id, progress)

    if not question:
        return jsonify({"msg": "No more questions"}), 404

    return jsonify({
        "id": question.id,
        "text": question.question_statement,
        "options": [question.option1, question.option2, question.option3, question.option4],
        "progress": progress,
        "correct_option": question.correct_option}), 201

@user.post('/submit_answer')
@user_required
def submit_answer():
    data = request.json
    question_id = data.get("question_id")
    selected_option = data.get("selected_option")
    quiz_id = data.get("quiz_id")

    question = Question.query.get(question_id)

    if not question:
        return jsonify({"msg": "Question not found"}), 404

    selected_option = int(selected_option)
    correct = selected_option == int(question.correct_option)

    next_progress = int(data.get("progress", 0)) + 1
    total_questions = Question.query.filter_by(quiz_id=quiz_id).count()

    quiz = {"finished": next_progress >= total_questions, "correct": correct,
            "next_progress": next_progress if next_progress < total_questions else None}

    if quiz["finished"]:
        start_time_str = data.get("start_time")
        try:
            start_time = datetime.fromisoformat(start_time_str.replace("Z", "+00:00"))
            end_time = datetime.now(timezone.utc)
            quiz["time_taken"] = (end_time - start_time).total_seconds()
        except:
            quiz["time_taken"] = None

    return jsonify(quiz), 201

# -------- RESULT --------

@user.post('/quiz_result')
@user_required
def save_quiz_result():
    data = request.json
    user_id = get_jwt_identity()

    try:
        time_taken_secs = float(data['time_taken'])
        time_taken_mins = round(time_taken_secs / 60, 2)
    except (ValueError, TypeError):
        return jsonify({"msg": "Invalid time_taken value"}), 400
    
    quiz_id = data['quiz_id']
    score_value = data['score']
    total_questions = data['total_questions']

    existing_score = Score.query.filter_by(user_id=user_id, quiz_id=quiz_id).first()

    if existing_score:
        existing_score.total_scored = score_value
        existing_score.total_questions = total_questions
        existing_score.time_taken = time_taken_mins
    else:
        new_score = Score(
            quiz_id=quiz_id,
            user_id=user_id,
            total_scored=score_value,
            total_questions=total_questions,
            time_taken=time_taken_mins)
        db.session.add(new_score)
    db.session.commit()

    cache.delete(f"scores:{user_id}")

    return jsonify({"msg": "Score saved successfully"}), 201

# -------- SCORES --------

@user.get('/scores')
@user_required
@cache.cached(timeout=60, key_prefix=lambda: f"scores:{get_jwt_identity()}")
def get_scores():
    user_id = get_jwt_identity()
    scores = Score.query.filter_by(user_id=user_id).all()
    scores_data = []
    for score in scores:
        quiz = score.quiz
        scores_data.append({
            "quiz_id": quiz.id,
            "chapter": quiz.chapter.name,
            "subject": quiz.chapter.subject.name,
            "duration": quiz.time_duration,
            "remarks": quiz.remarks,
            "date_of_quiz": quiz.date_of_quiz.isoformat(),
            "total_scored": score.total_scored,
            "total_questions": score.total_questions,
            "time_taken": score.time_taken})

    return jsonify(scores=scores_data), 201

# -------- EXPORT REQUEST --------

@user.post("/export_quiz")
@user_required
@limiter.limit("3 per minute", key_func=lambda: get_jwt_identity())
def trigger_export():
    user_id = get_jwt_identity()
    task = export_user_quiz_details.delay(user_id)
    return jsonify({
        "status": "processing",
        "message": "Export started",
        "task_id": task.id}), 202

# -------- STATUS --------

@user.get('/check_export_status/<task_id>')
@user_required
def check_export_status(task_id):
    from celery.result import AsyncResult
    result = AsyncResult(task_id)
    
    if result.state == 'SUCCESS':
        data = result.result
        if data['status'] == 'success':
            return jsonify({
                "status": "success",
                "filename": data['filename'],
                "download_url": f"/api/user/downloads/{data['filename']}"}), 200
        else:
            return jsonify({"status": "error", "message": data.get("message", "Export failed")}), 500

    elif result.state == 'FAILURE':
        return jsonify({"status": "error", "message": "Export failed"}), 500
    else:
        return jsonify({"status": "processing"}), 202
    
# -------- DOWNLOAD --------
    
@user.get('/downloads/<path:filename>')
@user_required
def download_csv(filename):
    download_dir = os.path.join(os.getcwd(), 'downloads')
    full_path = os.path.join(download_dir, filename)

    if not os.path.exists(full_path):
        return {"error": f"File not found at {full_path}"}, 404

    return send_from_directory(download_dir, filename, as_attachment=True)