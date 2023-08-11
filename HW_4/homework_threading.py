'''
Написать программу, которая скачивает изображения с заданных URL-адресов и сохраняет их на диск. 
Каждое изображение должно сохраняться в отдельном файле, название которого соответствует 
названию изображения в URL-адресе.
Например, URL-адрес: https://example/images/image1.jpg -> файл на диске: image1.jpg
— Программа должна использовать многопоточный, многопроцессорный и асинхронный подходы.
— Программа должна иметь возможность задавать список URL-адресов через аргументы командной строки.
— Программа должна выводить в консоль информацию о времени скачивания каждого изображения и общем 
времени выполнения программы.
'''

import sys
import requests
import time
import threading

urls = ['https://funart.pro/uploads/posts/2019-11/1572808974_jelloustoun-nacionalnyj-park-ssha-34.jpg',
        'https://uniticket.ru/wp-content/uploads/2021/12/Park-Yellouston7.jpg',
        'https://funart.pro/uploads/posts/2019-11/1572809040_jelloustoun-nacionalnyj-park-ssha-54.jpg',
        'https://i2.wp.com/rvplacestogo.com/wp-content/uploads/2017/04/firelake-drive-lower-geyser.jpg',
        'https://vsegda-pomnim.com/uploads/posts/2022-05/1651426140_84-vsegda-pomnim-com-p-yelloustoun-vulkan-foto-95.jpg',
        ]


def download(url):
    '''Многопоточное скачивание изображений'''
    response = requests.get(url).content
    # content = response.read()
    filename = url.rsplit('/', 1)[-1]
    with open(filename, 'wb') as f:
        f.write(response)
        print(
            f"Downloaded {filename} in {time.time() - start_time:.2f} seconds")


threads = []
start_time = time.time()

if __name__ == '__main__':
    if len(sys.argv) > 5:   # Если в командную строку передан аргумент url-адреса
        urls = [sys.argv[-1]]
    for url in urls:
        start_time = time.time()
        thread = threading.Thread(target=download, args=[url])
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    print(f"Everithing downloaded for {time.time() - start_time:.2f} seconds")
