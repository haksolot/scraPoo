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
    os.makedirs(path + "/" + sanitize_filename(infos['name']), exist_ok=True)
    with open(path + "/" + sanitize_filename(infos['name']) + "/" + "seller_infos.json", "w") as file:
        json.dump(infos, file, indent=4) 

def scrape_albums(base_url, output_dir):
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
        write_album_infos(info_obj, output_dir)
        response = requests.get(album_link)
        if response.status_code != 200:
            print(f"Error trying to get sellers Yupoo page: ({response.status_code})")
            return
        soup = BeautifulSoup(response.text, 'html.parser')
        medias = soup.find_all('div', class_='showalbum__children image__main')
        for media in medias:
            if(media.find('div')['data-type'] == 'photo'):
                new_output_dir = output_dir + "/" +sanitize_filename(info_obj['name']) + "/photos"
                write_album_photo(media, new_output_dir, base_url)
            elif(media.find('div')['data-type'] == 'video'):
                new_output_dir = output_dir + "/" +sanitize_filename(info_obj['name']) + "/videos"
                write_album_video(media, new_output_dir, base_url)
    return 

def write_album_infos(infos, output_dir):
    os.makedirs(output_dir + "/" + sanitize_filename(infos['name']), exist_ok=True)
    os.makedirs(output_dir + "/" + sanitize_filename(infos['name']) + "/photos" , exist_ok=True)
    os.makedirs(output_dir + "/" + sanitize_filename(infos['name']) + "/videos" , exist_ok=True)
    with open(output_dir + "/" + sanitize_filename(infos['name']) + "/" +"album_infos.json", "w") as file:
        json.dump(infos, file, indent=4) 

def write_album_photo(media, output_dir, base_url):
    image_name = media.find('h3').text.strip()
    image_link = "http:" + media.find('img')['data-origin-src']
    headers = {
        "Referer": base_url
    }
    response = requests.get(image_link, stream=True, headers=headers)
    if response.status_code != 200:
        print(f"Error trying to scrape image: ({response.status_code})")
        return
    with open(output_dir + "/" + image_name, "wb") as file:
        for chunk in response.iter_content(1024):
            file.write(chunk)

def write_album_video(media, output_dir, base_url):
    video_name = media.find('h3').text.strip()
    video_link = "http://uvd.yupoo.com" + media.find('img')['data-path']
    headers = {
        "Referer": base_url
    }
    response = requests.get(video_link, stream=True, headers=headers)
    if response.status_code != 200:
        print(f"Error trying to scrape image: ({response.status_code})")
        return
    with open(output_dir + "/" + video_name, "wb") as file:
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
