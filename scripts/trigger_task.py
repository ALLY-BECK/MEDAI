import os
import sys

# Добавляем корневую директорию в PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.tasks import dummy_task

app = create_app()
with app.app_context():
    result = dummy_task.delay("Test Celery Integration")
    print(f"Task dispatched with ID: {result.id}")
