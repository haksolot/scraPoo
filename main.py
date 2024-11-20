import os
import requests
from bs4 import BeautifulSoup

def scrape_page(base_url, output_dir):
    catalogue = base_url + "?tab=gallery"
    response = requests.get(catalogue)
    if response.status_code != 200:
        print(f"Erreur de connexion au site ({response.status_code})")
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')

    albums = soup.find_all('a', class_='album__main')
    for album in albums:
        album_name = album.find('div', class_='text_overflow album__title').text.strip()
        album_link = base_url.replace("/albums", "") + album['href']

        response = requests.get(album_link)
        if response.status_code != 200:
            print(f"Erreur de connexion au site ({response.status_code})")
            return
        
        soup = BeautifulSoup(response.text, 'html.parser')

        imageHolders = soup.find_all('div', class_="image__imagewrap")

        # print(imageHolders)

        for imageData in imageHolders:
            imageElem = imageData.find('img')
            imageLink = imageElem['data-origin-src']
            imageLink = ("https:") + imageLink
            imageId = imageData.find('div')['data-photoid']

            # response = requests.get(imageLink, stream=True)
            # response.raise_for_status()
            # with open('test.jpg', 'wb') as file:
            #     for chunk in response.iter_content(1024):
            #         file.write(chunk)

            # print("lol")
        
            print(imageLink)

scrape_page("https://no1factory.x.yupoo.com/albums", "rienpourlinstant")
