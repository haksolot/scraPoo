import os
import requests
from bs4 import BeautifulSoup
import json
import re

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

def scrape_album_infos(base_url):
    result = []
    catalogue = base_url + "/albums?tab=gallery"
    response = requests.get(catalogue)
    if response.status_code != 200:
        print(f"Error trying to get sellers Yupoo page: ({response.status_code})")
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')
    albums = soup.find_all('div', class_='showindex__children')

    for album in albums:
        album_name = album.find('div', class_='text_overflow album__title').text.strip()
        album_link = base_url + album.find('a', class_='album__main')['href']
        album_image_number = album.find('div', class_='text_overflow album__photonumber').text.strip()
        info_obj = {
            "name": album_name,
            "link": album_link,
            "image_number": album_image_number
        }
        result.append(info_obj)

        response = requests.get(album_link)
        if response.status_code != 200:
            print(f"Error trying to get sellers Yupoo page: ({response.status_code})")
            return
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('div', class_='showalbum__children image__main')
        date = soup.find('time', class_='text_overflow').text.strip()
        info_obj['date'] = date
        images = []
        for article in articles:
            image_infos = {}
            image_infos['file_name'] = article.find('h3').text.strip()
            image_infos['file_link'] = "http:" + article.find('img')['data-origin-src']
            images.append(image_infos)
        info_obj['images'] = images
    return result

def write_album_infos(infos, path):
    with open(path + "/" + "album_infos.json", "w") as file:
        json.dump(infos, file, indent=4) 
        
def media_download(url, name, path):
    _, ext = os.path.splitext(url)
    if not ext:
        print("Impossible de déterminer le suffixe à partir de l'URL.")
        return
    response = requests.get(url, stream=True)
    if response.status_code != 200:
            print(f"Error trying to get sellers Yupoo page: ({response.status_code})")
            return
    full_name = name + ext
    with open(path + "/" + full_name, "wb") as file:
        for chunk in response.iter_content(1024):
            file.write(chunk)

def sanitize_filename(filename):
    replacements = {
        '*': '-',    
        ':': '-',    
        '<': '(',    
        '>': ')',    
        '?': '',     
        '|': '-',    
        '"': "'",    
        '/': '-',    
        '\\': '-',   
    }
    
    for char, replacement in replacements.items():
        filename = filename.replace(char, replacement)
    
    return filename

def build_seller_page(base_url, path):
    seller_infos = scrape_seller_infos(base_url)
    os.makedirs(path + "/" + sanitize_filename(seller_infos['name']), exist_ok=True)
    with open(path + "/" + sanitize_filename(seller_infos['name']) + "/data.json", 'w') as file:
        json.dump(seller_infos, file, indent=4)
    albums_infos = scrape_album_infos(base_url)
    for album in albums_infos:
        album_path = path + "/" + sanitize_filename(seller_infos['name']) + "/" + sanitize_filename(album['name'])
        os.makedirs(album_path, exist_ok=True)
        with open(album_path + "/data.json", 'w') as file:
            json.dump(album, file, indent=4)
        for image in album['images']:
            media_download(image['file_link'], sanitize_filename(image['file_name']), album_path)

build_seller_page("https://no1factory.x.yupoo.com", ".")