from flask import Flask, jsonify, request
import pandas as pd
import requests
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)
GEOCODING_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
API_KEY = "AIzaSyA7HVl51-Q-QWMotQfWU87ZEdCADSkpGU0"

@app.route('/api/data', methods=['GET'])
def get_dataframe():
    # Load the dataframe from a CSV file
    df = pd.read_csv('company_websites_with_address.csv')
    
    # Convert dataframe to JSON
    df_json = df[df['address'] != "null"].to_json(orient='records')
    # Return the JSON response
    df_json = df_json.replace("null", "None")
    df_results = []
    for i,row in df.iterrows():
        if pd.notnull(df.loc[i, "address"]) and df.loc[i, "address"] != "":
            df_results.append({
                'domain': row['domain'],
                'address': row['address']
            })
    return jsonify(df_results)

@app.route('/api/stats', methods=['GET'])
def get_statistics():
    # Load the dataframe from a CSV file
    df_links = pd.read_csv('company_websites_with_address.csv')
    sum = 0
    sum2 = 0
    directory = "./text_from_links"
    
    for i in range(len(df_links)):
        # Check if the address is present and not empty
        if pd.notnull(df_links.loc[i, "address"]) and df_links.loc[i, "address"] != "":
            sum += 1
        try:
            with open(f"{directory}/text_link_{i}.txt", "r") as f:
                lines = f.readlines()
                text = " ".join(lines)
                if len(text) < 10:
                    sum2 += 1
        except FileNotFoundError:
            sum2 += 1
    
    return jsonify({"extracted": sum, "empty": sum2})

@app.route('/api/geocode', methods=['GET'])
def get_geocode():
   # get the json from geocode_results.json file
    with open('geocode_results.json', 'r') as f:
        geocode_results = json.load(f)
    return jsonify(geocode_results)

if __name__ == '__main__':
    app.run(debug=True)
