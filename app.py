from flask import Flask, request, jsonify
# New code
from numpy.random import Generator, MT19937
rng = Generator(MT19937())
import joblib
import pandas as pd
import json
import numpy as np

app = Flask(__name__)

# Load ML artifacts
model = joblib.load('salary_model.pkl')
feature_names = joblib.load('feature_names.joblib')
with open('label_mappings.json', 'r') as f:
    label_mappings = json.load(f)

@app.route('/predict', methods=['POST'])
def predict():
    """Salary prediction endpoint"""
    try:
        # Get and validate input data
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data provided"}), 400
        
        # Validate required fields
        required_fields = ['Age', 'Gender', 'Education_Level', 'Job_Title', 'Years_of_Experience']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required field(s)"}), 400
        
        # Create input array
        input_data = [
            data['Age'],
            label_mappings['Gender'][data['Gender']],
            label_mappings['Education'][data['Education_Level']],
            label_mappings['Job_Title'][data['Job_Title']],
            data['Years_of_Experience']
        ]
        
        # Create input dataframe
        input_df = pd.DataFrame([input_data], columns=feature_names)
        
        # Make prediction
        prediction = model.predict(input_df)[0]
        
        return jsonify({
            "predicted_salary": round(float(prediction), 2)
        })
    
    except KeyError as e:
        return jsonify({"error": f"Invalid category value: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/categories', methods=['GET'])
def get_categories():
    """Get category mappings"""
    return jsonify(label_mappings)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)