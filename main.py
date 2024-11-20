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
    i = 0
    for album in albums:
        i = i + 1
        os.makedirs(str(i), exist_ok=True)
        album_name = album.find('div', class_='text_overflow album__title').text.strip()
        album_link = base_url.replace("/albums", "") + album['href']

        response = requests.get(album_link)
        if response.status_code != 200:
            print(f"Erreur de connexion au site ({response.status_code})")
            return
        
        soup = BeautifulSoup(response.text, 'html.parser')

        imageHolders = soup.find_all('div', class_="image__imagewrap")

        # print(imageHolders)
        j = 0
        for imageData in imageHolders:
            j = j + 1
            fileDir = str(i) + "/" + str(j) + ".png"
            imageElem = imageData.find('img')
            imageLink = imageElem['data-origin-src']
            imageLink = ("https:") + imageLink
            imageId = imageData.find('div')['data-photoid']

            headers = {
                "Referer": base_url
            }

            response = requests.get(imageLink, stream=True, headers=headers)
            response.raise_for_status()
            with open(fileDir, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)

            # print("lol")
        
            print(imageLink)

        # Changer le nom du dossier par le nom de la case
        changer_nom(i, album_name)


def changer_nom(i, nom, add=0):
    try:
        if add == 0:
            os.rename(str(i), nom.replace("*", " "))
        else:
            os.rename(str(i), nom.replace("*", " ") + " " +str(add))
    except FileExistsError:  # dossier deja existant
        changer_nom(i, nom, add+1)



scrape_page("https://no1factory.x.yupoo.com/albums", "rienpourlinstant")
