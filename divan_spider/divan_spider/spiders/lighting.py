import scrapy

class LightingSpider(scrapy.Spider):
    name = "lighting"
    allowed_domains = ["divan.ru"]
    start_urls = ["https://www.divan.ru/kazan/category/svet"]

    # Переносим headers внутрь методов, либо задаем как словарь напрямую
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        divans = response.css('div._Ud0k')  # адаптируй под реальный HTML страницы

        for divan in divans:
            yield {
                'name': divan.css('div.lsooF span::text').get(),
                'price': divan.css('div.pY3d2 span::text').get(),
                'url': response.urljoin(divan.css('a::attr(href)').get())
            }

        # Пагинация
        next_page = response.css('a.Pagination-module__next::attr(href)').get()
        if next_page:
            yield scrapy.Request(url=response.urljoin(next_page), headers=self.headers, callback=self.parse)
