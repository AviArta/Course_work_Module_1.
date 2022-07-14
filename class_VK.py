import requests
from datetime import datetime
import json
from tqdm import trange
from time import sleep
from pprint import pprint
import class_YaUploader
import course_work_Modul_1

with open('token_vk_ya.txt', 'r') as file_object:
    VK_TOKEN = file_object.readline().strip()
    VK_ID = file_object.readline().strip()

class VK:
    url = 'https://api.vk.com/method/'

    # def config_read(self):
    #     filename = 'my_tokens.config'
    #     contents = open(filename).read()
    #     config = eval(contents)
    #     VK_TOKEN = config['VK_TOKEN']
    #     VK_ID = config['VK_ID']
        # YA_TOKEN = config['YA_TOKEN']

    def __init__(self, access_token=VK_TOKEN, user_id=VK_ID, version='5.131'):
        # self.config_read()
        # access_token = input('Введите Ваш токен VK: ')
        # user_id = input('Введите Ваш user ID или screen_name VK: ')
        self.params = {'access_token': access_token,
                       'user_id': user_id,
                       'v': version}


    def search_photos_dict(self, album_id='profile', photo_sizes=1, rev=0, extended=1):
        search_photos_url = self.url + 'photos.get'
        search_photos_params = {
            'album_id': album_id,
            'photo_sizes': photo_sizes,
            'rev': rev,
            'extended': extended}
        response = requests.get(search_photos_url, params={**self.params, **search_photos_params}).json()
        #pprint(response['response']['items'])
        sleep(.1)
        return response['response']['items']

    def type_by_size(self):
        size_dict = {'0': 0, 's': 1, 'm': 2, 'x': 3, 'o': 4, 'p': 5, 'q': 6, 'r': 7, 'y': 8, 'z': 9, 'w': 10}
        size_list_sort = sorted(size_dict, key=size_dict.get)
        return size_list_sort

    def search_photo_max_size(self):
        final_photo_list = []
        name_photos_list = []
        for photo_dict in self.search_photos_dict():
            sizes_list = photo_dict.get('sizes')
            likes = photo_dict.get('likes')
            name_photo = likes.get('count')
            name_photos_dict = {}
            #name_photos_list = []
            photo_all_size_dict = {}
            name_size_url_dict = {}
            max_type = 0
            if name_photo not in name_photos_list:
                full_name_photo = str(name_photo) + '.jpg'
                name_photos_list.append(name_photo)
            else:
                date_seconds = photo_dict.get('date')
                date = str(datetime.fromtimestamp(date_seconds))[:10]
                full_name_photo = str(name_photo) + '.' + date + '.jpg'
                name_photos_list.append(full_name_photo)
            for each_size_dict in sizes_list:
                if each_size_dict.get('width') == 0 and each_size_dict.get('height') == 0:
                    size_ = '0'
                else:
                    size_ = each_size_dict.get('type')
                photo_all_size_dict[each_size_dict.get('url')] = size_
            for el in self.type_by_size():
                for url, photo_size in photo_all_size_dict.items():
                    if el == photo_size:
                        max_type = photo_size
            name_size_url_dict['file_name'] = full_name_photo
            name_size_url_dict['size'] = max_type
            name_size_url_dict['url'] = url
            final_photo_list.append(name_size_url_dict)
        sleep(.1)
        return final_photo_list

    def final_photo_list_by_size(self, count=5):
        self.count = int(input('Введите нужное количество фотографий для загрузки: '))
        final_photo_list = self.search_photo_max_size()
        final_photo_list_by_size = []
        for el in self.type_by_size()[::-1]:
            for photo_data in final_photo_list:
                if len(final_photo_list_by_size) < self.count and el == photo_data['size']:
                    final_photo_list_by_size.append(photo_data)
        return final_photo_list_by_size

    def add_file_result(self):
        final_photo_list_by_size = self.final_photo_list_by_size()
        with open('cw_result.json', 'w') as result_file:
            json.dump(final_photo_list_by_size, result_file, indent=4)
        return 'Success'

    # def upload_photos_by_url(self, disk_file_path):
    #     disk_file_path = 'Нетология/Курсовая_1(VK_profile)'
    #     url_upload = class_YaUploader.url + '/v1/disk/resources/upload'
    #     headers = self.get_headers()
    #     with open('cw_result.json', 'r', encoding='utf-8') as file_for_url:
    #         data_files = json.load(file_for_url)
    #         for one_file in data_files:
    #             params = {'url': one_file['url'],
    #                       'path': f"{disk_file_path}/{one_file['file_name']}"}
    #         response = requests.post(url_upload, headers=headers, params=params, data=open(url_upload, 'rb'))
    #         response.raise_for_status()
    #         if response.status_code == 201:
    #             print('Success')