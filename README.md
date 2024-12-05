# Blog Management System

The Blog Management System is a Django web application for managing blog posts and their associated comments.

## Installation

Follow these steps to set up the project on your local machine:

```bash
# Clone the Repository
git clone <URL_DU_DEPOT>
cd <NOM_DU_DOSSIER_CLONE>

# Create a Virtual Environment (Optional but Recommended)
python -m venv env
source env/bin/activate   # For Linux/Mac
env\Scripts\activate      # For Windows

# Install Dependencies
pip install -r requirements.txt

# Apply Database Migrations
python manage.py makemigrations
python manage.py migrate

# Create a Superuser
python manage.py createsuperuser

# Run the Development Server
python manage.py runserver
