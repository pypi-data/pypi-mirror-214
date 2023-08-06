class RepositoriesAPI:
    def __init__(self, fetcher, namespace):
        self._fetcher = fetcher
        self._url = f"https://hub.docker.com/v2/namespaces/{namespace}/repositories/"

    def get_list(self):
        repos = []
        number = 1

        while True:
            page_url = f"{self._url}?page={number}"
            status, json_data = self._fetcher.get(page_url)

            results = json_data["results"]

            names = list(map(lambda element:element["name"], results))
            repos += names

            # check for next page
            next_page = json_data['next']

            if next_page is None:
                break

            number+=1

        return repos

