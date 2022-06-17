# Social Media API

Social Media API built using FastAPI

## Public REST API

https://fastapi-social-media-api.herokuapp.com/

## Features

1) OAuth Authentication using JWT Token and Expiry Time.
 - Login with credentials.

2) User :-
 - Create a user.
 - Get all users.
 - Get a specific user by its id.
 - Update a user.
 - Delete a user.

3) Post :- 
 - Get all posts.
 - Get a specific post by its id.
 - Things only Registered and Authorized User can perform.
   - Create a post.
   - Update a post.
   - Delete a post. 
  
4) Vote :-
 - Only Register and Authorized User's can Vote on any post.


## Local Setup

1) Create a virtual environment using the command :-
  ```python 
    virtualenv venv
  ```

2) Now install all the requirements using the command :-
 ```python
    pip3 install -r requiremnts.txt
 ```

3) Now just run the command :-
 ```python
    uvicorn app.main:app --reload
 ```
 - Lets Break this command in pieces to understand this uvicorn command.
   - Uvicorn is an ASGI web server implementation for Python. Learn more about [Uvicorn](https://www.uvicorn.org/)
   - [app](/app) is the parent directory for the [main](/app/main.py) file (Note :- any other name can also be given to the directory as well as to the main file).
   - [app.main:app](/app/main.py) at last app is the instance of the fastAPI.
   - reload flag is used so that if any changes occur server gets reload by itself and the changes could get visible.