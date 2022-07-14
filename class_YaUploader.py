import requests
from datetime import datetime
import tqdm
from time import sleep
from pprint import pprint
import class_VK
import course_work_Modul_1
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
        # VK_TOKEN = config['VK_TOKEN']
        # VK_ID = config['VK_ID']

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

    def upload_photos_by_url(self, disk_file_path):
        disk_file_path = 'Нетология/Курсовая_1(VK_profile)'
        url_upload = self.url + '/v1/disk/resources/upload'
        headers = self.get_headers()
        with open('cw_result.json', 'r', encoding='utf-8') as file_for_url:
            data_files = json.load(file_for_url)
        #pprint(data_files)
        for one_file in data_files:
            #print(one_file['url']) # вывод корректный.
            params = {'url': one_file['url'],
                      'path': f'{disk_file_path}/{one_file["file_name"]}'}
            response = requests.post(url=url_upload, headers=headers, params=params) # отсюда идёт ощибка
            print(response.status_code) # выводит 409. (при requests.put 403).
            if response.status_code == 201:
                print(f'Файл {one_file["file_name"]} загружен в папку {disk_file_path} на Яндекс Диск.')
                sleep(.1)