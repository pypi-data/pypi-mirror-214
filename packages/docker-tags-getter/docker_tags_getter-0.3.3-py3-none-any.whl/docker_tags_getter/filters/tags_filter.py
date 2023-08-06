import re

class TagsFilter:
    def __init__(self):
        self._pattern = r'-\D\w+'
        self.regexp = re.compile(self._pattern)

    def check(self):
        return lambda tag: len(self.regexp.findall(tag)) == 0

    def filter_list(self, tags: list):
        return list(filter(self.check(), tags))

