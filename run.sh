export MODEL_URL="https://tfhub.dev/tensorflow/ssd_mobilenet_v2/2"

python setup.py
gunicorn -c gunicorn_config.py flaskr.server:app