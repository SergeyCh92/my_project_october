import requests
from pprint import pprint

# with open('toc_ya.txt') as f:
#     token_ya = f.read().strip()


class YaUpLoader:
    def __init__(self, token):
        self.token = token
        self.my_dir = 'Файлы Вк'

    def get_headers(self):
        return {'Content-Type': 'application/json', 'Authorization': f'OAuth {self.token}'}

    def request(self):
        url = 'https://cloud-api.yandex.net/v1/disk/resources/files'
        headers = self.get_headers()
        response = requests.get(url=url, headers=headers)
        return response.json()

    def _get_upload_link(self, disk_path):
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        params = {'path': disk_path, 'overwrite': 'true'}
        headers = self.get_headers()
        response = requests.get(url=url, params=params, headers=headers, timeout=5)
        # pprint(response.json())
        return response.json()

    def upload_file(self, disk_path, filename):
        href = self._get_upload_link(disk_path=disk_path).get('href', '')
        response = requests.put(href, data=open(filename, 'rb'))
        response.raise_for_status()
        # if response.status_code == 201:
        #     print(f'Файл {filename} успешно загружен!')

    def create_dir_vk(self):
        count = 1
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers()
        while True:
            params = {'path': self.my_dir}
            r = requests.put(url=url, params=params, headers=headers)
            # r.raise_for_status()
            if r.status_code == 409:
                self.my_dir = f'Файлы Вк{count}'
                count += 1
            else:
                break
