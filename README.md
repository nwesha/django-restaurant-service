# Django Restaurant Service

Django Restaurant Service is a Django-based web application designed to manage a restaurant service. The project provides functionalities for managing menus, orders, and users within a restaurant context.

## Features

### Menu Management

- **Create Menu Items:** Add new dishes to the menu with details like name, description, price, and category.
- **Update Menu Items:** Modify existing menu items as needed.
- **Delete Menu Items:** Remove items that are no longer offered.

### User Management

- **User Registration:** Allow new users to register and create accounts.
- **User Authentication:** Secure login/logout functionality.


## Installation

### Prerequisites

- Python 3.8+
- Django 3.2+
- pip

### Steps

1. **Clone the repository:**

   ```sh
   git clone https://github.com/nwesha/django-restaurant-service.git
   cd django-restaurant-service
   
2. **Create and activate a virtual environment:**
   
   ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
   
3. **Install the dependencies:**

    ```sh
    pip install -r requirements.txt

4. **Apply the migrations:**

    ```sh
    python manage.py migrate

5. **Create a superuser (for accessing the admin interface):**

    ```sh
    python manage.py createsuperuser

6. **Run the development server:**

    ```sh
    python manage.py runserver

## Usage

### Accessing the Application

Open your browser and navigate to [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

### Admin Interface

Navigate to [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) and log in using the superuser credentials to manage menus and users.

### Menu Management

- Use the admin interface to add, update, or delete menu items.
- Menu items can be categorized for easier browsing by customers.

### User Registration and Authentication

- Users can register for a new account through the registration page.
- Registered users can log in to place orders and manage their profiles.

### Order Processing

- Logged-in users can browse the menu and add items to their cart.
- Users can place orders, which will be tracked through the order management system (not implemented in this project yet).

## Project Structure

- **menu/**: Contains the menu-related models, views, and templates.
- **restaurant_service/**: Core application settings and configurations.
- **users/**: User authentication and profile management.
- **media/**: Storage for uploaded media files.
