from flask import Flask,request
import requests
import json
import os
app = Flask(__name__)


@app.route("/")
def landing():
   return "Hello World!"




@app.route("/getPrediction")
def index():
    # NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
    API_KEY = "6FRDmF9DhIK1Iw7IH9xM9vk8CaRfRhNH_cxKvu1eS3TL"

    email = request.args.get("email");
    Gender = request.args.get("Gender");
    education = request.args.get("education");
    dependents = request.args.get("dependents");
    Self_Employed = request.args.get("Self_Employed");
    LoanAmount = request.args.get("LoanAmount");
    Loan_Amount_Term = request.args.get("Loan_Amount_Term");
    Credit_History = request.args.get("Credit_History");
    ApplicantIncome = request.args.get("ApplicantIncome");
    married = request.args.get("married");
    Property_Area = request.args.get("Property_Area");


    token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
    mltoken = token_response.json()["access_token"]
    # payload_scoring = {"input_data": [{"fields": ["Gender","Married","Dependents","Education","Self_Employed","ApplicantIncome","LoanAmount","Loan_Amount_Term","Credit_History","Property_Area"], "values": [[ 1, 1, 1, 1, 0, 4583, 128, 360, 1, "Rural" ]]}]}
    payload_scoring = {"input_data": [{"fields": ["Gender","Married","Dependents","Education","Self_Employed","ApplicantIncome","LoanAmount","Loan_Amount_Term","Credit_History","Property_Area"], "values": [[ Gender, married, dependents, education, Self_Employed, ApplicantIncome, LoanAmount, Loan_Amount_Term, Credit_History, Property_Area ]]}]}

    response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/65e0afca-ba80-4df2-9f69-6b5d086f1c39/predictions?version=2021-09-16', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    dictionary ={ 
    "status": "200", 
    "response_scoring": response_scoring.json()['predictions'][0]['values'][0][0],
    "probability" :response_scoring.json()['predictions'][0]['values'][0][1][1]
    } 
    return  json.dumps(dictionary)
        
port = os.getenv('VCAP_APP_PORT', '8080')
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=port)