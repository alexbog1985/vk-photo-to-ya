from vk import VKAPIClient
from secret import VK_TOKEN


def start_program():
    print('Программа загружает фотографии VK пользователя из выбранного альбома и сохраняет на Я.Диске.')
    user_id = input('Введите VK ID пользователя: ')
    vk_user = VKAPIClient(user_id=user_id, token=VK_TOKEN)
    if vk_user.user_int_id:
        print(f'Найден пользователь: {vk_user.user_name}\n')
        print('Вы хотите посмотреть список альбомов пользователя?')
        ask = input('Введите "Да" или "Нет": ')
        print()
        if ask.lower() == 'да':
            show_albums(vk_user)


def show_albums(vk_user):
    for album in vk_user.get_photo_albums():
        print(f'{album[0]} - "{''.join(album[1].values())}"')


if __name__ == '__main__':
    start_program()
