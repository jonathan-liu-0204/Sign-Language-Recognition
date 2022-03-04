from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from datetime import datetime

from PIL import Image
import io

from threading import Thread, Event

from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials

ENDPOINT = "PUT YOUR CUSTOM VISION ENDPOINT HERE"
prediction_key = "PUT YOUR CUSTOM VISION PREDICTION KEY HERE"
prediction_resource_id = "PUT YOUR CUSTOM VISION PREDICTION RESOURCE ID HERE"
project_id = "PUT YOUR CUSTOM VISION PROJECT ID HERE"
publish_iteration_name = "PUT YOUR CUSTOM VISION PUBLISH ITERATION NAME HERE"
prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)

output = []

async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['TEMPLATES_AUTO_RELOAD'] = True
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on("image")
def process(msg):
    #print(msg)
    image = Image.open(io.BytesIO(msg))
    # image.show()

    # Azure Custom Vision Part
    # try:
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    output.clear()
    results = predictor.classify_image(
        project_id, publish_iteration_name, img_byte_arr)

    # Display the results.
    count = 0
    for prediction in results.predictions:
        # print("\t" + prediction.tag_name +": {0:.2f}%".format(prediction.probability * 100))
        output.append(prediction.tag_name)
        if count > 1:
            break
        count = count + 1
    print(output)
    print()

    now = datetime.now()

    emit("answer", "Received Time:　%s 　 Top 3 results:　1: %s　2: %s　3: %s" %(now.strftime("%H : %M : %S"), output[0], output[1], output[2]))

@app.route("/")

def home():
    return render_template('website.html', async_mode=socketio.async_mode)

if __name__ == "__main__":
    socketio.run(app, debug=True, port=5002)
