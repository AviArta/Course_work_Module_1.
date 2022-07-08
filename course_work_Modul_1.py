import requests
from datetime import datetime
from tqdm import trange
from time import sleep
from pprint import pprint

for a in trange((100), desc=''):
    sleep(.1)

with open('my_tokens_vk_ya.txt', 'r') as file_object:
    VK_TOKEN = file_object.readline().strip()
    VK_ID = file_object.readline().strip()
    YA_TOKEN = file_object.readline().strip()

class VK:
    url = 'https://api.vk.com/method/'

    def __init__(self, access_token, user_id, version):
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
        for photo_dict in self.search_photos_dict():
            sizes_list = photo_dict.get('sizes')
            likes = photo_dict.get('likes')
            name_photo = likes.get('count')
            name_photos_dict = {}
            photo_all_size_dict = {}
            name_size_url_dict = {}
            max_type = 0
            if name_photo not in name_photos_dict.keys():
                full_name_photo = str(name_photo) + '.jpg'
            else:  # часть "like + дата" не работает.
                date_seconds = photo_dict.get('date')
                date = str(datetime.fromtimestamp(date_seconds))[:10]
                full_name_photo = str(name_photo) + '.' + str(date) + '.jpg'
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
            name_size_url_dict[full_name_photo] = max_type, url
            final_photo_list.append(name_size_url_dict)
            sleep(.1) #
        return final_photo_list

    def add_file_result(self):
        final_photo_list = self.search_photo_max_size()
        for el in final_photo_list:
            for k, v in el.items():
                file_name = k
                file_link = v[1]
                with open('cw_result.txt', 'a', encoding='utf-8') as result_file:
                    result_file.write(f"{file_name}\n {file_link}\n")

class YaUploader:
    url = 'https://cloud-api.yandex.net'
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def get_upload_link(self, disk_file_path):
        url_get_link = self.url + '/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {
            'path': disk_file_path,
            'overwrite': 'true'}
        response = requests.get(url_get_link, headers=headers, params=params)
        return response.json()

    # идея функции в том, чтобы брать из файла 'cw_result.txt' поочерёдно каждые 2 строчки и записывать
    # в переменные file_url, file_name, но я запуталась в ноль, вернусь к ней на свежую голову
    def upload_photos_by_url(self, disk_file_path, file_name, file_url):
        url_upload = self.url + '/v1/disk/resources/upload'
        headers = self.get_headers()
        with open('cw_result.txt', 'r', encoding='utf-8') as file:
            for line in file:
                for line in range(1, 3):
                    file_name = file.readlines()
                    url_photo = file.readlines()
                    pprint(file_name, url_photo)
                    print('____')
                    params_upload = {
                        'url': file_url,
                        'path': file_name}
                    response = requests.put(url_upload, data=open(file_url, 'rb'))
                    response.raise_for_status()
                    if response.status_code == 201:
                        print('Success')
    # def upload_photos_by_url(self, disk_file_path, url_photo):
    #     response_href = self.get_upload_link(disk_file_path=disk_file_path)
    #     url = response_href.get('href', '')
    #     with open('cw_result.txt', 'r', encoding='utf-8') as file:
    #         for line in file:
    #             file_name = file.readlines()
    #             url_photo = file.readlines()
    #             pprint(file_name, url_photo)
    #             print('____')
                # response = requests.put(url, data=open(url_photo, 'rb'))
                # response.raise_for_status()
                # if response.status_code == 201:
                #     print('Success')

if __name__ == '__main__':
    vk_client = VK(VK_TOKEN, VK_ID, '5.131')
    ya_uploader = YaUploader(YA_TOKEN)
    pprint(vk_client.search_photo_max_size())
    pprint(vk_client.add_file_result())
    disk_file_path = 'Курсовая_1(VK_profile)/{file_name}'
    #pprint(ya_uploader.search_name_url_photos())
    #ya_uploader.upload_photos_by_url(disk_file_path=disk_file_path, file_name='', file_url=r'file_url')
