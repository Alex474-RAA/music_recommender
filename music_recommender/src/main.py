import os
import sys

# Добавляем корень проекта в sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.recommender import get_available_artists, recommend_tracks  # noqa: E402


def main():
    """Основная функция программы."""
    print("🎵 Музыкальный рекомендатель 🎵")
    print("Доступные исполнители:", ", ".join(get_available_artists()))
    print("\nВведите ваших любимых исполнителей (через запятую или скопируйте предложенное,поставте "" после ввода):")
    artists_lines = []
    while True:
        line = input()
        if not line:
            break
        artists_lines.append(line)

    artists_input = " ".join(artists_lines)
    artists = [artist.strip() for artist in artists_input.split(",")]

    mood_input = input("Какое у вас настроение? (веселое/грустное/нейтральное): ")
    mood = mood_input.lower().strip()

    # Проверка корректности ввода настроения
    valid_moods = ["веселое", "грустное", "нейтральное"]
    if mood not in valid_moods:
        print("Ошибка: настроение должно быть 'веселое', 'грустное' или 'нейтральное'")
        return

    # Получение рекомендаций
    recommendations = recommend_tracks(artists, mood)

    # Вывод результатов
    if recommendations:
        print(f"\n🎧 Рекомендованные треки для {mood} настроения:")
        for i, track in enumerate(recommendations, 1):
            print(f"{i}. {track['name']} - {track['artist']} (настроение: {track['mood']})")
    else:
        print("К сожалению, не найдено треков для вашего запроса.")

        # Предложим альтернативу
        alternative_mood = "веселое" if mood == "грустное" else "грустное"
        alternative_recs = recommend_tracks(artists, alternative_mood)
        if alternative_recs:
            print(f"\nМожет быть, вам подойдет {alternative_mood} настроение?")
            for i, track in enumerate(alternative_recs[:3], 1):
                print(f"{i}. {track['name']} - {track['artist']}")


if __name__ == "__main__":
    main()  # pragma: no cover
