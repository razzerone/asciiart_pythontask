"""
Файл настроек

В переменной ASCII_symbols сопоставлены наборы символов (так как высота и
ширина символов различны, есть возможность указывать набор символов) и
уровень яркости

В переменной contrast_step лежит число, равное шагу между уровнями яркости
"""
import cv2

contrast_step = 3

ASCII_symbols_width = 1

ASCII_symbols = \
    ' .,`\'"""_-+<>=*^:;!co()/\[]?iljnaef1JILY7' \
    'VTCUZ4AO0PX23hbhbdk56GF89%DEKSNQR&WB$WHM#@@@@'

image_font = cv2.FONT_HERSHEY_TRIPLEX
image_font_size = 0.5
image_font_line_type = cv2.FILLED
image_font_thickness = 2

image_font_width = 12
image_font_height = 17
