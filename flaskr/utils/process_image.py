import numpy as np
from PIL import Image
import io
import tensorflow as tf
from flaskr.utils.classnames import getClassName
from flaskr.celery_config import celery_app

MODEL_DIR = "flaskr/model"
model = tf.saved_model.load(MODEL_DIR)

def image_np(data):
    return np.array(Image.open(io.BytesIO(data)))

@celery_app.task
def process_image(path):
    try:
        with open(path, 'rb') as f:
            data = f.read()
            image = image_np(data)
        
        if len(image.shape) == 2:  
            image = np.stack([image] * 3, axis=-1)
        elif image.shape[2] == 1:  
            image = np.concatenate([image] * 3, axis=-1)
        elif image.shape[2] == 4:
            image = image[..., :3]

        input_tensor = tf.convert_to_tensor(image, dtype=tf.uint8)
        input_tensor = tf.expand_dims(input_tensor, axis=0)

        detections = model(input_tensor)
        
        detection_scores = detections['detection_scores'][0].numpy()
        detection_classes = detections['detection_classes'][0].numpy().astype(np.int64)
        detection_boxes = detections['detection_boxes'][0].numpy()

        results = []
        for i in range(len(detection_scores)):
            if detection_scores[i] > 0.5:
                class_id = int(detection_classes[i])
                class_name = getClassName(class_id)
                result = {
                    'score': float(detection_scores[i]),
                    'class': class_id,
                    'name': class_name,
                    'box': detection_boxes[i].tolist()
                }
                results.append(result)

        return results
    
    except Exception as e:
        return {'error': str(e)}

