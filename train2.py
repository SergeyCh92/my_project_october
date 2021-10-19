import requests
import json
from ya import YaUpLoader
import os
import time
from tqdm import tqdm
import datetime

# my_id = ''
#
# with open('toc_vk.txt') as f:
#     token = f.read().strip()
URL = 'https://api.vk.com/method/'
#
# with open('toc_ya.txt') as f:
#     token_ya = f.read().strip()


class Vk:
    """Класс создан для взаимодействия с ВК, в качестве атрибута принимает токен для вк."""

    def __init__(self, token):
        self.token = token
        self.URL = 'https://api.vk.com/method/'
        self.list_sizes = []
        self.list_photo_info = []

    def get_data(self, id):
        """Функция возвращает в словарь с информацией о фотографиях в пользовательском профиле, в качестве аргумента
        принимает id пользователя ВК."""
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

    def _count_likes(self, likes):
        """Функция вернет синтаксически верное склонение слова 'лайк', в зависимости от того, какое целочисленное
        значение имеет аргумент likes"""
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

    def check_error(self, result):
        """Функция вернет True и выведет в консоль уведомление об ошибке, если при выгрузке массива с данными о фото
        возникли проблемы."""
        if 'error' in result:
            if result['error']['error_code'] == 30:
                print('Данный профиль является приватным. У Вас нет разрешения на просмотр и скачивание фотографий.')
                print()
                return True
            elif result['error']['error_code'] == 15:
                print('Страница данного пользователя удалена или еще не создана.')
                print()
                return True
        else:
            return False

    def get_photo(self, result, quantity_photo=5):
        """В процесе доработки: планируется декомпозиция данной функции.Функция сохраняет фотографии наилучшего качества
        на ПК, пишет информацию о них в json-файл, и отбирает фото самого высокого качества для последующей загрузки на
        яндекс-диск."""
        max_size = 0
        quantity_likes = []
        dict_photo = {}

        for num, photo in enumerate(tqdm(result['response']['items'], desc='Загрузка файлов на ПК'), start=1):
            element = ''
            if photo['sizes'][0]['height'] == 0:
                continue
            for i in photo['sizes']:
                if int(i['height']) + int(i['width']) > max_size:
                    max_size = int(i['height']) + int(i['width'])
                    download_image = requests.get(url=i['url'])
                    type_photo = i['type']
            likes = str(photo['likes']['count'])
            date = datetime.datetime.utcfromtimestamp(photo['date']).strftime('%Y-%m-%d')
            word = self._count_likes(likes)
            if int(likes) in quantity_likes:
                element = f' {date}'
            with open(likes + f' {word}{element}.png', 'wb') as file:
                file.write(download_image.content)
            photo_info = {'file_name': f'{likes} {word}{element}.png', 'size': type_photo}
            self.list_photo_info.append(photo_info)
            if num == len(result['response']['items']):
                with open('vk_info.json', 'a', encoding='utf-8') as f:
                    json.dump(self.list_photo_info, f, ensure_ascii=False, indent=4)
                    # json.dump('\n', f)
            dict_photo[f'{likes} {word}{element}.png'] = max_size
            max_size = 0
            quantity_likes.append(int(likes))

        for name, size in dict_photo.items():
            self.list_sizes.append([name, size])
        self.list_sizes.sort(key=lambda el: el[1], reverse=True)
        self.list_sizes = self.list_sizes[:quantity_photo]

    def _get_list_png(self):
        """Возвращает список имен файлов фотографий наилучшего качества в директории по умолчанию."""
        final_list = []
        # data = os.getcwd()
        # docs = os.listdir(data)
        # docs_py = []
        #
        # for file in docs:
        #     if file[-4:] == '.png':
        #         docs_py.append(file)
        # return docs_py

        for name, size in self.list_sizes:
            final_list.append(name)
        return final_list

    def load_on_disk(self):
        """Загружает фотографии на яндекс-диск."""
        list_png = self._get_list_png()
        for i in tqdm(list_png, desc='Загрузка файлов на яндекс диск'):
            yan.upload_file(f'{yan.my_dir}/{i}', i)

    def clear_dir(self):
        """Удаляет в директории по умолчанию все ранее скачанные файлы."""
        data = os.getcwd()
        docs = os.listdir(data)
        docs_py = []

        for file in docs:
            if file[-4:] == '.png':
                docs_py.append(file)

        for i in tqdm(docs_py, desc='Удаление загруженных файлов с ПК'):
            os.remove(f'{data}/{i}')
            time.sleep(0.2)


if __name__ == '__main__':
    token_ya = input('Введите токен для яндекс-диска:\n')
    token = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
    while True:
        my_id = input('Введите id vk:\n')
        user = Vk(token)
        res = user.get_data(my_id)
        if user.check_error(res):
            continue
        user.get_photo(res)
        yan = YaUpLoader(token_ya)
        yan.create_dir_vk()
        user.load_on_disk()
        user.clear_dir()
        time.sleep(0.2)
        print()
        final = input('Хотите продолжить? (да/нет)\n')
        if final.lower().startswith('н'):
            break
