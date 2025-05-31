import requests
import json
import time

def run_test():
    url = "http://localhost:5000/predict"
    
    # Load test data from data.json
    try:
        with open('data.json') as f:
            test_data = json.load(f)
    except FileNotFoundError:
        print("Error: data.json file not found. Using fallback data.")
        test_data = [
            {
                "Age": 32,
                "Gender": "Male",
                "Education_Level": "Bachelor's",
                "Job_Title": "Software Engineer",
                "Years_of_Experience": 5
            },
            {
                "Age": 28,
                "Gender": "Female",
                "Education_Level": "Master's",
                "Job_Title": "Data Analyst",
                "Years_of_Experience": 3
            },
            {
                "Age": 45,
                "Gender": "Male",
                "Education_Level": "PhD",
                "Job_Title": "Senior Manager",
                "Years_of_Experience": 15
            },
            {
                "Age": 36,
                "Gender": "Female",
                "Education_Level": "Bachelor's",
                "Job_Title": "Sales Associate",
                "Years_of_Experience": 7
            }
        ]
    
    try:
        # Try the requests
        print("Starting API tests...")
        print("-" * 50)
        
        for i, data in enumerate(test_data, 1):
            print(f"Test #{i}: {data['Job_Title']}")
            try:
                response = requests.post(url, json=data, timeout=5)
                
                # Print results
                print(f"Status Code: {response.status_code}")
                if response.status_code == 200:
                    print("Response:", response.json())
                else:
                    print("Error Response:", response.text)
                
                print("-" * 30)
            except Exception as e:
                print(f"Request failed: {str(e)}")
                print("-" * 30)
        
        return 0  # Success
        
    except requests.exceptions.ConnectionError:
        print("Error: Flask server not running. Start it with 'python app.py'")
        return 1
    except Exception as e:
        print("Error:", str(e))
        return 1

if __name__ == "__main__":
    # Wait briefly to allow server to start if run together
    time.sleep(1)
    
    # Run test and exit with status code
    exit(run_test())