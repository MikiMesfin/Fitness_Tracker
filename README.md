# Fitness Tracking API

A RESTful API built with Django REST Framework for tracking fitness activities and goals.

## Features

- User authentication with JWT tokens
- Activity tracking (running, cycling, weightlifting, swimming, yoga)
- Goal setting and progress monitoring
- Activity statistics
- Admin interface for data management

## Prerequisites

- Python 3.x
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd <project-directory>
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with:
```
DJANGO_SECRET_KEY=your_secret_key_here
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

## API Endpoints

### Authentication
- `POST /api/token/` - Obtain JWT token
- `POST /api/token/refresh/` - Refresh JWT token

### Users
- `POST /api/users/` - Register new user
- `GET /api/users/me/` - Get current user details

### Activities
- `GET /api/activities/` - List activities
- `POST /api/activities/` - Create activity
- `GET /api/activities/{id}/` - Retrieve activity
- `PUT /api/activities/{id}/` - Update activity
- `DELETE /api/activities/{id}/` - Delete activity
- `GET /api/activities/statistics/` - Get activity statistics

### Goals
- `GET /api/goals/` - List goals
- `POST /api/goals/` - Create goal
- `GET /api/goals/{id}/` - Retrieve goal with progress
- `PUT /api/goals/{id}/` - Update goal
- `DELETE /api/goals/{id}/` - Delete goal

## Testing

Run the test suite:
```bash
python manage.py test
```

## Admin Interface

Access the admin interface at `http://localhost:8000/admin/` using your superuser credentials.

## Tech Stack

- Django
- Django REST Framework
- Simple JWT
- SQLite (default database)

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

