import json
import requests
import os
import sys
from tqdm import tqdm

from contextlib import suppress


class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def upload(self, file_path: str, disk_path: str):
        """Uploads files to Ya.Disk"""
        
        headers = {

            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)

        }
        files_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        params = {"path": disk_path, "overwrite": "True"}
        response = requests.get(files_url, headers=headers, params=params)
        response_data = response.json()
        href = response_data["href"]

        response = requests.put(href, data=open(file_path, 'rb'))
    
    def create_folder(self, folder_name):
        """ Creates a folder for the upload to Ya Disk"""

        headers = {

            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)

        }
        folder_url = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {"path": folder_name}
        response = requests.put(folder_url, headers=headers, params=params)
        response_data_folder = response.json()


def get_user_data(token, user_id):
    ''' Connects to VK API and gets JSON data from response '''
    url = 'https://api.vk.com/method/photos.get'
    params = {
        'owner_id': user_id,
        'access_token': token,
        'album_id': 'profile',
        'extended': '1',
        'photo_sizes': '1',
        'v': '5.131'
        }

    response = requests.get(url, params=params)
    data = response.json()
    return data


def create_directory():
    ''' Creates directory for temporary storage of downloaded photos. '''
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, r'temp')
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)
    return final_directory


def download_photos(data, final_directory):
    ''' Actually downloads photos through API and saves to the Temp folder '''
    with suppress(Exception):
        if data['error']:
            print("Some response errors popped up. Program terminated.")
            sys.exit()
    
    for element in tqdm(data['response']['items'], desc="Downloading photos.."):

        maximum = {}
        file_info = {}
        output_json = []

        for picture in element['sizes']:
                   
            maximum[picture['height']] = []
            maximum.update({picture['height']: [picture['url'], element['likes'], element['date']]})

        keymax = max(maximum.keys())
        r = requests.get(maximum[keymax][0], allow_redirects=True)
        name = str(maximum[keymax][1]['count']) + ("_") + str(maximum[keymax][2]) + '.jpg' 
        open(os.path.join(final_directory, name), 'wb').write(r.content)
        file_info['file_name'] = name
        file_info['size'] = os.path.getsize(os.path.join(final_directory, name))
        output_json.append(file_info)
    with open('output.json', 'w', encoding='utf-8') as f:
        json.dump(output_json, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':

    create_directory()

    user_id = input("Enter user_id:")
    ya_token = input("Enter Yandex.Disk's token:")
    ya_folder_name = input("Enter name for new Yandex.Disk's folder:")

    with open("token.txt", 'r') as token_file:
        token = token_file.readline()

    data = get_user_data(token, user_id)

    download_photos(data, create_directory())

    path_to_file = os.path.join(os.getcwd(), 'temp')
    uploader = YaUploader(ya_token)
    uploader.create_folder(ya_folder_name)
    list_of_photos = os.listdir(path_to_file)
    for photo in tqdm(list_of_photos, desc="Uploading photos to Yandex Disk"):
        path_to_file = os.path.join(os.getcwd(), 'temp', photo)
        result = uploader.upload(path_to_file, (ya_folder_name + "/" + photo))
print("Execution completed")