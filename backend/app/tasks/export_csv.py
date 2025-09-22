import csv
import os
from io import StringIO
from app import celery, flask_app
from app.model.models import User

def format_time(minutes_float):
    total_seconds = int(minutes_float * 60)
    minutes = total_seconds // 60
    secs = total_seconds % 60

    if minutes > 0 and secs > 0:
        return f"{minutes} min {secs} sec"
    elif minutes > 0:
        return f"{minutes} min"
    else:
        return f"{secs} sec"

@celery.task
def export_user_quiz_details(user_id):
    try:
        with flask_app.app_context():
            print("📤 Export Task Started")
            user = User.query.get(user_id)
            if not user:
                return {"status": "error", "message": f"User with ID {user_id} not found"}

            output = StringIO()
            writer = csv.writer(output)
            writer.writerow([
                'Quiz ID', 'Quiz Title', 'Course', 'Date',
                'Total Questions', 'Score',
                'Time Spent'])

            for score in user.scores:
                quiz = score.quiz
                if not score.quiz:
                    continue

                chapter_name = quiz.chapter.name
                subject_name = quiz.chapter.subject.name
                remarks = quiz.remarks
                quiz_title = f"{chapter_name} {remarks}".strip()
                time_str = format_time(score.time_taken)

                writer.writerow([
                    quiz.id,
                    quiz_title,
                    subject_name,
                    str(quiz.date_of_quiz.strftime('%Y-%m-%d')),
                    score.total_questions,
                    score.total_scored,
                    time_str])

            os.makedirs("downloads", exist_ok=True)
            filename = f"{user.full_name.replace(' ', '_')}_quiz_export.csv"
            filepath = os.path.join("downloads", filename)

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(output.getvalue())

            return {"status": "success", "message": "Export completed", "filepath": filepath, "filename": filename}

    except Exception as e:
        return {
            "status": "error", "message": f"Export failed: {str(e)}"}