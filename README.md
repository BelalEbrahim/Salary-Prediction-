# Salary Prediction API - Project Documentation

![Salary Prediction API](https://via.placeholder.com/800x400?text=Salary+Prediction+API+Diagram)

## Project Overview
This project provides a RESTful API for predicting employee salaries based on attributes like age, gender, education level, job title, and years of experience. The solution consists of:

- **Flask API**: Python-based backend service
- **Machine Learning Model**: Gradient Boosting Regressor trained on salary data
- **Test Suite**: Automated API tests

## Technology Stack
| Component       | Technology |
|-----------------|------------|
| **Backend**     | Python 3.9, Flask |
| **ML Framework**| Scikit-learn |
| **Frontend**    | React.js (planned) |
| **Testing**     | Requests library |

## Getting Started

### Prerequisites
- Python 3.9+
- pip package manager
- Node.js 16+ (for frontend development)

### Installation
```bash
# Clone repository
git clone https://github.com/your-username/salary-prediction-api.git
cd salary-prediction-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt
```

## Project Structure
```
salary-prediction-api/
├── app.py                # Flask application
├── train_model.py        # Model training script
├── test_api.py           # API test script
├── data.json             # Sample test data
├── requirements.txt      # Python dependencies
├── salary_model.pkl      # Trained ML model
├── feature_names.joblib  # Model feature names
└── label_mappings.json   # Categorical value mappings
```

## Running the Application

### Start Flask API
```bash
python app.py
```
API will be available at: `http://localhost:5000`

### Test API Endpoints
```bash
python test_api.py
```

## API Endpoints

### 1. Predict Salary
**Endpoint**: `POST /predict`  
**Request**:
```json
{
  "Age": 35,
  "Gender": "Female",
  "Education_Level": "PhD",
  "Job_Title": "Director",
  "Years_of_Experience": 10
}
```

**Response**:
```json
{
  "predicted_salary": 182300.0
}
```

### 2. Get Category Mappings
**Endpoint**: `GET /categories`  
**Response**:
```json
{
  "Education": {
    "Bachelor's": 0,
    "Master's": 1,
    "PhD": 2
  },
  "Gender": {
    "Female": 0,
    "Male": 1
  },
  "Job_Title": {
    "Data Analyst": 1,
    "Director": 3,
    "Sales Associate": 2,
    "Senior Manager": 4,
    "Software Engineer": 0
  }
}
```

## For Frontend (React.js) Team

### Integration Points
1. **API Base URL**: `http://localhost:5000` (development)
2. **Required Components**:
   - Salary prediction form
   - Results display
   - Error handling

### Example React Component
```jsx
import React, { useState } from 'react';

function SalaryPredictor() {
  const [formData, setFormData] = useState({
    Age: '',
    Gender: '',
    Education_Level: '',
    Job_Title: '',
    Years_of_Experience: ''
  });
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:5000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      
      if (!response.ok) throw new Error(await response.text());
      
      const result = await response.json();
      setPrediction(result.predicted_salary);
      setError(null);
    } catch (err) {
      setError(err.message);
      setPrediction(null);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        {/* Form fields here */}
        <button type="submit">Predict Salary</button>
      </form>
      
      {prediction && (
        <div className="result">
          <h3>Predicted Salary: ${prediction.toLocaleString()}</h3>
        </div>
      )}
      
      {error && <div className="error">{error}</div>}
    </div>
  );
}
```

### Form Validation Requirements
1. **Age**: Number between 18-70
2. **Years of Experience**: Number between 0-50
3. **Gender**: Must be "Male" or "Female"
4. **Education Level**: Must be one of:
   - "Bachelor's"
   - "Master's"
   - "PhD"
5. **Job Title**: Must match an existing job title from `/categories` endpoint

## For Backend (Node.js) Team

### Integration Guide
1. **Proxy Requests**: Route salary prediction requests to Flask API
2. **Caching**: Implement response caching for common queries
3. **Authentication**: Add JWT authentication layer
4. **Rate Limiting**: Protect against abuse

### Example Node.js Proxy Endpoint
```javascript
const express = require('express');
const axios = require('axios');
const router = express.Router();

const FLASK_API = 'http://localhost:5000';

router.post('/predict-salary', async (req, res) => {
  try {
    const response = await axios.post(`${FLASK_API}/predict`, req.body);
    res.json(response.data);
  } catch (error) {
    res.status(error.response?.status || 500)
       .json({ error: error.response?.data || error.message });
  }
});

router.get('/categories', async (req, res) => {
  try {
    const response = await axios.get(`${FLASK_API}/categories`);
    res.json(response.data);
  } catch (error) {
    res.status(error.response?.status || 500)
       .json({ error: error.response?.data || error.message });
  }
});

module.exports = router;
```

## Model Training

### Retraining the Model
```bash
python train_model.py
```

### Training Data Requirements
CSV file should contain these columns:
1. Age (numeric)
2. Gender (Male/Female)
3. Education Level (Bachelor's/Master's/PhD)
4. Job Title (string)
5. Years of Experience (numeric)
6. Salary (numeric)

### Model Performance
| Metric | Value |
|--------|-------|
| **RMSE** | $11,200 |
| **R²** | 0.91 |
| **MAE** | $8,500 |

## Troubleshooting

### Common Issues
1. **Flask server not starting**:
   - Check for port conflicts (`lsof -i :5000`)
   - Verify Python dependencies (`pip install -r requirements.txt`)

2. **Invalid category errors**:
   - Get current valid categories: `GET /categories`
   - Ensure exact match (case-sensitive)

3. **Prediction accuracy issues**:
   - Retrain model with updated data
   - Verify data quality in input CSV

4. **CORS errors (frontend)**:
   ```python
   from flask_cors import CORS
   app = Flask(__name__)
   CORS(app)  # Add this line
   ```

## Environment Setup

### Production Deployment
```bash
# Install production WSGI server
pip install gunicorn

# Start server
gunicorn --bind 0.0.0.0:5000 app:app
```

### Docker Setup
```Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

## Contributing
1. Fork the repository
2. Create feature branch (`git checkout -b feature/your-feature`)
3. Commit changes (`git commit -am 'Add feature'`)
4. Push to branch (`git push origin feature/your-feature`)
5. Open pull request

## License
This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## Contact
For technical support contact: [your.email@example.com](mailto:your.email@example.com)
