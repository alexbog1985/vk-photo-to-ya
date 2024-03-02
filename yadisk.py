import secret
import requests

YA_TOKEN = secret.YA_TOKEN

YA_DISK_URL = "https://cloud-api.yandex.net/v1/disk/"


class YaDiskAPI:
    def __init__(self, token=YA_TOKEN, url=YA_DISK_URL):
        self.token = token
        self.url = url

    def get_common_headers(self):
        return {
            "Authorization": "OAuth " + self.token,
            "Content-Type": "application/json"
        }

    def get_disk_info(self):
        headers = self.get_common_headers()
        response = requests.get(self.url, headers=headers)
        print(response.text)

    def add_dir(self, path):
        headers = self.get_common_headers()
        params = {
            'path': path,
        }
        response = requests.put(self.url + "resources", headers=headers, params=params)
        return {
            "statuscode": response.status_code
        }

    def save_images(self, path, file_name, content):
        self.add_dir(path)
        headers = self.get_common_headers()
        params = {
            'path': f'{path}/{file_name}',
            'overwrite': 'true'
        }
        response = requests.get(self.url + "resources/upload", headers=headers, params=params)
        current_url_upload = response.json().get('href')
        response = requests.put(current_url_upload, files={"file": content})
        return response.status_code


if __name__ == "__main__":
    ya = YaDiskAPI()
