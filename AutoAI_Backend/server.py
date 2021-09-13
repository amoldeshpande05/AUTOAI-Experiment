from flask import Flask
import requests
import os
import json

app = Flask(__name__)

@app.route("/getPrediction")
def index():
    # NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
    API_KEY = "eRKyWEXWZLGx5VuQp9TGrvSs5JAxzPlIgrwV3qQH4PTr"
    token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
    mltoken = token_response.json()["access_token"]

    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"fields": ["Loan_ID","Gender","Married","Dependents","Education","Self_Employed","ApplicantIncome","CoapplicantIncome","LoanAmount","Loan_Amount_Term","Credit_History","Property_Area"], "values": [[ "LP001999", "Male", "Yes", "0", "Not Graduate", "No", 2589, 2358, 129, 360, 1, "Urban" ]]}]}

    response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/d86b6736-b617-471b-b27d-65f27ddf20a2/predictions?version=2021-09-13', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})

    print("response_scoring  : ",response_scoring.json())
    # your logic ... 

    dictionary ={ 
    "status": "200", 
    "message": "Loan Approved!!", 
    } 



    return  json.dumps(dictionary)
        
port = os.getenv('VCAP_APP_PORT', '8080')
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=port)