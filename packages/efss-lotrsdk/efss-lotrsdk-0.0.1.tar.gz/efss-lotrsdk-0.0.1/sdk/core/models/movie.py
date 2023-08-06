from ..utils.helpers import format_url, request

class Movie:
    def __init__(self, client):
        self.client = client
        
    def get_all(self, fields=None):
        url = format_url(self.client.base_url, 'movie')
        response = request(self.client.session, 'GET', url, fields)
        return response
    
    def get_movie(self, movie_id, fields=None):
        url = format_url(self.client.base_url, f'movie/{movie_id}')
        response = request(self.client.session, 'GET', url, fields)
        return response
    
    def get_quote(self, movie_id, fields=None):
        url = format_url(self.client.base_url, f'movie/{movie_id}/quote')
        response = request(self.client.session, 'GET', url, fields)
        return response
