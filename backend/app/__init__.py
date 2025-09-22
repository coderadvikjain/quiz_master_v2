from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from sqlalchemy import event
from sqlalchemy.engine import Engine
import sqlite3
from werkzeug.security import generate_password_hash
from app.model.models import db, User
from app.config import Config
import redis
from celery import Celery
from celery.schedules import crontab
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Initial extensions
jwt = JWTManager()
cors = CORS()
celery = Celery(__name__)

# Initialize cache
cache = Cache()

# Initialize limiter
limiter = Limiter(key_func=get_remote_address,storage_uri=Config.RATE_LIMIT_REDIS_URI)
flask_app = None

# Foreign key support in Sqlite for auto deletion of child data
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()

# Celery work setup
def make_celery(app):
    celery.config_from_object(app.config)
    celery.autodiscover_tasks(['app.tasks'])

    class FlaskTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with flask_app.app_context():
                return self.run(*args, **kwargs)
    celery.Task = FlaskTask
    
    # Celery Beat(scheduling task)
    celery.conf.beat_schedule = {
        "daily_reminder": {
            "task": "app.tasks.reminders.daily_reminder",
            "schedule": crontab(minute=30, hour=18)
        },
        "monthly_reports": {
            "task": "app.tasks.monthly_report.monthly_reports",
            "schedule": crontab(minute=0, hour=10, day_of_month='1')
        }
    }
    
    # Celery scheduled tasks
    import app.tasks.reminders
    import app.tasks.monthly_report

    return celery

# create app
def create_app():
    global flask_app
    app = Flask(__name__)
    app.config.from_object(Config)

    # Init extensions
    cors.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    cache.init_app(app)
    limiter.init_app(app)
    flask_app = app
    make_celery(app)

    with app.app_context():
        db.create_all()

        # Auto creation admin account
        admin_email = app.config["ADMIN_EMAIL"]
        admin_password = app.config["ADMIN_PASSWORD"]
        existing_admin = User.query.filter_by(email=admin_email).first()
        if not existing_admin:
            admin = User(
                email=admin_email,
                password=generate_password_hash(admin_password),
                full_name="Admin User",
                role="admin")
            db.session.add(admin)
            db.session.commit()

    # Register routers
    from app.routes.auth import auth
    from app.routes.admin import admin
    from app.routes.user import user

    app.register_blueprint(auth, url_prefix="/api/auth")
    app.register_blueprint(admin, url_prefix="/api/admin")
    app.register_blueprint(user, url_prefix="/api/user")

    return app

flask_app = create_app()