import os
import json
from urllib.parse import urlencode
import requests


def create_params(**kwargs):
    url = kwargs.get("url")
    params = kwargs.get("params")

    if params:
        query_string = urlencode(eval(params))
    return f'{url}?{query_string}'

class PathBuilder:
    def __init__(self,**kwargs):
        self.base_url = kwargs.get('base_url')
        self.domain = kwargs.get('domain')
        self.version = kwargs.get('version')
        self.movie_id = kwargs.get("movie_id")
        self.quote_id = kwargs.get('quote_id')
        self.domain_id = kwargs.get("domain_id")
        self.domain_action = "quote"
        self.params = kwargs.get('params')
    
    def build(self):
        paths ={
            "domains" :{
                "movie": {
                    "path":f'{self.version}/movie',
                    "name" : None
                },
                "quote": {
                    "path": f'{self.version}/quote',
                    "name": None
                }
            }
        }
        domain_info = paths['domains'][self.domain]
        sections = [domain_info['path']]

        if self.movie_id:
            sections.append(self.movie_id)
        if self.quote_id:
            sections.append(self.quote_id)
        if domain_info["name"]:
            sections.append(domain_info["name"])
        if self.domain_id:
            if self.domain_action:
                sections.append(self.domain_action)

        print(sections)
        
        path = f'/{"/".join(sections)}'
        url = f'{self.base_url}{path}'

        params = {}
        if params:
            url = create_params(params=json.dumps(params, url=url))


        return [path,url]
    

class APIRequester:
    def __init__(self, **kwargs):
        self.method = kwargs.get("method")
        self.url = kwargs.get("url")
        # self.headers = kwargs.get("headers")
        self.data = kwargs.get("data")
        self.auth = kwargs.get("auth")

    def get(self):
        headers = {
            "Authorization": f"Bearer {self.auth}"
        }
        response = requests.get(
            self.url,
            headers=headers,
        )
        return response


class Client(object):
    def __init__(self, version=None, env=None, environ=None):
        environ = environ or os.environ
        self.the_one_sdk_version = version
        self.env = env

        base_url = {
            "lotr": 'https://the-one-api.dev',
        }
        try:
            self.base_url = base_url['lotr']
        except AttributeError:
            raise Exception("a valid link as env")

        # Domains
        self._movie = None
        self._quote = None

    def request(self, method, base_url, domain, version, quote_id=None, movie_id=None, domain_id=None, domain_action=None, params=None, data=None, headers=None, auth=None):

        headers = headers or {}
        params = params or {}
        method = method.upper()

        path, url = PathBuilder(base_url=base_url, domain=domain, version=version, quote_id=quote_id,
                                movie_id=movie_id, domain_id=domain_id, domain_action=domain_action, params=params).build()

        print(f'Endpoint (url): \n{url}\n\n')
        api = APIRequester(url=url, auth="w-HYNs-_L5aETSI9VqEn")
        response = api.get()

        print(
            f'Response:\nStatus:\n{response.status_code}\nJson Response:\n{response.json()}'
        )
        json_response = response.json()
        return {
            "status": response.status_code,
            "json": json_response
        }

    @property
    def movie(self):
        """
        Access the did_sdk movie API
        """
        if self._movie is None:
            from rest.LOTR import Movie
            self._movie = Movie(
                self, self.base_url, 'movie', self.the_one_sdk_version)
        return self._movie

    @property
    def quote(self):
        """
        Access the did_sdk quote API
        """
        if self._quote is None:
            from rest.LOTR import Quote
            self._quote = Quote(
                self, self.base_url, 'quote', self.the_one_sdk_version)
        return self._quote

