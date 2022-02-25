from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from datetime import datetime

from PIL import Image
import io

from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials

ENDPOINT = "https://signlanguageproject-prediction.cognitiveservices.azure.com/"
prediction_key = "ada5705628444484993c32a0776ca965"
prediction_resource_id = "/subscriptions/979b4825-25a2-4a44-b45b-9ec15fb3d60c/resourceGroups/Jonathan-Sign-Language-Proect/providers/Microsoft.CognitiveServices/accounts/SignLanguageProject-Prediction"
project_id = "7eae198c-b416-4b84-b5d9-c2a4e7ec876a"
publish_iteration_name = "Iteration1"
prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)

async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['TEMPLATES_AUTO_RELOAD'] = True
socketio = SocketIO(app)

@socketio.on("image")
def process(msg):
    print(msg)
    image = Image.open(io.BytesIO(msg))
    image.show()

    # Azure Custom Vision Part
    # do image processing thing
    emit("answer", 'Server received message "%s" at %s' % (msg, datetime.now().strftime("%H:%M:%S")))

@app.route("/")
def home():
    return render_template('website.html', async_mode=socketio.async_mode)

if __name__ == "__main__":
    socketio.run(app, debug=True, port=5005)
