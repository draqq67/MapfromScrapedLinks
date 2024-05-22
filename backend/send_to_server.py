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
    extracted = 0
    not_working_sites = 0
    address_not_found = 0
    directory = "./text_from_links"
    
    for i in range(len(df_links) -1 ):
        # Check if the address is present and not empty
        if pd.notnull(df_links.loc[i, "address"]) and df_links.loc[i, "address"] != "":
            extracted += 1
        with open(f"{directory}/text_link_{i}.txt", "r") as f:
            lines = f.readlines()
            text = " ".join(lines)
            if len(text) < 100:
                not_working_sites += 1
            else :
                address_not_found += 1
    data = requests.get(f"http://localhost:5000/api/geocode").json()
    countries = {}
    usa_counties ={}
    usa_cities = {}
    uk_counties = {}
    uk_cities = {}
    for address in data:
        for address_data in address['geocode_data']['results']:
            for component in address_data['address_components']:
                if "country" in component['types']:
                    if component['long_name'] in countries:
                        countries[component['long_name']] += 1
                    else:
                        countries[component['long_name']] = 1  
                if component['long_name'] == "United States":
                    for county in address_data['address_components']:
                        if "administrative_area_level_1" in county['types']:
                            if county['long_name'] in usa_counties:
                                usa_counties[county['long_name']] += 1
                            else:
                                usa_counties[county['long_name']] = 1
                        #add locality count
                        if "locality" in county['types']:
                            if county['long_name'] in usa_cities:
                                usa_cities[county['long_name']] += 1
                            else:
                                usa_cities[county['long_name']] = 1
                if component['long_name'] == "United Kingdom":
                    for county in address_data['address_components']:
                        if "administrative_area_level_1" in county['types']:
                            if county['long_name'] in uk_counties:
                                uk_counties[county['long_name']] += 1
                            else:
                                uk_counties[county['long_name']] = 1
                        if "postal_town" in county['types']:
                            if county['long_name'] in uk_counties:
                                uk_cities[county['long_name']] += 1
                            else:
                                uk_cities[county['long_name']] = 1
                    
    return jsonify({"extracted": extracted, 
                    "empty": not_working_sites,
                    "countries": countries, 
                    "address_not_found": address_not_found,
                    "usa_counties": usa_counties,
                    "uk_counties": uk_counties,
                    "usa_cities": usa_cities,
                    "uk_cities": uk_cities})

@app.route('/api/geocode', methods=['GET'])
def get_geocode():
   # get the json from geocode_results.json file
    with open('geocode_results.json', 'r') as f:
        geocode_results = json.load(f)
    return jsonify(geocode_results)

if __name__ == '__main__':
    app.run(debug=True)
