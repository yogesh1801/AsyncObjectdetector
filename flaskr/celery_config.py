from celery import Celery
import os 

broker_url = os.getenv('CELERY_BROKER_URL', 'redis://127.0.0.1:6379/0')
backend_url = os.getenv('CELERY_RESULT_BACKEND', 'redis://127.0.0.1:6379/0')

celery_app = Celery('main', broker=broker_url, backend=backend_url)
celery_app.autodiscover_tasks(['flaskr.utils.process_image'])

celery_app.conf.task_routes = {
    'flaskr.utils.process_image': {'queue': 'cloud_queue'},
}

celery_app.conf.update(
    result_expires=60,  
)


with celery_app.connection() as connection:
    connection.ensure_connection()
    print("Connected to Redis successfully")