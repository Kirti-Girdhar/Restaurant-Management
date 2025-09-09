# Restaurant Management System

This is a Django-based mini project for managing restaurant operations. The project is organized into two main apps:

## Apps

### 1. hotel
Handles core hotel management logic and configuration.
- `settings.py`: Django settings for the project
- `urls.py`: URL routing
- `wsgi.py`/`asgi.py`: Server entry points

### 2. restaurant
Manages restaurant-specific features:
- `models.py`: Database models for menu items, staff, customers, and orders
- `views.py`: API and view logic
- `serializers.py`: Data serialization for API endpoints
- `admin.py`: Admin interface configuration
- `migrations/`: Database migration files

## Features
- Menu item management
- Staff and customer records
- Order processing
- RESTful API endpoints

## Setup
1. Clone the repository:
	```bash
	git clone https://github.com/Kirti-Girdhar/Restaurant-Management.git
	```
2. Install dependencies:
	```bash
	pip install -r requirements.txt
	```
3. Run migrations:
	```bash
	python manage.py migrate
	```
4. Start the development server:
	```bash
	python manage.py runserver
	```

## Notes
- The project uses SQLite for development.
- Sensitive and unnecessary files are ignored via `.gitignore`.

## License
This project is for educational purposes.
