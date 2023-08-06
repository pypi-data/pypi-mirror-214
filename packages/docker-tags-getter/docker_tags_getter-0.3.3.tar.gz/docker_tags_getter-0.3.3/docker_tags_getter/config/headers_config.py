class HeadersConfig:
    _HEADERS = {
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0'
    }

    def get_headers(self):
        return self._HEADERS

