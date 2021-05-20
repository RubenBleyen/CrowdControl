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

def webcam():
    cap = cv2.VideoCapture("rtsp://ubnt:Ferr0l0gic1@192.168.99.41:554/s1")
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

if __name__ == '__main__':
    app.run(port=5002)    