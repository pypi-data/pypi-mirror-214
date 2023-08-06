from requests import Session
from .core.configs.variables import BASE_URL, API_KEY
from .core.models.movie import MovieActions
from .core.utils.helpers import create_session

class Movie:
    def __init__(self, base_url=BASE_URL, api_key=API_KEY):
        self.base_url = base_url
        self.api_key = api_key
        self.session = create_session(self.api_key)
        self.movie = MovieActions(self)
    
    def list(self, fields=None):
        return self.movie.get_all(fields=fields)
    def get(self, movie_id, fields=None):
        return self.movie.get_movie(movie_id, fields=fields)
    def list_quotes(self, movie_id, fields=None):
        return self.movie.get_quote(movie_id)   