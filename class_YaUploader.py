import requests
from tqdm import tqdm
from time import sleep
import json

with open('token_vk_ya.txt', 'r') as file_object:
    YA_TOKEN = file_object.readline().strip()

class YaUploader:
    url = 'https://cloud-api.yandex.net'

    # def config_read(self):
    #     filename = 'my_tokens.config'
    #     contents = open(filename).read()
    #     config = eval(contents)
    #     YA_TOKEN = config['YA_TOKEN']
    #     VK_TOKEN = config['VK_TOKEN']
    #     VK_ID = config['VK_ID']

    def __init__(self, ya_token=YA_TOKEN):
        # self.config_read()
        self.ya_token = ya_token
        #ya_token = input('Введите токен Яндекс Диска: ')

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.ya_token)
        }

    # def get_upload_link(self, disk_file_path):
    #     url_get_link = self.url + '/v1/disk/resources/upload'
    #     headers = self.get_headers()
    #     params = {
    #         'path': disk_file_path,
    #         'overwrite': 'true'}
    #     response = requests.get(url_get_link, headers=headers, params=params)
    #     return response.json()

    def create_new_folder(self, dir_ya='/VK_photos_profile'):
        folder_url = self.url + '/v1/disk/resources'
        headers = self.get_headers()
        params = {'path': dir_ya}
        response = requests.put(folder_url, headers=headers, params=params)
        dir_status = False
        if response.status_code == 201:
            print(f'Папка {dir_ya} на Яндекс.Диске создана.')
            dir_status = False
        if response.status_code == 409:
            print(f'Папка {dir_ya} на Яндекс.Диске уже существует.')
        if dir_status:
            self.folder = dir_ya
        return dir_status

    def upload_photos_by_url(self):
        url_upload = self.url + '/v1/disk/resources/upload'
        headers = self.get_headers()
        dir_ya = '/VK_photos_profile'
        with open('cw_result.json', 'r', encoding='utf-8') as file_for_url:
            data_files = json.load(file_for_url)
        #pprint(data_files)
        for one_file in tqdm(data_files):
            #print(one_file['url']) # вывод корректный.
            params = {'url': one_file['url'],
                      'path': f'{dir_ya}/{one_file["file_name"]}',
                      'overwrite': 'true'}
            response = requests.post(url=url_upload, headers=headers, params=params)
            #print(response.status_code)
            if response.status_code == 202:
                print(f'Файл {one_file["file_name"]} загружен в папку {dir_ya} на Яндекс.Диск.')
                sleep(.1)