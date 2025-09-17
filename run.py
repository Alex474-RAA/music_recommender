import os
import sys

# Добавляем папку music_recommender в путь
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'music_recommender'))

from src.main import main

if __name__ == "__main__":
    main()