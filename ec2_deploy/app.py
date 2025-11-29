# app.py
from flask import Flask, request, jsonify
from model import decode_base64_image,predict_age_gender # We'll modify model.py to export these

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    # 1. Get JSON data from the request
    data = request.get_json()
    if not data or 'image' not in data:
        return jsonify({"error": "No image field found in JSON payload"}), 400

    base64_image_string = data['image']
    
    # 2. Decode the base64 string to a PIL Image
    image = decode_base64_image(base64_image_string)
    
    if image is None:
        return jsonify({"error": "Failed to decode base64 image string"}), 400

    # 3. Call the prediction function with the PIL Image
    try:
        # Note: predict_age_gender now accepts a PIL Image object, not a path
        prediction_result = predict_age_gender(image) 
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {e}"}), 500

    # 4. Format and return the result
    response = {
        "age": prediction_result["age"],
        "gender": prediction_result["gender"],
        "confidence": f"{prediction_result['gender_confidence']:.1%}"
    }
    
    # Example for the string format you had:
    # response_string = f"{prediction_result['age']} years, {prediction_result['gender']} ({prediction_result['gender_confidence']:.1%} confidence)"
    
    return jsonify(response)

if __name__ == '__main__':
    # Use Gunicorn or a proper WSGI server in production (see Dockerfile)
    app.run(debug=True, host='0.0.0.0', port=5000)