from ..utils.helpers import format_url, request

class Quote:
    def __init__(self, client):
        self.client = client
        
    def get_all(self, fields=None):
        url = format_url(self.client.base_url, 'quote')
        response = request(self.client.session, 'GET', url, fields)
        return response
    
    def get_quote(self, quote_id, fields=None):
        url = format_url(self.client.base_url, f'quote/{quote_id}')
        response = request(self.client.session, 'GET', url, fields)
        return response
