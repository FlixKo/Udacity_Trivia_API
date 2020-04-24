# Full Stack Trivia API Final Project

Documentation on how to setup a local test environment can be found in the READMEs of the subpages (frontend and backend).

## Endpoints
GET '/categories'
GET '/questions'
DELETE '/questions/<int:question_id>'
POST 'questions'
POST 'searchQuestions'
GET '/categories/<int:category_id>/questions'
POST '/quizzes'

# GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

# GET '/questions'
- Fetches a list of questions in which the keys are the ids, answer, category, difficulty and the question itself
- Request Arguments: None
- Returns: A list of categories, the current category, number of questions overall and a list of question objects with ids, answer, category, difficulty and the question itself 
{
  "categories": [
    "Science", 
    "Art", 
    "Geography", 
    "History", 
    "Entertainment", 
    "Sports"
  ], 
  "current_category": [
    2, 
    3, 
    4, 
    5, 
    6
  ], 
  "questions": [
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }, 
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }
  ], 
  "success": true, 
  "total_questions": 26
}

# DELETE '/questions/<int:question_id>'
- Deletes a question using its id
- Request Arguments: None
- Returns: the id of the deleted object
{
  "deleted": 31, 
  "message": "Question successfully deleted.", 
  "success": true
}

# POST 'questions'
- posts a new question
- Request Arguments: a question object
{question: "Test ", answer: "test", difficulty: 1, category: 1}
- Returns: the submitted question
{
  "created": 37, 
  "questions": {
    "answer": "test", 
    "category": 1, 
    "difficulty": 1, 
    "id": null, 
    "question": "Test "
  }, 
  "success": true, 
  "total_questions": 26
}

# POST 'searchQuestions'
- searches for a question using any word contained in the question, case insensitive
- Request Arguments: the search term
{searchTerm: "test"}
- Returns: the list of found questions
{
  "current_category": [
    1
  ], 
  "questions": [
    {
      "answer": "test", 
      "category": 1, 
      "difficulty": 1, 
      "id": 37, 
      "question": "Test "
    }
  ], 
  "success": true, 
  "total_questions": 26
}

# GET '/categories/<int:category_id>/questions'
- get questions based on their category
- Request Arguments: None
- Returns: the list of found questions for the matching category
{
  "categories": [
    {
      "id": 1, 
      "type": "Science"
    }, 
    {
      "id": 2, 
      "type": "Art"
    }, 
    {
      "id": 3, 
      "type": "Geography"
    }, 
    {
      "id": 4, 
      "type": "History"
    }, 
    {
      "id": 5, 
      "type": "Entertainment"
    }, 
    {
      "id": 6, 
      "type": "Sports"
    }
  ], 
  "current_category": [
    6
  ], 
  "questions": [
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ], 
  "success": true, 
  "total_questions": 2
}

# POST '/quizzes'
- play the game
- Request Arguments: previous questions and the quiz category
{previous_questions: [], quiz_category: {type: "Art", id: 1}}
- Returns: a random question of that category that should be answered
{
  "previous_questions": [], 
  "question": {
    "answer": "Blood", 
    "category": 1, 
    "difficulty": 4, 
    "id": 22, 
    "question": "Hematology is a branch of medicine involving the study of what?"
  }, 
  "quizCategory": {
    "id": 1, 
    "type": "Art"
  }, 
  "success": true
}

