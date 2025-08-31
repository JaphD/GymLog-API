
1. About The Project
The GymLog API is the backend service for a comprehensive fitness tracker. It provides a secure and organized way for users to store their workout data and access powerful analytics. It is designed with a clear focus on scalability, performance, and security, making it a reliable foundation for any frontend application (web or mobile).

Built With:

Python 3.13

Django

Django REST Framework

Django Simple JWT

MySQL

2. Key Features
User Authentication & Management: Secure user registration and login using JSON Web Tokens (JWT).

Workout Management: Full CRUD (Create, Retrieve, Update, Delete) functionality for workout logs, including details like exercise name, weight, reps, sets, and workout duration.

Real-time Analytics: On-demand calculation of key weekly metrics such as total workout volume, max lift, and estimated calories burned.

API Enhancements: Implemented pagination and filtering to handle large datasets and provide a user-friendly way to query data.

Security: Secured with JWT authentication and configured to use environment variables for sensitive data, ensuring a secure production environment.

3. Prerequisites
To run this project locally, you need the following installed:

Python 3.13

pip (Python package installer)

A MySQL database

4. Getting Started
Follow these steps to get a local copy of the project up and running.

1. Clone the repository

Bash

git clone https://github.com/JaphD/GymLog-API.git
2. Create and activate a virtual environment

Bash

python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
3. Install dependencies

Bash

pip install -r requirements.txt
4. Set up environment variables
Create a .env file in the root directory and add your database credentials and Django's secret key.

# .env file
SECRET_KEY=your_very_long_and_complex_secret_key
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=3306
5. Run database migrations

Bash

python manage.py makemigrations
python manage.py migrate
6. Run the development server

Bash

python manage.py runserver
5. API Endpoints
All API endpoints are prefixed with /api/.

Authentication
| Endpoint | Method | Description |
| :--- | :--- | :--- |
| /api/users/register/ | POST | Create a new user account. |
| /api/users/login/ | POST | Authenticate a user and get JWT tokens. |
| /api/users/profile/ | GET | Retrieve the authenticated user's profile. |

Workouts
| Endpoint | Method | Description |
| :--- | :--- | :--- |
| /api/workouts/ | GET | List all workouts for the authenticated user. Supports pagination and filtering. |
| /api/workouts/ | POST | Create a new workout entry. |
| /api/workouts/<id>/ | GET | Retrieve a single workout by ID. |
| /api/workouts/<id>/ | PUT | Update a specific workout. |
| /api/workouts/<id>/ | DELETE | Delete a workout. |

Analytics
| Endpoint | Method | Description |
| :--- | :--- | :--- |
| /api/analytics/weekly/ | GET | Retrieve weekly analytics (total volume, max lift, etc.). |

6. Authentication
To access protected endpoints, you must include a valid JWT access token in the Authorization header of your request, using the Bearer token scheme.

Example Request Header:

Authorization: Bearer <your_access_token>
7. Deployment
The project is configured for deployment on Heroku. The following files are included in the root directory to facilitate deployment:

Procfile: Specifies the command to run the web server (gunicorn).

runtime.txt: Specifies the Python version to be used by Heroku.

requirements.txt: Lists all project dependencies.
