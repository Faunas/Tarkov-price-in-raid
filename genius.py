import pyautogui
import cv2
import pytesseract
import keyboard
import numpy as np
from api_requst import run_query
from gtts import gTTS
import os
import pygame

# Укажите путь к исполняемому файлу Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Ожидаемое нажатие клавиши
target_key = 'insert'

# Желаемое смещение для определения прямоугольной области
offset_x = 50
offset_y = 100
width = 500  # Ширина прямоугольной области
height = 50  # Высота прямоугольной области
# Ожидаем нажатие клавиши target_key
while True:
    print(f"Ожидание нажатия клавиши {target_key}...")
    keyboard.wait(target_key)

    # Загрузка скриншота
    screenshot = pyautogui.screenshot()
    screenshot_np = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # Загрузка иконки лупы для поиска
    icon_template = cv2.imread('magnifying_glass.png', cv2.IMREAD_COLOR)

    # Поиск иконки лупы в скриншоте
    result = cv2.matchTemplate(screenshot_np, icon_template, cv2.TM_CCOEFF_NORMED)

    # Поиск координат лучшего совпадения
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # Создание координат прямоугольной области для распознавания текста
    x, y = max_loc
    rect_top_left = (x, y)
    rect_bottom_left = (x, y + height)
    rect_top_right = (x + width, y)
    rect_bottom_right = (x + width, y + height)

    # Выводим результат
    print(f"Иконка лупы найдена в координатах {max_loc}")
    pyautogui.click(max_loc)

    # Создание подизображения из оригинального изображения
    screenshot_roi = screenshot.crop((rect_top_left[0]+20, rect_top_left[1], rect_bottom_right[0]-100, rect_bottom_right[1]-15))
    screenshot_roi_np = cv2.cvtColor(np.array(screenshot_roi), cv2.COLOR_RGB2BGR)

    # Преобразуем изображение в текст с использованием Tesseract OCR
    scanned_text = pytesseract.image_to_string(screenshot_roi_np, config='--psm 6 --oem 3 -l eng')
    scanned_text = scanned_text.replace('\n', '')


    # Ваш запрос GraphQL с использованием форматированной строки
    new_query = """
    {{
        items(name: "{}") {{
            id
            shortName
            sellFor {{
                price
                source
            }}
        }}
    }}
    """.format(scanned_text)

    result = run_query(new_query)
    print("Распознанный текст:", scanned_text, "\n")

    if result:
        # Получаем список цен
        try:
            sell_for_list = result['data']['items'][0]['sellFor']

            # Исключаем 'fleaMarket'
            filtered_sell_for_list = [entry for entry in sell_for_list if entry['source'] != 'fleaMarket']
        except Exception:
            print("Не найдено")
            text_to_speak = "Не найдено"
            language = 'ru'

            # Создание объекта gTTS
            tts = gTTS(text=text_to_speak, lang=language, slow=False)

            # Сохранение аудиофайла
            audio_file_path = 'output.mp3'
            tts.save(audio_file_path)

            # Инициализация pygame
            pygame.mixer.init()

            # Загрузка звукового файла
            sound = pygame.mixer.Sound(audio_file_path)

            # Воспроизведение аудиофайла
            sound.play()

            # Ждем, пока проигрывание не завершится
            pygame.time.wait(int(sound.get_length() * 1000))  # Преобразуем секунды в миллисекунды

            # Удаляем временный аудиофайл
            os.remove(audio_file_path)
            continue

        # Если после фильтрации остались элементы, находим максимальное значение
        if filtered_sell_for_list:
            max_price_entry = max(filtered_sell_for_list, key=lambda x: x['price'])
            print("-------- Максимальная цена:", max_price_entry['price'], " --------\n")
            print("Торговец:", max_price_entry['source'])
            text_to_speak = "{} рублей.".format(max_price_entry['price'])
            language = 'ru'

            # Создание объекта gTTS
            tts = gTTS(text=text_to_speak, lang=language, slow=False)

            # Сохранение аудиофайла
            audio_file_path = 'output.mp3'
            tts.save(audio_file_path)

            # Инициализация pygame
            pygame.mixer.init()

            # Загрузка звукового файла
            sound = pygame.mixer.Sound(audio_file_path)

            # Воспроизведение аудиофайла
            sound.play()

            # Ждем, пока проигрывание не завершится
            pygame.time.wait(int(sound.get_length() * 1000))  # Преобразуем секунды в миллисекунды

            # Удаляем временный аудиофайл
            os.remove(audio_file_path)
        else:
            print("Все цены от 'fleaMarket', нет данных для сравнения.")
    else:
        print("Ошибка выполнения запроса GraphQL.")