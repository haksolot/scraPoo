import os
import requests
from bs4 import BeautifulSoup
import json

def scrape_page(base_url, output_dir):
    catalogue = base_url + "?tab=gallery"
    response = requests.get(catalogue)
    if response.status_code != 200:
        print(f"Erreur de connexion au site ({response.status_code})")
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')

    # with open(os.path.join("response.html"), "w", encoding="utf-8") as file:
    #     file.write(response.text)

    # print(catalogue)

    # seller_name = base_url.split(".")[0].replace("https://", "")
    seller_name = soup.find('h1', class_='showheader__nickname').text.strip()
    print(seller_name)

    # Infos "Contact"
    req_contact = requests.get(base_url.replace("/albums", "/contact"))
    soup_contact = BeautifulSoup(req_contact.text, 'html.parser')
    contact = soup_contact.find('main').text.strip()

    # Créer le dossier de l'artiste (si existe pas)
    os.makedirs(seller_name, exist_ok=True)

    # Créer maintenant un fichier data.json contenant les infos de l'artiste
    data = {
        "name": seller_name,
        "contact": contact
        # Ajouter d'autres infos : nombres albums, etc...
    }

    # Enregistrer dans un fichier "data.json"
    with open(f"{seller_name}/data.json", "w+") as file:
        json.dump(data, file)

    albums = soup.find_all('a', class_='album__main')
    i = 0
    for album in albums:
        i = i + 1
        # Créer maintenant le dossier de l'album (stocké dans le dossier de l'artiste)
        os.makedirs(f"{seller_name}/{str(i)}", exist_ok=True)

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
            # Les images sont maintenant stockées dans "{artist_name}/{str(i)}"
            # (et non "str(i)")
            fileDir = f"{seller_name}/{str(i)}/{str(j)}.png"

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

        # Changer le nom du dossier par le nom de la case (plus nécessaire)
        # changer_nom(i, album_name)


def changer_nom(i, nom, add=0):
    try:
        if add == 0:
            os.rename(str(i), nom.replace("*", " "))
        else:
            os.rename(str(i), nom.replace("*", " ") + " " +str(add))
    except FileExistsError:  # dossier deja existant
        changer_nom(i, nom, add+1)



scrape_page("https://no1factory.x.yupoo.com/albums", "rienpourlinstant")
