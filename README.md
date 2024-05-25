# Veridion Challenge 1
realised by Zarnescu Dragos - Ioan for Deeptech Engineer Intern

Write a program that extracts all the valid addresses that are found on a list of company websites. The format in which you will have to extract this data is the following: country, region, city, postcode, road, and road numbers. 
- presentation : https://docs.google.com/presentation/d/1OwlcNwEXhezbCsmk6yOEEiYRX4pLBNzE6ijVW6NX4bs/edit?usp=sharing
## Project Overview
- have scrapped every text from the links given using selenium alongside ChromeDriverManager
    - implemented multithreading into scraping it as it required kind of a lot of time.
- used https://github.com/vladimarius/pyap library for detecting and parsing the data to get the address.
  - why not use a ner approach ? because it was to needy and find it difficult to tokenize + it took more time to parse then a regex approach
- verified the validity of the data using the geocode api from google maps
- returned in server the geocode data of the address scrapped alongside some simple statistics calculated.
- connected with a simple React interface where i have:
  - a page where it shows the google maps map with markers for each address scrapped
  - a page with plots of the locations of the addresses scrapped.
## How to run
-run the front-end application
```
git clone https://github.com/draqq67/MapfromScrappedLinks.git
cd interface
npm i 
npm start
```
-in a new terminal run the flask server
```
cd MapfromScrappedLinks/backend
python3 send_to_server.py
```
- if is not working consider installing into virtual env the following:
  ```
  python3 -m venv path/to/dir/MapfromScrappedLinks/backend
  pip install flask
  pip install pandas
  pip install requests
  pip install flask_cors
  ```
map photo link : https://drive.google.com/file/d/1Tr6bUu_Tsv6duDqWzP4n6USuE_S-1VLq/view?usp=sharing 

statistics page link : https://drive.google.com/file/d/1hMT8WiPw-D8VgjU6lboMRtmb0OHky1u7/view?usp=drive_link

## Thinks I should have done better
- Aggregate all pages by searching recusively through links of the site. I just got about 600 addresses and have 1.5k addresses not found, but with text on them and about 600 links that didn't work.
- Maybe I could have scrapped the contact page in case it wasn't posted on home page.
- My solution consists in different steps taken separately. Maybe for the best, I could have first start scrapping the footer, verify if the address exists then scrappe all the page and contact page, but I am not so experimented on scrapping and it took me a lot of time. Not to mention that I got memory leak bc I didn't consider to take different drivers for each thread 😂
- I think better separation of addresses, I didn't take much in consideration if there were 2 or more different addresses, as I just filter the duplicates, but as much I have seen i dont have many addresses on a single site.
- Better interface, ui/ux consists in templates from past projects, from react site and a little bit of chat gpt )))
- ik my api key is public 😂😂
