from download_model import download_model
import os

try : 
    os.makedirs('tmp')
except OSError:
    pass

MODEL_URL = os.environ.get('MODEL_URL')
MODEL_DIR = 'flaskr/model'

os.makedirs(MODEL_DIR)
download_model(MODEL_URL, MODEL_DIR)
