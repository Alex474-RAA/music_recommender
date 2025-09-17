#!/usr/bin/env python3
"""
Файл для запуска музыкального рекомендателя.
Добавляет корень проекта в sys.path и запускает основное приложение.
"""
import os
import sys

# Добавляем корень проекта в sys.path
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Запускаем основное приложение
from src.main import main

if __name__ == "__main__":
    main()
