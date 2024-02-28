import boto3
import json
import pandas as pd

s3 = boto3.client('comprehendmedical', region_name = 'ap-southeast-2', aws_access_key_id = 'YOUR_ACCESS_KEY', aws_secret_access_key = 'YOUR_SECRET_KEY')

def get_medical_report():
    while True:
        text = input("Enter your Medical Report: ")
        if text.strip():
            return text
        else:
            print("Please provide a valid input.")

medical_report = get_medical_report()

print('Calling infer_icd10_cm')
try:
    infer_icd10_cm_response = s3.infer_icd10_cm(Text=medical_report)
    # Write the response to a JSON file
    with open('infer_icd10_cm_response_medical_data.json', 'w') as outfile:
        json.dump(infer_icd10_cm_response, outfile, indent=4)
    print("Response written to 'infer_icd10_cm_response_medical_data.json'")
    print(json.dumps(infer_icd10_cm_response, indent=4))
except Exception as e:
    print("Error:", e)

with open('infer_icd10_cm_response_medical_data.json', 'r') as file:
    data = json.load(file)

with open('infer_icd10_cm_response_medical_data.json', 'r') as file:
    data = json.load(file)

df = pd.json_normalize(data['Entities'])

df.to_csv('medical_data.csv', index=False)

print("CSV file saved successfully.")

print("\n", df.loc[:, ["Text", "Category", "Score"]])
