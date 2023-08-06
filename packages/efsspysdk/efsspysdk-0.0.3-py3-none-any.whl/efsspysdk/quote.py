from requests import Session
from .core.configs.variables import BASE_URL, API_KEY
from .core.models.quote import QuoteActions
from .core.utils.helpers import create_session

class Quote:
    def __init__(self, base_url=BASE_URL, api_key=API_KEY):
        self.base_url = base_url
        self.api_key = api_key
        self.session = create_session(self.api_key)
        self.quote = QuoteActions(self)
    
    def get(self, quote_id, fields=None):
        return self.quote.get_quote(quote_id, fields=fields)
    def list(self, fields=None):
        return self.quote.get_all()

