import requests
import json
from ya import YaUpLoader
import os
from pprint import pprint


my_id = '22708602'

with open('toc_vk.txt') as f:
    token = f.read().strip()
URL = 'https://api.vk.com/method/'

with open('toc_ya.txt') as f:
    token_ya = f.read().strip()


def get_data(id):
    url_get_photo = URL + 'photos.get'
    params = {
        'owner_id': id,
        'album_id': 'profile',
        'extended': 1,
        'access_token': token,
        'v': '5.131'
    }
    result = requests.get(url=url_get_photo, params=params).json()
    return result


def count_likes(likes):
    digits_list_one = list(range(11, 20))
    digits_list_two = list(range(2, 5))
    digits_list_three = list(range(5, 10))

    if likes[-1] == '0':
        return 'Лайков'
    elif int(likes[-2:]) in digits_list_one:
        return 'Лайков'
    elif likes[-1] == '1':
        return 'Лайк'
    elif int(likes[-1]) in digits_list_two:
        return 'Лайка'
    elif int(likes[-1]) in digits_list_three:
        return 'Лайков'


def get_photo(result):
    max_size = 0
    quantity_likes = None
    count = 1

    for num, photo in enumerate(result['response']['items'], start=1):
        for i in photo['sizes']:
            if int(i['height']) + int(i['width']) > max_size:
                max_size = int(i['height']) + int(i['width'])
                download_image = requests.get(url=i['url'])
                type_photo = i['type']
        likes = str(photo['likes']['count'])
        if likes == quantity_likes:
            likes = f'{likes}({str(count)})'
            count += 1
        word = count_likes(likes)
        with open(likes + f' {word}.png', 'wb') as file:
            file.write(download_image.content)
        photo_info = {'file_name': f'{likes} {word}.png', 'size': type_photo}
        with open('vk_info.json', 'a', encoding='utf-8') as f:
            json.dump(photo_info, f, ensure_ascii=False)
            json.dump('\n', f)
        max_size = 0


def get_list_png():
    data = os.getcwd()
    docs = os.listdir(data)
    docs_py = []

    for file in docs:
        if file[-4:] == '.png':
            docs_py.append(file)
    return docs_py


def load_on_disk():
    list_png = get_list_png()
    for i in list_png:
        yan.upload_file(f'{yan.my_dir}/{i}', i)

# res = get_data(my_id)
# get_photo(res)


yan = YaUpLoader(token_ya)
yan.create_dir_vk()
load_on_disk()
