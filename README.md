# Web Programming Course - Homework 2

This repository contains the code for Homework 2 of the Web Programming Course Sharif University Fall 2025.
This is an implementaition of 'Achare' backend using Django and Django REST Framework.


## Quick Start

+ **Create virtual environment**
    ```bash
    python -m venv venv
    ```
+ **Activate virtual environment**
    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```
+ **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```
+ **Apply migrations**
    ```bash
    python manage.py migrate
    python manage.py makemigrations
    ```
+ Create basic groups (as roles)
    ```bash
    python manage.py setup_roles
    ```
+ **Run the development server**
    ```bash
    python manage.py runserver
    ```


## API Documentation
API documentation is available at `localhost:8000/docs/` once the server is running.
