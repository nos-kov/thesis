from vkclass import VKdownload
from yaclass import YaUploader
from tqdm import tqdm
import configparser

import os
import glob


def create_directory():
    ''' Creates directory for temporary storage of downloaded photos. '''
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, r'temp')
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)
    return final_directory


def cleanup():
    ''' Delete temp dir '''
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, r'temp')
    files = glob.glob(final_directory + '\\*')
    for f in files:
        os.remove(f)
    os.rmdir(final_directory)


if __name__ == '__main__':

    urls = {}

    user_id = input("Enter user_id or screen name:")
    threshold = input(
        "Enter number of photos you'd like to limit your selection with:")
    ya_token = input("Enter Yandex.Disk's token:")
    ya_folder_name = input("Enter name for new Yandex.Disk's folder:")
    config = configparser.ConfigParser()
    config.read("token.ini")
    token = config["VK"]["token"]

    download = VKdownload(token)
    if not user_id.isnumeric():
        data = download.get_user_data(
            token, download.get_id_by_scrname(user_id, token))
    else:
        data = download.get_user_data(token, user_id)

    urls = download.get_photos_url(data, create_directory(), int(threshold))

    path_to_file = os.path.join(os.getcwd(), 'temp')
    uploader = YaUploader(ya_token)
    uploader.create_folder(ya_folder_name)
    for name, url in tqdm(urls.items(), desc="Uploading photos.."):
        result = uploader.upload(
            url, (ya_folder_name + "/" + name.replace(":", "")))
        #url[:url.rfind("?size")]
    cleanup()
print("Execution completed")