import scrapy
import json
import re
from datetime import datetime, timedelta
import time
from scrapy.selector import Selector
from ondisk.items import OndiskItem
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser 
from scrapy_playwright.page import PageMethod
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
from crawlab import save_item #for Crawlab
import scrapy.utils.misc
import scrapy.core.scraper

class OndiskSpider(scrapy.Spider):
    name = "ondisk"

    custom_settings = {
        'DOWNLOAD_TIMEOUT': 10,
        #'FEEDS': { 'data/%(name)s_' + datetime.datetime.today().strftime('%y%m%d')+'.csv': {"format": "csv"}},
        #'FEEDS_URI' : 'data/%(name)s_' + datetime.datetime.today().strftime('%y%m%d')+'.csv',
        #'FEED_FORMAT': 'csv', 
        #'FEED_EXPORTERS':{
                #'csv':'scrapy.exporters.CsvItemExporter',
        #},
        'FEED_EXPORT_ENCODING' : 'utf-8',
    }

    def warn_on_generator_with_return_value_stub(spider, callable):
        pass

    scrapy.utils.misc.warn_on_generator_with_return_value = warn_on_generator_with_return_value_stub
    scrapy.core.scraper.warn_on_generator_with_return_value = warn_on_generator_with_return_value_stub

    def __init__(self, category='', subsec='', *args, **kwargs):
        super(OndiskSpider, self).__init__(*args, **kwargs)
        self.category = category
        self.subsec = subsec

    def start_requests(self):
        yield scrapy.Request(
            url="https://www.ondisk.co.kr/index.php",
            callback=self.parse,
        )        

    def parse(self, response):
        self.category = getattr(self, 'category', '')
        self.subsec = getattr(self, 'subsec', '')

        inputs = response.css('form[name="loginFrm"] input') 
        formdata = {}
        for input in inputs:
            name = input.css('::attr(name)').get()
            value = input.css('::attr(value)').get()
            formdata[name] = value
        formdata['mb_id'] = 'whenicu'
        formdata['mb_pw'] = 'paim0321!'
#        print(formdata)
        yield scrapy.FormRequest.from_response(response,
                          formdata=formdata,
                          callback=self.parseMenu,
                          dont_filter=True,
                          meta={"playwright": True, 
                                "playwright_include_page": True,
                                "playwright_page_methods" : [
                                    PageMethod('click', selector='a#gnb_button'),
                                    PageMethod('wait_for_selector', 'div#js-fullMenuLayer'),
                                ],
                               },
                          )

    async def parseMenu(self, response):
        page = response.meta["playwright_page"]
        content = await page.content()
        sel = Selector(text=content)
#       await page.context.close()

#        loginName = sel.xpath('//div[@id="page-loginWrap"]//p[@class="name"]').get()
#        print(loginName)

        fullMenu = sel.xpath('//div[@id="js-fullMenuLayer"]//dl[@class="menu"]')

        for menu in fullMenu:
            f1_link = menu.css('dt>a::attr(href)').get()
            if f1_link.find('search_type=') > 0:
                cat1_code = f1_link[-3:]
                if self.category:
                    if cat1_code not in self.category:
                        continue
                else:
                    hackMenu =["MVO","DRA", "MED", "ANI",] #hack by pocachip
                    #hackMenu =["MVO",] #hack by pocachip
                    if cat1_code not in hackMenu:
                        continue

                cat1_title = menu.css('a::text').get()
                CatMenu2 = menu.css('dd')
                for menu2 in CatMenu2:
                    f2_link = menu2.css('a::attr(href)').get()
                    if f2_link.find('sub_sec=') > 0:
                        cat2_code = f2_link[-7:]
                        cat2_title = menu2.css('a::text').get()
                        #hackSubMenu =["MVO_013",] #hack by pocachip
                        #if cat2_code not in hackSubMenu:
                            #continue
                        if self.subsec:
                            if cat2_code not in self.subsec:
                                continue
                        #print("call>>>>"+cat1_code+"..."+cat2_code)
                        cat_url = "https://ondisk.co.kr/index.php?mode=ondisk&search_type="+cat1_code+"&sub_sec="+cat2_code
                        yield scrapy.Request(
                            url=cat_url,
                            callback=self.getCategoryCnt,
                            errback=self.errback,
                            dont_filter=True,
                            meta={
                                  "playwright": True, 
                                  "playwright_include_page": True,
                                  "playwright_context_kwargs": {
                                     "ignore_https_errors": True,
                                  },
                                  "playwright_page_methods" : [
                                      #PageMethod("wait_for_load_state", "networkidle"),
#                                      PageMethod('wait_for_selector', 'div#page-footer'),
                                      PageMethod('wait_for_selector', 'ul#list_order_btn'),
                                      PageMethod('wait_for_selector', 'tbody#contents_list'),
##                                      PageMethod("evaluate", "window.scrollBy(0, document.body.scrollHeight)"),
                                  ],
                                  "cat1_code": cat1_code,
                                  "cat2_code": cat2_code,
                                  "max_retry_times" : 5, 
                                 },
                        )        

    async def getCategoryCnt(self, response):
        page = response.meta["playwright_page"]
        content = await page.content()
        cat1_code = response.meta["cat1_code"]
        cat2_code = response.meta["cat2_code"]
        sel = Selector(text=content)

        last_page =  sel.css('form>input#last_page::attr(value)').get() 
        change = False
        current ='dafault'
        for order in sel.xpath('//ul[@id="list_order_btn"]/li'):
            order_str = order.css('a::text').get()
            order_cur = order.css('a::attr(class)').get()
            order_link = order.css('a::attr(href)').get()
            if order_cur:
                m = re.search(r"javascript:doSortType\(\'(.*?)\'\);", order_link)
                if m:
                    current=m.group(1)
                    if (current == 'new_rank') or (current =='30day_comment'):
                        change = True
                        await page.click('ul#list_order_btn>li:nth-child(1)>a')
                        print("click!!")
                        content = await page.content()

        #if not change:
        #    await page.close()
            
#        last_page =  sel.css('form>input#last_page::attr(value)').get() 
#        print(cat2_code + ":"+ last_page) 
        url = "https://www.ondisk.co.kr/main/module/bbs_list_sphinx_prc.php"
        headers = {'Accept': 'application/json, text/javascript, */*; q=0.01', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Host': 'www.ondisk.co.kr', 'Pragma': 'no-cache', 'Referer': response.url, 'Sec-Ch-Ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"', 'Sec-Ch-Ua-Mobile': '?0', 'Sec-Ch-Ua-Platform': '"Windows"', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36', 'X-Requested-With': 'XMLHttpRequest'}
#        print("getCategoryCnt:"+headers['Referer'])
        await page.close()  
        yield FormRequest(url, 
            method = "GET", 
            headers = headers,
            errback=self.errback,
            dont_filter=True,
            formdata={
                'mode': 'ondisk', 
                'list_row': '20' , 
                'page': '1',  
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
            callback=self.parseCategory,
        )

    def parseCategory(self, response):
        if response.status != 200:
            #print("Page_Item Faild!!!!!")
            print(response.status)
        j_response = json.loads(response.text)
        bbs_body = Selector(text=j_response["list"])
        #idx_arr = Selector(text=j_response["idx_arr"]) #79753592,94526455,94526405,94427787,94427805,94427864,89798916,94427926,89797570,94326621,94326505,94326482,94242545,94242466,94242640,87030087,91976509,94792828,89797589,87030071
        cat1_code = j_response["search_type"] # "MVO"
        cat2_code = ''
        m = re.search(r"sub_sec=(.*?)&", response.url)
        if m:
            cat2_code=m.group(1)
        else:
            print("Page_Item func fail to cat2_code!!!!!!!!!!!!!!!!!!!!!!!")
        
        cur_page_n = 1
        tot_page_n = j_response["tpage"] # "MVO"

        #await page.close()
        #if m_cur_page is None:
        while cur_page_n <= tot_page_n:
            #print("=====================================================")
            #print(cat1_code+'>'+cat2_code+':('+str(cur_page_n)+'/'+str(tot_page_n))
            url = "https://www.ondisk.co.kr/main/module/bbs_list_sphinx_prc.php"
            cur_page_s =str(cur_page_n)
            headers = {'Accept': 'application/json, text/javascript, */*; q=0.01', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Host': 'www.ondisk.co.kr', 'Pragma': 'no-cache', 'Referer': response.url, 'Sec-Ch-Ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"', 'Sec-Ch-Ua-Mobile': '?0', 'Sec-Ch-Ua-Platform': '"Windows"', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36', 'X-Requested-With': 'XMLHttpRequest'}
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
#               print(cat1_code+'>'+cat2_code+':'+cat1_title+'>'+cat2_title+':'+cur_page_s+'/'+tot_page_s+'\n')

    def Page_Item(self, response):
        if response.status != 200:
            print("Page_Item Faild!!!!!")
            print(response.status)

        j_response = json.loads(response.text)
        bbs_body = Selector(text=j_response["list"])
        #idx_arr = Selector(text=j_response["idx_arr"]) #79753592,94526455,94526405,94427787,94427805,94427864,89798916,94427926,89797570,94326621,94326505,94326482,94242545,94242466,94242640,87030087,91976509,94792828,89797589,87030071
        cat1_code = j_response["search_type"] # "MVO"
        #print('Page_Item===>cat1_code'+cat1_code)
        cat2_code = ''
        m = re.search(r"sub_sec=(.*?)&", response.url)
        if m:
            cat2_code=m.group(1)
            #print('Page_Item===============================>cat2_code'+cat2_code)
        else:
            print("Page_Item func fail to cat2_code!!!!!!!!!!!!!!!!!!!!!!!")

        category_title = j_response["category_title"]# #"영화"
        sub_category_title = j_response["sub_category_title"] #고화질HD
        #tpage = Selector(text=j_response["tpage"]) # 308
        #print ('    '+category_title+'>'+sub_category_title+':\n')

        for bbs_line in bbs_body.xpath("//tr[not(@*)]"):  
            # blank line skip
            chk_line = bbs_line.css('td.sumy_view').get()
            if chk_line:
                continue
            idx = bbs_line.css('td.check>span.summy_brd>input::attr(value)').get()
            txt = bbs_line.css('td.subject>span.summy_brd>a.summy_link>span.textOverflow>span.txt>span::text').get()

            icon_img_19_new = bbs_line.css('td.subject>span.summy_brd>a.summy_link>span.textOverflow>img').getall()
            for icon in icon_img_19_new: 
                if 'icon-19' in icon:
                    Lvl19 = "True" 
                else: 
                    Lvl19 = "False"
            else:
               Lvl19 = "False"

#            if bbs_line.css('td.subject>span.summy_brd>a.summy_link>span.textOverflow>img').get():
#               Lvl19 = "True"
#            else:
#               Lvl19 = "False"

            item_detail_url = "https://ondisk.co.kr/pop.php?sm=bbs_info&idx="+idx
            yield scrapy.Request(
                url=item_detail_url,
                callback=self.Page_Item_Detail,
                errback=self.errback,
                dont_filter=True,
                meta={"playwright": True, 
                      "playwright_include_page": True,
                      #"playwright_page_goto_kwargs": {
                      #    "wait_until": "networkidle",
                      #},
                      "playwright_context_kwargs": {
                          "ignore_https_errors": True,
                      },
                      "cat1_code": cat1_code,
                      "cat2_code": cat2_code,
                      "category_title": category_title,
                      "sub_category_title": sub_category_title,
                      "idx": idx,
                      "txt": txt,
                      "Lvl19": Lvl19,
                      "max_retry_times" : 3, 
                     },
            )        

    async def Page_Item_Detail(self, response):
        #print('Page_Item_Detail===============================start')
        if response.status != 200:
            print("Page_Item_Detail Faild!!!!!")
            print(response.status)
        page = response.meta["playwright_page"]
        content = await page.content()
        sel = Selector(text=content)
        await page.close()

        cat1_code = response.meta["cat1_code"]
        cat2_code = response.meta["cat2_code"]
        category_title = response.meta["category_title"] 
        sub_category_title = response.meta["sub_category_title"] 
        idx = response.meta["idx"]
        txt = response.meta["txt"]
        Lvl19 = response.meta["Lvl19"]

        item_page_detail = sel.xpath('//div[@class="ctvSellerInfo"]')
        point = sel.xpath('//strong[@class="ctvTblPoint"]/text()').get()
        seller = sel.xpath('//a[@id="js-infoLayer-btn"]/text()').get()
        attach_file_size = item_page_detail.css('table.ctvTbl>tbody>tr>td:nth-child(4)').get()

        # 제휴 아이콘 유무로 판단
        part_f = sel.css('div.ctvTitle h2')
        part_img = part_f.css('img::attr(src)').get()
        if part_img:
            partner = "True"
        else:
            partner = "False"

        bbs_item = OndiskItem()
        bbs_item["website"] = 1 # it mean "www.ondisk.co.kr"
        bbs_item["cat1_code"] = cat1_code
        bbs_item["cat2_code"] = cat2_code
        bbs_item["category_title"] = category_title
        bbs_item["sub_category_title"] = sub_category_title
        bbs_item["idx"] = idx
        bbs_item["txt"] = txt
        bbs_item["Lvl19"] = Lvl19

        bbs_item["point"] = point 
        bbs_item["seller"] = seller
        bbs_item["partner"] = partner 
        bbs_item["attach_file_size"] = attach_file_size 

        now = datetime.now() + timedelta(days=10)
        #now = datetime.datetime.now()
        a_str = now.strftime('%Y-%m-%d %H:%M:%S')
        #print(a_str) # 👉️ 2023-07-19 17:47:16
        json_str = json.dumps(a_str)
        #print(json_str) # 👉️ "2023-07-19 17:47:16"
        bbs_item["time"] = json_str

        #save_item(bbs_item) #for crawlab
        yield bbs_item

        if False:
            print("==============================")
            print("1>" + cat1_code +"\r\n")
            print("2>" + cat2_code +"\r\n")
            print("3>" + category_title+"\r\n")
            print("4>" + sub_category_title+"\r\n")
            print("5>" + idx+"\r\n")
            print("6>" + txt+"\r\n")
            print("7>" + Lvl19+"\r\n")
            print("8>" + point+"\r\n")
            print("9>" + seller+"\r\n")
            print("10>" + attach_file_size+"\r\n")
#        await page.close()

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
#        url = failure.request.url
#        print("errorback============================"+url)

#       await page.context.close()
        # log all failures
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
