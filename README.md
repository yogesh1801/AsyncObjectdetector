# Flask Application with Redis, Celery and Gunicorn

This project is a web application for object detection built with Flask, utilizing Redis for caching and task queue management, Celery for asynchronous task processing, and Gunicorn as the WSGI HTTP server.

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yogesh1801/allos-assign.git
    cd allos-assign
    ```

2. Create and activate a virtual environment:

    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the dependencies:

    ```sh
    pip install -r requirements.txt
    ```

## Configuration

1. To use your custom model on the flask application change the `MODEL_URL` in `run.sh` to link of your own model. 
(This application currently uses a lite version of Darknet framework trained on COCO 2017 dataset)

2. The link to Redis server can also be changed by defining `CELERY_BROKER_URL` and `CELERY_RESULT_BACKEND` in `run.sh` and `worker.sh` shell script

## Running the Application

1. Start the Redis server:

    ```sh
    sudo systemctl start redis
    ```

2. Start the Celery worker:

    ```sh
    bash worker.sh
    ```

3. Run the Flask application using Gunicorn:

    ```sh
    bash run.sh
    ```

# SSD MobileNet V2 Object Detection Model

This repository contains code for using the SSD MobileNet V2 object detection model from TensorFlow Hub. The model is designed for efficient and high-speed object detection in images and video streams.

## Model Overview

- **Model Name**: SSD MobileNet V2
- **Version**: 2
- **Framework**: TensorFlow
- **Source**: [TensorFlow Hub](https://tfhub.dev/tensorflow/ssd_mobilenet_v2/2)

The SSD MobileNet V2 model combines the Single Shot Multibox Detector (SSD) framework with the MobileNet V2 backbone, optimized for mobile and embedded vision applications. It is pre-trained on the COCO dataset, which contains over 330,000 images and more than 80 object categories.

## Key Features

- **SSD (Single Shot Multibox Detector)**: Enables detection of multiple objects within an image in a single pass.
- **MobileNet V2**: Lightweight and efficient, designed for fast inference on mobile and embedded devices.
- **Pre-trained Weights**: Trained on the COCO 2017 dataset, allowing recognition of common objects.

# Deployment on AWS EC2

1. Create a EC2 instance using you amazon AWS console on a ubuntu image.
2. Clone the repository:

    ```sh
    git clone https://github.com/yogesh1801/allos-assign.git
    cd allos-assign
    ```
3. Install and setup a redis server.

    ```sh
    sudo apt install redis
    ```

4. Follow the instructions, same as setting up the project locally.

5. setup nginx
    ```sh
    sudo apt install nginx
    ```

6. configure your nginx

    ```sh
    vi /etc/nginx/sites-enabled/{your-app-name}
    ```
    Go to insert mode and paste the following snippet

    ```sh
    server {
        listen 80;

        location / {
                proxy_pass {address-to-your-gunicorn-server};
                proxy_set_header Host $host;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        }

    }
    ```

# Object Detection API

This project provides an API for object detection using the SSD MobileNet V2 model. The API supports uploading an image to detect objects and querying the status and result of the detection task.

## API Endpoints

### 1. Detect Objects in an Image

- **Endpoint**: `/api/detect/`
- **Method**: `POST`
- **Description**: This endpoint accepts an image file, initiates an object detection task, and returns a task ID.

#### Request

- **Headers**:
  - `Content-Type: multipart/form-data`
- **Body**:
  - `file`: The image file to be uploaded for object detection.

#### Response

- **Status Code**: `200 OK`
- **Body**:
  ```json
  {
    "task_id": "your-task-id"
  }
  ```


### 2. Get Results

- **Endpoint**: `/task/{task_id}`
- **Method**: `GET`
- **Description**: This endpoint returns result of your task. 


#### Response

- **Status Code**: `200 OK`
- **Body**:
  ```json
  {
    "result": [
        {
            "box" : [],
            "class" : "value",
            "name" : "class_name",
            "score" : "confidence_score",
        },
    ],
    "status": "{status_of_request}"
    }
  ```

# Deployed Model

1. The model is currently deployed at http://3.26.55.124/ and can be used to test the APIs.

 

