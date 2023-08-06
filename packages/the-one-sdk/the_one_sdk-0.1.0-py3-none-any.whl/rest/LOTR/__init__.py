class Movie:
    def __init__(self, the_one_sdk, base_url, domain, version, **kwargs):
        """Initialize the Lord of the Rings domain"""
        super().__init__()
        self.the_one_sdk = the_one_sdk
        self.base_url = base_url
        self.domain = domain
        self.version = version

    def get(self, params=None, data=None, headers=None, auth=None, movie_id=None, domain_id=None, domain_action=None):
        return self.the_one_sdk.request(
            'get',
            self.base_url,
            self.domain,
            self.version,
            params=params,
            data=data,
            headers=headers,
            auth=auth,
            movie_id=movie_id,
            domain_id=domain_id,
            domain_action=domain_action
        )

    def get_movie_quotes(self, movie_id):
        """
        Get quotes unique to a specific movie.
        """
        return self.get(movie_id=movie_id, domain_action="quote", domain_id=1)


class Quote:
    def __init__(self, the_one_sdk, base_url, domain, version, **kwargs):
        """Initialize the Lord of the Rings domain"""
        super().__init__()
        self.the_one_sdk = the_one_sdk
        self.base_url = base_url
        self.domain = domain
        self.version = version

    def get(self, params=None, data=None, headers=None, auth=None, quote_id=None, domain_id=None, domain_action=None):
        return self.the_one_sdk.request(
            'get',
            self.base_url,
            self.domain,
            self.version,
            params=params,
            data=data,
            headers=headers,
            auth=auth,
            quote_id=quote_id,
            domain_id=domain_id,
            domain_action=domain_action
        )
