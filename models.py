from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from uuid import uuid4


db = SQLAlchemy()


# generate uuid
def generate_uuid():
    return str(uuid4())


class User(db.Model):
    """
    id, username, password
    """

    __tablename__ = "users"
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    tasks = db.relationship("Task", backref="user")
    
    def __init__(self, username, password):
        self.username = username
        self.password = password

class Task(db.Model):
    """
    id, title, description, completd, created_at, updated_at
    """

    __tablename__ = "tasks"

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    title = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

    user_id = db.Column(db.String, db.ForeignKey("users.id"), nullable=False)

    def __init__(self, title, description, user_id):
        self.title = title
        self.description = description
        self.user_id = user_id
