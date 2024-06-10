import time

import scrapy, json


class DramthscrapySpider(scrapy.Spider):
    name = "DramThScrapy"
    allowed_domains = ["mdt-dodin.ru", "mdtdodin.core.ubsystem.ru"]

    def __init__(self, event_url=None, *args, **kwargs):
        super(DramthscrapySpider, self).__init__(*args, **kwargs)
        self.event_url = event_url

    def start_requests(self):
        if self.event_url:
            if "?event=" in self.event_url:
                yield scrapy.Request(url=self.event_url, callback=self.get_link)
            elif "buy-tickets" in self.event_url:
                id = self.event_url.split("/")
                yield scrapy.Request(
                    url="https://mdtdodin.core.ubsystem.ru/uiapi/event/scheme?id=" + str(id[len(id) - 1]),
                    callback=self.parse)
            else:
                print("Введите ссылку на мероприятие.")
        else:
            print("Введите ссылку на мероприятие.")

    def get_link(self, response):
        href = "https://www.mdt-dodin.ru" + response.css('div.visible-lg a').attrib['href']
        yield scrapy.Request(url=href, callback=self.parse_all_dates)

    def parse_all_dates(self, response):
        print("Отправка пост запроса")
        ids = response.css('li.performance-afisha__buy::attr(data-hwm-event-id)').getall()

        yield scrapy.Request(
            url="https://mdtdodin.core.ubsystem.ru/uiapi/event/sale-status",
            method='POST',
            headers={
                'Accept': '*/*',
                'Accept-Encoding:': 'gzip, deflate, br, zstd',
                'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                'Content-Type': 'application/json;charset=UTF-8',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
            },
            body=json.dumps({
                'ids': ids
            }),
            callback=self.actual_sell
        )

    def actual_sell(self, response):
        data = response.json()
        allows = []
        ids = []
        for item in data:
            allows.append(data[item]["salesAvailable"])
            ids.append(data[item]["id"])

        for x in allows:
            if x == False:
                ind = allows.index(x)
                ids.pop(ind)

        if ids == []:
            print("Список мероприятий пуст")
        else:
            for id in ids:
                yield scrapy.Request(url="https://mdtdodin.core.ubsystem.ru/uiapi/event/scheme?id=" + str(id),
                                     callback=self.parse)

    def parse(self, response):
        id = response.url.split("id=")[1]
        data = response.json()["seats"]
        for myitem in data:
            if myitem["htmlTitle"] == "Место недоступно":
                pass
            else:
                yield {
                    "sector": myitem["areaTitle"],
                    "row": myitem["row"],
                    "seat": myitem["seat"],
                    "price": myitem["price"],
                    "count": 1,
                    "id": id
                }