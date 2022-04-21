"""
Файл настроек

В переменной ASCII_symbols сопоставлены наборы символов (так как высота и
ширина символов различны, есть возможность указывать набор символов) и
уровень яркости

В переменной contrast_step лежит число, равное шагу между уровнями яркости
"""
import cv2

contrast_step = 26

ASCII_symbols_width = 2
ASCII_symbols = {
            0: '  ',
            1: '..',
            2: ';:',
            3: '//',
            4: 'oo',
            5: 'OO',
            6: '00',
            7: '83',
            8: '##',
            9: '@@',
        }

image_font = cv2.FONT_HERSHEY_TRIPLEX
image_font_size = 0.5

image_font_width = 12
image_font_height = 17
