import pytest
import allure
from pages.search_page import SearchPage
from DataProvider import DataProvider


@pytest.fixture(scope='session')
def data_provider():
    """Фикстура для доступа к тестовым данным через DataProvider."""
    return DataProvider()


class TestSearch:

    @allure.feature('Поиск контента')
    @allure.story('Базовый поиск по названию фильма')
    @allure.title('Поиск по конкретному названию фильма')
    def test_search_with_valid_title(
            self,
            search_page: SearchPage,
            data_provider
    ) -> None:
        """Поиск по названию фильма.

        :param search_page: SearchPage — экземпляр класса страницы поиска
        :return: None
        """
        with allure.step('Вводим название фильма "Принцесса Мононоке"'):
            search_page.enter_search_query(
                data_provider.get('search_query_valid')
            )

        with allure.step('Нажимаем на кнопку поиска'):
            search_page.click_search()

        with (allure.step('Проверяем отображение результатов')):
            assert search_page.are_results_displayed(), (
                'Результаты не отобразились'
            )

        with allure.step('Проверяем соответствие первого результата запросу'):
            first_title = search_page.get_first_result_title()
            expected = 'Принцесса Мононоке'
            assert expected in first_title, (
                f'Первый результат не содержит "{expected}": {first_title}'
            )

    @allure.feature('Поиск контента')
    @allure.story('Обработка крайних случаев')
    @allure.title('Поиск с пустым запросом')
    def test_search_with_empty_query(
            self,
            search_page: SearchPage,
            data_provider
    ) -> None:
        """Проверка поведения при пустом запросе.

        :param search_page: SearchPage — экземпляр класса страницы поиска
        :return: None
        """
        with allure.step('Вводим пустой запрос'):
            search_page.enter_search_query(
                data_provider.get('search_query_empty')
            )

        with allure.step('Нажимаем на кнопку поиска'):
            search_page.click_search()

        with allure.step('Проверяем отсутствие результатов'):
            assert not search_page.are_results_displayed(), (
                'Результаты отобразились при пустом запросе'
            )

    @allure.feature('Поиск контента')
    @allure.story('Поиск по фрагменту названия')
    @allure.title('Поиск по фрагменту "Ават" (подразумевается "Аватар")')
    def test_search_with_fragment(
            self,
            search_page: SearchPage,
            data_provider
    ) -> None:
        """Поиск по части названия.

        :param search_page: SearchPage — экземпляр класса страницы поиска
        :return: None
        """
        with allure.step('Вводим фрагмент названия "Ават"'):
            search_page.enter_search_query(
                data_provider.get('search_query_fragment')
            )

        with allure.step('Нажимаем на кнопку поиска'):
            search_page.click_search()

        with allure.step('Проверяем наличие фильма "Аватар" в результатах'):
            assert search_page.are_results_displayed(), (
                'Результаты не отобразились'
            )
            first_title = search_page.get_first_result_title()
            assert ('Аватар' in first_title or
                   'avatar' in first_title.lower()), (
                f'Фильм "Аватар" не найден в результатах: {first_title}'
            )

    @allure.feature('Поиск контента')
    @allure.story('Проверка чувствительности к регистру')
    @allure.title('Поиск с разными регистрами: "шёпот сердца"')
    def test_search_case_insensitivity(
            self,
            search_page: SearchPage,
            data_provider
    ) -> None:
        """Проверка нечувствительности поиска к регистру.

        :param search_page: SearchPage — экземпляр класса страницы поиска
        :return: None
        """
        with allure.step('Вводим запрос "шёпот сердца" строчными буквами'):
            search_page.enter_search_query(
                data_provider.get('search_query_case_insensitive')
            )

        with allure.step('Нажимаем на кнопку поиска'):
            search_page.click_search()

        with allure.step(
            'Проверяем отображение результатов (поиск не зависит от регистра)'
        ):
            assert search_page.are_results_displayed(), (
                'Результаты не отобразились при вводе строчными буквами'
            )
            first_title = search_page.get_first_result_title()
            expected = 'Шёпот сердца'
            assert (expected in first_title or
                   'шёпот сердца' in first_title.lower()), (
                f'Фильм "{expected}" не найден: {first_title}'
            )

    @allure.feature('Поиск контента')
    @allure.story('Обработка опечаток в запросах')
    @allure.title('Поиск с опечаткой: "Илюзия обмана"')
    def test_search_with_typo(
            self,
            search_page: SearchPage,
            data_provider
    ) -> None:
        """Проверка поиска с опечаткой.

        :param search_page: SearchPage — экземпляр класса страницы поиска
        :return: None
        """
        with allure.step('Вводим запрос с опечаткой "Илюзия обмана"'):
            search_page.enter_search_query(
                data_provider.get('search_query_typo')
            )

        with allure.step('Нажимаем на кнопку поиска'):
            search_page.click_search()

        with allure.step(
            'Проверяем, что фильм "Иллюзия обмана" найден несмотря на опечатку'
        ):
            assert search_page.are_results_displayed(), (
                'Результаты не отобразились при опечатке'
            )
            first_title = search_page.get_first_result_title()
            expected = 'Иллюзия обмана'
            assert (expected in first_title or
                   'иллюзия обмана' in first_title.lower()), (
                f'Фильм "{expected}" не найден при опечатке: {first_title}'
            )

    @allure.feature('Поиск контента')
    @allure.story('Поиск с использованием спецсимволов')
    @allure.title('Поиск: "Игра Престолов!"')
    def test_search_special_chars(
            self,
            search_page: SearchPage,
            data_provider
    ) -> None:
        """Проверка обработки спецсимволов в запросе.

        :param search_page: SearchPage — экземпляр класса страницы поиска
        :return: None
        """
        with allure.step('Вводим запрос со спецсимволом "Игра Престолов!"'):
            search_page.enter_search_query(
                data_provider.get('search_query_special_chars')
            )

        with allure.step('Нажимаем на кнопку поиска'):
            search_page.click_search()

        with allure.step(
            'Проверяем наличие несмотря на спецсимвол'
        ):
            assert search_page.are_results_displayed(), (
                'Результаты не отобразились при использовании спецсимвола'
            )
            first_title = search_page.get_first_result_title()
            expected = 'Игра престолов'
            assert (expected in first_title or
                   'игра престолов' in first_title.lower()), (
                f'Сериал "{expected}" не найден при спецсимволе: {first_title}'
            )
