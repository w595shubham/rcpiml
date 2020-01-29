from src import app
from src.infrastructure.security.authentication.token import mod as token
from src.resources.objectdetection.objectdetection import object_detection_blueprint

app.register_blueprint(object_detection_blueprint)
app.register_blueprint(token)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
