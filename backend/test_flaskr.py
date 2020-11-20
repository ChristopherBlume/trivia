import os
import unittest
import json
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
        self.database_name = "trivia_test"
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

    def test_get_questions(self):
        # Test the response from the endpoint
        response = self.client().get('/questions')
        self.assertEqual(response.status_code, 200)
        # Loading response in json
        data = json.loads(response.data)
        self.assertEqual(data['success'], True)

    """
    Test Case: GET - /categories
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()