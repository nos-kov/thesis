import requests

from pprint import pprint


def get_user_data(token, user_id, ya_token):

    #url = 'https://api.vk.com/method/users.get'
    
    url = 'https://api.vk.com/method/photos.get'
    params = {'owner_id': user_id, 'access_token': token, 'album_id': 'profile', 'extended' : '1', 'photo_sizes': '1' , 'v': '5.131'}

    response = requests.get(url, params=params)
    data = response.json()
    return data

if __name__ == '__main__':
        
    user_id = input("Enter user_id:")
    ya_token = input("Enter Yandex.Disk's token:")

    with open("token.txt", 'r') as token_file:
        token = token_file.readline()

    data = get_user_data(token, user_id, ya_token)
    maximum = {}
    counter = 0
    for element in data['response']['items']:
        for picture in element['sizes']:
            
            maximum[picture['height']] = []
            maximum.update({picture['height']: [picture['url'] , element['likes']]})
        keymax = max(maximum.keys())
        r = requests.get(maximum[keymax][0], allow_redirects=True)
        name = str(maximum[keymax][1]['count']) + '.jpg' 
        open( name, 'wb').write(r.content)

            #pprint(element['id'])



