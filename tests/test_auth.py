from app import app
from models import db
from models import User, Task


def setup_config():
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SECRET_KEY"] = "test"
    app.config["JWT_SECRET_KEY"] = "jwt_test"

    with app.app_context():
        db.create_all()


def clear_db():
    with app.app_context():
        Task.query.delete()
        User.query.delete()
        db.session.commit()


def destroy():
    with app.app_context():
        db.drop_all()


def test_register():
    clear_db()
    client = app.test_client()

    res = client.post("/register", json={"username": "John", "password": "test123"})

    assert res.status_code == 200
    assert res.get_json()["message"] == "User registered"


def test_login():
    clear_db()
    client = app.test_client()

    client.post("/register", json={"username": "john", "password": "test123"})

    res = client.post("/login", json={"username": "john", "password": "test123"})

    assert res.status_code == 200
    assert "access_token" in res.get_json()
