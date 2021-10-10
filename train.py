import requests
import json
import ya
from pprint import pprint


my_id = '22708602'

with open('toc_vk.txt') as f:
    token = f.read().strip()
URL = 'https://api.vk.com/method/'


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
        likes = str(photo['likes']['count'])
        if likes == quantity_likes:
            likes = f'{likes}({str(count)})'
            count += 1
        word = count_likes(likes)
        with open(likes + f' {word}.png', 'wb') as f:
            f.write(download_image.content)
        max_size = 0


def write_data(result):
    get_data(my_id)
    with open('vk_info.txt', 'a') as f:
        json.dump(result, f)
        json.dump('\n', f)


res = get_data(my_id)
get_photo(res)
write_data(res)








# URL = 'https://api.vk.com/method/users.get'
# params = {
#     'user_ids': '1',
#     'access_token': token,
#     'v': '5.131',
#     'fields': 'photo_max, education, sex'
# }
#
# result = requests.get(url=URL, params=params)
# pprint(result.json())
# spam = result.json()['response'][0]['photo_max']
# s = requests.get(url=spam)
# with open('new.png', 'wb') as f:
#     f.write(s.content)

# url_search = 'https://api.vk.com/method/groups.get'
# params = {
#     'user_id': 1,
#     'extended': 1,
#     'access_token': token,
#     'v': '5.131',
#     'count': '1000',
#     'field': 'members_count'
# }
# res = requests.get(url=url_search, params=params).json()
# pprint(res)

