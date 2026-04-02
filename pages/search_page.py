import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException

from config import EXPLICIT_WAIT


class SearchPage:
    """Класс для работы со страницей поиска Кинопоиска."""

    def __init__(self, driver) -> None:
        """Инициализация страницы поиска.

        :param driver: экземпляр WebDriver
        """
        if driver is None:
            raise ValueError('Driver не может быть None')
        self.driver = driver
        self.wait = WebDriverWait(driver, EXPLICIT_WAIT)

        # Локаторы элементов
        self.search_input = (By.NAME, 'kp_query')
        self.search_button = (By.CSS_SELECTOR, "button[type='submit']")
        self.result_container = (By.CSS_SELECTOR, 'div.search_results')
        self.first_result_title = (By.CSS_SELECTOR, 'div.element.most_wanted')

    def close_overlays(self) -> None:
        """Закрывает все всплывающие окна, баннеры, попапы и т.д."""
        with allure.step('Закрыть всплывающие окна и баннеры'):
            overlay_selectors = [
                '.overlay',
                '.modal',
                '.popup',
                '.cookie-banner',
                '.ad-banner',
                '.promo-popup',
                '.notification',
                '[class*="overlay"]',
                '[class*="modal"]',
                '[aria-modal="true"]'
            ]

            for selector in overlay_selectors:
                try:
                    close_button = self.driver.find_element(
                        By.CSS_SELECTOR,
                        f'{selector} .close, '
                        f'{selector} .dismiss, '
                        f'{selector} button'
                    )
                    if close_button.is_displayed():
                        close_button.click()
                        WebDriverWait(self.driver, 5).until(
                            EC.invisibility_of(close_button)
                        )
                except Exception:
                    continue

    @allure.step('Открыть главную страницу Кинопоиска: {base_url}')
    def open(self, base_url: str) -> None:
        """Открывает главную страницу Кинопоиска.

        :param base_url: URL главной страницы Кинопоиска
        :return: None
        """
        if self.driver is None:
            raise RuntimeError('Driver не инициализирован в SearchPage')
        self.driver.get(base_url)
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )

    @allure.step('Ввести запрос в поле поиска: {query}')
    def enter_search_query(self, query: str) -> None:
        """Вводит запрос в поле поиска.

        :param query: текст поискового запроса
        :raises: TimeoutException — если поле поиска не стало кликабельным
            в течение 10 секунд
        :return: None
        """
        self.close_overlays()

        search_input_element = self.wait.until(
            EC.element_to_be_clickable(self.search_input)
        )
        search_input_element.clear()
        search_input_element.send_keys(query)

    @allure.step('Нажать кнопку поиска')
    def click_search(self) -> None:
        """Нажимает на кнопку поиска.

        :raises: TimeoutException — если кнопка поиска не стала кликабельной
            в течение 20 секунд
        :return: None
        """
        long_wait = WebDriverWait(self.driver, 20)
        self.close_overlays()

        search_button_element = long_wait.until(
            EC.element_to_be_clickable(self.search_button)
        )
        search_button_element.click()

    @allure.step('Получить заголовок первого результата')
    def get_first_result_title(self) -> str:
        """Получает заголовок первого результата в списке поиска.

        :return: текст заголовка первого найденного элемента
        :raises: TimeoutException — если элемент не стал видимым
            в течение 10 секунд
        """
        first_result = self.wait.until(
            EC.visibility_of_element_located(self.first_result_title)
        )
        return first_result.text

    @allure.step('Проверить результаты поиска')
    def are_results_displayed(self) -> bool:
        """Проверяет отображение результатов поиска.

        :return: True, если результаты видны; False,
            если не видны или не найдены
        """
        try:
            self.wait.until(
                EC.visibility_of_element_located(self.result_container)
            )
            return True
        except WebDriverException:
            return False
