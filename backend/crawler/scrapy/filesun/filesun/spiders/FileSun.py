import scrapy
import json
import re
from datetime import datetime, timedelta
import time
from scrapy.selector import Selector
from filesun.items import FilesunItem 
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser 
from scrapy_playwright.page import PageMethod
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
#from crawlab import save_item #for Crawlab
import scrapy.utils.misc
import scrapy.core.scraper
from urllib.parse import urljoin
import w3lib.html

def innertext_quick(elements, delimiter=""):
    return list(delimiter.join(el.strip() for el in element.css('*::text').getall()) for element in elements)

class FilesunSpider(scrapy.Spider):
    name = "filesun"
    custom_settings = {
        'DOWNLOAD_TIMEOUT': 10,
        'FEED_EXPORT_ENCODING' : 'utf-8',
        }

    def warn_on_generator_with_return_value_stub(spider, callable):
        pass

    scrapy.utils.misc.warn_on_generator_with_return_value = warn_on_generator_with_return_value_stub
    scrapy.core.scraper.warn_on_generator_with_return_value = warn_on_generator_with_return_value_stub

    def __init__(self, category='', subsec='', *args, **kwargs):
        super(FilesunSpider, self).__init__(*args, **kwargs)
        self.category = category
        self.subsec = subsec

    start_urls = ["https://m.filesun.com/login.php"]
    
    def parse(self, response):
#        print("parse fn")
        inputs = response.css('div.myLoginpage>section.loginform>form>div>input')
        formdata = {}
        for input in inputs:
            name = input.css('::attr(name)').get()
            value = input.css('::attr(value)').get()
            if name:
                formdata[name] = value
#                print("name:" + str(name) + "   value:"+str(value))
        formdata['id'] = 'mediamo'
        formdata['password'] = 'media123!'
        formdata['passsave'] = '0'
        formdata['autosave'] = '0'
        formdata['out'] = 'xml'
        return scrapy.FormRequest.from_response(
            response,
            formdata=formdata,
            dont_click=True,
            callback=self.after_login,
        )

    def after_login(self, response):
        #print("after_login!!! rediect!!")
        yield scrapy.Request(url="https://m.filesun.com/", callback=self.parseMenu)

    def parseMenu(self, response):
#        print("parseMenu"+response.url)

#https://m.filesun.com/?all_promotion=1
#https://m.filesun.com/disk/1?hotlist=cp&listmode=all
#https://m.filesun.com/disk/1
        category1 = response.xpath('//div[@id="diskSnb"]/ul/li')
        for cat1_item in category1:
            cat1_name = cat1_item.css('a::text').get()
            cat1_url = cat1_item.css('a::attr(href)').get()
            fstr1_index = cat1_url.find('disk/')
            if (fstr1_index > 0) and ("hotlist" not in cat1_url[fstr1_index+5:]): 
                cat1_code = cat1_url[fstr1_index+5:]
                cat1_name = cat1_item.css('a::text').get()
#                print(cat1_code+"->"+cat1_url+">"+cat1_name)
                if self.category:
                    if cat1_code not in self.category:
                        continue
                else:
                    hackMenu =["1","2", "3", "5",] #hack by pocachip
                    #hackMenu =["MVO",] #hack by pocachip
                    if cat1_code not in hackMenu:
                        continue
                yield scrapy.Request( url=cat1_url, 
                                      meta={
                                          "cat1_name": cat1_name,
                                          "cat1_code": cat1_code,
                                      },
                                      errback = self.errback,
                                      callback=self.parseMenu2)

    def parseMenu2(self, response):
#        print("parseMenu2"+response.url)
        cat1_name = response.meta["cat1_name"]
        cat1_code = response.meta["cat1_code"]

        category2 = response.xpath('//div[@id="diskSnb2"]/ul/li')
        for cat2_item in category2:
            cat2_url = cat2_item.css('a::attr(href)').get()
            cat2_name = cat2_item.css('a::text').get()
            fstr2_index = cat2_url.find('category=')
            if fstr2_index > 0: #javascript 성인 처리
                #1. test 
                cat2_code = cat2_url[fstr2_index+9:]
#                print(cat2_code+"->"+cat2_url+">"+cat2_name)
                if self.subsec:
                    if cat2_code not in self.subsec:
                        continue
            else:
                break # skip while don't have 'catergory=?' ..it's maybe Javacript for audult authentication

            cat2_url  = urljoin('https://filesun.com',cat2_url)
            yield scrapy.Request(
                url = cat2_url, 
                meta={
                    "cat1_name": cat1_name,
                    "cat2_name": cat2_name,
                    "cat1_code": cat1_code,
                    "cat2_code": cat2_code,
                },
                errback = self.errback,
                callback=self.Parse_Page,
            )

    def Parse_Page(self, response):
        cat1_name = response.meta["cat1_name"]
        cat2_name = response.meta["cat2_name"]
        cat1_code = response.meta["cat1_code"]
        cat2_code = response.meta["cat2_code"]
#        print('Page_Page start!! url:'+response.url)
        #print(cat1_name+'('+ cat1_code + ')' + cat2_name+'/('+ cat2_code+')')
        if response.status != 200:
            print(response.status)
            return
#check start
        bbs_table = response.xpath('//ul[@id="articleSelectUl"]')
        for bbs_line in bbs_table.xpath("li"):  
            item_url = bbs_line.css('a::attr(href)').get()
#https://m.filesun.com/disk/1/111111611?category=2
#https://m.filesun.com/disk/3/111112738?category=1
            attach_file_size = bbs_line.css('a>span.thumb>span.size::text').get()
            chk_lvl19 = bbs_line.css('a>strong.subject>p.iconAdult')
            if chk_lvl19:
                Lvl19 = True
            else:
                Lvl19 = False 
#            idx = bbs_line.xpath("a/@href").re("\?m=(.+?)&")
            ids_str = w3lib.html.remove_tags(bbs_line.xpath("a/@href").get().strip())
#            print("=======================")
#            print(item_url)
            idx = ""
            regex = re.compile(r'/(\d+)\?')
            mo = regex.search(item_url)
            if mo: 
                idx =  mo.group(1)
        
            #txt = bbs_line.css('a>strong.subject::text').get()
            t_txt = bbs_line.css('a>strong.subject')
            
            t2_txt = innertext_quick(t_txt, delimiter="")
            txt = t2_txt[0]


            point_size = bbs_line.css('a>span.price>span.default::text').get()
            seller = "" #비제휴라 pop 안뛰고고 null 처리
            partner = "" #비제휴라 pop 안뛰고고 null 처리
            
            bbs_item = FilesunItem()
            bbs_item["website"] = 2 
            bbs_item["cat1_code"] = cat1_code 
            bbs_item["cat2_code"] = cat2_code
            bbs_item["category_title"]  = cat1_name 
            bbs_item["sub_category_title"]  =  cat2_name
            bbs_item["idxs"] = idx
            bbs_item["txt"]  = txt 
            bbs_item["Lvl19"] = Lvl19
            bbs_item["point"]  = point_size
            bbs_item["seller"]  = seller
            bbs_item["partner"]  = partner 
            bbs_item["attach_file_size"] = attach_file_size
            bbs_item["item_url"] = item_url

            now = datetime.now() + timedelta(days=10)
            #now = datetime.datetime.now()
            a_str = now.strftime('%Y-%m-%d %H:%M:%S')
            #print(a_str) # 👉️ 2023-07-19 17:47:16
            json_str = json.dumps(a_str)
            #print(json_str) # 👉️ "2023-07-19 17:47:16"
            bbs_item["time"] = json_str

    #       save_item(bbs_item) #for crawlab
            yield bbs_item
#            item_pop_url  = urljoin('https://filesun.com',item_url)
##                headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Host': 'filesun.com', 'Pragma': 'no-cache', 'Referer': 'https://filesun.com/', 'Sec-Ch-Ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"', 'Sec-Ch-Ua-Mobile': '?0', 'Sec-Ch-Ua-Platform': '"Windows"', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-User': '?1', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
#            yield scrapy.Request(
#                url = item_pop_url, 
#                meta={
#                    "errback": self.errback,
#                    "cat1_name": cat1_name,
#                    "cat2_name": cat2_name,
#                    "cat1_code": cat1_code,
#                    "cat2_code": cat2_code,
#                    "idx": idx,
#                    "txt": txt,
#                    "Lvl19": Lvl19,
#                },
#                callback=self.Page_Item,
#            )
#
        #하단 Next ">" 버튼 있을시에 10page 점프를 위한 새로운 Parse_Page Call
        pagings = response.xpath('//nav[@class="pagingTypeMobile"]/a')
        has_next = False
        nxpage = ""
        last_page_n = 0
        cur_page_s = ""
        for page in pagings:
            classtype = page.css('::attr(class)').get()
            if classtype == "page":
                pagestr = page.css('::text').get()
                last_page_n = int(pagestr)
            elif classtype == "nowpage":
                cur_page_s = page.css('::text').get()
                cur_page_n = int(cur_page_s)
            elif classtype == "next":
                has_next = True
                
        #print("curpage:"+cur_page_s)
        if not has_next and (cur_page_n > last_page_n):
            print('this is last page')
        else:
            #print('page big nuber is'+str(last_page_n))
            cur_page_n = cur_page_n + 1
            next_page_s = str(cur_page_n)
            #print("curpage()"+cur_page_s+")->go page("+next_page_s+")")
            new_url = 'https://filesun.com/disk/%s?cateogry=%s&page=%s' % (cat1_code, cat2_code, next_page_s)
            #print("nexturl:"+new_url)
            yield scrapy.Request(
                url = new_url, 
                meta={
                    "errback": self.errback,
                    "cat1_name": cat1_name,
                    "cat2_name": cat2_name,
                    "cat1_code": cat1_code,
                    "cat2_code": cat2_code,
                },
                callback=self.Parse_Page,
            )

    async def Page_Item(self, response):
        if response.status != 200:
            print("Page_Item Faild!!!!!")
            print(response.status)

        page = response.meta["playwright_page"]

        content = await page.content()
        sel = Selector(text=content)
        await page.close()

        cat1_name = response.meta["cat1_name"]
        cat2_name = response.meta["cat2_name"]
        cat1_code = response.meta["cat1_code"]
        cat2_code = response.meta["cat2_code"]
        idx = response.meta["idx"]
        txt = response.meta["txt"]
        Lvl19 = response.meta["Lvl19"]

        point_size = sel.css('span.pointSize').get().split(" / ")
        point  = point_size[0]  
        attach_file_size = point_size[1]
        seller = sel.css('span.commonNickName')

        # 제휴 아이콘 유무로 판단
        part_f = sel.css('td.title')
        part_img = part_f.css('img::attr(src)').get()
        if part_img:
            partner = "True"
        else:
            partner = "False"
        print('Page_Page===============================start'+response.url)
        #print('cat1:'+ cat1_code + '   cat2:' + cat2_code)
        bbs_item = FilesunItem()
        bbs_item["website"] = 2 
        bbs_item["cat1_code"] = cat1_code 
        bbs_item["cat2_code"] = cat2_code
        bbs_item["category_title"]  = cat1_name 
        bbs_item["sub_category_title"]  =  cat2_name
        bbs_item["idxs"] = idx
        bbs_item["txt"]  = txt 
        bbs_item["Lvl19"] = Lvl19
        bbs_item["point"]  = point_size
        bbs_item["seller"]  = seller
        bbs_item["partner"]  = partner 
        bbs_item["attach_file_size"] = Lvl19

        now = datetime.now() + timedelta(days=10)
        #now = datetime.datetime.now()
        a_str = now.strftime('%Y-%m-%d %H:%M:%S')
        #print(a_str) # 👉️ 2023-07-19 17:47:16
        json_str = json.dumps(a_str)
        #print(json_str) # 👉️ "2023-07-19 17:47:16"
        bbs_item["time"] = json_str

#        save_item(bbs_item) #for crawlab
        yield bbs_item

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()

        self.logger.error(repr(failure)) 

        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error("HttpError on %s", response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error("DNSLookupError on %s", request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error("TimeoutError on %s", request.url)