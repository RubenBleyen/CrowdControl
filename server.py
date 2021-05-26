from flask import Flask, request, Response, session
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
from flask_session import Session
from json import dumps
from flask_jsonpify import jsonify
import object_detection
import cv2

app = Flask("Solita")
api = Api(app)
CORS(app)
SECRET_KEY = "qsmdlfkqjsdmfkqjezk"
Session(app)

@app.route("/")

@app.route("/webcam", methods=["POST", "GET"])
def video_feed():    
    if request.method == "POST":
        object_detection.set_source((int(request.data)))
        return Response()
    return Response(object_detection.detection(object_detection.get_source()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/object_list")    
def object_list():
    return object_detection.get_detection_list()

if __name__ == '__main__':
    app.run(port=5002)    