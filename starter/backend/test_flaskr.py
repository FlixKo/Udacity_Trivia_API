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
        self.database_name = "trivia_test"
        #self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        self.database_path = 'postgres://ubuntu:ubuntu@localhost:5432/' + self.database_name
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'What is 1+1?',
            'answer': '2',
            'category': '2',
            'difficulty': '1'
        }

        self.search_term = {'searchTerm': 'Cassius'}
        self.error_search_term = {'searchTerm': 'asdgfdfgads'}

        self.quizzes = {
            'previous_questions': [22],
            'quiz_category': {
                'type': 'Art',
                'id': 1}}
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

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_categories'], 6)
        self.assertEqual(res.status_code, 200)

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)

    def test_delete_question(self):
        res = self.client().delete('/questions/1')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 1).one_or_none()

        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        self.assertEqual(res.status_code, 200)

    def test_post_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)

    def test_search_question(self):
        res = self.client().post('/searchQuestions', json=self.search_term)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['current_category'], [4])
        self.assertEqual(res.status_code, 200)

    def test_get_questions_based_on_category(self):
        res = self.client().get('/categories/4/questions')
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['current_category'], [4])
        self.assertEqual(res.status_code, 200)

    def test_quizzes(self):
        res = self.client().post('/quizzes', json=self.quizzes)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)

    def test_404_no_questions_on_search(self):
        res = self.client().post('/searchQuestions', json=self.error_search_term)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'Not found')
        self.assertEqual(data['success'], False)

    def test_422_no_question_of_category(self):
        res = self.client().get('/categories/100/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['message'], 'Not processable')
        self.assertEqual(data['success'], False)
        


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
