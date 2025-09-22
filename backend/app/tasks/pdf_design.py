from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generate_pdf(user, scores, total_quizzes, total_score, avg_score, start_date, filepath, rank):
    c = canvas.Canvas(filepath, pagesize=A4)
    width, height = A4

    margin_x = 50
    y = height - 50

    # Title
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width / 2, y, "Monthly Activity Report")
    y -= 40

    # User Info
    c.setFont("Helvetica", 13)
    c.drawString(margin_x, y, f"Name: {user.full_name.strip().title()}")
    y -= 20
    c.drawString(margin_x, y, f"Email: {user.email}")
    y -= 20
    c.drawString(margin_x, y, f"Report Month: {start_date.strftime('%B %Y')}")
    y -= 20
    c.drawString(margin_x, y, f"Rank: #{rank}")
    y -= 30

    # Summary Section
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin_x, y, "Summary")
    y -= 20
    c.setFont("Helvetica", 12)
    c.drawString(margin_x + 10, y, f"Total Quizzes Taken: {total_quizzes}")
    y -= 20
    c.drawString(margin_x + 10, y, f"Total Score: {total_score}")
    y -= 20
    c.drawString(margin_x + 10, y, f"Average Score: {avg_score}")

    total_time = sum(s.time_taken for s in scores)
    total_minutes = int(total_time)
    total_seconds = int(round((total_time - total_minutes) * 60))

    if total_minutes:
        time_spent_str = f"{total_minutes} mins {total_seconds} secs"
    else:
        time_spent_str = f"{total_seconds} secs"
    y -= 20
    c.drawString(margin_x + 10, y, f"Total Time Spent: {time_spent_str}")
    y -= 30

    # Quiz Breakdown Table
    if scores:
        c.setFont("Helvetica-Bold", 13)
        c.drawString(margin_x, y, "Quiz Breakdown")
        y -= 25

        c.setFont("Helvetica-Bold", 11)
        c.drawString(margin_x, y, "Quiz Title")
        c.drawString(margin_x + 120, y, "Date")
        c.drawString(margin_x + 220, y, "Score")
        c.drawString(margin_x + 320, y, "Course")
        c.drawString(margin_x + 420, y, "Time Taken")
        y -= 5
        c.line(margin_x, y, margin_x + 480, y)
        y -= 15

        c.setFont("Helvetica", 10)
        for s in scores:
            if y < 60:
                c.showPage()
                y = height - 50
                c.setFont("Helvetica", 10)

            title = f"{s.quiz.chapter.name} {s.quiz.remarks or ''}".strip()
            quiz_date = s.quiz.date_of_quiz.strftime('%d-%b-%Y')
            score_str = f"{s.total_scored}/{s.total_questions}"
            Course = s.quiz.chapter.subject.name
            minutes = int(s.time_taken)
            seconds = round((s.time_taken - minutes) * 60)
            time_str = f"{minutes} mins {seconds} secs" if minutes else f"{seconds} secs"

            c.drawString(margin_x, y, title)
            c.drawString(margin_x + 120, y, quiz_date)
            c.drawString(margin_x + 220, y, score_str)
            c.drawString(margin_x + 320, y, Course)
            c.drawString(margin_x + 420, y, time_str)
            y -= 18

    # Footer
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(margin_x, 30, "Keep learning and growing. - Team StudiQ")
    c.save()