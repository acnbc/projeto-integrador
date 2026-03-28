# FastAPI-Todo
github code for article https://gerrysabar.medium.com/fastapi-simple-crud-with-mysql-sqlalchemy-e60dd04a5c7e

## Installation

### Prerequisites

Ensure you have the following installed:
- [Python] (https://www.python.org/downloads/) (v3)

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/gerry-sabar/fastapi-todo

2. Inside project root directory create virtual environment:
    ```bash
    python3 -m venv venv

3. Activate the virtual enviroment:
    ```bash
    source venv/bin/activate

4. Install requirements:
    ```bash
    pip3 install -r requirements.txt

5. Adjust database connection in database.py according to your mysql configuration

6. Run locally:
    ```bash
    fastapi dev main.py

7. You can access API documentation from here:
    ```bash
    http://localhost:8000/docs