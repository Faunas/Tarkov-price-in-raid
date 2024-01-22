<div align="center">

# Tarkov-price-in-raid

![GitHub](https://img.shields.io/github/license/Faunas/Tarkov-price-in-raid)
![GitHub last commit](https://img.shields.io/github/last-commit/Faunas/Tarkov-price-in-raid)

</div>

## Overview

EscapeFromTarkov-Trader-Assistant is a simple and efficient tool designed for players of Escape from Tarkov. It provides automated real-time search and price information for in-game items from traders without impacting performance. At this stage, it does not display prices from the Flea Market, focusing solely on traders. The tool operates exclusively in fullscreen mode at a screen resolution of 1920x1080 and has an English-language interface.

## Key Features

**Automated Item Search:** The project utilizes Optical Character Recognition (OCR) to extract information about in-game items, focusing on a rectangular area of the screen.

**Sound Notifications:** After recognizing item information, the tool provides sound notifications with the maximum selling price and identifies the trader offering the maximum profit.

**Voice Response for Missing Data:** If the tool cannot recognize item information or if all prices are linked to the Flea Market, it provides a voice response indicating the absence of data.

## Requirements

- Screen Resolution: 1920x1080 (Fullscreen Mode)
- Interface Language: English

## Installation and Usage Instructions

1. Install the latest version of [Tesseract OCR](https://github.com/tesseract-ocr/tesseract/releases/).
2. Install the necessary dependencies listed in the `requirements.txt` file.
3. Specify the path to the Tesseract OCR executable in the `pytesseract.tesseract_cmd` variable (line 11).
4. Run the project and use the "insert" key to activate the search for in-game item information. You can customize the activation key by changing the value of the `target_key` variable.

**Note:** Please adhere to the rules and conditions set by the game developers. This project is intended solely to enhance the gaming experience and should not be used to violate game rules.

</div>
