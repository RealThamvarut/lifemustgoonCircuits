import cv2
import time
from flask import Flask, Response, render_template, request
import random
from picamera2 import Picamera2

app = Flask(__name__)

# Camera setup
picam2 = Picamera2()
video_cfg = picam2.create_video_configuration(
    main={"size": (1280, 720), "format": "XRGB8888"},
    buffer_count=3
)
picam2.configure(video_cfg)
picam2.start()
time.sleep(5)  # Wait for camera warm-up

# Frame generator
def generate_frames():
     while True:
        frame = picam2.capture_array()
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/ad", methods=["GET", "POST"])
def ad():
    # Template URL for testing
    youtube_url = "https://www.youtube.com/watch?v=v0NDDoNRtQ8" 
    video_id = None
    if request.method == "POST":
        if "watch?v=" in youtube_url:
            video_id = youtube_url.split("watch?v=")[1]
        elif "youtu.be/" in youtube_url:
            video_id = youtube_url.split("youtu.be/")[1]
    return render_template("ad.html", video_id=video_id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)