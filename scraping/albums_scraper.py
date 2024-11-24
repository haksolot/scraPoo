import os
import requests
from bs4 import BeautifulSoup
import json

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