import os
import requests
from bs4 import BeautifulSoup
import json

def scrape_seller_infos(base_url):
    result = {}
    response = requests.get(base_url)
    if response.status_code != 200:
        print(f"Error trying to get sellers Yupoo page: ({response.status_code})")
        return
    soup = BeautifulSoup(response.text, 'html.parser')
    result['name'] = soup.find('h1', class_='showheader__nickname').text.strip()
    response = requests.get(base_url + '/contact')
    soup = BeautifulSoup(response.text, 'html.parser')
    result['description'] = soup.find('main').text.strip()
    return result

def write_seller_infos(infos, path):
    with open(path + "/" + "seller_infos.json", "w") as file:
        json.dump(infos, file, indent=4) 
