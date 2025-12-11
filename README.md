### Padrones-CSE1-L-RestAPI
# CS New REST API - Final

Finals project for CSE1/L REST API.

## Description:
A Flask-based REST API with MySQL, CRUD operations, JWT security, XML/JSON output formatting, API testing, and search functionality.

## Status:
Completed

### 📌 Project Overview

This project is a CRUD REST API built using Flask and MySQL. It supports:

1. Create, Read, Update, Delete operations
2. MySQL database integration
3. Search functionality
4. JWT Authentication for protected routes
5. Response formatting (JSON or XML)
6. REST API testing using unittest
7. Clean project structure with Blueprints

### 🚀 Technologies Used

1. Python (Flask)
2. MySQL / MySQL Workbench (for my Database)
3. Flask-JWT-Extended (for authentication)
4. dicttoxml (for XML formatting)
5. flask_mysqldb (database connection)
6. unittest (for API testing)

## PROJECT STRUCTURE:

### PADRONES-CSE1-L-RESTAPI
    1. CSE1env:
        -Include
        -Lib
        -Scripts
        -.gitignore
    2. Routes:
        -elements.py
    3. Tests:
        -tests_api.py
    4. app.py
    5. README.md
    6. requirements.txt

### Installation Process: 
    
    1. Create a GitHub Repository.

    2. On CMD or Bash, Do this:
        - git clone <Repo Link>
        - cd <Repo Folder>

    3. Create and Activate Virtual Environment.
        - python -m venv venv
        - venv\scripts\activate

    4. Install Dependencies:
        - pip install -r requirements.txt

    5. Import Database.
        - Open MySQL Workbench → Server → Data Import
        - Select the file:cs_new_dump.sql
        - Choose database:cs_new
        - Click Start Import
    (In our situation, we've created our own database first right before, we've created the GitHub Repository - we need atleast 20 records for this one).

    6. 🔑 JWT Authentication
        - To access protected endpoints, obtain a token using: POST /login

        Sample Body:
        {
            "username": "USER",
            "password": "USER123"
        }
        
        Response:
        {
            "token": "<your_jwt_token>"
        }
        
        Include this token in your headers:
        Authorization: Bearer <token>

    7. 📡 API Endpoints
        - Public Endpoints (No Token Required)

        1. GET All Elements
        GET /api/elements?format=json or
        GET /api/elements?format=xml
        
        2. GET Element by ID
        GET /api/elements/<element_id>
        
        3. Search Elements
        GET /api/elements/search
        query=value&format=json|xml

        4. CREATE Element
        POST /api/elements

        sample:
        {
            "element":"Water",
            "element_state":"Liquid"
        }

        5. UPDATE Element
        PUT /api/elements/<element_id>
        
        6. DELETE Element
        DELETE /api/elements/<element_id>
    
    8. 💾 XML / JSON Formatting
        - All GET endpoints accept:

        ?format=json    (default)
        ?format=xml
        
        Example:
        GET /api/elements?format=xml

    9. 🧪 Running the Test Suite
        - From the project root: python -m unittest Tests/tests_api.py
        
        - Tests include:
            *GET all (public)
            *CREATE element (JWT)
            *UPDATE element (JWT)
            *DELETE element (JWT)
            *Invalid input validation
            *Public endpoint without token

    ***END***

### Author:
Kim Andrei D. Padrones -
BSCS3 BLOCK 2


