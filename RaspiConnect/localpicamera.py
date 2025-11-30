# initialize camera
import base64
import cv2
import time
import datetime
from flask import Flask, Response, render_template, request, send_from_directory
import random

import requests
from picamera2 import Picamera2

picam2 = None
def start_camera():
    global picam2

    if picam2 is not None:
        return  # Already started

    picam2 = Picamera2()
    video_cfg = picam2.create_video_configuration(
        main={"size": (1280, 720), "format": "XRGB8888"},
        buffer_count=3
    )
    picam2.configure(video_cfg)
    picam2.start()
    time.sleep(5)  # Warm-up

# stop camer
def stop_camera():
    global picam2

    if picam2:
        picam2.stop()
        picam2 = None


# frame generator
def generate_frames():
    global picam2

    while picam2 is not None:
        frame = picam2.capture_array()
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


def capture_frame_base64():
    global picam2
    if picam2 is None:
        print("Camera is not started.")
        return None

    frame = picam2.capture_array()
    ret, buffer = cv2.imencode('.jpg', frame)
    if not ret:
        print("Failed to encode frame.")
        return None

    frame_base64 = base64.b64encode(buffer).decode('utf-8')
    return frame_base64