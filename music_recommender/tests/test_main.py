import os
import sys
import unittest
from unittest.mock import patch

# Добавляем корень проекта в sys.path для импорта модулей
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Импортируем main модуль
import src.main


def test_main_function_with_valid_input():
    """Тест основной функции с корректным вводом."""
    # Мокируем ввод пользователя
    with patch("builtins.input", side_effect=["Bruno Mars, Taylor Swift", "", "грустное"]):
        # Мокируем функцию recommend_tracks
        with patch("src.main.recommend_tracks") as mock_recommend:
            # Настраиваем мок для возврата рекомендаций
            mock_recommend.return_value = [
                {
                    "name": "Grenade",
                    "artist": "Bruno Mars",
                    "mood": "грустное",
                    "valence": 0.3,
                },
                {
                    "name": "All Too Well",
                    "artist": "Taylor Swift",
                    "mood": "грустное",
                    "valence": 0.2,
                },
            ]

            # Захватываем вывод
            with patch("builtins.print") as mock_print:
                # Вызываем основную функцию
                src.main.main()

                # Проверяем, что функция recommend_tracks была вызвана с правильными аргументами
                mock_recommend.assert_called_with(["Bruno Mars", "Taylor Swift"], "грустное")

                # Проверяем, что вывод содержит ожидаемые элементы
                assert mock_print.call_count >= 3
                # Проверяем, что были напечатаны рекомендации
                recommendations_printed = any(
                    "Grenade" in str(call) or "All Too Well" in str(call)
                    for call in mock_print.call_args_list
                )
                assert recommendations_printed


def test_main_function_with_invalid_mood():
    """Тест основной функции с неверным настроением."""
    # Мокируем ввод пользователя
    with patch("builtins.input", side_effect=["Bruno Mars", "", "неправильное"]):
        with patch("builtins.print") as mock_print:
            # Вызываем основную функцию
            src.main.main()

            # Проверяем, что был вывод об ошибке
            error_printed = any(
                "ошибка" in str(call).lower()
                or "error" in str(call).lower()
                or "настроение" in str(call).lower()
                for call in mock_print.call_args_list
            )
            assert error_printed


def test_main_function_with_no_recommendations():
    """Тест основной функции без рекомендаций."""
    # Мокируем ввод пользователя
    with patch("builtins.input", side_effect=["Unknown Artist", "", "веселое"]):
        with patch("src.main.recommend_tracks") as mock_recommend:
            # Настраиваем мок для возврата пустого списка
            mock_recommend.return_value = []

            with patch("builtins.print") as mock_print:
                # Вызываем основную функцию
                src.main.main()

                # Проверяем, что был вывод о отсутствии рекомендаций
                no_recommendations_printed = any(
                    "не найдено" in str(call).lower()
                    or "not found" in str(call).lower()
                    for call in mock_print.call_args_list
                )
                assert no_recommendations_printed


def test_main_function_with_alternative_recommendations():
    """Тест основной функции с альтернативными рекомендациями."""
    # Мокируем ввод пользователя
    with patch("builtins.input", side_effect=["Unknown Artist", "", "грустное"]):
        with patch("src.main.recommend_tracks") as mock_recommend:
            # Настраиваем мок: для запрошенного настроения нет рекомендаций,
            # но для альтернативного настроения есть
            mock_recommend.side_effect = [
                [],  # Первый вызов - нет рекомендаций для "грустное"
                [  # Второй вызов - есть рекомендации для "веселое"
                    {
                        "name": "Happy Song",
                        "artist": "Some Artist",
                        "mood": "веселое",
                        "valence": 0.8,
                    }
                ],
            ]

            with patch("builtins.print") as mock_print:
                # Вызываем основную функцию
                src.main.main()

                # Проверяем, что было предложено альтернативное настроение
                alternative_suggested = any(
                    "веселое" in str(call) or "альтернатив" in str(call).lower()
                    for call in mock_print.call_args_list
                )
                assert alternative_suggested


def test_main_function_with_whitespace_input():
    """Тест основной функции с вводом, содержащим пробелы."""
    # Мокируем ввод пользователя с пробелами
    with patch(
        "builtins.input",
        side_effect=["  Bruno Mars  ,  Taylor Swift  ", "", "  грустное  "],
    ):
        with patch("src.main.recommend_tracks") as mock_recommend:
            # Настраиваем мок для возврата рекомендаций
            mock_recommend.return_value = [
                {
                    "name": "Grenade",
                    "artist": "Bruno Mars",
                    "mood": "грустное",
                    "valence": 0.3,
                }
            ]

            with patch("builtins.print"):
                # Вызываем основную функцию
                src.main.main()

                # Проверяем, что функция recommend_tracks была вызвана с очищенными аргументами
                mock_recommend.assert_called_with(["Bruno Mars", "Taylor Swift"], "грустное")


@patch("src.main.recommend_tracks")
@patch("builtins.input")
@patch("builtins.print")
def test_main_function_integration(mock_print, mock_input, mock_recommend):
    """Интеграционный тест основной функции."""
    # Настраиваем моки
    mock_input.side_effect = ["Bruno Mars, Taylor Swift", "", "веселое"]
    mock_recommend.return_value = [
        {
            "name": "Shake It Off",
            "artist": "Taylor Swift",
            "mood": "веселое",
            "valence": 0.9,
        },
        {
            "name": "Uptown Funk",
            "artist": "Bruno Mars",
            "mood": "веселое",
            "valence": 0.9,
        },
    ]

    # Вызываем основную функцию
    src.main.main()

    # Проверяем, что функция recommend_tracks была вызвана с правильными аргументами
    mock_recommend.assert_called_with(["Bruno Mars", "Taylor Swift"], "веселое")

    # Проверяем, что были напечатаны рекомендации
    recommendations_printed = any(
        "Shake It Off" in str(call) or "Uptown Funk" in str(call)
        for call in mock_print.call_args_list
    )
    assert recommendations_printed