from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request, get_jwt
from functools import wraps
from app import cache
from app.model.models import *
from datetime import datetime, date

admin = Blueprint('admin', __name__)

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            claims = get_jwt()
            identity = get_jwt_identity()

            if claims.get("role") != "admin":
                return jsonify({"msg": "Admins only!"}), 403
        except Exception as e:
            print("JWT Error:", e)
            return jsonify({"msg": "Invalid or missing token"}), 401
        return fn(*args, **kwargs)
    return wrapper

# -------- SUBJECTS --------

@admin.get('/subjects')
@admin_required
@cache.cached(timeout=300, key_prefix='all_subjects')
def get_all_subjects():
    subjects = Subject.query.all()
    subjects_data = [{"id": s.id, "name": s.name, "description": s.description} for s in subjects]
    return jsonify(subjects=subjects_data), 201

@admin.post('/subject')
@admin_required
def create_subject():
    data = request.get_json()
    name = data.get("name")
    description = data.get("description")

    if not name or not description:
        return jsonify({"msg": "Missing name or description"}), 400
    
    if Subject.query.filter_by(name=name).first():
        return jsonify({"msg": "Course already exists"}), 409

    new_subject = Subject(name=name, description=description)
    try:
        db.session.add(new_subject)
        db.session.commit()
        cache.delete('all_subjects')
        return jsonify({"msg": "Subject added", "id": new_subject.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Database error", "error": str(e)}), 500

@admin.put('/subject/<int:subject_id>')
@admin_required
def edit_subject(subject_id):
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    if not name or not description:
        return jsonify({"msg": "Missing name or description"}), 400
    
    subject = Subject.query.get_or_404(subject_id)
    
    if Subject.query.filter(Subject.name == name, Subject.id != subject_id).first():
        return jsonify({"msg": "Course name already taken"}), 409

    subject.name = name
    subject.description = description
    try:
        db.session.commit()
        cache.delete('all_subjects')
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Database error", "error": str(e)}), 500

    return jsonify({"msg": "Subject updated"}), 201

@admin.delete('/subject/<int:subject_id>')
@admin_required
def delete_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)

    chapter_ids = [chapter.id for chapter in subject.chapters]
    quiz_ids = []

    for chapter in subject.chapters:
        for quiz in chapter.quizzes:
            quiz_ids.append(quiz.id)

    try:
        db.session.delete(subject)
        db.session.commit()
        cache.delete('all_subjects')
        for chapter_id in chapter_ids:
            cache.delete(f"chapters_subject_{subject_id}")
            cache.delete(f"quizzes_{chapter_id}")
        cache.delete('all_chapters')
        cache.delete('all_quizzes')
        for quiz_id in quiz_ids:
            cache.delete(f"questions_{quiz_id}")
        cache.delete('all_questions')
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Database error", "error": str(e)}), 500

    return jsonify({"msg": "Subject deleted"}), 201


# -------- CHAPTERS --------

@admin.get('/chapters')
@admin_required
@cache.cached(timeout=300, key_prefix='all_chapters')
def get_all_chapters():
    chapters = Chapter.query.all()
    chapters_data = [{"id": c.id, "name": c.name, "description": c.description, "subject_id": c.subject_id} for c in chapters]
    return jsonify(chapters=chapters_data), 201

@admin.get('/chapters/<int:subject_id>')
@admin_required
@cache.cached(timeout=300, key_prefix=lambda: f'chapters_{request.view_args["subject_id"]}')
def get_chapters_by_subject(subject_id):
    chapters = Chapter.query.filter_by(subject_id=subject_id).all()
    data = [{"id": c.id, "name": c.name, "description": c.description} for c in chapters]
    return jsonify(chapters=data), 201

@admin.post('/chapter')
@admin_required
def create_chapter():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    subject_id = data.get('subject_id')

    if not name or not description or not subject_id:
        return jsonify({"msg": "Missing name, description or subject id"}), 400

    if Chapter.query.filter_by(name=name, subject_id=subject_id).first():
        return jsonify({"msg": "Chapter already exists for this subject"}), 409

    new_chapter = Chapter(name=name, description=description, subject_id=subject_id)
    try:
        db.session.add(new_chapter)
        db.session.commit()
        cache.delete('all_chapters')
        cache.delete(f"chapters_{subject_id}")
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Database error", "error": str(e)}), 500

    return jsonify({"msg": "Chapter added", "id": new_chapter.id}), 201

@admin.put('/chapter/<int:chapter_id>')
@admin_required
def edit_chapter(chapter_id):
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    if not name or not description:
        return jsonify({"msg": "Missing name or description"}), 400

    chapter = Chapter.query.get_or_404(chapter_id)
    subject_id = chapter.subject_id

    if Chapter.query.filter(Chapter.name == name, Chapter.subject_id == chapter.subject_id, Chapter.id != chapter_id).first():
        return jsonify({"msg": "Chapter name already taken"}), 409

    chapter.name = name
    chapter.description = description
    try:
        db.session.commit()
        cache.delete('all_chapters')
        cache.delete(f"chapters_{subject_id}")
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Database error", "error": str(e)}), 500

    return jsonify({"msg": "Chapter updated"}), 201

@admin.delete('/chapter/<int:chapter_id>')
@admin_required
def delete_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    subject_id = chapter.subject_id

    quiz = [quiz.id for quiz in chapter.quizzes]

    try:
        db.session.delete(chapter)
        db.session.commit()
        cache.delete('all_chapters')
        cache.delete(f"chapters_{subject_id}")
        cache.delete(f"quizzes_{chapter_id}")
        cache.delete('all_quizzes')
        for quiz_id in quiz:
            cache.delete(f"questions_{quiz_id}")
        cache.delete('all_questions')
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Database error", "error": str(e)}), 500

    return jsonify({"msg": "Chapter deleted"}), 201


# -------- QUIZZES --------

@admin.get('/quizzes')
@admin_required
@cache.cached(timeout=300, key_prefix='all_quizzes')
def get_quizzes():
    quizzes = Quiz.query.all()
    quizzes_data = [{"id": q.id, "date_of_quiz": q.date_of_quiz.strftime('%Y-%m-%d'), "time_duration": q.time_duration,
                     "chapter_id": q.chapter_id, "remarks": q.remarks} for q in quizzes]
    return jsonify(quizzes=quizzes_data), 201

@admin.get('/quizzes/<int:chapter_id>')
@admin_required
@cache.cached(timeout=300, key_prefix=lambda: f'quizzes_{request.view_args["chapter_id"]}')
def get_quizzes_by_chapter(chapter_id):
    quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()
    quiz_data = [{"id": q.id, "date_of_quiz": q.date_of_quiz.strftime('%Y-%m-%d'), "time_duration": q.time_duration, "chapter_id": q.chapter_id, "remarks": q.remarks} for q in quizzes]
    return jsonify(quizzes=quiz_data), 201

# This function reassigns Quiz no. based on their order
def remarks_for_chapter(chapter_id):
    quizzes = Quiz.query.filter_by(chapter_id=chapter_id).order_by(Quiz.date_of_quiz.asc(), Quiz.id.asc()).all()
    for idx, quiz in enumerate(quizzes, start=1):
        quiz.remarks = f"Quiz {idx}"
    db.session.commit()

@admin.post('/quiz')
@admin_required
def add_quiz():
    data = request.get_json()
    date_of_quiz_str = data.get('date_of_quiz')
    chapter_id = data.get('chapter_id')
    duration = data.get('time_duration')

    if not chapter_id or not date_of_quiz_str or duration is None:
        return jsonify({"msg": "Missing chapter id, date of quiz or time duration"}), 400

    try:
        date_of_quiz = datetime.strptime(date_of_quiz_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'msg': 'Invalid date format. Use YYYY-MM-DD'}), 400

    if date_of_quiz < date.today():
        return jsonify({'msg': 'Quiz date must not be in the past'}), 400

    remarks = "temp"

    new_quiz = Quiz(chapter_id=chapter_id, date_of_quiz=date_of_quiz, time_duration=duration, remarks=remarks)
    try:
        db.session.add(new_quiz)
        db.session.commit()
        remarks_for_chapter(chapter_id)
        cache.delete('all_quizzes')
        cache.delete(f"quizzes_{chapter_id}")
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Database error", "error": str(e)}), 500

    return jsonify({"msg": "Quiz added", "id": new_quiz.id}), 201

@admin.put('/quiz/<int:quiz_id>')
@admin_required
def edit_quiz(quiz_id):
    data = request.get_json()
    new_chapter_id = data.get('chapter_id')
    date_of_quiz_str = data.get('date_of_quiz')
    time_duration = data.get('time_duration')

    if not new_chapter_id or not date_of_quiz_str or time_duration is None:
        return jsonify({"msg": "Missing date of quiz or time duration or chapter id"}), 400

    try:
        date_of_quiz = datetime.strptime(date_of_quiz_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'msg': 'Invalid date format. Use YYYY-MM-DD'}), 400

    quiz = Quiz.query.get_or_404(quiz_id)
    old_chapter_id = quiz.chapter_id
    chapter_changed = old_chapter_id != new_chapter_id

    quiz.chapter_id = new_chapter_id
    quiz.date_of_quiz = date_of_quiz
    quiz.time_duration = time_duration
    try:
        db.session.commit()
        
        if chapter_changed:
            remarks_for_chapter(old_chapter_id)
            remarks_for_chapter(new_chapter_id)
        else:
            remarks_for_chapter(new_chapter_id)

        cache.delete('all_quizzes')
        cache.delete(f"quizzes_{new_chapter_id}")
        if chapter_changed:
            cache.delete(f"quizzes_{old_chapter_id}")

    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Database error", "error": str(e)}), 500

    return jsonify({"msg": "Quiz updated"}), 201

@admin.delete('/quiz/<int:quiz_id>')
@admin_required
def delete_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    chapter_id = quiz.chapter_id

    try:
        db.session.delete(quiz)
        db.session.commit()
        cache.delete('all_quizzes')
        cache.delete(f"quizzes_{chapter_id}")
        cache.delete(f"questions_{quiz_id}")
        cache.delete('all_questions') 
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Database error", "error": str(e)}), 500

    return jsonify({"msg": "Quiz deleted"}), 201


# -------- QUESTIONS --------

@admin.get('/questions')
@admin_required
@cache.cached(timeout=300, key_prefix='all_questions')
def get_questions():
    questions = Question.query.all()
    questions_data = [{"id": q.id, "question_statement": q.question_statement, "option1": q.option1,
             "option2": q.option2, "option3": q.option3, "option4": q.option4,
             "correct_option": q.correct_option,"quiz_id": q.quiz_id} for q in questions]
    return jsonify(questions=questions_data), 201

@admin.get('/questions/<int:quiz_id>')
@admin_required
@cache.cached(timeout=300, key_prefix=lambda: f'questions_{request.view_args["quiz_id"]}')
def get_questions_by_quiz(quiz_id):
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    question_data = [{"id": q.id, "question_statement": q.question_statement,
                      "option1": q.option1, "option2": q.option2, "option3": q.option3, "option4": q.option4,
                      "correct_option": q.correct_option} for q in questions]
    return jsonify(questions=question_data), 201

@admin.post('/question')
@admin_required
def add_question():
    data = request.get_json()
    quiz_id = data.get('quiz_id')
    question_statement = data.get('question_statement')
    option1 = data.get('option1')
    option2 = data.get('option2')
    option3 = data.get('option3')
    option4 = data.get('option4')
    correct_option = data.get('correct_option')

    if not all([quiz_id, question_statement, option1, option2, option3, option4, correct_option]):
        return jsonify({"msg": "Missing required question fields"}), 400

    new_question = Question(
        quiz_id=quiz_id,
        question_statement=question_statement,
        option1=option1,
        option2=option2,
        option3=option3,
        option4=option4,
        correct_option=correct_option)
    
    try:
        db.session.add(new_question)
        db.session.commit()
        cache.delete('all_questions')
        cache.delete(f"questions_{quiz_id}")
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Database error", "error": str(e)}), 500

    return jsonify({"msg": "Question added", "id": new_question.id}), 201

@admin.put('/question/<int:question_id>')
@admin_required
def edit_question(question_id):
    data = request.get_json()
    question = Question.query.get_or_404(question_id)
    quiz_id = question.quiz_id

    question_statement = data.get('question_statement')
    option1 = data.get('option1')
    option2 = data.get('option2')
    option3 = data.get('option3')
    option4 = data.get('option4')
    correct_option = data.get('correct_option')

    if not all([question_statement, option1, option2, option3, option4, correct_option]):
        return jsonify({"msg": "Missing required question fields"}), 400

    question.question_statement = question_statement
    question.option1 = option1
    question.option2 = option2
    question.option3 = option3
    question.option4 = option4
    question.correct_option = correct_option

    try:
        db.session.commit()
        cache.delete('all_questions')
        cache.delete(f"questions_{quiz_id}")
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Database error", "error": str(e)}), 500

    return jsonify({"msg": "Question updated"}), 201

@admin.delete('/question/<int:question_id>')
@admin_required
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    quiz_id = question.quiz_id

    try:
        db.session.delete(question)
        db.session.commit()
        cache.delete('all_questions')
        cache.delete(f"questions_{quiz_id}")
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Database error", "error": str(e)}), 500

    return jsonify({"msg": "Question deleted"}), 201

# -------- USERS --------

@admin.get('/users')
@admin_required
def get_all_users():
    try:
        users = User.query.filter_by(role='user').all()
        users_data = [{"id": user_obj.id, "email": user_obj.email, "full_name": user_obj.full_name,
                       "qualification": user_obj.qualification, "dob": user_obj.dob.strftime('%Y-%m-%d')} for user_obj in users]

        return jsonify(users=users_data), 201
    except Exception as e:
        return jsonify({'msg': 'Server error'}), 500