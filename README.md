# Task Manager

A simple Django task manager: create, edit, delete, complete, search and filter tasks.

## Run locally
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Open http://127.0.0.1:8000/ (admin at /admin/).
