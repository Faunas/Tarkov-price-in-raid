import pyautogui
import cv2
import pytesseract
import keyboard
import numpy as np
from pydub import AudioSegment

from api_requst import run_query
from gtts import gTTS
import os
import pygame
import Levenshtein
import json
import pywintypes
import tkinter as Tkinter
import win32api
import win32con
import threading

def get_mouse_position():
    x, y = win32api.GetCursorPos()
    return x, y

def play_voice_with_price(price_text):
    text_to_speak = "{} рублей.".format(price_text)
    language = 'ru'
    tts = gTTS(text=text_to_speak, lang=language, slow=False)
    audio_file_path = 'output.mp3'
    tts.save(audio_file_path)
    sound = AudioSegment.from_mp3(audio_file_path)
    speedup_sound = sound.speedup(playback_speed=1.4)

    # Сохраняем измененный звук в тот же файл
    speedup_sound.export(audio_file_path, format="mp3")
    pygame.mixer.init()
    sound = pygame.mixer.Sound(audio_file_path)
    sound.play()
    pygame.time.wait(int(sound.get_length() * 1000))  # Преобразуем секунды в миллисекунды

    # Удаляем временный аудиофайл
    os.remove(audio_file_path)

def show_price_label(price, trader_name, duration=3000):
    x, y = get_mouse_position()
    label = Tkinter.Label(text=f'{price} ₽\n{trader_name}', font=('Times New Roman', '26'), fg='yellow', bg='white')
    label.master.overrideredirect(True)
    label.master.geometry(f"+{x}+{y+50}")
    label.master.lift()
    label.master.wm_attributes("-topmost", True)
    label.master.wm_attributes("-disabled", True)
    label.master.wm_attributes("-transparentcolor", "white")

    hWindow = pywintypes.HANDLE(int(label.master.frame(), 16))

    exStyle = (win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE |
               win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT)
    win32api.SetWindowLong(hWindow, win32con.GWL_EXSTYLE, exStyle)

    label.pack()

    label.after(duration, label.master.destroy)  # Закрываем окно через duration миллисекунд

    label.mainloop()

def find_most_similar(json_data, search_text):
    min_distance = float('inf')
    most_similar_value = None

    for key, value in json_data.items():
        if "Name" in key:
            distance = Levenshtein.distance(search_text.lower(), value.lower())
            if distance < min_distance:
                min_distance = distance
                most_similar_value = {"id": key.split()[0], "value": value, "distance": distance}

    return most_similar_value


def main():
    offset_x = 50
    offset_y = 100
    width = 500  # Ширина прямоугольной области
    height = 50  # Высота прямоугольной области

    with open('en.json', 'r', encoding='utf-8') as file:
        json_data_eng = json.load(file)

    with open('ru.json', 'r', encoding='utf-8') as file:
        json_data_ru = json.load(file)

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
        # print(f"Иконка лупы найдена в координатах {max_loc}")
        pyautogui.click(max_loc)

        # Создание подизображения из оригинального изображения
        screenshot_roi = screenshot.crop(
            (rect_top_left[0] + 20, rect_top_left[1], rect_bottom_right[0] - 100, rect_bottom_right[1] - 15))
        screenshot_roi_np = cv2.cvtColor(np.array(screenshot_roi), cv2.COLOR_RGB2BGR)

        # Преобразуем изображение в текст с использованием Tesseract OCR
        scanned_text = pytesseract.image_to_string(screenshot_roi_np, config='--psm 6 --oem 3 -l rus+eng')
        scanned_text = scanned_text.replace('\n', '')
        result_ru = find_most_similar(json_data_ru, scanned_text)
        # print(result_ru)
        if result_ru is not None:
            id_to_search = result_ru['id']
            english_name = json_data_eng.get(f"{id_to_search} Name", "Not Found")
            # print(
            #     f"ID: {id_to_search}\nRussian Name: {result_ru['value']}\nEnglish Name: {english_name}, Distance: {result_ru['distance']}")
            new_query = """
                    {{
                        items(name: "{}") {{
                            id
                            name
                            sellFor {{
                                price
                                source
                            }}
                        }}
                    }}
                    """.format(english_name.replace('"', r'\"'))
            result_query = run_query(new_query)
            # print("Распознанный текст:", scanned_text, "\n")
            # print("Ответ от API:", result_query, "\n")

            if result_query:
                # Получаем список цен
                try:
                    sell_for_list = result_query['data']['items'][0]['sellFor']
                    item_name_eng = result_query['data']['items'][0]['name']
                    item_name_rus = result_ru['value']


                    # Исключаем 'Барахолку'
                    if game_lvl < 15:
                        filtered_sell_for_list = [entry for entry in sell_for_list if entry['source'] != 'fleaMarket']
                    else:
                        filtered_sell_for_list = [entry for entry in sell_for_list if entry['source'] != 'f']
                except Exception:
                    show_price_label(price="Нет инфы", trader_name=" ", duration=1000)
                    print("Не найдено")
                    continue

                # Если после фильтрации остались элементы, находим максимальное значение
                if game_lvl < 15:
                    max_price_entry = max(filtered_sell_for_list, key=lambda x: x['price'])
                    print("\n------------------------------------------------------\n-------- Наименование:", item_name_rus, "\n-------- Максимальная цена:", max_price_entry['price'])
                    trader_name = max_price_entry['source']
                    trader_name = trader_name.replace("therapist", "Терапевт").replace("fleaMarket", "Барахолка").replace("mechanic", "Механик").replace("prapor", "Прапор").replace("jaeger", "Егерь")
                    print("-------- Торговец:", trader_name,"\n------------------------------------------------------")

                    # Вызываем функцию show_price_label в отдельном потоке
                    thread = threading.Thread(target=show_price_label, args=(max_price_entry['price'], trader_name, 2000))
                    thread.start()

                    # Вызываем функцию play_voice_with_price в основном потоке
                    play_voice_with_price(price_text=max_price_entry['price'])
                elif game_lvl >= 15:
                    max_price_entry = max(filtered_sell_for_list, key=lambda x: x['price'])
                    print("\n------------------------------------------------------\n-------- Наименование:", item_name_rus,
                          "\n-------- Максимальная цена:", max_price_entry['price'])
                    trader_name = max_price_entry['source']
                    trader_name = trader_name.replace("therapist", "Терапевт").replace("fleaMarket", "Барахолка").replace("mechanic", "Механик").replace("prapor", "Прапор").replace("jaeger", "Егерь")
                    print("-------- Торговец:", trader_name, "\n------------------------------------------------------")
                    show_price_label(price=max_price_entry['price'],trader_name=trader_name, duration=2000)
                    play_voice_with_price(price_text=max_price_entry['price'])
                else:
                    print("Все цены от 'fleaMarket', нет данных для сравнения.")
            else:
                print("Ошибка выполнения запроса GraphQL.")

if __name__ == '__main__':
    game_lvl = 14
    interface_language = "rus"
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    target_key = 'insert'
    main()