from datetime import datetime, timedelta
import os
from app import celery, flask_app
from app.model.models import User, Quiz, Score
from app.tasks.pdf_design import generate_pdf
from app.utils.report_mailer import send_report_email

@celery.task
def monthly_reports():
    with flask_app.app_context():
        print("📤 Monthly Report Task Started")
        
        today = datetime.today()
        first_day_of_this_month = today.replace(day=1)
        last_day_of_last_month = first_day_of_this_month - timedelta(days=1)
        start_date = last_day_of_last_month.replace(day=1)
        end_date = last_day_of_last_month

        users = User.query.filter_by(role='user').all()
        user_scores = {}

        for user in users:
            scores = Score.query.join(Quiz).filter(
                Score.user_id == user.id,
                Quiz.date_of_quiz >= start_date.date(),
                Quiz.date_of_quiz <= end_date.date()).all()

            total_score = sum(s.total_scored for s in scores)
            avg_score = round(total_score / len(scores), 2) if scores else 0

            user_scores[user.id] = {
                "user": user,
                "scores": scores,
                "total_score": total_score,
                "avg_score": avg_score,
                "total_quizzes": len(scores)}

        ranked_users = sorted(user_scores.items(), key=lambda item: item[1]["total_score"], reverse=True)
        os.makedirs("reports", exist_ok=True)

        for rank,(user_id, data) in enumerate(ranked_users, start=1):
            user = data["user"]
            scores = data["scores"]
            total_quizzes = data["total_quizzes"]
            total_score = data["total_score"]
            avg_score = data["avg_score"]

            filename = f"Monthly_Report_{user.full_name.strip().title()}_{start_date.strftime('%B_%Y')}.pdf"
            filepath = os.path.join("reports", filename)

            generate_pdf(user, scores, total_quizzes, total_score, avg_score, start_date, filepath, rank)

            try:
                send_report_email(
                    to_email=user.email,
                    subject=f"📅 Monthly Quiz Report - {start_date.strftime('%B %Y')}",
                    body=
                    f"""
                    <html>
                    <head>
                        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
                    </head>
                        <body style="font-family: Arial, sans-serif; padding: 20px;">
                            <div style="max-width: 600px; margin: auto; padding: 30px; border-radius: 10px;">
                                <h2 style="color: #2c3e50;">📊 Monthly Quiz Report</h2>
                                <p>Hello <strong>{user.full_name.strip().title()}</strong>,</p>
                                <p>Hope you're doing great! 👋</p>
                                <p>Here's your <strong>Monthly Quiz Report</strong>, reflecting your hard work and quiz achievements over the last month.</p>
                                <p>We're proud of your progress. Keep learning and growing! 🚀</p>
                                <p style="margin-top: 30px; font-size: 0.9em; color: #555;">Regards,<br><strong>Team StudiQ</strong></p>
                            </div>
                        </body>
                    </html>"""
                    ,attachment_path=filepath)
                print(f"📧 Sent report to {user.email}")
            except Exception as e:
                print(f"❌ Failed to send report to {user.email}: {e}")
            finally:
                if os.path.exists(filepath):
                    os.remove(filepath)