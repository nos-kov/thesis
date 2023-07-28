import requests


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
        params = {"path": disk_path, "url": file_path, "overwrite": "True"}
        response = requests.get(files_url, headers=headers, params=params)
        response_data = response.json()
        href = response_data["href"]

        response = requests.put(href)
    
    def create_folder(self, folder_name):
        """ Creates a folder for the upload to Ya Disk"""

        headers = {

            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)

        }
        folder_url = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {"path": folder_name}
        response = requests.put(folder_url, headers=headers, params=params)
        #response_data_folder = response.json()