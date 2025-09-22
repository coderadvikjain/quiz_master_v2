from datetime import date
from app import celery, flask_app
from app.model.models import Quiz, User, Score
from datetime import date
from app.utils.mailer import send_email

@celery.task
def daily_reminder():
    with flask_app.app_context():
        print("🚀 Scheduler script started")

        today = date.today()
        today_quizzes = Quiz.query.filter(Quiz.date_of_quiz == today).all()
        valid_quizzes = [quiz for quiz in today_quizzes if len(quiz.questions) > 0]

        if not valid_quizzes:
            print("📭 No valid quizzes scheduled for today.")
        else:
            print(f"✅ {len(valid_quizzes)} quizzes found for today.")
            users = User.query.filter_by(role='user').all()

            for user in users:
                unattempted_quizzes = [quiz for quiz in valid_quizzes
                if not Score.query.filter_by(user_id=user.id, quiz_id=quiz.id).first()]

                if not unattempted_quizzes:
                    print(f"🚫 {user.email} has attempted all quizzes for today.")
                    continue

                subject="🎯 Pop Quiz? Nah... It's a Power Quiz!"
                body=f"""
                <html>
                <body style="font-family: Arial, sans-serif; padding: 20px;">
                    <div style="max-width: 600px; margin: auto; padding: 30px;">
                        <h2>Hello {user.full_name.strip().title()} 👋,</h2>
                        <p>
                            A new quiz has been <strong>scheduled for today</strong> 🗓️.
                            Don't miss the chance to test your knowledge!
                        </p>
                        <div style="text-align: center; margin: 30px 0;">
                            <a href="http://192.168.29.89:8080/dashboard" 
                            style="background-color: #3a4fbb; color: #fff; padding: 14px 28px; text-decoration: none; border-radius: 6px;">
                                Start Quiz
                            </a>
                        </div>
                        <p>Best of luck! 💪<br>- <strong>Team StudiQ</strong></p>
                    </div>
                </body>
                </html>"""
                try:
                    send_email(user.email, subject, body)
                except Exception as e:
                    print(f"❌ Failed to send email to {user.email}: {e}")