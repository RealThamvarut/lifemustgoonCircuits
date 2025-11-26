import base64
import json
import os 
import logging
import shutil

import numpy as np
import cv2

from deepface import DeepFace

logger = logging.getLogger(__name__)

def model_fn(model_dir):
    print("Executing model_fn for inference.py...")
    env = os.environ
    
    #model_dir should be in /opt/ml/model which might be Read-Only
    #target_home should be in /tmp which is Read-Write, use for copying weights without redownloading on every server start
    source_weight_path = os.path.join(model_dir, ".deepface")
    target_home = "/tmp"
    target_weight_path = os.path.join(target_home, ".deepface")

    if not os.path.exists(target_weight_path):
        print(f"Copying weights from {source_weight_path} to {target_weight_path}...")
        if os.path.exists(source_weight_path):
            shutil.copytree(source_weight_path, target_weight_path)
        else:
            os.makedirs(target_weight_path, exist_ok=True)
    else:
        print(f"Weights already exist at {target_weight_path}, skipping copy.")
    os.environ["DEEPFACE_HOME"] = target_home

    DeepFace.build_model(model_name="Age")
    DeepFace.build_model(model_name="Gender")

    return "model loaded" #return anything actually

def input_fn(request_body, request_content_type):
    if request_content_type:
        jpg_original = base64.b64decode(request_body)
        jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
        img = cv2.imdecode(jpg_as_np, flags=cv2.IMREAD_COLOR)
        return img
    else:
        raise Exception(f"Unsupported request content type: {request_content_type}")
    
def predict_fn(input_object, model):
    print("executing predict_fn...")
    try:
        results = DeepFace.analyze(
            input_object,
            actions=['age', 'gender'],
            enforce_detection=False,
            detector_backend='opencv'
        )
        result = results[0]
        return {
            "age": result.get("age"),
            "gender": result.get("gender"),
            "gender_confidence": result.get("gender", {}).get(result.get("dominant_gender"), 0) if isinstance(result.get("gender"), dict) else "N/A"
        }
    except Exception as e:
        print(f"Error during prediction: {e}")
        return {
            "error": str(e)
        }

def output_fn(prediction_output, content_type):
    return json.dumps({'data': prediction_output})

    
    

