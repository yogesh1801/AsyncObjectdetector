from flask import Blueprint, request, jsonify
import tensorflow as tf
from ..utils.process_image import process_image
import os

dt = Blueprint('detect', __name__, url_prefix='/api')

@dt.route('/detect/', methods=(['POST']))
def detect():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    file_path = os.path.join("tmp", file.filename)
    file.save(file_path)

    task = process_image.delay(file_path)

    return jsonify({'task_id': task.id}), 202
    