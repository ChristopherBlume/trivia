# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## API

### Base URLs

- Backend Base: `http:127.0.0.1:5000`
- Frontend Base: `http:127.0.0.1:3000`

### Error Codes

- 400: Bad Request
- 402: Resource not found
- 422: Unprocessable Entity
- 500: Internal Server Error

### Endpoints

GET `/categories` fetches a python dictionary of all available quiz categories.

- Request Parameters: None
- Sample: `http://127.0.0.1:5000/categories`
- Example Response:

```bash
{
  'categories': {
    '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports"
  },
  'success': True
}
```

GET `/questions` returns all questions paginated.

- Request Parameters: None
- Sample: `http://127.0.0.1:5000/questions`
- Example Response:

```bash
{
  'categories': {
    '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports"
  },
  'questions': [
    {
      "id":15,
      "question":"The Taj Mahal is located in which Indian city?"
      "answer":"Agra",
      "category":3,
      "difficulty":2,
    },
    {
      "id":6,
      "question":"What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
      "answer":"Edward Scissorhands",
      "category":5,
      "difficulty":3,
    }
  ],
  'success':true,
  'total_questions': 2
}
```

DELETE `/questions/<int:question_id>` Delete an existing question from the database.

- Request Parameters: id of question which should be deleted
- Example Response:

```bash
{
  'success': True,
  'deleted': 2,
  'message': "Question successfully deleted"
}
```

POST `/questions` Adds a new question to the database.

- Request Parameter - Body: {question:string, answer:string, difficulty:int, category:string}
- Example Response:

```bash
{
  'success': True,
  'message': "Question successfully created"
}
```

POST `/questions/search` Fetches all questions where a substring matches the search term (not case-sensitive).

- Request Parameter - Body: {searchTerm:string}
- Example Response:

```bash
{
  "questions": [
    {
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
    }
  ],
  "success": true,
  "total_questions": 2
}
```

GET `/categories/<int:category_id>/questions` Fetches a python dictionary of questions for a specific category.

- Request: `http://127.0.0.1/categories/6/questions`
- Example Response:

```bash
{
  "current_category":6,
  "questions":[
    {
      "answer":"Edward Scissorhands",
      "category":5,
      "difficulty":3,
      "id":6,
      "question":"What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "success":true,
  "total_questions":1
}
```

POST `/quizzes` Fetches random questions within a category.

- Request Parameter - Body: {previous_question:array, quiz_category: {type:string, id:int}}
- Example Response:

```bash
{
  "question": {
    "answer": "The Liver",
    "category": 1,
    "difficulty": 4,
    "id": 20,
    "question": "What is the heaviest organ in the human body?"
  },
  "success": true
}
```

## Testing

To run the tests, run

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
