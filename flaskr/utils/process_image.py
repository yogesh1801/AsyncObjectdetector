import numpy as np
from PIL import Image
import io
import tensorflow as tf

MODEL_DIR = "flaskr\model"
model = tf.saved_model.load(MODEL_DIR)

def image_np(data):
    return np.array(Image.open(io.BytesIO(data)))

def process_image(path):
    try:
        with open(path, 'rb') as f:
            data = f.read()
            image = image_np(data)
        input_tensor = tf.convert_to_tensor(image)
        input_tensor = input_tensor[tf.newaxis,...]

        detections = model(input_tensor)    
        print(detections)
        detection_scores = detections['detection_scores'][0].numpy()
        detection_classes = detections['detection_classes'][0].numpy().astype(np.int64)
        detection_boxes = detections['detection_boxes'][0].numpy()

        results = []
        for i in range(len(detection_scores)):
            if(detection_scores[i] > 0.5):
                result = {
                    'score': float(detection_scores[i]),
                    'class': int(detection_classes[i]),
                    'box': detection_boxes[i].tolist()
                }
                results.append(result)

        return results
    
    except Exception as e:
        return {'error' : str(e)}

