import requests

def get_youtube_link_from_cloud(api_url: str) -> str:
    try:
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()

        # Cloud server may return:
        #   - raw text: "https://youtube.com/watch?v=XXXX"
        #   - JSON: {"url": "https://youtube.com/watch?v=XXXX"}

        data = response.text.strip()

        # Try JSON first
        try:
            json_data = response.json()
            youtube_url = json_data.get("url", None)
        except ValueError:
            youtube_url = data

        if youtube_url is None:
            print("Cloud server did not provide a URL.")
            return None

        # Extract YouTube video ID
        video_id = extract_video_id(youtube_url)
        return video_id

    except Exception as e:
        print(f"Error fetching from cloud: {e}")
        return None


def extract_video_id(url: str) -> str:
    if "watch?v=" in url:
        return url.split("watch?v=")[1].split("&")[0]
    if "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    if "embed/" in url:
        return url.split("embed/")[1].split("?")[0]
    
    return None
