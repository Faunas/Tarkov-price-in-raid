<div align="center">

# Tarkov-price-in-raid

![GitHub](https://img.shields.io/github/license/Faunas/Tarkov-price-in-raid)
![GitHub last commit](https://img.shields.io/github/last-commit/Faunas/Tarkov-price-in-raid)

</div>

## Обзор

Tarkov-price-in-raid - простой и эффективный инструмент, созданный для игроков Escape from Tarkov. Предоставляет автоматизированный поиск и информацию о ценах на предметы у торговцев в режиме реального времени без влияния на производительность. На текущем этапе не отображает цены на Барахолке, сосредотачивая внимание только на торговцах. Инструмент работает исключительно в полноэкранном режиме с разрешением экрана 1920x1080 и с интерфейсом на английском языке.

## Основные функции

**Автоматизированный поиск товаров:** Проект использует оптическое распознавание символов (OCR) для извлечения информации об игровых предметах, фокусируясь на прямоугольной области экрана.

**Звуковые уведомления:** После распознавания информации о предмете инструмент предоставляет звуковые уведомления с максимальной ценой продажи товара и указывает торговца, предлагающего максимальную выгоду.

**Голосовой ответ при отсутствии данных:** Если инструмент не может распознать информацию о предмете или если все цены связаны с Барахолкой, он предоставляет голосовой ответ о том, что данные отсутствуют.

## Требования

- Разрешение экрана: 1920x1080 (полноэкранный режим)
- Язык интерфейса: Английский

## Инструкции по установке и использованию

1. Установите последнюю версию [Tesseract OCR](https://github.com/tesseract-ocr/tesseract/releases/).
2. Установите необходимые зависимости, перечисленные в файле `requirements.txt`.
3. Укажите путь к исполняемому файлу Tesseract OCR в переменной `pytesseract.tesseract_cmd` (строка 11).
4. Запустите проект и используйте клавишу "insert" для активации поиска информации о предметах в игре. Вы можете настроить клавишу активации, изменив значение переменной `target_key`.

## Могу ли я получить блокировку?
Нет. Это не чит. Он не внедряется в игру и никак не работает с оперативной памятью, из-за чего этот инструмент подходит под правила разработчиков и сводит риски получения блокировки к нулю.


</div>