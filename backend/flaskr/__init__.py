import os
from flask import Flask, request, abort, jsonify
from flask.globals import current_app
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# Paginate Method similar to bookshelf application
def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]

  return current_questions


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  # * DONE
  '''
  CORS(app, resources={'/api': {'origins': '*'}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  # * DONE
  @app.after_request
  def after_request(response):
    """ Set Access Control """

    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')

    return response

  '''
  Home Path
  '''
  @app.route('/')
  def index():
    return jsonify({
      'succees': True,
      'message': 'Welcome!'
    })

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  # * DONE
  @app.route('/categories')
  def get_all_categories():
    """[GET all categories endpoint]

    Returns:
        list of categories: returns all categories
    """
    try:
      categories = Category.query.all()
      # Format the categorie to be correctly rendered in the frontend
      categories_dictonary = {}
      for category in categories:
        categories_dictonary[category.id] = category.type

      # Response
      return jsonify({
        'success': True,
        'categories': categories_dictonary
      }), 200
    except Exception as e:
      print(e)
      abort(500)


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  # * Done
  @app.route('/questions')
  def get_all_questions():
    '''
    [GET all questions endpoint]

    Returns:
        list of questions: returns all questions paginated
        number of total questions: integer
        current category: the category that suits the list of questions
        categories: all categories
    '''
    # Get all questions and paginate them
    questions = Question.query.all()
    total_questions = len(questions)
    current_questions = paginate_questions(request, questions)

    # Get categories and add them to a dictionary
    categories = Category.query.all()
    categories_dictonary = {}
    for category in categories:
      categories_dictonary[category.id] = category.type

    # Abort, if no questions found
    if(len(current_questions) == 0):
      abort(404)

    # Response, if success
    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': total_questions,
      'categories': categories_dictonary
    }), 200


  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  # * Done
  @app.route('/questions/<int:question_id>', methods=["DELETE"])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

      if Question is None:
        abort(404)
        
      question.delete()

      return jsonify({
        'success': True,
        'deleted': question_id,
        'message': "Question successfully deleted"
      }), 200

    except Exception as e:
      print(e)
      abort(500)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  # * Done
  @app.route('/questions', methods=['POST'])
  def create_question():
    # Get json data from request
      data = request.get_json()

    # Assign individual data from json data into variables
      question = data.get('question', '')
      answer = data.get('answer', '')
      difficulty = data.get('difficulty', '')
      category = data.get('category', '')

      # Validate to ensure no data is empty
      if ((question == '') or (answer == '') or (difficulty == '') or (category == '')):
        abort(422)

      try:
        # Create a new question instance
        question = Question(question=question, answer=answer, difficulty=difficulty, category=category)

        #  Save the question
        question.insert()

        # Return a success message
        return jsonify({
          'success': True,
          'message': 'Question successfully created!'
        }), 201

      except Exception as e:
        print(e)
        # Return 422 status code if there is an error
        abort(422)

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  # * Done
  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    data = request.get_json()
    search_term = data.get('searchTerm', None)

    if search_term == '':
      abort(422)

    try:
      selection = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
      current_questions = paginate_questions(request, selection)

      if len(selection) == 0:
        abort(404)
              
      return jsonify({
        'success': True,
        'questions': current_questions,
        'total_questions': len(Question.query.all())
      }), 200
    except Exception as e:
      print(e)
      abort(404)


  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  # * DONE
  @app.route('/categories/<int:category_id>/questions')
  def get_questions_by_category(category_id):
    category = Category.query.filter_by(id=category_id).one_or_none()

    if (category is None):
      abort(404)

    questions = Question.query.filter_by(category=category_id).all()
    current_questions=paginate_questions(request, questions)

    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': len(questions),
      'current_category': category_id
    }), 200

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
    # Get data
    data = request.get_json()
    previous_questions = data.get('previous_questions')
    quiz_category = data.get('quiz_category')

    if ((quiz_category is None) or (previous_questions is None)):
      abort(404)

    if(quiz_category['id'] == False):
      questions = Question.query.all()
    else:
      questions = Question.query.filter_by(category=quiz_category['id']).all()

    # Randomize Method
    def random_question():
      return questions[random.randint(0, len(questions)-1)]

    next_question = random_question()

    return jsonify({
      'success': True,
      'question': next_question.format()
    }), 200

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  # * DONE
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False, 
      'error': 404,
      'message': "Resource not found"
      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "Unprocessable request"
      }), 422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": "bad request"
      }), 400

  @app.errorhandler(500)
  def internal_server_error(error):
    return jsonify({
      'success': False,
      'error': 500,
      'message': 'An error has occured, please try again'
      }), 500
  
  return app
    