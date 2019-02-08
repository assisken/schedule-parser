import asyncio
import json

import aiohttp
import requests
from lxml import html

from parser.config import GROUP_CHECK_URL, GROUP_SCHEDULE_URL, VERSION_CHECK_URL, SAVE_PATH
from .coroutine import fetch


class Manager:
    """Класс, объект которого контролирует процесс записи данных в файл и обрабатывает корутины-парсеры"""

    __loop = asyncio.get_event_loop()
    __schedule = {
        'version': None,
        'data': []
    }

    require_update = True
    require_file_update = False
    new_version = None

    def __init__(self):
        """При инициализации объекта происходит загрузка данных с файла, проверка свежей версии обновления."""

        self.__load()
        version = self.__check_version()
        if version == self.__schedule['version']:
            self.require_update = False
        self.new_version = version

    def __load(self) -> None:
        """Загрузка файла."""
        try:
            with open(SAVE_PATH, 'r') as file:
                self.__schedule = json.loads(file.read())
        except FileNotFoundError:
            return

    @staticmethod
    def __check_version():
        """Процесс проверки версии нового расписания."""

        response = requests.get(VERSION_CHECK_URL)
        if response.status_code != 200:
            # TODO: обработать исключение, если сайт, внезапно, не доступен на время проверки расписания
            pass

        tree = html.fromstring(response.content.decode('utf-8'))
        response.close()

        version = tree.xpath('//*[@id="schedule-content"]/div[2]/text()')[0]
        return version

    def __added_groups(self, *groups: str):
        """Находит группы, которые были указаны при запуске, но не были найдены в файле.
        Назовём это «дельта групп»
        """
        added_groups = []
        saved_groups = [data['group'] for data in self.__schedule['data']]
        for group in groups:
            if group not in saved_groups:
                added_groups.append(group)

        return added_groups

    async def __run_parsing(self, *groups: str):
        """Служебная функция для запуска корутин.
        Сами корутины должны парсить сайт с расписанием, где каждая корутина парсит свою отдельную группу.
        """
        async with aiohttp.ClientSession() as session:
            tasks = [
                fetch(session, group=group, url=GROUP_SCHEDULE_URL) for group in groups
            ]
            done, _ = await asyncio.wait(tasks)

        for task in done:
            self.__schedule['data'].append({
                'group': task.result()[1],
                'weeks': task.result()[0]
            })

    def run(self, *all_groups: str):
        """Публичная команда для запуска всего процесса парсинга.
        Ничего не сделает, если не требуется обновление ИЛИ если дельта групп пуста.
        """
        new_groups = self.__added_groups(*all_groups)
        if not (self.require_update or new_groups):
            return

        if self.require_update:
            groups = all_groups
        else:
            groups = new_groups

        if self.__loop.is_closed():
            raise Exception

        response = requests.get(GROUP_CHECK_URL)
        html = response.content.decode('utf-8')
        for group in all_groups:
            if group not in html:
                self.__schedule['data'].append({
                    'group': group,
                    'weeks': None
                })

        self.__loop.run_until_complete(self.__run_parsing(*groups))
        self.__loop.close()

        self.__schedule['version'] = self.new_version
        self.require_file_update = True

    def save(self):
        """Сохранение данных в json.
        Ничего не сделает, если обновление файла не требуется.
        """
        if not self.require_file_update:
            return

        with open(SAVE_PATH, 'w') as file:
            file.write(json.dumps(self.__schedule, ensure_ascii=False, indent=2))
