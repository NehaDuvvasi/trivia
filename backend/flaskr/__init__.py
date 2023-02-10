import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import json

from models import setup_db, Question, Category, db

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
        categories = db.session.query(Category).order_by(Category.type).all()
        result = {
            "success": True,
            "categories": {category.id: category.type for category in categories},
        }
        if len(categories) == 0:
            abort(404)
        return jsonify(result)

    @app.route("/questions")
    def get_questions():
        selection = Question.query.all()
        # questions = paginate_questions(request, selection)
        

        categories = Category.query.all()
        questions = paginate_questions(request, selection)
        result = {
            "success": True,
            "questions": questions,
            "total_questions": len(selection),
            "categories": {category.id: category.type for category in categories},
            "current_categories": None,
        }
        if len(questions) == 0:
            abort(404)
        return jsonify(result)

    @app.route("/questions/<question_id>", methods=["DELETE"])
    def delete_question(question_id):
        question = db.session.query(Question).get(question_id)
        question.delete()
        return jsonify({"success": True, "deleted": question_id})

    @app.route("/questions", methods=["GET", "POST"])
    def add_question():
        question_data = json.loads(request.data)
        new_question = question_data["question"]
        new_answer = question_data["answer"]
        new_difficulty = question_data["difficulty"]
        new_category = question_data["category"]

        if (
            question_data,
            new_question,
            new_answer,
            new_category,
            new_difficulty,
        ) == None:
            abort(422)


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
        try:
            question_data = json.loads(request.data)
            search_term= question_data['searchTerm']
            if (search_term):
                search_word = search_term
                selection = db.session.query(Question).filter(
                    Question.question.ilike("%" + search_word + "%")).all()
                paginated = paginate_questions(request, selection)
                question = Question.query.all()
                result = ({
                    'success': True,
                    'questions': paginated,
                    'total_questions': len(question)
                })
                return jsonify(result)
        except Exception as e:
            print(e)

    @app.route("/categories/<int:category_id>/questions", methods=["GET", "POST"])
    def get_questions_by_category(category_id):
        question_data = Question.category == str(category_id)
        selection = db.session.query(Question).filter(question_data).all()
        paginated = paginate_questions(request, selection)
        result = (
            {
                "success": True,
                "questions": paginated,
                "total_questions": len(selection),
                "category": category_id,
            }
        )
        return jsonify(result)

    @app.route("/quizzes", methods=["POST"])
    def play_quiz():
        try:
            data =json.loads(request.data)
            if not all(key in data for key in ["quiz_category", "previous_questions"]):
                abort(422)
            prev_ques = data['previous_questions']
            choose_category = data['quiz_category']
            if choose_category["type"] == "click":
                available_questions = db.session.query(Question).all()
            else:
                available_questions = db.session.query(Question).filter_by(category=choose_category['id']).all()
                question =db.session.query(Question).all()
            new_question = (
                random.choice(available_questions).format()
                if available_questions
                else None
            )
            total = len(available_questions)
            def random_question():
                return available_questions[random.randrange(0, len(available_questions))] if len(available_questions) > 0 else None
            def repeated(question):
                repeated = False
                for n in prev_ques:
                    if (n == question.id):
                        repeated = True
                return repeated
            question = random_question()
            while (repeated(question)):
                question = random_question()
                if (len(prev_ques) == total):
                    result = ({
                        'success': True
                    })
                    return jsonify(result)
            result = ({
                'success': True,
                'question': question.format()
            })
            return jsonify(result)
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
