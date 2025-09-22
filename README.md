<h3 align="center">MAD2 Project </h3>
</div>

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#technology-used">Technology-Used</a>
    </li>
    <li>
      <a href="#installation-guide">Installation Guide</a>
    </li>
    <li><a href="#usage">Usage of application</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

## About The Project

This Project is made by Jatin Nahata,
for Modern Application Development 2 (MAD-II) course project.

Main theme of this project is to make a Quiz Master application, 
which help students to prepare for various courses,
enabling it for users(students) to explore quizzes that are available for
courses, chapters and can see there scores after attending a quiz.
admin has CRUD control over Courses, Chapters, Quizzes and Questions.
admin can see users which registered themself for preparation.

<p align="right">(<a href="#readme">go to top</a>)</p>

## Technology Used

I. Flask: Handling HTTP requests, defining routes.
<br>
II. Flask-SQLAlchemy: ORM to interact with the SQLite database.
<br>
III. Flask-Cors: Enabling CORS (Cross-Origin Resource Sharing) between frontend and backend.
<br>
IV. Flask-JWT-Extended: Managing authentication and protecting routes using JSON Web Tokens.
<br>
V. Flask-Caching + Redis: Caching expensive computations or data frequently used
<br>
VI. Flask-Limiter + Redis: Rate-limiting API requests.
<br>
VII. Celery + Redis: Handling asynchronous tasks and scheduled jobs (e.g., sending quiz results, processing long tasks).
<br>
VIII. python-dotenv: Managing environment variables securely.
<br>
IX. Werkzeug: Underlying Flask library for password hashing and security.
<br>
X. reportlab: Generating PDF reports (e.g., monthly reports)
<br>
XI. SQLite: Lightweight, file-based DB suitable for small to medium-scale apps and during development.
<br>
XII. datetime: Useful for tracking quiz timers, task schedules, timestamps.
<br>
XIII. npm + node_modules: Managing frontend dependencies (like Vue.js) and also Required to build and serve the frontend UI.
<br>
XIV. io: Ideal for generating CSV exports of user reports via APIs without saving temporary files to disk.

<p align="right">(<a href="#readme">go to top</a>)</p>

## Installation Guide

1. To run the flask Api, create a virtual environment by using ‘python -m venv venv’ in backend folder (cd backend)
Now, enable the created virtual environment you have, by running “venv\Scripts\activate” command on terminal.
After creating a virtual environment, run command ‘pip install -r requirements.txt’ and then all required packages will be installed and then run “api.py” file or run using the python command ‘python api.py’ on the terminal.
Or
Simply, run command ‘pip install -r requirements.txt’ in backend folder (cd backend) and then all required packages will be installed. and then run “api.py” file or run using the python command ‘python api.py’ on the terminal.
2. Now, to create ‘node_module’ folder run ‘npm install’ in frontend folder
(cd frontend). It will install all required package.
3. To run, the frontend, use ‘npm run serve’ on terminal in frontend folder
(cd frontend).
4. To install redis server use ‘sudo apt install redis-server’ in wsl terminal and then start redis by using ‘redis-server’ in wsl terminal.
[To install wsl in windows: How to Install Ubuntu in WSL2 in Just 3 Steps]
5. Now to run celery worker using redis, run command ‘python -m celery -A app.celery worker --loglevel=info --pool=solo’ on terminal in backend folder (cd backend).
6. Then, to run celery beat using redis, run command ‘python -m celery -A app.celery beat --loglevel=info’ on terminal in backend folder (cd backend).

<p align="right">(<a href="#readme">go to top</a>)</p>

## Usage

StuiQ is a multi-user web application designed to help students prepare for various courses through structured quizzes. The platform supports two types of users: Administrator and Users (students). Administrator can manage course content, chapter, quizzes, and questions, while students engage in self-paced learning and assessments.

<p align="right">(<a href="#readme">go to top</a>)</p>

## Contact

Jatin Nahata - jatinnahatajain24@gmail.com

Project Report: [Project Report](https://github.com/coderadvikjain/quiz_master_v2/blob/main/Project%20Report.pdf)

Previous Version: [Quiz Master v1](https://github.com/coderadvikjain/quiz_master_v1)

<p align="right">(<a href="#readme">go to top</a>)</p>
