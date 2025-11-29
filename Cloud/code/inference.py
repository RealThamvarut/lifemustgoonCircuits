import json
import torch
import base64
import io
from PIL import Image
from transformers import AutoImageProcessor, AutoModel, AutoConfig

def model_fn(model_dir):
    """
    Load the model from the Hugging Face Hub.
    SageMaker calls this function when the container starts.
    """
    device = 0 if torch.cuda.is_available() else -1
    print(f"Loading model to device: {device}")
    
    #load processor
    processor = AutoImageProcessor.from_pretrained("abhilash88/age-gender-prediction", trust_remote_code=True)
    config = AutoConfig.from_pretrained("abhilash88/age-gender-prediction", trust_remote_code=True)
    model = AutoModel.from_pretrained("abhilash88/age-gender-prediction", config=config, trust_remote_code=True).to(device)
    if device != -1:
        model.eval()
    
    return {"model": model, "processor": processor, "device": device}
    

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

def predict_fn(input_object, context):
    """
    Run the prediction on the decoded input.
    """
    model = context['model']
    processor = context['processor']
    device = context['device']
    
    input = processor(images=input_object, return_tensors="pt")
    
    if device != -1:
        input = {k: v.to(device) for k, v in input.items()}
        
    with torch.no_grad():
        outputs = model(**input)
        
        age_logits = outputs.age_logits if hasattr(outputs, 'age_logits') else outputs['age_logits']
        gender_logits = outputs.gender_logits if hasattr(outputs, 'gender_logits') else outputs['gender_logits']
        
        predicted_age = float(age_logits.item())
        
        gender_probs = torch.softmax(gender_logits, dim=1).cpu().numpy()[0]
        gender_maps = ['Female', 'Male']
        predicted_gender_idx = gender_probs.argmax()
        predicted_gender = gender_maps[predicted_gender_idx]
        confidence = float(probs[predicted_gender_idx])

    return {
        "age": round(predicted_age, 1),
        "gender": predicted_gender,
        "gender_confidence": round(confidence, 3)
    }

def output_fn(prediction, response_content_type):
    """
    Serialize the prediction result to JSON.
    """
    # Example output from model: {'age': 28, 'gender': 'Male', 'gender_confidence': 0.98}
    return json.dumps(prediction)