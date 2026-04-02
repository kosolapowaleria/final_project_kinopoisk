import requests
from api.base_api import BaseAPI


class MovieAPI(BaseAPI):
    def get_movie_by_id(self, movie_id: int) -> requests.Response:
        """
        GET /movie/{id}
        :param movie_id: ID фильма (int)
        :return: объект Response с данными фильма
        """
        endpoint = f'movie/{movie_id}'
        return self.get(endpoint)

    def search_movies(self, query: str) -> requests.Response:
        """
        GET /movie/search
        :param query: название фильма (str)
        :return: объект Response со списком фильмов
        """
        params = {'query': query}
        endpoint = 'movie/search'
        return self.get(endpoint, params)

    def get_possible_genres(self) -> requests.Response:
        """
        GET /movie/possible-values-by-field?field=genres.name
        :return: объект Response со списком жанров
        """
        params = {'field': 'genres.name'}
        endpoint = 'movie/possible-values-by-field'
        return self.get(endpoint, params, api_version='v1')

    def get_season_details(
            self,
            movie_id: int,
            season_number: int,
            episode_number: int = None,
            page: int = 1,
            limit: int = 10
    ) -> requests.Response:
        """
        GET /season
        :param movie_id: ID сериала (int)
        :param season_number: номер сезона (int)
        :param episode_number: номер эпизода (int, опционально)
        :param page: номер страницы (int)
        :param limit: количество элементов на странице (int)
        :return: объект Response с данными сезона/эпизода
        """
        params = {
            'movieId': movie_id,
            'number': season_number,
            'page': page,
            'limit': limit
        }
        if episode_number:
            params['episodes.number'] = episode_number
        endpoint = 'season'
        return self.get(endpoint, params)

    def get_person_by_id(self, person_id: int) -> requests.Response:
        """
        GET /person/{id}
        :param person_id: ID актёра (int)
        :return: объект Response с данными актёра
        """
        endpoint = f'person/{person_id}'
        return self.get(endpoint)
