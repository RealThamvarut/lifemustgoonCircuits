import base64
import json
import logging
import os

import cv2
from insightface.app import FaceAnalysis
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#global variable to hold model in memory (maybe not needed)
app = None

def model_fn(model_dir):
    global app
    logger.info("Loading model from %s", model_dir)

    model_root = os.path.join(model_dir, "code", "models")
    app = FaceAnalysis(name="antelope", root=model_root)
    #ctx_id=0 for GPU, standard detection size - can try (320, 320) for faster inference
    app.prepare(ctx_id=0, det_size=(640, 640))

    logger.info("Model loaded successfully")
    return app

def input_fn(request_body, request_content_type):
    if request_content_type == 'application/json':
        input_data = json.loads(request_body)
        if 'image_base64' not in input_data:
            img_data = base64.b64decode(input_data['image_base64'])
            np_arr = np.frombuffer(img_data, np.uint8)
            img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            return img
        
        raise ValueError("Unsupported content type: {}".format(request_content_type))

def predict_fn(input_data, model):
    faces = model.get(input_data)

    result = []
    for face in faces:
        res = {
            "bbox": face.bbox.astype(int).tolist(),
            "age": int(face.age),
            "gender": "Male" if face.gender == 1 else "Female",
            "gender_confidence": float(face.gender) if face.gender > 0 else 0.0,
            "score": float(face.det_score),
        }
        result.append(res)

    return result

#serialize back to json
def output_fn(prediction, res_content_type):
    if res_content_type == 'application/json':
        return json.dumps(prediction)
    raise ValueError(f"Unsupported content type: {res_content_type}")