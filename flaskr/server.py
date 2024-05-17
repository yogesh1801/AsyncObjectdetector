from flaskr import create_app
from .apis.detect import dt
import os

app = create_app()
app.register_blueprint(dt)

@app.route('/')
def ready():
    return ("server is ready")