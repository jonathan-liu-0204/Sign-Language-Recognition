#Import necessary libraries
from multiprocessing import Process
from flask import Flask, render_template, Response
import cv2
from bs4 import BeautifulSoup
from turbo_flask import Turbo
import threading

from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials
import os, time, uuid

# Initialize the Flask app
app = Flask(__name__)
turbo = Turbo(app)

ENDPOINT = "https://signlanguageproject-prediction.cognitiveservices.azure.com/"
prediction_key = "ada5705628444484993c32a0776ca965"
prediction_resource_id = "/subscriptions/979b4825-25a2-4a44-b45b-9ec15fb3d60c/resourceGroups/Jonathan-Sign-Language-Proect/providers/Microsoft.CognitiveServices/accounts/SignLanguageProject-Prediction"

project_id = "7eae198c-b416-4b84-b5d9-c2a4e7ec876a"
publish_iteration_name = "Iteration1"

prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)

#capture video through cv2
camera = cv2.VideoCapture(0)
'''
for ip camera use - rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' 
for local webcam use cv2.VideoCapture(0)
'''

output = []

def update_ans():
    with app.app_context():
        while True:
            time.sleep(1)
            turbo.push(turbo.replace(render_template('result.html'), 'load'))

# def classify():
#     # properties of azure cv
#     # while True:
#     try:
#         output = []

#         # result, image = camera.read()
#         # cv2.imwrite("output.png", image)

#         with open("output.jpg", "rb") as image_contents:
#             results = predictor.classify_image(project_id, publish_iteration_name, image_contents.read())

#             # Display the results.
#             count = 0
#             for prediction in results.predictions:
#                 # print("\t" + prediction.tag_name +": {0:.2f}%".format(prediction.probability * 100))
#                 output.append([prediction.tag_name, (prediction.probability * 100)])
#                 if count > 1:
#                     break
#                 count = count + 1
#             print(output)
#             print()
            
#     except KeyboardInterrupt:
#         print ('KeyboardInterrupt exception is caught')
#         # break
#     except:
#         print("Sth went wrong with the recognition. :(")

def changeText(text):
    # document.getElementById("result").data = text
    html_file = open("templates/index.html", "r")
    soup = BeautifulSoup(html_file, 'html.parser')
    tmp = soup.find(id="ans")
    tmp.string.replace_with('hahahahaha')
    # tmp = tmp.replaceWith('<div class="ans" id="ans">' + text + '</div>')
    open("templates/index.html", 'wb').write(tmp)
    print(tmp)


def gen_frames():  
    while True:
        # changeText("yoyoyo")
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            cv2.imwrite("output.jpg", frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')  # concat frame one by one and show result

@app.before_first_request
def before_first_request():
    threading.Thread(target = update_ans).start()

@app.route('/')
def index():
    # return "Hello World! This is Hello Page "
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.context_processor
def update_result():    
    try:
        output.clear()
        # result, image = camera.read()
        # cv2.imwrite("output.png", image)

        with open("output.jpg", "rb") as image_contents:
            results = predictor.classify_image(project_id, publish_iteration_name, image_contents.read())

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
    except KeyboardInterrupt:
        print ('KeyboardInterrupt exception is caught')
    except:
        print("Sth went wrong with the recognition. :(")
    # yield({'pos1': output[0], 'pos2': output[1], 'pos3': output[2]})
    return {'pos1': output[0], 'pos2': output[1], 'pos3': output[2]}

if __name__ == "__main__":
    app.run()

#this tells how to update text without refreshing
# https://blog.miguelgrinberg.com/post/dynamically-update-your-flask-web-pages-using-turbo-flask

#Local Git deployment to Azure App Service
#https://docs.microsoft.com/en-us/azure/app-service/deploy-local-git?tabs=portal

#Video Streaming in Web Browsers with OpenCV & Flask
#https://towardsdatascience.com/video-streaming-in-web-browsers-with-opencv-flask-93a38846fe00

#Deploy
# 1. git add . 
# 2. git commit -m ""
# 3. git push azure main:master 