import scrapy
import json
from scrapy.selector import Selector
from ondisk.items import OndiskItem
from scrapy_playwright.page import PageMethod
from scrapy.http import FormRequest


class OndiskSpider(scrapy.Spider):
    name = "ondisk1"
    custom_settings = {'DOWNLOAD_TIMEOUT': 10}

    def start_requests(self):
        yield scrapy.Request(
            url = 'https://www.ondisk.co.kr/index.php?mode=ondisk&search_type=MVO&sub_sec=MVO_011',
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
        page = response.meta["playwright_page"]

        content = await page.content()
        sel = Selector(text=content)

        this_page_num = sel.xpath('//input[@name="this_page"]/@value').get()
        print ('<-----------')
        print(this_page_num)
        print ('<-----------')
        fullMenu = sel.xpath('//div[@id="js-fullMenuLayer"]//dl[@class="menu"]')
        for menu in fullMenu:
            ##print(menu.get())
            f1_link = menu.css('dt>a::attr(href)').get()
            if f1_link.find('search_type=') > 0:
                cat1_code = f1_link[-3:]
                cat1_title = menu.css('a::text').get()

                CatMenu2 = menu.css('dd')
                for menu2 in CatMenu2:
                    f2_link = menu2.css('a::attr(href)').get()
                    if f2_link.find('sub_sec=') > 0:
                        cat2_code = f2_link[-7:]
                        cat2_title = menu2.css('a::text').get()
                        print(cat1_code+'>'+cat2_code+':'+cat1_title+'>'+cat2_title+'\n')
                        cur_page_s = response.xpath('//input[@name="this_page"]/@value').get()
                        tot_page_s = response.xpath('//input[@name="last_page"]/@value').get()
                        cur_page_n = int(cur_page_s)
                        tot_page_n = int(tot_page_s)
                        tot_page_n = 2

                        #if m_cur_page is None:
                        while cur_page_n < tot_page_n:
                            #1. test 
                            url = "https://www.ondisk.co.kr/main/module/bbs_list_sphinx_prc.php"
                            cur_page_s =str(cur_page_n)
                            headers = {'Accept': 'application/json, text/javascript, */*; q=0.01', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Host': 'www.ondisk.co.kr', 'Pragma': 'no-cache', 'Referer': 'https://www.ondisk.co.kr/index.php?mode=ondisk&search_type=MVO&sub_sec=MVO_011', 'Sec-Ch-Ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"', 'Sec-Ch-Ua-Mobile': '?0', 'Sec-Ch-Ua-Platform': '"Windows"', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36', 'X-Requested-With': 'XMLHttpRequest'}
                            yield FormRequest(url, 
                                method = "GET", 
                                headers = headers,
                                formdata={
                                    'mode': 'ondisk', 
                                    'list_row': '20' , 
                                    'page': cur_page_s,  
                                    'search_type': cat1_code, 
                                    'search_type2': 'title', 
                                    'sub_sec': cat2_code, 
                                    'search': '', 
                                    'hide_adult': 'N' , 
                                    'blind_rights': 'N' , 
                                    'sort_type': 'default' , 
                                    'sm_search': '',  
                                    'plans_idx':'' 
                                    }, 
                                callback=self.Page_Item, 
                            )
                            cur_page_n += 1
                            print(cat1_code+'>'+cat2_code+':'+cat1_title+'>'+cat2_title+':'+cur_page_s+'/'+tot_page_s+'\n')
                    else:
                        break # temporary block by pocachip 
            else:
                break

    async def Page_Item(self, response):
        #print('Page_Item===============================start')
        if response.status != 200:
            print(response.status)
            self.stopflag = True
#        res = response.body
        j_response = json.loads(response.text)
        bbs_body = Selector(text=j_response["list"])

        category_title = j_response["category_title"]# #"영화"
        #idx_arr = Selector(text=j_response["idx_arr"]) #79753592,94526455,94526405,94427787,94427805,94427864,89798916,94427926,89797570,94326621,94326505,94326482,94242545,94242466,94242640,87030087,91976509,94792828,89797589,87030071

        cat1 = j_response["search_type"] # "MVO"
        sub_category_title = j_response["sub_category_title"] #고화질HD
        #tpage = Selector(text=j_response["tpage"]) # 308
        #print(j_response["list"])
        #cat2 = Selector(text=j_response["sub_sec"])

        for bbs_line in bbs_body.xpath("//tr[not(@*)]"):  
            # blank line skip
            chk_line = bbs_line.css('td.sumy_view').get()
            if chk_line :
                continue

            bbs_item = OndiskItem()
            bbs_item['cat1'] = category_title
            bbs_item['cat2'] = sub_category_title
            #print ('    '+category_title+'>'+sub_category_title+':\n')
            bbs_item['idx'] = bbs_line.css('td.check>span.summy_brd>input::attr(value)').get()
            bbs_item['txt'] = bbs_line.css('td.subject>span.summy_brd>a.summy_link>span.textOverflow>span.txt>span::text').get()
            #bbs_item['Lvl19'] = bbs_line.css('td.subject>span.summy_brd>a.summy_link>span.textOverflow>img').get()
            if bbs_line.css('td.subject>span.summy_brd>a.summy_link>span.textOverflow>img').get():
                bbs_item['Lvl19'] = True
            else:
                bbs_item['Lvl19'] = False
            #print('<<<<<<<<<<<<<<<<<')
            #print(bbs_item)
            yield bbs_item

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()