# authentification_system

Custom Authentication & Access Control System
1. Overview

This Django project implements a custom authentication and authorization system without relying entirely on Django’s built-in authentication features. It allows user registration, login, logout, profile update, and soft deletion. Access to business resources is controlled based on roles and permissions.

2. Database Schema
Users

Custom user model User:

Field	Type	Description
first_name	Char	First name of the user
last_name	Char	Last name of the user
patronymic	Char	Optional middle name
email	Email	Unique email, used for login
password	Char	Hashed password
is_active	Boolean	Active status (soft deletion support)
is_staff	Boolean	Admin status
Roles & Permissions

Tables in permissions_app:

Role

name: role name (e.g., admin, user)

BusinessElement

name: resource name (e.g., documents, products)

AccessRoleRule

role → ForeignKey to Role

element → ForeignKey to BusinessElement

can_read: Boolean

can_write: Boolean

Example rules:

Role	Element	can_read	can_write
admin	documents	True	True
user	documents	True	False
3. Access Control Logic

Middleware AuthMiddleware checks:

If the user is authenticated → 401 Unauthorized if not.

If the user has access to the resource → 403 Forbidden if not.

Decorator @requires_permission("resource_name") marks API views with required access.

4. API Endpoints
Users
Endpoint	Method	Description
/api/users/register/	POST	Register new user
/api/users/login/	POST	Login
/api/users/logout/	POST	Logout
/api/users/update/	PUT	Update profile
/api/users/delete/	DELETE	Soft delete user
Business (Mock Objects)
Endpoint	Method	Description
/api/business/documents/	GET	Get list of documents (401/403 based on role)
5. How to Run

Activate environment:

.\env\Scripts\activate


Install dependencies (if needed):

pip install -r requirements.txt


Make migrations and migrate:

python manage.py makemigrations
python manage.py migrate


Seed initial roles and permissions:

python manage.py seed_permissions


Run the server:

python manage.py runserver

6. Testing Permissions

Unauthorized user:
Access /api/business/documents/ without login → returns 401 Unauthorized

User with no write access:
Login as user@example.com → POST/PUT attempts on restricted resources → returns 403 Forbidden

Admin user:
Login as admin@example.com → Full access → returns resource data

7. Notes

Soft deletion sets is_active=False, preventing login.

Roles and access rules can be extended via the permissions_app tables.

Mock business objects simulate real resources without database tables.