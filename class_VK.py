import json
from datetime import datetime

import requests


class VK:
    url = 'https://api.vk.com/method/'

    def __init__(self, access_token, user_id, version='5.131'):
        self.params = {'access_token': access_token,
                       'user_id': user_id,
                       'v': version}

    def search_photos_dict(self, album_id='profile', photo_sizes=1, rev=0, extended=1):
        """ Функция создания словаря с полной информацией по всем фото """
        search_photos_url = self.url + 'photos.get'
        search_photos_params = {
            'album_id': album_id,
            'photo_sizes': photo_sizes,
            'rev': rev,
            'extended': extended}
        response = requests.get(search_photos_url, params={**self.params, **search_photos_params}).json()
        return response['response']['items']

    def type_by_size(self):
        """ Функция сортировки всех существующих размеров фото по типу """
        size_dict = {'0': 0, 's': 1, 'm': 2, 'x': 3, 'o': 4, 'p': 5, 'q': 6, 'r': 7, 'y': 8, 'z': 9, 'w': 10}
        size_list_sort = sorted(size_dict, key=size_dict.get)
        return size_list_sort

    def search_photo_max_size(self):
        """ Функция сортировки размеров каждого фото.
        Результат: список всех фото, каждое из которых уже с мах размером.
        """
        final_photo_list = []
        name_photos_list = []
        for photo_dict in self.search_photos_dict():
            sizes_list = photo_dict.get('sizes')
            likes = photo_dict.get('likes')
            name_photo = likes.get('count')
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
        return final_photo_list

    def final_photo_list_by_size(self, count=5):
        """ Функция создания финального списка фото, каждый размер которого уже мах.
        Количество фото в списке запрашивается у пользователя, по умолчанию 5.
        """
        self.count = int(input('Введите нужное количество фотографий для загрузки: '))
        final_photo_list = self.search_photo_max_size()
        final_photo_list_by_size = []
        for el in self.type_by_size()[::-1]:
            for photo_data in final_photo_list:
                if len(final_photo_list_by_size) < self.count and el == photo_data['size']:
                    final_photo_list_by_size.append(photo_data)
        return final_photo_list_by_size

    def add_file_result(self):
        """ Функция добавления отсортированного списка фото
        в результирующий json файл.
        """
        final_photo_list_by_size = self.final_photo_list_by_size()
        with open('cw_result.json', 'w') as result_file:
            json.dump(final_photo_list_by_size, result_file, indent=4)
        return 'Success'
