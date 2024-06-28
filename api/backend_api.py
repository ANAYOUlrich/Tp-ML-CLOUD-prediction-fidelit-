from flask import Flask, jsonify, request
from tensorflow.keras.models import load_model
import numpy as np

app = Flask(__name__)

# Load the model 
model_path = "fidelite_model.h5"
app.model = load_model(model_path, compile=False)
app.model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
print("Model loaded")

@app.route("/", methods=["GET"])
def home():
    return "hello"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = [
            request.values.get('CreditScore', type=float),
            request.values.get('Age', type=int),
            request.values.get('Tenure', type=int),
            request.values.get('Balance', type=float),
            request.values.get('NumOfProducts', type=int),
            request.values.get('HasCrCard', type=int),
            request.values.get('IsActiveMember', type=int),
            request.values.get('EstimatedSalary', type=float),
            1 if request.values.get('Geography_Germany') == "Germany" else 0,
            1 if request.values.get('Geography_Spain') == "Spain" else 0,
            1 if request.values.get('Gender_Male') == "M" else 0
        ]
        
        data = np.array(data).reshape(1, -1)
        print(data)
        
        # Prediction
        prediction = app.model.predict(data)
        rec = float(prediction[0][0])  

        return jsonify({'prediction': rec})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
