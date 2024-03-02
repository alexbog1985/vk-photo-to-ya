import json
import os
from vk import VKAPIClient
from yadisk import YaDiskAPI
from secret import VK_TOKEN
from log import error_log, info_log


def main():
    print('Программа загружает фотографии VK пользователя из выбранного альбома и сохраняет на Я.Диске.')
    ya_token = input('Введите Я.Токен с "Яндекс Полигона"')
    user_id = input('Введите VK ID пользователя: ')
    vk_user = VKAPIClient(user_id=user_id, token=VK_TOKEN)
    ya_disk = YaDiskAPI(token=ya_token)
    if vk_user.user_int_id:
        print(f'Найден пользователь: {vk_user.user_name}\n')
        print('Список альбомов пользователя:')
        show_albums(vk_user)
        album_id = input('Чтобы выбрать альбом, введите номер альбома: ')
        if album_id.isdigit():
            get_user_photos(vk_user, album_id=int(album_id))
        else:
            print('Вы ввели неверный номер альбома.')
        vk_user.download_photo()
        save_photos(vk_user, ya_disk)


def show_albums(vk_user):
    vk_user.get_photo_albums()
    for album in vk_user.albums:
        print(f'{album[0]} - "{''.join(album[1].values())}"')


def get_user_photos(vk_user, album_id):
    count = input('Введите количество фотографий: ')
    if count.isdigit() and int(count) > 0:
        photos = vk_user.get_photos(album_id=album_id, count=int(count))
        return photos
    else:
        print('Введено неверное количество фотографий')
        get_user_photos(vk_user, album_id)


def save_photos(vk_user, ya_disk):
    path = input('Введите название папки на Я.Диске для сохранения фотографий: ')
    ya_disk.add_dir(path)
    if not os.path.isdir(f'{os.getcwd()}{os.sep}files_info'):
        os.mkdir(f'{os.getcwd()}{os.sep}files_info')
    info_ = []
    for photo in vk_user.photos:
        status_code = ya_disk.save_images(path, photo['file_name'], photo['content'])
        if status_code == 201:
            print(f'Фотография {photo['file_name']} загружена в папку {path}')
            info_log(f'Фотография {photo['file_name']} загружена в папку {path}')
            info_.append({'file_name': photo['file_name'], 'size': photo['size'], 'path': path})
        else:
            print('Что-то пошло не так...')
            print(status_code)
            error_log(f'Ошибка: {status_code}')
    with open(f"{os.getcwd()}{os.sep}files_info{os.sep}info.json", 'w') as f:
        json.dump(info_, f)


if __name__ == '__main__':
    main()
