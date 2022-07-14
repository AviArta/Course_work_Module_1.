from tqdm import trange
from time import sleep
from pprint import pprint
import class_VK
import class_YaUploader

for a in trange((100), desc=''):
    sleep(.1)

# # чтение файла .config работает, но переменные не передаются в классы.
# def config_read():
#     filename = 'my_tokens.config'
#     contents = open(filename).read()
#     config = eval(contents)
#     VK_TOKEN = config['VK_TOKEN']
#     VK_ID = config['VK_ID']
#     YA_TOKEN = config['YA_TOKEN']
#     return VK_TOKEN, VK_ID, YA_TOKEN

with open('token_vk_ya.txt', 'r') as file_object:
    VK_TOKEN = file_object.readline().strip()
    VK_ID = file_object.readline().strip()
    YA_TOKEN = file_object.readline().strip()

if __name__ == '__main__':
    # config_read()
    vk_client = class_VK.VK(VK_TOKEN, version='5.131')
    pprint(vk_client.final_photo_list_by_size())
    pprint(vk_client.add_file_result())
    #ya_uploader = class_YaUploader.YaUploader(YA_TOKEN)
    #pprint(ya_uploader.create_new_folder())
    #pprint(ya_uploader.upload_photos_by_url())

