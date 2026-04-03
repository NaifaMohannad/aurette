import os
from aurette_project.wsgi import application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aurette_project.settings')

app = application