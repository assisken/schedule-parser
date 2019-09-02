import asyncio
import dataclasses
from random import choices
from typing import List
from urllib.parse import quote

from aiohttp import ClientSession, ClientResponse
from lxml import html
from lxml.html import HtmlElement

from parser.types import Item, Week, Day


async def fetch(session: ClientSession, group: str, url: str):
    res = []
    for week in range(1, 19):
        url = url.format(group=quote(group), week=week)
        response: ClientResponse = await session.get(url)
        code = response.status
        body = await response.text('utf-8')
        response.close()

        if code != 200:
            print(code, group, week, url)
            return None, None

        data = parse_table(week, body)
        res.append(
            dataclasses.asdict(data)
        )

        await asyncio.sleep(1)

    return res, group


def parse_table(week: int, body: str) -> Week:
    tree = html.fromstring(body)
    days: List[Day] = []
    for element in tree.xpath('//div[@class="sc-container"]'):
        date = element.xpath(
            './/div[contains(@class, "sc-day-header")]/text()')[0]
        day = element.xpath('.//span[@class="sc-day"]/text()')[0]
        items = element.xpath(
            './/div[contains(@class, "sc-table-detail")]')[0]

        days.append(
            Day(date=date, day=day, items=parse_items(items))
        )
    return Week(week=week, days=days)


def parse_items(element: HtmlElement) -> List[Item]:
    res: List[Item] = []
    for item in element.xpath('.//div[@class="sc-table-row"]'):
        time = item.xpath(
            './/div[contains(@class, "sc-item-time")]/text()')[0]
        item_type = item.xpath(
            './/div[contains(@class, "sc-item-type")]/text()')[0]
        place = item.xpath(
            './/div[contains(@class, "sc-item-location")]/text()')[0]
        name = item.xpath('.//*[@class="sc-title"]/text()')[0]
        try:
            teachers = item.xpath(
                './/span[@class="sc-lecturer"]/text()')[0].split(', ')
        except IndexError:
            teachers = []
        item = Item(time=time,
                    item_type=item_type,
                    name=name,
                    place=place,
                    teachers=teachers)
        print(item)
        res.append(item)
    return res
