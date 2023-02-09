# TRIVIA API 

## API
### Getting Started
BASE URL: At present this app can only be run locally and is not hosted as a base URL.The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.
Authentication: This version of the application does not require authentication or API keys.
### Error Handling
Errors are returned as JSON objects in the following format:
```JSON
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:

400: Bad Request
404: Resource Not Found
422: Not Processable

### END POINTS
`GET/Categories`
General: Returns all available categories
Sample: curl http://127.0.0.1:5000/categories
```json
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}
```

`GET/questions`

General: Returns all available questions
Sample: curl http://127.0.0.1:5000/questions
```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
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
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "total_categories": null,
  "total_questions": 20
}
```

`GET/questions?page=<page_number>`
Genral: Fetches a paginated dictionary of questions of all available categories
Sample: curl http://127.0.0.1:5000/questions?page=<page_number>
 
 ```json
 {
    "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
    }, 
    "current_category": null, 
    "questions": [
    {
        "answer": "Maya Angelou", 
        "category": 4, 
        "difficulty": 2, 
        "id": 5, 
        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
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
    "total_questions": 2
}
```

`DELETE/questions/<question_id>`
General:  Delete the question of the given ID if it exists.
Sample: curl -X DELETE http://127.0.0.1:5000/books/26
```json
{
  "deleted": "26", 
  "success": true
}
```

`POST/questions`
General: Add a new question to the repository of available questions
```json
{
    "answer": "blue",
    "category": "2",
    "created": 31,
    "difficulty": 1,
    "success": true
}
```

`POST/questions/search`
General: Fetches all questions where a substring matches the search term
```json
{   
  "current_category": null, 
  "questions": [
    {
      "answer": "orange", 
      "category": 2, 
      "difficulty": 1, 
      "id": 29, 
      "question": "What is the colour of orange"
    }
  ], 
  "success": true, 
  "total_questions": 1
}
```

`GET/categories/<int:category_id>/questions`
General: Fetches a dictionary of questions for the specified category
```json
{
  "current_category": 1,
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ],
  "success": true,
  "total_questions": 3
}
```

`POST/quizzes`
General: Fetches one random question within a specified category. Previously asked questions are not asked again.
```json
{
  "question": {
    "answer": "Red", 
    "category": 1, 
    "difficulty": 4, 
    "id": 20, 
    "question": "What is the colour of apple"
  }, 
  "success": true
}
```
## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```