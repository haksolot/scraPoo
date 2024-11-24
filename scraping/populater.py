import os
import requests
import json
import shutil


def create_seller_dir(seller_infos, destination_path):
    with open(seller_infos, 'rb') as file:
        data = json.load(file)
        os.makedirs(destination_path + "/" + data.get("name"), exist_ok=True)
        shutil.copy(seller_infos, destination_path + "/" + data.get("name") + "/data.json")
        # with open(destination_path + "/" + data.get("name") + "/data.json", 'wb') as dst:
        #     dst.write(file.read())
        
