import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * 10
    end = start + 10

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    return current_questions


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization"
        )
        response.headers.add(
            "Access-Control-Allow-Headers", "GET, POST, PATCH, DELETE, OPTIONS"
        )
        return response

    @app.route("/categories")
    def get_categories():
        categories = Category.query.order_by(Category.type).all()
        result = {
            "success": True,
            "categories": {category.id: category.type for category in categories},
        }
        if len(categories) == 0:
            abort(404)
        return jsonify(result)

    @app.route("/questions")
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        questions = paginate_questions(request, selection)

        categories = Category.query.order_by(Category.type).all()
        result = {
            "success": True,
            "questions": questions,
            "total_questions": len(selection),
            "categories": {category.id: category.type for category in categories},
            "total_categories": None,
        }
        if len(questions) == 0:
            abort(404)
        return jsonify(result)

    @app.route("/questions/<question_id>", methods=["DELETE"])
    def delete_question(question_id):
        question = Question.query.get(question_id)
        question.delete()
        return jsonify({"success": True, "deleted": question_id})

    @app.route("/questions", methods=["GET", "POST"])
    def add_question():
        data = request.get_json()

        if not (
            "question" in data
            and "answer" in data
            and "difficulty" in data
            and "category" in data
        ):
            abort(422)

        new_question = data.get("question")
        new_answer = data.get("answer")
        new_difficulty = data.get("difficulty")
        new_category = data.get("category")

        question = Question(
            question=new_question,
            answer=new_answer,
            difficulty=new_difficulty,
            category=new_category,
        )
        question.insert()

        return jsonify(
            {
                "success": True,
                "created": question.id,
                "answer": new_answer,
                "difficulty": new_difficulty,
                "category": new_category,
            }
        )

    @app.route("/questions/search", methods=["GET", "POST"])
    def search_questions():
        data = request.get_json()
        search_term = data.get("searchTerm", None)
        if search_term:
            search_questions = Question.query.filter(
                Question.question.ilike(f"%{search_term}%")
            ).all()
            return jsonify(
                {
                    "success": True,
                    "questions": [question.format() for question in search_questions],
                    "total_questions": len(search_questions),
                    "current_category": None,
                }
            )
        abort(404)

    @app.route("/categories/<int:category_id>/questions", methods=["GET", "POST"])
    def retrieve_questions_by_category(category_id):

        questions = Question.query.filter(Question.category == str(category_id)).all()

        return jsonify(
            {
                "success": True,
                "questions": [question.format() for question in questions],
                "total_questions": len(questions),
                "current_category": category_id,
            }
        )

    @app.route("/quizzes", methods=["POST"])
    def play_quiz():

        try:

            data = request.get_json()

            if not ("quiz_category" in data and "previous_questions" in data):
                abort(422)

            category = data.get("quiz_category")
            previous_questions = data.get("previous_questions")

            if category["type"] == "click":
                available_questions = Question.query.filter(
                    Question.id.notin_((previous_questions))
                ).all()
            else:
                available_questions = (
                    Question.query.filter_by(category=category["id"])
                    .filter(Question.id.notin_((previous_questions)))
                    .all()
                )

            new_question = (
                available_questions[
                    random.randrange(0, len(available_questions))
                ].format()
                if len(available_questions) > 0
                else None
            )

            return jsonify({"success": True, "question": new_question})
        except Exception as e:
            print(e)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"success": False, "error": 404, "message": "Not found"}), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    if __name__ == "__main__":
        app.run(debug=True)

    return app
