# Animal Registry System - Back-end

## Overview
This is the back-end of the Animal Registry System, built with Django and Django REST Framework. It allows users to register animals, define their parents, and retrieve family trees. The application also provides a search functionality for animals by species, breed, and name.

## Technologies Used
- Django 4.x
- Django REST Framework
- SQLite (for data storage)
- Python 3.10+

## Installation and Configuration

### 1. Clone the Repository
Clone the repository to your local machine:

```bash
git clone <REPOSITORY_URL>
cd animal-registry-backend
2. Set Up Virtual Environment
Create and activate a virtual environment:

bash
Copiar
Editar
python -m venv venv
source venv/bin/activate  # On Linux/Mac
venv\Scripts\activate     # On Windows
3. Install Dependencies
Install the required dependencies:

bash
Copiar
Editar
pip install -r requirements.txt
4. Apply Database Migrations
Run the migrations to set up the database:

bash
Copiar
Editar
python manage.py migrate
5. Run the Application
Start the development server:

bash
Copiar
Editar
python manage.py runserver
The application will be available at http://127.0.0.1:8000/.

6. Run Tests
To run the unit tests for the project, use the following command:

bash
Copiar
Editar
python manage.py test
API Endpoints
The API is built using Django REST Framework and includes the following endpoints:

POST /api/animals/: Create a new animal.

PATCH /api/animals/<int:pk>/set-parents/: Set parents for an animal.

GET /api/animals/<int:pk>/tree/: Get the family tree (ancestors) of an animal.

GET /api/animals/<int:pk>/descendants/: Get the descendants of an animal.

GET /api/animal-search/: Search for animals by species, breed, and name.

Folder Structure
pgsql
Copiar
Editar
backend/
│── registry/
│   ├── migrations/       # Database migration files
│   ├── models.py         # Database models
│   ├── views.py          # API views
│   ├── urls.py           # URL routing
│   ├── serializers.py    # Serializers for data conversion
│   ├── tests.py          # Unit tests for the app
│   ├── admin.py          # Admin panel configuration
│   ├── apps.py           # App configuration
│── manage.py             # Django project management file
│── requirements.txt      # Project dependencies
│── db.sqlite3            # SQLite database file (for development)
Features
Animal Registration: Register new animals with name, species, breed, and birth date.

Parent Assignment: Assign parents to animals to build a family tree.

Family Tree: Retrieve the ancestors (family tree) of an animal.

Descendants: Get the descendants of an animal.

Animal Search: Search animals by species, breed, and name.

Final Considerations
The back-end is built with Django and Django REST Framework, providing a scalable and maintainable API.

The database is managed using SQLite for development purposes, but it can be replaced by any other database system if required.

The API has been tested with unit tests to ensure proper functionality.

About
This project is a back-end solution for an animal registry system. It manages animal data, family relationships, and allows querying of animals through a REST API.
