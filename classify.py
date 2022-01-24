from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials
import os, time, uuid

import cv2

# Replace with valid values
ENDPOINT = "https://signlanguageproject-prediction.cognitiveservices.azure.com/"
prediction_key = "ada5705628444484993c32a0776ca965"
prediction_resource_id = "/subscriptions/979b4825-25a2-4a44-b45b-9ec15fb3d60c/resourceGroups/Jonathan-Sign-Language-Proect/providers/Microsoft.CognitiveServices/accounts/SignLanguageProject-Prediction"

project_id = "7eae198c-b416-4b84-b5d9-c2a4e7ec876a"
publish_iteration_name = "Iteration1"

prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)

while True:
    output = []

    cam_port = 0
    cam = cv2.VideoCapture(cam_port)
    result, image = cam.read()

    if result:
        cv2.imwrite("input.png", image)

        with open("input.png", "rb") as image_contents:
            results = predictor.classify_image(project_id, publish_iteration_name, image_contents.read())

            # Display the results.
            count = 0
            for prediction in results.predictions:
                # print("\t" + prediction.tag_name +": {0:.2f}%".format(prediction.probability * 100))
                output.append([prediction.tag_name, (prediction.probability * 100)])
                if count >= 2:
                    break
                count = count + 1
            print(output)
            print()
            time.sleep(1)
    else:
        print("camera cannot work properly...")
