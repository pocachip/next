import scrapy
import json
from urllib import parse
from scrapy.selector import Selector
from filesun.items import FilesunItem
from scrapy_playwright.page import PageMethod
from scrapy.http import FormRequest

class FilesunSpider(scrapy.Spider):
    name = "FileSun_org"
    allowed_domains = ["filesun.com"]

    custom_settings = {'DOWNLOAD_TIMEOUT': 10}

    def start_requests(self):
        yield scrapy.Request(
            url = "https://filesun.com",
            meta={
                'playwright':True,
                'playwright_include_page': True,
                'playwright_page_methods':  [
                    PageMethod('wait_for_selector', 'tbody#contents_list'),
                ],
                'playwright_context_kwargs': {
                    "ignore_https_errors": True,
                },
                "errback": self.errback,
            },
            callback=self.parse,
        )

    async def parse(self, response):
        url = "https://filesun.com/disk/1?category=2"
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', 
        'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7', 'Cache-Control': 'max-age=0', 'Cookie':'SUNSSID=angsigbknbfidlk4d457420975; _ga=GA1.1.1774650834.1690453640; wcs_bt=540bc5ea0a185c:1690454185; _ga_M4ZBDTM067=GS1.1.1690453639.1.1.1690454185.0.0.0; _ga_8QXW6WZFW3=GS1.1.1690453640.1.1.1690454185.0.0.0', 'Sec-Ch-Ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"', 'Sec-Ch-Ua-Mobile': '?0', 'Sec-Ch-Ua-Platform': "Windows", 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'none', 'Sec-Fetch-User': '?1', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
        yield FormRequest(url, 
            method = "GET", 
            headers = headers,
            callback=self.Parse_Item,
            )
    
    async def Parse_Item(self, response):
        print('Parse_Item===============================start'+response.url)
        if response.status != 200:
            print(response.status)
            self.stopflag = True

        pagingPart = response.xpath('//div[@id="commonPaginate1"]')
        next_page = pagingPart.css('a.nextBtn').xpath("./@href").re("javascript:movePage\((.+?)\);")

        print(next_page)
        cat1 = "1"
        cat2 = "2"
        pagen = "11"
        url_org = '/%s?category=%s&page=%s'% (cat1, cat2, pagen)
        url_next = parse.urljoin(response.url, url_org)
        print(url_next)
        return
#        yield scrapy.Request(
#            url = url_next2,
#            meta={
#                'playwright':True,
#                'playwright_include_page': True,
#                'playwright_page_methods':  [
#                    PageMethod('wait_for_selector', 'tbody#contents_list'),
#                ],
#                'playwright_context_kwargs': {
#                    "ignore_https_errors": True,
#                },
#                "errback": self.errback,
#            }
#            callback=self.parse,
#        )


    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()