import base64
import cv2
import time
import datetime
from flask import Flask, Response, jsonify, render_template, request, send_from_directory
import random

import requests
<<<<<<< HEAD
from localpicamera import generate_frames, start_camera
=======
from RaspiConnect.adsmatcher import AdMatcher
from RaspiConnect.localpicamera import generate_frames, start_camera
>>>>>>> eb000e5 (add ads matching:)
from picamera2 import Picamera2

app = Flask(__name__)

AI_API_URL = "http://ec2-18-140-57-238.ap-southeast-1.compute.amazonaws.com:5000/predict"
VIDEO_PATH = "/home/admin/Documents/lifemustgoonCircuits/RaspiConnect/cache_videos"

ad_triggered = False

current_ad_state = {
    "triggered": False,
    "video_filename": "b0099-001.mp4", #default ad'
    "duration": 5.0
}

def infer_demographics(img_base64: str):
    try:
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "image":img_base64
        }

        print("Sending image to AI API for inference...")
        response = requests.post(
            AI_API_URL,
            headers=headers,
            json=payload
        )

        print("Response received from AI API.")
        if response.status_code == 200:
            return response.json()
        else:
            print("Return code not 200")
            return None
    except Exception as e:
        print(f"Connection error : {e}")
        return None
    
# Estimate video duration
def get_video_duration_opencv(video_name):
    filename = f"{VIDEO_PATH}/{video_name}"
    video = cv2.VideoCapture(filename)
    if not video.isOpened():
        print(f"Error: Could not open video file {filename}")
        return None

    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    
    if fps == 0:  # Handle cases where FPS might be zero
        print("Warning: FPS is zero, duration cannot be calculated accurately.")
        return None

    duration_seconds = frame_count / fps
    video.release()
    return duration_seconds




def create_app():

    app = Flask(__name__)
    global ad_triggered
    global current_ad_state

    adsmatcher = AdMatcher() #init rules for ad selection

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/video_feed')
    def video_feed():
        return Response(generate_frames(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    
    @app.route("/trigger_ad", methods=["POST"])
    def trigger_ad():
        global current_ad_state
        
        data = request.json or {}
        gender = data.get("gender", "Male")
        age = data.get("age", 25)

        selected_video = adsmatcher.select_ad(gender, age)
        duration = get_video_duration_opencv(selected_video)  # returns timedelta

        current_ad_state = {
            "triggered": True,
            "video_filename": selected_video,
            "duration": duration
        }

        return jsonify({
            "status": "ok",
            "video_filename": selected_video,
            "duration": duration
        })
    
    @app.route("/check_ad")
    def check_ad():
        global current_ad_state
        return jsonify({"ad": current_ad_state["triggered"]})
    
    @app.route("/ad", methods=["GET", "POST"])
    def ad():
        global current_ad_state
        current_ad_state["triggered"] = False
        video_filename = current_ad_state["video_filename"]
        duration = current_ad_state["duration"]  # returns timedelta

        duration_seconds = int(duration)

        return render_template(
            "ad.html",
            video_filename=video_filename,
            duration_seconds=duration_seconds+1  # add 1 second buffer
        )

    @app.route("/videos/<path:filename>")
    def serve_video(filename):
        return send_from_directory("videos", filename)

    return app


if __name__ == '__main__':
    start_camera()
    app = create_app()
    app.run(host='0.0.0.0', port=5000)