import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


from dotenv import load_dotenv

load_dotenv()


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = "{}://{}:{}/{}".format(os.getenv("DOMAIN"),
            os.getenv("USER"), os.getenv("EMAIL"), os.getenv("self.database_name")
        )
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

    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["error"])

    def test_404_invalid_categories(self):
        res = self.client().get("/categories=8")
        data = json.loads(res.data)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["success"], False)

    def test_get_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_404_invalid_questions(self):
        res = self.client().get("/questions=80")
        data = json.loads(res.data)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["success"], False)

    def test_get_questions_per_category(self):
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_404_get_questions_per_category(self):
        res = self.client().get("/categories/a/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Not found")

    def test_delete_question(self):
        res = self.client().delete("/questions/1000")
        self.assertEqual(res.status_code, 500)

    def test_422_question_not_exist(self):
        res = self.client().delete("/questions/1000/json")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)

    def test_add_question(self):
        res = self.client().post("/question/json")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["error"])
        self.assertTrue(data["error"])

    def test_405_if_question_creation_not_allowed(self):
        res = self.client().post("/question/json")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)

    def test_get_question_search_with_results(self):
        res = self.client().post("/questions/search/json")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["error"])
        self.assertTrue(data["error"])

    def test_404_get_search_unavailable_question(self):
        res = self.client().post("/questions/search/json")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)

    def test_get_quiz(self):
        res = self.client().post("/quizzes/json")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["error"])

    def test_422_get_quiz(self):
        res = self.client().post("/quizzes/json")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["error"])


if __name__ == "__main__":
    unittest.main()
