import allure
import pytest
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from config import BASE_URL, HEADLESS_MODE, WINDOW_SIZE
from pages.search_page import SearchPage
from api.movie_api import MovieAPI


@pytest.fixture(scope="session")
def base_url():
    """Возвращает базовый URL из конфигурационного файла.

    :return: str — базовый URL Кинопоиска
    """
    return BASE_URL


@pytest.fixture(scope="session")
@allure.title('Инициализация WebDriver для Chrome')
def driver():
    """Фикстура для создания и закрытия экземпляра WebDriver для Chrome
    с базовой изоляцией между тестами.

    Каждый тест получает:
    - режим инкогнито (для обхода капчи);
    - режим headless/headful в зависимости от конфигурации;
    - фиксированные настройки безопасности.

    :yield: WebDriver — инициализированный экземпляр драйвера браузера
    """
    with allure.step('Запуск браузера Chrome в режиме инкогнито'):
        driver_path = ChromeDriverManager().install()
        service = Service(driver_path)

        options = Options()
        options.add_argument('--incognito')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')

        if HEADLESS_MODE:
            options.add_argument('--headless')

        options.add_argument(f'--window-size={WINDOW_SIZE}')

        try:
            driver_instance = webdriver.Chrome(
                service=service,
                options=options
            )
            yield driver_instance
        finally:
            with allure.step('Закрытие браузера'):
                if driver_instance:
                    driver_instance.quit()


@pytest.fixture(scope="class")
@allure.step('Настройка страницы поиска')
def search_page(driver, base_url):
    """Фикстура для подготовки страницы поиска перед тестом.

    :param driver: WebDriver — экземпляр драйвера фикстуры driver
    :param base_url: str — URL главной страницы Кинопоиска
    :return: SearchPage — инициализированный объект страницы поиска
    """
    with allure.step(f'Открытие главной страницы: {base_url}'):
        page = SearchPage(driver)
        page.open(base_url)
    return page


@pytest.fixture(scope='session')
@allure.title('Инициализация клиента API фильмов')
@allure.description(
    'Создаёт один экземпляр MovieAPI на всю сессию тестов. '
    'Используется для всех API‑тестов.'
)
def movie_api():
    """
    Фикстура для клиента API фильмов.
    Создаёт один экземпляр MovieAPI на всю сессию тестов.
    Используется для всех API‑тестов.
    """
    with allure.step('Инициализация MovieAPI клиента'):
        api_client = MovieAPI()
        allure.attach(
            body=f'Base URL: {api_client.base_url}',
            name='API Configuration',
            attachment_type=allure.attachment_type.TEXT
        )
    return api_client
