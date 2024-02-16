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

    def get_user(self):
        params = self._get_common_params()
        params.update({'user_id': self.user_id})
        response = requests.get(self._build_url('users.get'), params=params)
        if 200 <= response.status_code < 300:
            if response.json().get('response'):
                result = response.json()['response'][0]
                self.user_int_id = result['id']
                self.user_name = result['first_name'] + ' ' + result['last_name']
                return
            elif response.json().get('error'):
                error_dict = response.json()['error']
                error_code = error_dict.get('error_code')
                error_msg = error_dict.get('error_msg')
                print(f'Ошибка: №{error_code} - {error_msg}')
            else:
                return print(f'Пользователя с id: {self.user_id} не существует')

        else:
            return print("Ошибка соединения с сервером:", response.status_code)


if __name__ == '__main__':
    vk = VKAPIClient('60453017')
    print(
        vk.user_name,
        vk.user_int_id,
    )
