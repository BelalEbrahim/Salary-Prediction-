import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import joblib
import json

# Load and clean data
df = pd.read_csv("Salary_Data.csv")
df.replace(['', 'NA', 'NaN', 'nan'], np.nan, inplace=True)
df.dropna(inplace=True)
df = df[df['Salary'] > 10000]

# Create label mappings for frontend
label_mappings = {
    'Gender': list(df['Gender'].unique()),
    'Education_Level': list(df['Education Level'].unique()),
    'Job_Title': list(df['Job Title'].unique())
}

# Define features and target
X = df[['Age', 'Gender', 'Education Level', 'Job Title', 'Years of Experience']]
y = df['Salary']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Create preprocessing pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), ['Age', 'Years of Experience']),
        ('cat', OneHotEncoder(handle_unknown='ignore'), ['Gender', 'Education Level', 'Job Title'])
    ])

# Create full pipeline
pipeline = make_pipeline(
    preprocessor,
    GradientBoostingRegressor(
        n_estimators=300,
        learning_rate=0.1,
        max_depth=4,
        random_state=42  # Use integer random state
    )
)

# Train pipeline
pipeline.fit(X_train, y_train)

# Save the entire pipeline
joblib.dump(pipeline, 'salary_pipeline.pkl')

# Save label mappings
with open('label_mappings.json', 'w') as f:
    json.dump(label_mappings, f, indent=4)

print("Model training complete. Artifacts saved:")
print("- salary_pipeline.pkl")
print("- label_mappings.json")