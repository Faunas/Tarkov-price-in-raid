import random
import time
import cv2
import pyautogui
import pytesseract
import numpy as np
from PIL import Image
import json


def load_russian_words_from_json(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
        words = [entry['word'] for entry in data]
    return words


def get_possible_words(letters, word_list):
    letter_count = {}
    for char in letters:
        letter_count[char] = letter_count.get(char, 0) + 1

    possible_words = []

    for word in word_list:
        if 5 <= len(word) <= 8:  # Filter words based on length
            word_count = {}
            for char in word:
                word_count[char] = word_count.get(char, 0) + 1

            if all(letter_count.get(char, 0) >= count for char, count in word_count.items()):
                possible_words.append(word)

    return possible_words


def is_russian_letter(letter):
    return 'А' <= letter <= 'Я' or 'а' <= letter <= 'я'


def find_letter_positions(image, letters, rect_top_left, rect_bottom_right):
    letter_positions = {}

    # Capture the entire screen to determine offset
    full_screenshot = pyautogui.screenshot()
    full_screenshot_np = np.array(full_screenshot)

    # Calculate offset between cropped screenshot and full screen
    offset_x = rect_top_left[0]
    offset_y = rect_top_left[1]

    # Use pytesseract to find character bounding boxes
    boxes = pytesseract.image_to_boxes(image, lang='rus')

    # Track letters we've already found
    found_letters = set()

    for box in boxes.splitlines():
        b = box.split()
        letter = b[0]
        x_crop, y_crop = int(b[1]), int(b[2])

        # Convert cropped coordinates to full screen coordinates
        x_full = x_crop + offset_x
        y_full = y_crop + offset_y

        # Debugging: print bounding box details
        print(f"Letter: {letter}, Position (full screen): ({x_full}, {y_full})")

        # Perform a click for debugging purposes
        # pyautogui.click(x_full, y_full)
        # time.sleep(0.3)

        # Check if the letter is a Russian letter and not already found
        if is_russian_letter(letter) and letter.upper() not in found_letters:
            if letter.upper() not in letter_positions:
                letter_positions[letter.upper()] = []
            letter_positions[letter.upper()].append((x_full, y_full))
            found_letters.add(letter.upper())
        else:
            print(f"Ignoring non-Russian letter or already found letter: '{letter}'")

    # Debugging: print letter_positions after processing
    print("Letter positions:", letter_positions)

    return letter_positions


def click_letters(letter_positions, word):
    print("я тут")
    for letter in word:
        print(f"Обрабатываю букву: '{str(letter)}' в слове {word}")
        if letter.upper() in letter_positions:  # Сравниваем с оригинальными заглавными буквами
            print("я тут2")
            for position in letter_positions[letter]:
                # Perform a click at the position (adjust the duration and tween here as needed)
                pyautogui.click(position[0], position[1], duration=0.25, tween=pyautogui.easeInOutQuad)


def main():
    n = 5000  # Number of words to output

    # Load Russian words from the JSON file
    json_file = 'words-russian-nouns.json'
    russian_words = load_russian_words_from_json(json_file)

    # Capture a screenshot
    screenshot = pyautogui.screenshot()

    # Coordinates of the rectangular area
    rect_top_left = (720, 509)
    rect_bottom_right = (1200, 888)

    # Crop the screenshot to the specified rectangular area
    screenshot_roi = screenshot.crop(
        (rect_top_left[0], rect_top_left[1], rect_bottom_right[0], rect_bottom_right[1])
    )
    screenshot_roi_np = np.array(screenshot_roi)

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(screenshot_roi_np, cv2.COLOR_BGR2GRAY)

    # Apply binary thresholding
    _, bw_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Save the black-and-white image
    bw_image_path = 'bw_image.png'
    cv2.imwrite(bw_image_path, bw_image)

    # Convert the black-and-white image to text using Tesseract OCR
    scanned_text = pytesseract.image_to_string(bw_image, config='--psm 6 --oem 3 -l rus')
    scanned_text = scanned_text.replace('\n', '').replace(' ', '')

    # Output the detected text
    print("Detected text: ", scanned_text.lower())

    # Extract letters
    letters = scanned_text.lower()

    # Find possible words from the loaded Russian words list
    possible_words = get_possible_words(letters, russian_words)

    # Filter to limit to n words with no more than 5 words starting with the same letter
    filtered_words = []
    letter_count = {}

    for word in possible_words:
        initial_letter = word[0]
        letter_count[initial_letter] = letter_count.get(initial_letter, 0) + 1
        if letter_count[initial_letter] <= 15:
            filtered_words.append(word)
            if len(filtered_words) == n:
                break

    # Output the filtered words
    for word in filtered_words:
        print(word)

    # Find positions of each letter in the detected text
    letter_positions = find_letter_positions(bw_image, letters, rect_top_left, rect_bottom_right)
    print(len(letter_positions))
    print("-----------")
    # # Click on each letter of the word "обелиск" in order
    word_to_click = str(random.choice(possible_words)).upper()
    click_letters(letter_positions, word_to_click)

    # Display the saved black-and-white image
    saved_image = Image.open(bw_image_path)
    # saved_image.show()


if __name__ == '__main__':
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    main()
