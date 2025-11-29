import base64
import json
import os
import numpy as np
import cv2
import onnxruntime
import insightface
from insightface.app import FaceAnalysis

model = None

def model_fn(model_dir):
    app = FaceAnalysis(
        name='buffalo_l',
        root=model_dir,
        providers=['CPUExecutionProvider'],
        allowed_modules=['detection', 'genderage']
    )
    app.prepare(ctx_id=0, det_size=(640,640))
    print("InsightFace pipeline loaded.")
    return app

def input_fn(request_body, request_content_type):
   if request_content_type == 'application/json':
        input_data = json.loads(request_body)
       
        if 'image' in input_data:
            raise ValueError("JSON body must contain an 'image' key.")
        b64_string = input_data['image']

        img_bytes = base64.b64decode(b64_string)
        
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return img
   else:
        raise ValueError(f"Unsupported content type: {request_content_type}")
   
def predict_fn(img, app):
    faces = app.get(img)
    if len(faces) == 0:
        return {"message": "No faces detected."}
    
    main_face = max(faces, key=lambda face: (face.bbox[2] - face.bbox[0]) * (face.bbox[3] - face.bbox[1]))

    return {
        "gender": "Male" if main_face.sex == 1 else "Female",
        "age": int(main_face.age), 
        "confidence": float(main_face.det_score),
        "bbox": [int(coord) for coord in main_face.bbox]
    }

def output_fn(prediction, response_content_type):
    return json.dumps(prediction)