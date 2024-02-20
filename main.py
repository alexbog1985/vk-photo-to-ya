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
        if ask.lower() == 'да' or ask is not None:
            print(show_albums(vk_user))
        album_id = input('Чтобы выбрать альбом, введите номер альбома: ')
        if album_id.isdigit():
            photos = get_user_photos(vk_user, album_id=int(album_id))
            print(photos)
        else:
            print('Вы ввели неверный номер альбома.')
            show_albums(vk_user)


def show_albums(vk_user):
    print(vk_user.get_photo_albums())
    for album in vk_user.get_photo_albums():
        print(f'{album[0]} - "{''.join(album[1].values())}"')


def get_user_photos(vk_user, album_id):
    count = input('Введите количество фотографий: ')
    if count.isdigit() and int(count) > 0:
        return vk_user.get_photos(album_id=album_id, count=int(count))
    else:
        print('Введено неверное количество фотографий')
        return get_user_photos(vk_user, album_id)


if __name__ == '__main__':
    start_program()
