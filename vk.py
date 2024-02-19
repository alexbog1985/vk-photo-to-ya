import secret
import requests

VK_TOKEN = secret.VK_TOKEN


class VKAPIClient:
    API_BASE_URL = 'https://api.vk.com/method'

    def __init__(self, user_id, token=VK_TOKEN):
        self.user_int_id = None
        self.user_name = None
        self.user_id = user_id
        self.token = token

        self.get_user()

    def _get_common_params(self):
        return {
            'access_token': self.token,
            'v': 5.131
        }

    def _build_url(self, api_method):
        return f'{self.API_BASE_URL}/{api_method}'

    def _check_error(self, response):
        if 200 <= response.status_code < 300:
            if response.json().get('response'):
                return response.json()['response']
            elif response.json().get('error'):
                error_dict = response.json()['error']
                error_code = error_dict.get('error_code')
                error_msg = error_dict.get('error_msg')
                print(f'Ошибка №{error_code} - {error_msg}')
            else:
                return response.json()
        else:
            print("Ошибка соединения с сервером:", response.status_code)

    def get_user(self):
        params = self._get_common_params()
        params.update({'user_id': self.user_id})
        response = requests.get(self._build_url('users.get'), params=params)
        if self._check_error(response):
            result = self._check_error(response)
            self.user_int_id = result[0]['id']
            self.user_name = result[0]['first_name'] + ' ' + result[0]['last_name']

    def get_photo_albums(self):
        params = self._get_common_params()
        params.update({
            'owner_id': self.user_int_id,
        })
        response = requests.get(self._build_url('photos.getAlbums'), params=params)
        if self._check_error(response):
            albums = [{'id': 'profile', 'title': 'Фотографии профиля'},
                      {'id': 'wall', 'title': 'Фотографии со стены'},
                      {'id': 'saved', 'title': 'Сохраненные фотографии'},
                      ] + ([item for item in self._check_error(response)['items']])
            result = []
            for num, album in enumerate(albums):
                result.append([num, {album['id']: album['title']}])
            print(result)
            return result


if __name__ == '__main__':
    vk = VKAPIClient('60453017')
    print(
        vk.user_name,
        vk.user_int_id,
        vk.get_photo_albums()
    )
