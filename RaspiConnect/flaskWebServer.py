import cv2
import time
import datetime
from flask import Flask, Response, render_template, request, send_from_directory
import random
from picamera2 import Picamera2

app = Flask(__name__)

# Camera setup
picam2 = None
VIDEO_PATH = "/home/admin/Documents/lifemustgoonCircuits/RaspiConnect/videos"

# initialize camera
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

# Estimate video duration
def get_video_duration_opencv():
    filename = f"{VIDEO_PATH}/ad_video.mp4"
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

# Flask app factory (CALLABLE FROM main.py)
ad_triggered = False  # global state

def create_app():

    app = Flask(__name__)
    global ad_triggered
    
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/video_feed')
    def video_feed():
        return Response(generate_frames(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    
    @app.route("/trigger_ad", methods=["POST"])
    def trigger_ad():
        global ad_triggered
        ad_triggered = True
        return "OK"
    
    @app.route("/check_ad")
    def check_ad():
        global ad_triggered
        return {"ad": ad_triggered}
    
    @app.route("/ad", methods=["GET", "POST"])
    def ad():
        global ad_triggered
        ad_triggered = False
        video_filename = "ad_video.mp4"
        duration = get_video_duration_opencv()  # returns timedelta

        duration_seconds = int(duration)

        return render_template(
            "ad.html",
            video_filename=video_filename,
            duration_seconds=duration_seconds
        )

    @app.route("/videos/<path:filename>")
    def serve_video(filename):
        return send_from_directory("videos", filename)

    return app


if __name__ == '__main__':
    start_camera()
    app = create_app()
    app.run(host='0.0.0.0', port=5000)