from flaskr import create_app   
from flask import jsonify
from flask_cors import  CORS
from .apis.detect import dt
from flaskr.celery_config import celery_app

app = create_app()
CORS(app)

app.register_blueprint(dt)

@app.route('/')
def ready():
    return ("server is ready")

@app.route('/task/<task_id>', methods=['GET'])
def check_task(task_id):
    task = celery_app.AsyncResult(task_id)
    print(f"Task {task_id} is currently in state: {task.state}") 
    if task.state == 'SUCCESS':
        response = jsonify({"status": "SUCCESS", "filename": task.result})
        return response
    elif task.state == 'PENDING':
        return jsonify({"status": "PENDING"})
    else:
        return jsonify({"status": task.state})