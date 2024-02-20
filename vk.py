import secret
import requests
import datetime

VK_TOKEN = secret.VK_TOKEN


class VKAPIClient:
    API_BASE_URL = 'https://api.vk.com/method'

    def __init__(self, user_id=None, token=VK_TOKEN):
        self.albums = None
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

    def get_user(self):
        params = self._get_common_params()
        params.update({'user_id': self.user_id})
        response = requests.get(self._build_url('users.get'), params=params)
        if _check_error(response):
            result = _check_error(response)
            if result:
                self.user_int_id = result[0]['id']
                self.user_name = result[0]['first_name'] + ' ' + result[0]['last_name']
        else:
            print(f'Пользователь с ID: "{self.user_id}" не найден')

    def get_photo_albums(self):
        print('Получаем список фотоальбомов пользователя')
        params = self._get_common_params()
        params.update({
            'owner_id': self.user_int_id,
        })
        response = requests.get(self._build_url('photos.getAlbums'), params=params)
        result = []
        if 'error' not in _check_error(response).keys():
            print('Вам доступны альбомы:')
            albums = [
                         {'id': 'profile', 'title': 'Фотографии профиля'},
                         {'id': 'wall', 'title': 'Фотографии со стены'},
                         {'id': 'saved', 'title': 'Сохраненные фотографии'},
                     ] + [item for item in _check_error(response)['items']]
            for num, album in enumerate(albums):
                result.append([num, {album['id']: album['title']}])
            self.albums = result
        else:
            print('Вам доступны альбомы: ')
            result = [[
                0,
                {'profile': 'Фотографии профиля'}
            ]]
            self.albums = result
        return result

    def get_photos(self, album_id=0):
        print('Получаем список фотографий альбома пользователя:')
        params = self._get_common_params()
        params.update({
            'owner_id': self.user_int_id,
            'extended': 1,
        })
        if list is type(self.albums):
            params.update({'album_id': ''.join([str(key) for key in self.albums[album_id][1].keys()])})
            album_title = ''.join([str(value) for value in self.albums[album_id][1].values()])
        else:
            params.update({'album_id': 'profile'})
            album_title = 'Фотографии профиля'
        response = requests.get(self._build_url('photos.get'), params=params)
        if self.user_name and _check_error(response):
            photos = []
            for photo in _check_error(response).get('items'):
                photos.append({
                    'likes': photo['likes']['count'],
                    'create_date': datetime.datetime.fromtimestamp(photo['date']).strftime('%d-%m-%Y'),
                    'url': photo['sizes'][-1]['url'],
                    'size': photo['sizes'][-1]['type']
                })
            print(f'В альбоме "{album_title}" найдено {len(photos)} фотографий')
            return photos


def _check_error(response):
    if 200 <= response.status_code < 300:
        if response.json().get('response'):
            return response.json()['response']
        elif response.json().get('error'):
            error_dict = response.json()['error']
            error_code = error_dict.get('error_code')
            error_msg = error_dict.get('error_msg')
            print(f'Ошибка №{error_code} - {error_msg}')
            return {'error': error_code}
    else:
        print("Ошибка соединения с сервером:", response.status_code)


if __name__ == '__main__':
    vk = VKAPIClient(
          # '60453017'
    )
    vk.get_photo_albums()
    print(
        vk.user_name, '\n',
        vk.user_int_id, '\n',
        # vk.albums, '\n',
        vk.get_photos()
    )
