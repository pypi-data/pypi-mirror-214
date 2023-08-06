from requests import Session
from .core.configs.variables import BASE_URL, API_KEY
from .core.models.movie import Movie
from .core.models.quote import Quote
from .core.utils.helpers import verify_api_key

class Client:
    def __init__(self, base_url=BASE_URL, api_key=API_KEY):
        self.base_url = base_url
        self.api_key = api_key
        self.session = self.create_session()
        self.movie = Movie(self)
        self.quote = Quote(self)
    
    def create_session(self):
        verify_api_key(self.api_key)
        session = Session()
        session.headers.update({'Authorization': f'Bearer {self.api_key}'})
        return session