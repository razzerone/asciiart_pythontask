"""
Файл настроек

В переменной ASCII_symbols сопоставлены наборы символов (так как высота и
ширина символов различны, есть возможность указывать набор символов) и
уровень яркости

В переменной contrast_step лежит число, равное шагу между уровнями яркости
"""
import cv2

contrast_step = 13

ASCII_symbols_width = 1
ASCII_symbols = {
    0: ' ',
    1: '.',
    2: ',',
    3: '_',
    4: '^',
    5: '+',
    6: '|',
    7: '<',
    8: 'o',
    9: '?',
    10: 'O',
    11: 'C',
    12: 'D',
    13: 'A',
    14: 'B',
    15: '$',
    16: '%',
    17: '#',
    18: '@',
    19: '&',
    20: 'W'
}

image_font = cv2.FONT_HERSHEY_TRIPLEX
image_font_size = 0.5
image_font_line_type = cv2.FILLED
image_font_thickness = 3

image_font_width = 12
image_font_height = 17
