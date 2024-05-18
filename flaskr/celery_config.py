from celery import Celery
from dotenv import load_dotenv
load_dotenv()

celery_app = Celery('main', broker='redis://127.0.0.1:6379/0', backend='redis://127.0.0.1:6379/0')
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