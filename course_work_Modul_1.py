from pprint import pprint
from time import sleep
# id1745821
import requests
from tqdm import trange

import class_VK
import class_YaUploader

for a in trange((100), desc=''):
    sleep(.1)

def config_read(path):
    filename = 'my_tokens.config'
    contents = open(filename).read()
    config = eval(contents)
    VK_TOKEN = config['VK_TOKEN']
    VK_ID = config['VK_ID']
    VK_SCREEN_NAME = config['VK_SCREEN_NAME']
    YA_TOKEN = config['YA_TOKEN']
    return VK_TOKEN, VK_ID, VK_SCREEN_NAME, YA_TOKEN

tokens = config_read('my_tokens.config')

def search_id_by_screen_name(access_token, screen_name, v='5.131'):
    """ Определяет id по screen_name """
    search_id_by_screen_name_url = 'https://api.vk.com/method/utils.resolveScreenName'
    params_by_screen_name = {'access_token': access_token, 'screen_name': screen_name, 'v': v}
    response = requests.get(search_id_by_screen_name_url, params=params_by_screen_name).json()
    return response['response']['object_id']

# Замена screen_name на id
user_id = tokens[1]
if tokens[1] == '':
  user_id = search_id_by_screen_name(tokens[0], tokens[2])
#print(user_id)

if __name__ == '__main__':
    vk_client = class_VK.VK(tokens[0], user_id, version='5.131')
    #pprint(vk_client.search_photos_dict())
    #pprint(vk_client.final_photo_list_by_size())
    pprint(vk_client.add_file_result())
    ya_uploader = class_YaUploader.YaUploader(tokens[3])
    pprint(ya_uploader.create_new_folder())
    pprint(ya_uploader.upload_photos_by_url())

