import scrapy
from scrapy_playwright.page import PageMethod


class OndiskSpider(scrapy.Spider):
    name = 'ondisk_1'

    def start_requests(self):
        yield scrapy.Request( 
            url="https://www.ondisk.co.kr/index.php?mode=ondisk&search_type=MVO&sub_sec=MVO_011",
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_context_kwargs= {
                    "ignore_https_errors": True,
                },
#                playwright_page_methods=[
#                    PageMethod("wait_for_selector", "tbody#contents_list"),
#                ],
            ),
        )

    async def parse(self, response):
        #for item in response.css('tbody#content.list'):
        #    yield {
        #        'title': item.css('tr>td.subject a:last-child[title]').extract()
        #    }
        #search_type = response.xpath('//tbody[@id="search_type"]').getall()
        #item = response.css('tbody#content.list')
        self.log('===========')
        self.log(response.text)
        self.log('===========')