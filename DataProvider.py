import json
import os

with open('test_data.json', 'r', encoding='utf-8') as f:
    global_data = json.load(f)


class DataProvider:
    def __init__(self) -> None:
        """Инициализирует DataProvider с данными из test_data.json."""
        self.data = global_data

    def get(self, prop: str) -> str:
        """Возвращает строковое значение по указанному ключу.

        :return: str — значение по ключу или None, если ключ не найден
        """
        return self.data.get(prop)

    def getint(self, prop: str) -> int:
        """Возвращает целочисленное значение по указанному ключу.

        :return: int — целочисленное значение по ключу
        """
        val = self.data.get(prop)
        return int(val)

    def get_token(self) -> str:
        """Возвращает токен API.

        Сначала пытается получить токен из переменной окружения KINO_API_TOKEN.
        Если переменная не установлена, берёт токен из test_data.json.

        :return: str — токен API или None, если токен не найден нигде
        """
        token = os.getenv('KINO_API_TOKEN')  # Исправлено: было os.getenv
        if token:
            return token
        return self.data.get('token')

    def movie_by_id_data(self):
        """Возвращает тестовые данные для проверки получения фильма по ID.

        Предоставляет список кортежей (movie_id, expected_title) для
        параметризации тестов. Каждый кортеж содержит ID фильма и
        ожидаемое название.

        :return: list[tuple[int, str]] — список кортежей вида
            (ID фильма, название)
        """
        return [
            (self.getint('movie_id_matrix'),
             self.get('expected_title_matrix')),
            (self.getint('movie_id_game_of_thrones'),
             'Игра престолов')
        ]

    def search_movies_data(self):
        """Возвращает тестовые данные для поиска фильмов.

        Предоставляет список кортежей (search_query, min_results) для
        параметризации тестов поиска. Каждый кортеж содержит поисковый
        запрос и минимальное ожидаемое количество результатов.

        :return: list[tuple[str, int]] — список кортежей вида
            (поисковый запрос, минимальное количество результатов)
        """
        return [
            (self.get('search_query_valid'), 1),
            (self.get('search_query_fragment'), 0),
            (self.get('search_query_typo'), 0)
        ]

    def episode_by_season_data(self):
        """Возвращает тестовые данные для проверки эпизодов сериала.

        :return: list[tuple[int, int, str]] — список кортежей вида
            (ID сериала, номер сезона, ожидаемое название эпизода)
        """
        return [
            (self.getint('movie_id_game_of_thrones'),
             1,
             self.get('expected_episode_name_game_of_thrones'))
        ]

    def person_by_id_data(self):
        """Возвращает тестовые данные для проверки информации об актёре.

        Предоставляет список кортежей (person_id, expected_name) для
        параметризации тестов. Каждый кортеж содержит ID актёра и
        ожидаемое имя.

        :return: list[tuple[int, str]] — список кортежей вида
            (ID актёра, имя)
        """
        return [
            (self.getint('person_id_jackie_chan'),
             self.get('person_name_jackie_chan'))
        ]
