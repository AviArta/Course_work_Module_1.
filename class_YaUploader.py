import json
from time import sleep

import requests
from tqdm import tqdm


class YaUploader:
    url = 'https://cloud-api.yandex.net'

    def __init__(self, ya_token):
        self.ya_token = ya_token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.ya_token)
        }

    def create_new_folder(self, dir_ya='/VK_photos_profile'):
        """ Функция создания новой папки """
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
        """ Функция загрузки фото по ссылке """
        url_upload = self.url + '/v1/disk/resources/upload'
        headers = self.get_headers()
        dir_ya = '/VK_photos_profile'
        with open('cw_result.json', 'r', encoding='utf-8') as file_for_url:
            data_files = json.load(file_for_url)
        for one_file in tqdm(data_files):
            params = {'url': one_file['url'],
                      'path': f'{dir_ya}/{one_file["file_name"]}',
                      'overwrite': 'true'}
            response = requests.post(url=url_upload, headers=headers, params=params)
            print(response.status_code)
            if response.status_code == 202:
                print(f'Файл {one_file["file_name"]} загружен в папку {dir_ya} на Яндекс.Диск.')
                sleep(.1)