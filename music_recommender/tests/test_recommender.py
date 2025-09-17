"""
Тесты для музыкального рекомендателя.
"""

import sys
import os
import random
from unittest.mock import patch

# Добавляем корень проекта в sys.path для импорта модулей
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Импортируем функции из модуля recommender
from src.recommender import predict_mood, get_available_artists, recommend_tracks

# Фиксируем random seed для предсказуемости тестов
random.seed(42)


# Мокируем random.sample для предсказуемости fallback-механизма
def mock_random_sample(items, k):
    """Моковая функция для random.sample."""
    return items[:k]


# Тесты для predict_mood
def test_predict_mood_happy():
    """Тест для веселого настроения."""
    assert predict_mood(0.8) == "веселое"


def test_predict_mood_sad():
    """Тест для грустного настроения."""
    assert predict_mood(0.3) == "грустное"


def test_predict_mood_neutral():
    """Тест для нейтрального настроения."""
    assert predict_mood(0.5) == "нейтральное"


# Тесты для get_available_artists
def test_get_available_artists():
    """Тест получения списка исполнителей."""
    artists = get_available_artists()
    assert isinstance(artists, list)
    assert len(artists) > 0


# Тесты для recommend_tracks
@patch("random.sample", side_effect=mock_random_sample)
def test_recommend_tracks_for_unknown_artist(mock_sample):
    """Тест рекомендаций для неизвестного исполнителя."""
    recommendations = recommend_tracks(["Unknown Artist"], "веселое")
    # Fallback-механизм должен добавить треки
    assert len(recommendations) > 0
    # Проверяем, что все треки имеют правильное настроение
    for track in recommendations:
        assert track["mood"] == "веселое"


@patch("random.sample", side_effect=mock_random_sample)
def test_recommend_tracks_for_sad_mood(mock_sample):
    """Тест рекомендаций для грустного настроения."""
    recommendations = recommend_tracks(["Billie Eilish"], "грустное")
    assert isinstance(recommendations, list)
    # Проверяем, что все рекомендованные треки имеют правильное настроение
    for track in recommendations:
        assert track["mood"] == "грустное"


@patch("random.sample", side_effect=mock_random_sample)
def test_recommend_tracks_for_happy_mood(mock_sample):
    """Тест рекомендаций для веселого настроения."""
    recommendations = recommend_tracks(["Dua Lipa"], "веселое")
    # Проверяем, что все рекомендованные треки имеют правильное настроение
    for track in recommendations:
        assert track["mood"] == "веселое"


@patch("random.sample", side_effect=mock_random_sample)
def test_recommend_tracks_for_unknown_artist(mock_sample):
    """Тест рекомендаций для неизвестного исполнителя."""
    recommendations = recommend_tracks(["Unknown Artist"], "веселое")
    # Fallback-механизм должен добавить треки
    assert len(recommendations) > 0


@patch("random.sample", side_effect=mock_random_sample)
def test_recommend_tracks_multiple_artists(mock_sample):
    """Тест рекомендаций для нескольких исполнителей."""
    recommendations = recommend_tracks(["Billie Eilish", "Dua Lipa"], "веселое")
    # Проверяем, что все треки имеют правильное настроение
    for track in recommendations:
        assert track["mood"] == "веселое"


@patch("random.sample", side_effect=mock_random_sample)
def test_recommend_tracks_contains_expected_tracks(mock_sample):
    """Тест, что рекомендации содержат ожидаемые треки."""
    recommendations = recommend_tracks(["Bruno Mars"], "грустное")
    # Получаем названия всех рекомендованных треков
    track_names = [track["name"] for track in recommendations]
    # Проверяем, что ожидаемые грустные треки Bruno Mars есть в рекомендациях
    expected_sad_tracks = ["Grenade", "When I Was Your Man"]
    found_expected = any(track in track_names for track in expected_sad_tracks)
    assert found_expected, f"Expected to find one of {expected_sad_tracks} in {track_names}"


# Интеграционные тесты
@patch("random.sample", side_effect=mock_random_sample)
def test_end_to_end_happy_path(mock_sample):
    """Тест полного цикла работы с известными данными."""
    artists = ["Bruno Mars"]
    mood = "грустное"

    recommendations = recommend_tracks(artists, mood)

    # Проверяем результаты - теперь учитываем fallback-механизм
    assert len(recommendations) >= 2  # Должно быть как минимум 2 грустных трека

    # Проверяем, что хотя бы один трек от указанного исполнителя
    artist_tracks = [track for track in recommendations if track["artist"] in artists]
    assert len(artist_tracks) >= 1

    # Проверяем, что все треки имеют правильное настроение
    for track in recommendations:
        assert track["mood"] == mood


@patch("random.sample", side_effect=mock_random_sample)
def test_no_recommendations_for_mismatch(mock_sample):
    """Тест, когда нет треков, соответствующих настроению."""
    artists = ["Billie Eilish"]
    mood = "веселое"

    recommendations = recommend_tracks(artists, mood)
    # Должно быть немного рекомендаций из-за fallback-механизма
    assert len(recommendations) > 0


# Тесты для edge cases
@patch("random.sample", side_effect=mock_random_sample)
def test_empty_artists_list(mock_sample):
    """Тест с пустым списком исполнителей."""
    recommendations = recommend_tracks([], "веселое")
    # Ожидаем, что будут рекомендованы треки из общего пула
    assert len(recommendations) > 0


@patch("random.sample", side_effect=mock_random_sample)
def test_artist_case_sensitivity(mock_sample):
    """Тест чувствительности к регистру имен исполнителей."""
    # Функция должна быть нечувствительна к регистру
    recommendations1 = recommend_tracks(["bruno mars"], "грустное")
    recommendations2 = recommend_tracks(["Bruno Mars"], "грустное")

    # Ожидаем одинаковые результаты
    assert len(recommendations1) == len(recommendations2)

    # Сортируем по имени трека для сравнения
    tracks1 = sorted([track["name"] for track in recommendations1])
    tracks2 = sorted([track["name"] for track in recommendations2])

    assert tracks1 == tracks2


@patch("random.sample", side_effect=mock_random_sample)
def test_mood_case_sensitivity(mock_sample):
    """Тест чувствительности к регистру настроения."""
    # Функция должна быть нечувствительна к регистру
    recommendations1 = recommend_tracks(["Bruno Mars"], "грустное")
    recommendations2 = recommend_tracks(["Bruno Mars"], "ГРУСТНОЕ")

    # Ожидаем одинаковые результаты
    assert len(recommendations1) == len(recommendations2)

    # Сортируем по имени трека для сравнения
    tracks1 = sorted([track["name"] for track in recommendations1])
    tracks2 = sorted([track["name"] for track in recommendations2])

    assert tracks1 == tracks2


if __name__ == "__main__":
    # Запуск тестов вручную
    test_predict_mood_happy()
    test_predict_mood_sad()
    test_predict_mood_neutral()
    test_get_available_artists()
    print("Все базовые тесты прошли успешно!")
