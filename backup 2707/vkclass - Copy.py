import requests
import json
import sys
from tqdm import tqdm
import os
from contextlib import suppress
from datetime import datetime


class VKdownload:
    def __init__(self, token: str):
        self.token = token

    def get_user_data(self, token, user_id):
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

    def get_id_by_scrname(self, user_id, token):
        """Gets integer user id from supplied screen name"""
    
        url = 'https://api.vk.com/method/users.get'
        params = {
            'user_ids': user_id,
            'access_token': token,
            'v': '5.131'
        }

        response = requests.get(url, params=params)
        data = response.json()
        return data["response"][0]["id"]

    def get_photos_url(
        self,
        data,
        final_directory,
            threshold: int):

        ''' Gets URL of photos to be downloaded '''

        counter = 0
        urls = {}
        output_json = []
        check_likes = []

        with suppress(Exception):
            if data['error']:
                print("Some response errors popped up. Program terminated.")
                sys.exit()
    
        for element in tqdm(
                data['response']['items'][:threshold],
                desc="Getting the URLs of photos.."):

            maximum = {}
            file_info = {}

            for picture in element['sizes']:

                maximum[picture['height']] = []
                maximum.update(
                    {picture['height']: ([picture['url'],
                     element['likes'], element['date']])})

            keymax = max(maximum.keys())
            check_likes.append(str(maximum[keymax][1]['count']))
            if check_likes.count(str(maximum[keymax][1]['count'])) > 1:

                name = str(maximum[keymax][1]['count']) + (
                    ("_") + str(datetime.fromtimestamp(maximum[keymax][2])) + (
                        '.jpg'))
            else:
                name = str(maximum[keymax][1]['count']) + '.jpg'
            clear_name = name.replace(":", "")
            urls[name] = maximum[keymax][0]
            r = requests.get(maximum[keymax][0], allow_redirects=True)
            open(os.path.join(final_directory, clear_name), 'wb').write(r.content)
            file_info['file_name'] = clear_name
            file_info['size'] = os.path.getsize(
                os.path.join(final_directory, clear_name))
            output_json.append(file_info)
            counter += 1
            if counter >= threshold:
                break
        with open('output.json', 'w', encoding='utf-8') as f:
            json.dump(output_json, f, ensure_ascii=False, indent=4)
        
        return urls
