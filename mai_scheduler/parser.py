from requests import get
from lxml import html

from mai_scheduler.types import Schedule


class Parser:
    def __init__(self, version_group, **kwargs):
        self.url_pattern = 'https://mai.ru/education/schedule/detail.php?group={group}&week={week}'
        self.version_group = version_group
        self._version = kwargs.get('v', None)

    @property
    def has_update(self):
        return self._version != self.__remote_version()

    def update(self):
        # product = 
        pass

    @property
    def version(self):
        if not self._version:
            self._version = self.__remote_version()
        return self._version

    def __request(self, url: str) -> str:
        return get(url).content.decode('utf8')

    def __remote_version(self):
        body = self.__request('https://mai.ru/education/schedule/detail.php?group={group}'
                              .format(group=self.version_group))
        tree = html.fromstring(body)
        return tree.xpath('//*[@id="schedule-content"]/div[2]/text()')[0]


