from flask import Flask, request, jsonify
import joblib
import pandas as pd
import json

app = Flask(__name__)

# Load ML artifacts
pipeline = joblib.load('salary_pipeline.pkl')
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
        
        # Create input dataframe with original column names
        input_data = {
            'Age': [data['Age']],
            'Gender': [data['Gender']],
            'Education Level': [data['Education_Level']],
            'Job Title': [data['Job_Title']],
            'Years of Experience': [data['Years_of_Experience']]
        }
        input_df = pd.DataFrame(input_data)
        
        # Make prediction using the pipeline
        prediction = pipeline.predict(input_df)[0]
        
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