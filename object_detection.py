from datetime import datetime
from queue import Queue
from threading import Thread
from ctypes import *
import random
import os
import cv2
import time
import darknet
from detected_object import Detection

network, class_names, class_colors = darknet.load_network(
    "./cfg/yolov4.cfg",
    "./cfg/coco.data",
    "yolov4.weights",
    1
)
frame_queue = Queue()
darknet_image_queue = Queue(maxsize=1)
detections_queue = Queue(maxsize=1)
last_detection = []
fps_queue = Queue(maxsize=1)

width = darknet.network_width(network)
height = darknet.network_height(network)
last_detection_list = []
last_frame_list = []
detection_list = []
source_list = [0 ,"wheelchair.mp4", "pushing.mp4"]
count = 0
source = 0

def get_source():
    print(source)
    return source

def set_source(source_id):
    global source 
    source = source_id
    print(source)

def detection(camera_id):
    cap = cv2.VideoCapture(source_list[camera_id])
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (width, height),
                                   interpolation=cv2.INTER_LINEAR)
        frame_queue.put(frame_resized)
        img_for_detect = darknet.make_image(width, height, 3)
        darknet.copy_image_from_bytes(img_for_detect, frame_resized.tobytes())
        darknet_image_queue.put(img_for_detect)
        darknet_image = darknet_image_queue.get()
        prev_time = time.time()
        detections = darknet.detect_image(network, class_names, darknet_image, 0.5)
        detections_queue.put(detections)
        fps = int(1 / (time.time() - prev_time))
        fps_queue.put(fps)
        #print("FPS: {}".format(fps))
        darknet.free_image(darknet_image)
        random.seed(3)  # deterministic bbox colors
        frame_resized = frame_queue.get()
        detections = detections_queue.get()
        fps = fps_queue.get()
        last_frame_list.append(get_frame(frame_resized, detections))
        last_detection_list.append(detections)
        if len(last_frame_list) == 2:
            last_frame_list.pop(0)
        if len(last_detection_list) == 2:
            last_detection_list.pop(0)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + get_frame(frame_resized,
                                                               detections) + b'\r\n')  # concat frame one by one and show result


def get_frame(frame_resized, detections):
    if frame_resized is not None:
        frame = darknet.draw_boxes(detections, frame_resized, class_colors)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        return frame


def get_detection():
    if len(last_frame_list) != 0:
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + last_frame_list[
                   -1] + b'\r\n')  # concat frame one by one and show result
    last_frame_list.clear()


def get_detection_list():
    global count
    item_list = []
    if len(last_detection_list) != 0:
        count = count + 1
        detections = last_detection_list[-1]
        dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        for label, confidence, bbox in detections:
            item_list.append('object: ' + label + ', confidence: ' + str(confidence))
        detection_obj = Detection(item_list, dt_string, count)
        detection_list.append(detection_obj)
        last_detection_list.clear()
    return detection_list

