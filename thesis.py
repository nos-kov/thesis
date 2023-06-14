import requests

from pprint import pprint



def get_user_data(token):

    url = 'https://api.vk.com/method/users.get'
    params = {'user_ids': '1', 'access_token': token, 'v': '5.131'}

    response = requests.get(url, params=params)
    data = response.json()
    return data

if __name__ == '__main__':
        
        
    with open("token.txt", 'r') as token_file:
        token = token_file.readline()

    data = get_user_data(token)
    pprint(data)



