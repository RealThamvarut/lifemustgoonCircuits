from flask import Flask, render_template, request
from getUrl import get_youtube_link_from_cloud

app = Flask(__name__)

@app.route('/')
def indexTest():
    return render_template('index.html')

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

# def play_video():
#     cloud_api = "https://your-cloud-server.com/api/getVideo"
#     video_id = get_youtube_link_from_cloud(cloud_api)

#     return render_template("index.html", video_id=video_id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
