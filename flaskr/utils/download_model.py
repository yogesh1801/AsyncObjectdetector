import tensorflow as tf
import tensorflow_hub as hub

def download_model(model_url, model_dir):
    print(f"Downloading model from {model_url}")
    model = hub.load(model_url)
    tf.saved_model.save(model, model_dir)
    print(f"Model saved to dir {model_dir}")
