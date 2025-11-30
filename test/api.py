import requests
import base64
import json



# ---------- CONFIG ----------
API_URL = "http://ec2-18-141-164-183.ap-southeast-1.compute.amazonaws.com:5000/predict"
IMAGE_PATH = "peter.jpg"   # your test image path

def load_image_base64(image_path):
    """Load image and convert to base64 string."""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

def invoke_endpoint(image_b64):

    payload = {
        "image": image_b64 
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(API_URL, json=payload, headers=headers)

    return json.loads(response)

def main():
    print("Encoding image...")
    img_b64 = load_image_base64(IMAGE_PATH)

    print("Invoking endpoint...")
    result = invoke_endpoint(img_b64)

    print(result)

if __name__ == "__main__":
    main()