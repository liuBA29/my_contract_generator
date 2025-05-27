
# src/config.py

# Copyright (c) 2025 Liubov Kovaleva (@liuBA29)
# Licensed under the MIT License.


import os
import sys

# Определяем базовую директорию — для .exe и для обычного запуска
if getattr(sys, 'frozen', False):
    # Запущено как .exe (например, после сборки PyInstaller + Inno Setup)
    # BASE_DIR = os.path.dirname(sys.executable)
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

DATA_DIR = os.path.join(BASE_DIR, 'data')
DB_PATH = os.path.join(DATA_DIR, 'customers.db')