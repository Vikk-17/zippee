# zippee

## Installation

### Local Installation
-   [Download & install python](https://www.python.org/downloads/)
- Clone the repository & setup the application

```bash
git clone git@github.com:Vikk-17/zippee.git
cd zippee

# create a virtual environment
python -m venv .venv

# activate the virtual environment
# linux
source .venv/bin/activate

# windows
venv\Scripts\activate.bat

# install dependencies
pip install -r requirements.txt

# run the application
flask run -h 0.0.0.0 -p 8000

# or
python app.py

```

### Docker Setup
- [Install docker](https://docs.docker.com/engine/install/)

```
# clone the repository and run the following commmand
docker compose up

# or else build the application first
docker build -t <image_name> .

# To check for the build image 
docker images

# run the image
docker run <image_name>

```

---

## Exposed routes

### Register User

- Endpoint: POST **/register**
- Request Body
```json
{
    "username": "Test",
    "password": "test123"
}
```
- Response
```json
{
    "message": "User registered"
}
```

### Login User

- Endpoint: POST **/login**
- Request Body
```json
{
    "username": "Test",
    "password": "test123"
}
```
- Response
```json
{
  "access_token": "JWT_TOKEN_HERE"
}
```

### Get all tasks

- Endpoint: GET **/tasks**
- Add header: `Authorization: Bearer <access_token>`
- Response: Fetch all tasks
- Query Parameters:

| Parameters | Type | Description |
| --------------- | --------------- | --------------- |
| page | int | Page Number, default = 1 |
| per_page | int | Task Per Page, default = 5 |
| completed | bool | Filtered by completion status |

- Example: **/tasks?page=1&per_page=5&completed=true**


### Create task 

- Endpoint: POST **/tasks** 
- Add header: `Authorization: Bearer <access_token>`
- Request Body:
```json
{
  "title": "Test task",
  "description": "whatever described is true"
}
```
- Response
```json
{
  "message": "Task Created"
}
```

### Get task by Id

- Endpoint: GET **/tasks/<id>**
- Add header: `Authorization: Bearer <access_token>`
- Response:
```json
{
  "id": "70aab78c-4e5a-4a47-8d2d-3d73181bbb23",
  "title": "Test task",
  "description": "whatever described is true",
  "completed": false
}
```

### Update by Id

- Endpoint: PUT **/tasks/<id>**
- Add header: `Authorization: Bearer <access_token>`
- Request Body: 
```json
{
  "title": "Test task updated",
  "description": "whatever described is most likely true",
  "completed": true
}

```
- Response:
```json
{
  "message": updated task "70aab78c-4e5a-4a47-8d2d-3d73181bbb23",
}
```

### Delete task by Id

- Endpoint: PUT **/tasks/<id>**
- Add header: `Authorization: Bearer <access_token>`
- Response:
```json
{
  "message": "Task deleted"
}
```

---

### Instruction to run test 
```bash
# go to root dir of the application
pytest -v # to run all the test at once
```

---

### References
- [Default DataTime - Stack Overflow](https://stackoverflow.com/questions/13370317/sqlalchemy-default-datetime)
- [PyJWT](https://pyjwt.readthedocs.io/en/stable/)
- [Flask Blueprint](https://www.geeksforgeeks.org/python/flask-blueprints/)
- [SqlAlchemy-Relationship](https://stackoverflow.com/questions/27647066/what-is-the-relationship-function-used-for-in-sqlalchemy)
- [SqlAlchemy-Relationship - Official](https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html)
- [Flask JWT Extended](https://flask-jwt-extended.readthedocs.io/en/stable/basic_usage.html)
- [App Configuration](https://www.geeksforgeeks.org/python/flask-app-configuation/)
- [Application Setup - Flask Official](https://flask.palletsprojects.com/en/stable/tutorial/factory/)
- [Testing Flask Application](https://flask.palletsprojects.com/en/stable/testing/)
- [Setting up config for setup - Stackoverflow](https://stackoverflow.com/questions/7786648/how-to-call-setup-once-for-all-tests-and-teardown-after-all-are-finished)
- [Pagination](https://www.geeksforgeeks.org/python/how-to-implement-filtering-sorting-and-pagination-in-flask/)
