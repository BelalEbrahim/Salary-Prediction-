import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import joblib
import json

# Load and clean data
df = pd.read_csv("Salary_Data.csv")
df.replace(['', 'NA', 'NaN', 'nan'], np.nan, inplace=True)
df.dropna(inplace=True)
df = df[df['Salary'] > 10000]

# Initialize and fit encoders
encoders = {
    'Gender': LabelEncoder().fit(df['Gender']),
    'Education': LabelEncoder().fit(df['Education Level']),
    'Job_Title': LabelEncoder().fit(df['Job Title'])
}

# Apply encodings
df['Gender_enc'] = encoders['Gender'].transform(df['Gender'])
df['Education_enc'] = encoders['Education'].transform(df['Education Level'])
df['Job_Title_enc'] = encoders['Job_Title'].transform(df['Job Title'])

# Prepare features and target
X = df[['Age', 'Gender_enc', 'Education_enc', 'Job_Title_enc', 'Years of Experience']]
y = df['Salary']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = GradientBoostingRegressor(
    n_estimators=300,
    learning_rate=0.1,
    max_depth=4,
    random_state=42
)
model.fit(X_train, y_train)

# Save model
joblib.dump(model, 'salary_model.pkl')

# Save encodings to JSON
encodings = {}
for col, encoder in encoders.items():
    encodings[col] = {label: int(code) for code, label in enumerate(encoder.classes_)}
    
with open('encodings.json', 'w') as f:
    json.dump(encodings, f, indent=4)

print("Model and encodings saved successfully")