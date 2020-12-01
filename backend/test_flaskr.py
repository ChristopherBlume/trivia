import os
import unittest
import json
from flask.globals import request
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.uname = 'postgres'
        self.pw = '12345'
        self.database_name = "trivia"
        self.database_path = "postgres://{}:{}@{}/{}".format(self.uname, self.pw,'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass


    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    """
    Test Case: GET - /questions
    """

    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    """
    Test Case: GET - /questions beyond valid page
    """
    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')
   
    """
    Test Case: POST - /questions to create a question
    """
    def test_create_question(self):

        mock_question = {
            'question': 'Mock Question',
            'answer': 'Mock Answer',
            'difficulty': 1,
            'category': 1
        }

        response = self.client().post('/questions', json=mock_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Question successfully created!')


    """
    Test Case: POST - /questions to create a question ERROR case
    """
    def test_create_question_emtpy_data(self):
        empty_question = {
            'question': '',
            'answer': '',
            'difficulty': 1,
            'category': 1,
        }

        response = self.client().post('/questions', json=empty_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable request')

    """
    Test Case: DELETE - /questions/<int:question_id> to delete a question
    """
    def test_successful_delete_question(self):
        # in order to test this endpoint i need a valid question in the database.
        question = Question(
            question='Test Question which needs to be deleted.',
            answer='Test Anwser to be deleted',
            difficulty=1,
            category='1'
        )

        # insert to database
        question.insert()

        # get id 
        id = question.id

        # delete mock question, process request
        response = self.client().delete('/questions/{}'.format(id))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], "Question successfully deleted")  

    """
    Test Case: DELETE - /questions/<int:question_id> to delete a question ERROR case
    """
    def test_unsuccessful_delete_question(self):
        # Test to delete a non-existing question

        response = self.client().delete('/questions/1348796')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'An error has occured, please try again')

    """
    Test Case: POST - /questions/search WITH Results
    """
    def test_get_question_search_with_results(self):
        res = self.client().post('/questions/search', json={'searchTerm': 'a'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    """
    Test Case: POST - /questions/search WITHOUT Results
    """
    def test_get_question_search_without_results(self):
        res = self.client().post('/questions/search', json={'searchTerm': 'ksadljfisoenfoöfioejfeisjfm,awdojda'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual((data['message']), 'Resource not found')    


    """
    Test Case: GET - /categories
    """

    def test_get_all_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    """
    Test Case: GET - /categories NON EXISTING category
    """

    def test_get_invalid_category(self):
        res = self.client().get('/categories/12345678')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')    


    """
    Test Case: GET - /categories/<int:category_id>/questions 
    """
    def test_get_questions_by_category(self):
        # 6 == Sports category
        response = self.client().get('/categories/6/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotEqual(len(data['questions']), 0)
        self.assertEqual(data['current_category'], 6)

    """
    Test Case: POST - /quizzes
    """
    def test_play_quiz(self):
        quiz_data = {
            'previous_questions': [3, 5],
            'quiz_category': {'type': 'Science', 'id': 1}
        }

        response = self.client().post('/quizzes', json=quiz_data)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    """
    Test Case: POST - /quizzes ERROR case
    """
    def test_play_quiz_no_data(self):
        # Test if playing is possible if no data is passed
        response = self.client().post('/quizzes', json={})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()