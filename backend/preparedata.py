import pandas as pd
import pyarrow.parquet as pq
import pyap
import requests
import json

df_links = pq.read_table("list of company websites.snappy.parquet").to_pandas()
# print(df_links.head())

for i in range(len(df_links)):
    if not df_links.loc[i, "domain"].startswith("http"):
        df_links.loc[i, "domain"] = "https://" + df_links.loc[i, "domain"]

# get the text from text_from_links directory for each row
directory = "./text_from_links"
#add address row to df_links
df_links["address"] = ""
def extract(directory,n,df_links):
    for number in range(n):
        with open(f"{directory}/text_link_{number}.txt", "r") as f:
            lines = f.readlines()
            text = " ".join(lines)
        
        if( len(text) > 10):
            address = pyap.parse(text, country='US')
            if(address == []):
                address = pyap.parse(text, country='CA')
            if(address == []):
                address = pyap.parse(text, country='GB')
        else :
            address = []
        #filter out the addresses that duplicates
        address = list(set([str(a) for a in address]))
        #put adress in one string
        address = ",".join(address)
        # add adress row into df_links
        df_links.loc[number, "address"] = address
    return df_links

# df_links = extract(directory,len(df_links)-1 ,df_links)
    # print(df_links.head())
    # # Save the dataframe to a new csv file
    # df_links.to_csv("company_websites_with_address.csv", index=False)
# df_links = pd.read_csv("company_websites_with_address.csv")

# add also a 
def stats():
    sum = 0
    sum2 = 0
    for i in range(len(df_links) - 1):
        # address row from the text_link files
        if pd.notnull(df_links.loc[i, "address"]) and df_links.loc[i, "address"] != "":
            sum += 1
        with open(f"{directory}/text_link_{i}.txt", "r") as f:
            lines = f.readlines()
            text = " ".join(lines)
            if len(text) < 10:
                sum2 += 1

    print(f"number of extracted pages {sum}\n number of empty pages {sum2}")
            
    print(df_links.head())

def geocode():
    API_KEY = "AIzaSyA7HVl51-Q-QWMotQfWU87ZEdCADSkpGU0"
    GEOCODING_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
    response = requests.get('http://127.0.0.1:5000/api/data')
    data = response.json()
    geocode_results = []
    for row in data:
            address = row['address']
            if address:
                params = {
                    'address': address,
                    'key': API_KEY
                }
                response = requests.get(GEOCODING_URL, params=params)
                geocode_data = response.json()
                geocode_results.append({
                    'domain': row['domain'],
                    'address': address,
                    'geocode_data': geocode_data
                })
    #create a json file with the geocode results
    with open('geocode_results.json', 'w') as f:
        json.dump(geocode_results, f)
geocode()
