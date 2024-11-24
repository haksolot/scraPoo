import os
import requests
from bs4 import BeautifulSoup
import json
from concurrent.futures import ThreadPoolExecutor

def fetch_album_details(album_link):
    response = requests.get(album_link)
    if response and response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        date = soup.find('time', class_='text_overflow').text.strip()
        articles = soup.find_all('div', class_='showalbum__children image__main')
        images = [
            {
                "file_name": article.find('h3').text.strip(),
                "file_link": "http:" + article.find('img')['data-origin-src']
            }
            for article in articles
        ]
        return {"date": date, "images": images}
    print(f"Error fetching album details: {album_link}")
    return None

def scrape_album_infos(base_url):
    catalogue = base_url + "/albums?tab=gallery"
    response = requests.get(catalogue)
    if not response or response.status_code != 200:
        print(f"Error fetching seller page: {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.text, 'lxml')
    albums = soup.find_all('div', class_='showindex__children')

    album_infos = [
        {
            "name": album.find('div', class_='text_overflow album__title').text.strip(),
            "link": base_url + album.find('a', class_='album__main')['href'],
            "image_number": album.find('div', class_='text_overflow album__photonumber').text.strip()
        }
        for album in albums
    ]

    with ThreadPoolExecutor(max_workers=5) as executor:
        detailed_infos = list(executor.map(lambda album: fetch_album_details(album['link']), album_infos))
    
    for i, detail in enumerate(detailed_infos):
        if detail:
            album_infos[i].update(detail)
    
    return album_infos

def write_album_infos(infos, path):
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, "album_infos.json"), "w") as file:
        json.dump(infos, file, indent=4)

# Exécution
base_url = "https://no1factory.x.yupoo.com"
album_infos = scrape_album_infos(base_url)
write_album_infos(album_infos, "output")
