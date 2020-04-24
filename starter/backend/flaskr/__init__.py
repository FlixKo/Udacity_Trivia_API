import os
from flask import Flask, request, abort, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__, instance_relative_config=True)
  app.secret_key = "super secret key"
  setup_db(app)

  '''
  @: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  # cors = CORS(app, resources={r"*/api/*": {"origins": "*"}})
  
  CORS(app, resources={r"*/*": {"origins": "*"}})


  def paginate_questions(request, questions_list):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in questions_list]
    paginated_questions = questions[start:end]
    return paginated_questions


  '''
  @: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods','GET, POST, DELETE')
    return response

  '''
  @: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route("/categories", methods=['GET'])
  @cross_origin()
  def get_categories():
    categories = Category.query.all()

    category_items = [ category.type for category in categories]
    
    if len(category_items) == 0:
      abort(404)

    return jsonify({
      'success':True,
      'categories':category_items,
      'total_categories':len(category_items)
    })


  '''
  @: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route("/questions", methods=['GET'])
  @cross_origin()
  def get_questions():
    questions = Question.query.all()
    #formatted_questions = [question.format() for question in questions]
    
    current_questions = paginate_questions(request, questions)
    current_category = list(set([q['category'] for q in current_questions]))
    
    categories = Category.query.all()
    #formatted_categories = [category.format() for category in categories]
    #category_items = [(category.id, category.type) for category in categories]
    category_items = [ category.type for category in categories]

    if len(current_questions) == 0:
      abort(404)

    return jsonify({
      'success':True,
      'questions':current_questions,
      'total_questions':len(questions),
      'current_category': current_category,
      'categories': category_items
    })

  '''
  @: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  @app.route("/questions/<int:question_id>", methods=['DELETE'])
  @cross_origin()
  def delete_question(question_id):
    error = False
    try:
      Question.query.filter_by(id=question_id).delete()
      db.session.commit()
    except Exception as e:
      flash('An error occurred. Question could not be deleted.')
      flash(f'Error: {e}')
      error = True
      db.session.rollback()
    finally:
      db.session.close()

    if error:
      return jsonify({ 
        'success': False,
        'message': "Question could not be deleted."
      })
    else:
      return jsonify({ 
        'success': True,
        'message': "Question successfully deleted.",
        'deleted': question_id
      })

  '''
  @: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route("/questions", methods=['POST'])
  @cross_origin()
  def add_question():

    new_question = Question(
      question = request.get_json()['question'],
      answer = request.get_json()['answer'],
      category = request.get_json()['category'],
      difficulty = request.get_json()['difficulty']
    )

    formatted_question = new_question.format()
    new_question.insert()

    return jsonify({
      'success': True,
      'questions': formatted_question,
      'created': new_question.id,
      'total_questions': len(Question.query.all())
    })


  '''
  @: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  @app.route("/searchQuestions", methods=['POST'])
  @cross_origin()
  def search_questions():
    form = request.get_json()
    search_term = form.get('searchTerm')

    searched_questions = Question.query.filter(Question.question.ilike('%{}%'.format(search_term))).all()
    
    if searched_questions is None:
        abort(404)
    
    current_questions = paginate_questions(request, searched_questions)
    current_category = list(set([q['category'] for q in current_questions]))

    return jsonify({ 
      'questions' : current_questions,
      'total_questions' : len(Question.query.all()),
      'success' : True,
      'current_category' : current_category
    })


  '''
  @: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  @cross_origin()
  def get_question_by_category(category_id):
    categories = Category.query.all()
    formatted_categories = [c.format() for c in categories]
    questions = Question.query.filter_by(category = str(category_id)).all()
    formatted_questions = [q.format() for q in questions]
    current_questions = paginate_questions(request, questions)
    current_category = list(set([q['category'] for q in current_questions]))
    
    if len(current_questions) == 0:
      abort(404)

    return jsonify({          
      'questions': current_questions,
      'total_questions': len(questions),
      'current_category':  current_category,
      'categories': formatted_categories,
      'success': True
      })


  '''
  @: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  @app.route('/quizzes', methods=['POST'])
  @cross_origin()
  def quizzes():    
    try:
      data = request.get_json()
      previous_questions = data['previous_questions']
      quiz_category = data['quiz_category']

      questions = None        
      if quiz_category['type'] == "click":
        questions = Question.query.all()    
      else:
        questions=Question.query.filter_by(category =(quiz_category['id'])).all()       
      formatted_questions = [q.format() for q in questions]  
        
      possible_questions = []      
      for q in formatted_questions:
        if q['id'] not in previous_questions:
          possible_questions.append(q)

      question_sel = None
      if len(possible_questions) > 0:
        question_sel = random.choice(possible_questions)        

      return jsonify({
        'success': True,
        'question':question_sel,
        'previous_questions': previous_questions,
        'quizCategory':quiz_category
      })
    except Exception as ex:
      abort(422)


  '''
  @: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(500)
  def server_error(error):
    return jsonify({
      "success":False,
      "error":500,
      "message":"Internal Server Error"
    }), 500

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success":False,
      "error":400,
      "message":"Bad request"
    }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success":False,
      "error":404,
      "message":"Not found"
    }), 404

  @app.errorhandler(405)
  def not_allowed(error):
    return jsonify({
      "success":False,
      "error":405,
      "message":"Method not allowed"
    }), 405

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success":False,
      "error":422,
      "message":"Sent instructions are unprocessable"
    }), 422
  
  return app

    