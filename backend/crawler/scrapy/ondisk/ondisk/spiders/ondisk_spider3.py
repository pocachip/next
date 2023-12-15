import scrapy
from scrapy import Spider, Request
from scrapy.utils.defer import maybe_deferred_to_future
from twisted.internet.defer import DeferredList
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
import pymysql
from scrapy.exceptions import CloseSpider

class OndiskSpider(scrapy.Spider):
    name = "ondisk_update2"   #this spider synchronos func for speed to update

    custom_settings = {
        'DOWNLOAD_TIMEOUT': 10,
        'DOWNLOAD_DELAY': 2,
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
        self.myPipeline = None

        #Dictionary key: cat1+cat2  value: no_new_cnt   0~max_no_new
        self.no_update_cnt = dict()
        self.sub_cate_cnt = dict()
        self.max_scan_new_page = 3
        
#        self.ids_seen = set()

#        self.ids_seen = set()
#        print("set size1:" + str(len(self.ids_seen)))
#        self.conn = pymysql.connect(host='127.0.0.1', user='pocachip', password='media2015!', db='rightwatch', charset='utf8')
#        with self.conn:
#            with self.conn.cursor() as cursor:
#                cursor.execute("select idx from post")
#                row = cursor.fetchone()
#                while row:
#                    self.ids_seen.add(row[0])
#                    row = cursor.fetchone()
#        print(self.ids_seen)

    def start_requests(self):
        yield scrapy.Request(
            url="https://www.ondisk.co.kr/index.php",
            callback=self.parse,
        )        

    def parse(self, response):
        #print("set size2:" + str(len(self.ids_seen)))
        self.category = getattr(self, 'category', '')
        self.subsec = getattr(self, 'subsec', '')
#        self.ids_seen = self.myPipeline.get_ids()


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

        fullMenu = sel.xpath('//div[@id="js-fullMenuLayer"]//dl[@class="menu"]')
        additional_requests = []

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
                        url = "https://www.ondisk.co.kr/main/module/bbs_list_sphinx_prc.php"
                        headers = {'Accept': 'application/json, text/javascript, */*; q=0.01', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Host': 'www.ondisk.co.kr', 'Pragma': 'no-cache', 'Referer': response.url, 'Sec-Ch-Ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"', 'Sec-Ch-Ua-Mobile': '?0', 'Sec-Ch-Ua-Platform': '"Windows"', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36', 'X-Requested-With': 'XMLHttpRequest'}
                        self.sub_cate_cnt.setdefault(cat2_code, 0)
#                        additional_requests.append(FormRequest(url, 
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
                                callback=self.categoryCnt,
                            )
                        self.no_update_cnt.setdefault(cat2_code, 0)
                        url = "https://www.ondisk.co.kr/main/module/bbs_list_sphinx_prc.php"
                        headers = {'Accept': 'application/json, text/javascript, */*; q=0.01', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Host': 'www.ondisk.co.kr', 'Pragma': 'no-cache', 'Referer': response.url, 'Sec-Ch-Ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"', 'Sec-Ch-Ua-Mobile': '?0', 'Sec-Ch-Ua-Platform': '"Windows"', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36', 'X-Requested-With': 'XMLHttpRequest'}
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
                                callback=self.checkNewArticle,
                            )


                        #yield scrapy.Request(
                            #url=cat_url,
                            #callback=self.getCategoryCntAll,
                            #errback=self.errback,
                            #dont_filter=True,
                            #meta={
                                  #"playwright": True, 
                                  #"playwright_include_page": True,
                                  #"playwright_context_kwargs": {
                                     #"ignore_https_errors": True,
                                  #},
                                  #"playwright_page_methods" : [
                                      ##PageMethod("wait_for_load_state", "networkidle"),
##                                      PageMethod('wait_for_selector', 'div#page-footer'),
                                      #PageMethod('wait_for_selector', 'ul#list_order_btn'),
                                      #PageMethod('wait_for_selector', 'tbody#contents_list'),
###                                      PageMethod("evaluate", "window.scrollBy(0, document.body.scrollHeight)"),
                                  #],
                                  #"cat1_code": cat1_code,
                                  #"cat2_code": cat2_code,
                                  #"max_retry_times" : 5, 
                                 #},
                        #)        
        #deferreds = []
        #for r in additional_requests:
            #deferred = self.crawler.engine.download(r)
            #deferreds.append(deferred)
        #responses = await maybe_deferred_to_future(DeferredList(deferreds))

        #print("Gooooooooooooooooooooooooooooooooood"+str(len(self.sub_cate_cnt)))
        #for key, value in self.sub_cate_cnt.items():
            #print(key, value)

    async def getCategoryCntAll(self, response):
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
                        #print("click!!")
                        content = await page.content()
            
#        last_page =  sel.css('form>input#last_page::attr(value)').get() 
#        print(cat2_code + ":"+ last_page) 
        url = "https://www.ondisk.co.kr/main/module/bbs_list_sphinx_prc.php"
        headers = {'Accept': 'application/json, text/javascript, */*; q=0.01', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Host': 'www.ondisk.co.kr', 'Pragma': 'no-cache', 'Referer': response.url, 'Sec-Ch-Ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"', 'Sec-Ch-Ua-Mobile': '?0', 'Sec-Ch-Ua-Platform': '"Windows"', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36', 'X-Requested-With': 'XMLHttpRequest'}
        print("getCategoryCnt:"+headers['Referer'])
        await page.close()  

        self.no_update_cnt.setdefault(cat2_code, 0)
        self.sub_cate_cnt.setdefault(cat2_code, 0)
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
            callback=self.parseCategoryCnt,
        )


    async def categoryCnt(self, response):
#        print("categoryCnt called!!!!!")
        if response.status != 200:
            print(response.status)
        j_response = json.loads(response.text)
        bbs_body = Selector(text=j_response["list"])
        idx_arr = Selector(text=j_response["idx_arr"]) #79753592,94526455,94526405,94427787,94427805,94427864,89798916,94427926,89797570,94326621,94326505,94326482,94242545,94242466,94242640,87030087,91976509,94792828,89797589,87030071
        cat1_code = j_response["search_type"] # "mvo"
        cat2_code = ''
        m = re.search(r"sub_sec=(.*?)&", response.url)
        if m:
            cat2_code=m.group(1)
        else:
            print("page_item func fail to cat2_code!!!!!!!!!!!!!!!!!!!!!!!")
        
        tot_page_n = j_response["tpage"] # "mvo"
        self.sub_cate_cnt[cat2_code]=tot_page_n
        #for key, value in self.sub_cate_cnt.items():
            #print(key, value)
        #return

    async def checkNew(self, response):
#        print("checkNew func....")
        j_response = json.loads(response.text)
        m = re.search(r"sub_sec=(.*?)&", response.url)
        if m:
            cat2_code=m.group(1)
        else:
            print("page_item func fail to cat2_code!!!!!!!!!!!!!!!!!!!!!!!")

        idx_str = j_response["idx_arr"] #79753592,94526455,94526405,94427787,94427805,94427864,89798916,94427926,89797570,94326621,94326505,94326482,94242545,94242466,94242640,87030087,91976509,94792828,89797589,87030071
        idx_arr = idx_str.split(',')

        hasNew = False
        for idx in idx_arr:
            if idx in self.myPipeline.get_ids():
                continue
            else:
#               print("1." + idx+": is new article")
                hasNew = True 

        if not hasNew:
            self.no_update_cnt[cat2_code] = self.no_update_cnt.get(cat2_code) + 1

        return hasNew
#            print("1. no new article"+str(self.no_update_cnt[cat2_code]))
#        else:
#            print("1.something new!!!")


    # getCategroyCnt and checkNewupdate
    async def checkNewArticle(self, response):
        if response.status != 200:
            print(response.status)
        j_response = json.loads(response.text)
#       bbs_body = Selector(text=j_response["list"])

        tot_page_n = j_response["tpage"] # "mvo"
        cat1_code = j_response["search_type"] # "mvo"
        cat2_code = ''
        cur_page_n = 1
        m = re.search(r"sub_sec=(.*?)&", response.url)
        if m:
            cat2_code=m.group(1)
        else:
            print("page_item func fail to cat2_code!!!!!!!!!!!!!!!!!!!!!!!")
        n = re.search(r"page=(.*?)&", response.url)
        if n:
            cur_page_s=n.group(1)
            cur_page_n=int(cur_page_s)
        else:
            print("page_item func fail to cur_page_s!!!!!!!!!!!!!!!!!!!!!!!")

#        await self.checkNew(response)
            
#        print (cat2_code+">noshowcount("+str(self.no_update_cnt[cat2_code])+")")

        while (cur_page_n <= tot_page_n):
            print(cat1_code+'>'+cat2_code+':('+str(cur_page_n)+'/'+str(tot_page_n)+')')
            if (self.no_update_cnt.get(cat2_code) > (self.max_scan_new_page-1)):
                print("exit becasuse no show page ouver:"+cat2_code+"<"+str(self.no_update_cnt.get(cat2_code))+"> curpage:"+cur_page_s)
                break
            url = "https://www.ondisk.co.kr/main/module/bbs_list_sphinx_prc.php"
            cur_page_s =str(cur_page_n)
            
            headers = {'Accept': 'application/json, text/javascript, */*; q=0.01', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Host': 'www.ondisk.co.kr', 'Pragma': 'no-cache', 'Referer': response.url, 'Sec-Ch-Ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"', 'Sec-Ch-Ua-Mobile': '?0', 'Sec-Ch-Ua-Platform': '"Windows"', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36', 'X-Requested-With': 'XMLHttpRequest'}
            additional_request =  FormRequest(url, 
            #yield FormRequest(url, 
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
                #callback=self.checkNewArticle,
                callback=self.Page_Item, 
            ) 
            deferred = self.crawler.engine.download(additional_request)
            additional_response = await maybe_deferred_to_future(deferred)
            #await self.checkNewArticle2(additional_response)
            new_article = await self.checkNew(additional_response)
            if new_article:
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

    async def Page_Item(self, response):
        if response.status != 200:
            print("Page_Item Faild!!!!!")
            print(response.status)
        
        n = re.search(r"page=(.*?)&", response.url)
        if n:
            cur_page_s=n.group(1)
        else:
            print("page_item func fail to cur_page_s!!!!!!!!!!!!!!!!!!!!!!!")


        #b_close = True
        #for value in  self.no_update_cnt.values():
            #if value < self.max_scan_new_page: 
                #b_close = False
        #if b_close:
            #for key, value in self.no_update_cnt.items():
              #print(key, value)
            #raise CloseSpider("max noNew count exceeded")

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
        print("-----------------------")
        print("Page_item: "+cat2_code+"("+cur_page_s+")")
        print("-----------------------")

        category_title = j_response["category_title"]# #"영화"
        sub_category_title = j_response["sub_category_title"] #고화질HD
        #tpage = Selector(text=j_response["tpage"]) # 308
        #print ('    '+category_title+'>'+sub_category_title+':\n')

        #self.new_dic.update(cat2_code=0)
        
        for bbs_line in bbs_body.xpath("//tr[not(@*)]"):  
            # blank line skip
            chk_line = bbs_line.css('td.sumy_view').get()
            if chk_line:
                continue
            idx = bbs_line.css('td.check>span.summy_brd>input::attr(value)').get()
            
            # hack by pocachip pass if alread ids in db
            # it use for update scraping new article
            #print("idx size:" + str(len(self.myPipeline.get_ids())))
            #if idx in self.ids_seen:
            if idx in self.myPipeline.get_ids():
                continue
            #else:
                #print("Page has a new Item!!!!!")
#                print("idx new:", idx)
#                continue

            txt = bbs_line.css('td.subject>span.summy_brd>a.summy_link>span.textOverflow>span.txt>span::text').get()

            icon_img_19_new = bbs_line.css('td.subject>span.summy_brd>a.summy_link>span.textOverflow>img').getall()
            for icon in icon_img_19_new: 
                if 'icon-19' in icon:
                    Lvl19 = "True" 
                else: 
                    Lvl19 = "False"
            else:
               Lvl19 = "False"

            item_detail_url = "https://ondisk.co.kr/pop.php?sm=bbs_info&idx="+idx
#           print ('PageItem    '+ item_detail_url + '\n')

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
        bbs_item["website"] = "1" # it mean "www.ondisk.co.kr"
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

        now = datetime.now() #+ timedelta(days=10)
        #now = datetime.datetime.now()
        a_str = now.strftime('%Y-%m-%d %H:%M:%S')
        bbs_item["time"] = a_str
        #print(a_str) # 👉️ 2023-07-19 17:47:16
        #json_str = json.dumps(a_str)
        #bbs_item["time"] = json_str
        #print(json_str) # 👉️ "2023-07-19 17:47:16"

#        save_item(bbs_item) #for crawlab
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