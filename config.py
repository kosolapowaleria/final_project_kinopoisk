from dotenv import load_dotenv
from DataProvider import DataProvider


# Загружаем переменные окружения из .env
load_dotenv()

# Создаём экземпляр DataProvider для доступа к данным
data_provider = DataProvider()


# Получаем настройки из test_data.json
BASE_URL = data_provider.get('base_url')
API_BASE_URL = data_provider.get('api_base_url')
API_VERSION = data_provider.get('api_version')

# Настройки API
API_TIMEOUT = data_provider.getint('api_timeout')
API_RETRIES = data_provider.getint('api_retries')

# Настройки браузера
HEADLESS_MODE = False
WINDOW_SIZE = data_provider.get('window_size')

# Таймауты
IMPLICIT_WAIT = data_provider.getint('implicit_wait')
EXPLICIT_WAIT = data_provider.getint('explicit_wait')


# Получаем токен через DataProvider (сначала из .env, потом из JSON)
API_TOKEN = data_provider.get_token()

# Проверка наличия токена
if not API_TOKEN:
    raise ValueError(
        'KINO_API_TOKEN не установлен. '
        'Создайте файл .env с переменной KINO_API_TOKEN=ваш_токен '
        'либо установите переменную окружения.'
    )

# Финальная проверка BASE_URL
if not BASE_URL:
    raise ValueError('BASE_URL не загружен из DataProvider. '
                     'Проверьте test_data.json и .env')
