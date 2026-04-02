import pytest
import allure
from api.movie_api import MovieAPI
from DataProvider import DataProvider


@pytest.fixture
def movie_api():
    return MovieAPI()


@pytest.fixture
def data_provider():
    """Фикстура для доступа к тестовым данным через DataProvider."""
    return DataProvider()


@allure.feature('Movie API')
class TestMovieAPI:

    @allure.story('Получение фильма по ID')
    @allure.title(
        'Получение информации о фильме по ID: {movie_id} — "{expected_title}"'
    )
    @pytest.mark.parametrize(
        "movie_id, expected_title",
        DataProvider().movie_by_id_data()
    )
    def test_get_movie_by_id(self, movie_api, movie_id, expected_title):
        with allure.step(
            f'Отправляем GET‑запрос для получения фильма с ID {movie_id}'
        ):
            response = movie_api.get_movie_by_id(movie_id)

        with allure.step('Проверяем статус‑код 200'):
            assert response.status_code == 200, (
                f'Ожидался статус 200, получен {response.status_code}'
            )

        with allure.step('Парсим JSON‑ответ'):
            data = response.json()

        with allure.step('Проверяем наличие и значение ID'):
            assert 'id' in data, 'Поле "id" отсутствует в ответе'
            assert data['id'] == movie_id, (
                f'ID в ответе ({data["id"]}) не совпадает с '
                f'запрошенным ({movie_id})'
            )

        with allure.step('Проверяем наличие и значение названия фильма'):
            assert 'name' in data, 'Поле "name" отсутствует в ответе'
            if expected_title:
                assert data['name'] == expected_title, (
                    f'Название фильма ({data["name"]}) не соответствует '
                    f'ожидаемому ({expected_title})'
                )

    @allure.story('Поиск фильмов по названию')
    @allure.title(
        'Поиск фильмов по запросу "{search_query}" — ожидается минимум '
        '{min_results} результатов'
    )
    @pytest.mark.parametrize(
        "search_query, min_results",
        DataProvider().search_movies_data()
    )
    def test_search_movies(self, movie_api, search_query, min_results):
        with allure.step(
            f'Отправляем GET‑запрос для поиска фильма "{search_query}"'
        ):
            response = movie_api.search_movies(search_query)

        with allure.step('Проверяем статус‑код 200 и наличие результатов'):
            assert response.status_code == 200, (
                f'Ожидался статус 200, получен {response.status_code}'
            )
            data = response.json()
            assert len(data) >= min_results, (
                f'В ответе меньше результатов ({len(data)}), чем '
                f'ожидалось ({min_results})'
            )

    @allure.story('Получение списка жанров')
    def test_get_possible_genres(self, movie_api):
        with allure.step('Отправляем GET-запрос для получения списка жанров'):
            response = movie_api.get_possible_genres()

        with allure.step('Проверяем статус-код 200 и наличие данных'):
            assert response.status_code == 200
            data = response.json()
            assert len(data) > 0

    @allure.story('Получение информации об актёре')
    @allure.title(
        'Получение информации об актёре с ID {person_id} — '
        'ожидается имя "{expected_name}"'
    )
    @pytest.mark.parametrize(
        "person_id, expected_name",
        DataProvider().person_by_id_data()
    )
    def test_get_person_by_id(self, movie_api, person_id, expected_name):
        with allure.step(
            f'Отправляем GET‑запрос для получения информации '
            f'об актёре с ID {person_id}'
        ):
            response = movie_api.get_person_by_id(person_id)

        with allure.step('Проверяем статус‑код 200'):
            assert response.status_code == 200, (
                f'Ожидался статус 200, получен {response.status_code}'
            )

        with allure.step('Парсим JSON‑ответ'):
            data = response.json()

        with allure.step('Проверяем наличие поля "name" в ответе'):
            assert 'name' in data, 'Поле "name" отсутствует в ответе'

        with allure.step('Проверяем наличие поля "id" в ответе'):
            assert 'id' in data, 'Поле "id" отсутствует в ответе'

        with allure.step('Проверяем соответствие ID'):
            assert data['id'] == person_id, (
                f'ID в ответе ({data["id"]}) не совпадает с запрошенным '
                f'({person_id})'
            )

        with allure.step('Проверяем соответствие имени актёра'):
            assert data['name'] == expected_name, (
                f'Имя актёра ({data["name"]}) не соответствует '
                f'ожидаемому ({expected_name})'
            )

    @allure.story('Получение эпизодов сериала')
    @allure.title(
        'Проверка названия эпизода: сериал {series_id}, '
        'сезон {season_num} — "{expected_episode}"'
    )
    @pytest.mark.parametrize(
        "series_id, season_num, expected_episode",
        DataProvider().episode_by_season_data()
    )
    def test_get_episodes_by_series_id(
            self, movie_api, series_id, season_num, expected_episode
    ):
        with allure.step(
                f'Отправляем GET‑запрос для получения эпизодов '
                f'сериала {series_id}, сезон {season_num}'
        ):
            response = movie_api.get_season_details(
                movie_id=series_id,
                season_number=season_num,
                page=1,
                limit=10
            )

        with allure.step('Проверяем статус‑код 200'):
            assert response.status_code == 200, (
                f'Ожидался статус 200, получен {response.status_code}. '
                f'Тело ответа: {response.text[:500]}'
            )

        with allure.step('Парсим JSON‑ответ'):
            data = response.json()

        with allure.step('Проверяем наличие массива эпизодов'):
            assert 'docs' in data, 'Поле "docs" отсутствует в ответе'
            assert len(data['docs']) > 0, 'Массив docs пуст'

        with allure.step('Находим нужный сезон и проверяем эпизод'):
            season_found = False
            for season in data['docs']:
                if season.get('number') == season_num:
                    season_found = True
                    episodes = season.get('episodes', [])
                    assert len(episodes) > 0, (
                        f'В сезоне {season_num} нет эпизодов'
                    )

                    with allure.step('Проверяем название первого эпизода'):
                        first_episode = episodes[0]
                        assert 'name' in first_episode, (
                            'Поле "name" отсутствует у эпизода'
                        )
                assert first_episode['name'] == expected_episode, (
                    f'Название эпизода ({first_episode["name"]}) '
                    f'не соответствует ожидаемому ({expected_episode})'
                )
                break

            assert season_found, f'Сезон {season_num} не найден в ответе'
