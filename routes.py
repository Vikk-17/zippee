from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
)
from werkzeug.security import generate_password_hash
from models import db, User, Task

api = Blueprint("api", __name__)


@api.route("/register", methods=["POST"])
def register():
    """
    User Registration
    ---
    tags:
      - Register User
    parameters:
        - name: Body
          in: body
          required: true
          schema:
            type: object
            required:
                - username
                - password
            properties:
                username:
                    type: string
                    example: John
                password:
                    type: string
                    example: test

    responses:
      200:
        description: User registered successfully
    """
    data = request.json
    hashed_password = generate_password_hash(data["password"])

    user = User(username=data["username"], password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered"}), 200


@api.route("/login", methods=["POST"])
def login():
    """
    User Login
    ---
    tags:
      - Login
    parameters:
        - name: Body
          in: body
          required: true
          schema:
            type: object
            required:
                - username
                - password
            properties:
                username:
                    type: string
                    examnd SQLAlchemy’s dynamic constple: John
                password:
                    type: string
                    example: test

    responses:
      200:
        description: Logged in successfully & JWT returned
    """
    data = request.json
    user = User.query.filter_by(username=data["username"]).first()

    # check credentials
    if not user:
        return jsonify({"message": "Invalid user"}), 404

    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token)


@api.route("/tasks", methods=["GET", "POST"])
@jwt_required()
def return_tasks():
    """
    Get all tasks or create a new task
    ---
    tags:
        - Tasks
    security:
        - Bearer: []

    get:
        summary: Get all tasks for the logged-in user
        responses:
        200:
            description: List of tasks
            schema:
            type: array
            items:
                type: object
                properties:
                id:
                    type: string
                title:
                    type: string
                description:
                    type: string
                completed:
                    type: boolean

    post:
        summary: Create a new task
        parameters:
        - name: body
          in: body
          required: true
          schema:
          type: object
          required:
            - title
            - description
          properties:
            title:
            type: string
            example: Learn Flask
            description:
            type: string
            example: Build CRUD API with JWT
        responses:
        201:
            description: Task created successfully
    """
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()

    if request.method == "GET":
        # read query params (?page=1&per_page=5)
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 5, type=int)
        completed = request.args.get("completed")
        query = Task.query.filter_by(user_id=current_user)

        if completed is not None:
            query = query.filter_by(completed=completed.lower() == "true")

        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False,
        )

        return (
            jsonify(
                {
                    "page": pagination.page,
                    "per_page": pagination.per_page,
                    "total": pagination.total,
                    "pages": pagination.pages,
                    "tasks": [
                        {
                            "id": item.id,
                            "title": item.title,
                            "description": item.description,
                            "completed": item.completed,
                        }
                        for item in pagination.items
                    ],
                }
            ),
            200,
        )

    elif request.method == "POST":
        data = request.json
        task = Task(
            title=data["title"], description=data["description"], user_id=current_user
        )
        db.session.add(task)
        db.session.commit()

        return jsonify({"message": "Task Created"}), 200


@api.route("/tasks/<id>", methods=["GET", "PUT", "DELETE"])
@jwt_required()
def return_tasks_id(id):
    """
    Get, update, or delete a task by ID
    ---
    tags:
      - Tasks
    security:
      - Bearer: []

    parameters:
      - name: id
        in: path
        required: true
        type: string
        description: Task ID

    get:
      summary: Get a single task by ID
      responses:
        200:
          description: Task retrieved successfully
          schema:
            type: object
            properties:
              id:
                type: string
              title:
                type: string
              description:
                type: string
              completed:
                type: boolean
        404:
          description: Task not found

    put:
      summary: Update a task
      parameters:
        - name: body
          in: body
          required: true
          schema:
            type: object
            properties:
              title:
                type: string
                example: Updated title
              completed:
                type: boolean
                example: true
      responses:
        200:
          description: Task updated successfully
        404:
          description: Task not found

    delete:
      summary: Delete a task
      responses:
        200:
          description: Task deleted successfully
        404:
          description: Task not found
    """
    current_user = get_jwt_identity()
    if request.method == "GET":
        task = Task.query.filter_by(id=id, user_id=current_user).first_or_404()
        return (
            jsonify(
                {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                }
            ),
            200,
        )

    elif request.method == "PUT":
        task = Task.query.filter_by(id=id, user_id=current_user).first_or_404()
        data = request.json
        task.title = data.get("title", task.title)
        task.completed = data.get("completed", task.completed)
        db.session.commit()

        return jsonify({"message": f"Updated task {id}"}), 200

    elif request.method == "DELETE":
        task = Task.query.filter_by(id=id, user_id=current_user).first_or_404()
        db.session.delete(task)
        db.session.commit()

        return jsonify({"message": "Task deleted"}), 200
