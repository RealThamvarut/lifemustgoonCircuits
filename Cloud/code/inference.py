import json
import torch
import base64
import io
from PIL import Image
from transformers import pipeline

def model_fn(model_dir):
    """
    Load the model from the Hugging Face Hub.
    SageMaker calls this function when the container starts.
    """
    device = 0 if torch.cuda.is_available() else -1
    print(f"Loading model to device: {device}")
    
    # We load the pipeline directly from the Hub.
    # 'trust_remote_code=True' is required because this model uses a custom architecture.
    pipe = pipeline(
        "age-gender-classification", 
        model="abhilash88/age-gender-prediction", 
        trust_remote_code=True,
        device=device
    )
    return pipe

def input_fn(request_body, request_content_type):
    """
    Deserialize the request body into an image object.
    Supports JSON (with base64 image) or raw image bytes.
    """
    if request_content_type == 'application/json':
        # Expects {"inputs": "base64_string"}
        input_data = json.loads(request_body)
        if 'inputs' in input_data:
            image_data = base64.b64decode(input_data['inputs'])
            return Image.open(io.BytesIO(image_data)).convert("RGB")
    
    if request_content_type in ('image/jpeg', 'image/png'):
        return Image.open(io.BytesIO(request_body)).convert("RGB")

    raise ValueError(f"Unsupported content type: {request_content_type}")

def predict_fn(input_object, model):
    """
    Run the prediction on the decoded input.
    """
    # The pipeline handles the inference details
    prediction = model(input_object)
    return prediction

def output_fn(prediction, response_content_type):
    """
    Serialize the prediction result to JSON.
    """
    # Example output from model: {'age': 28, 'gender': 'Male', 'gender_confidence': 0.98}
    return json.dumps(prediction)