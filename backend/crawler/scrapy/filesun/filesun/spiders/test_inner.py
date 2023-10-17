import re
from scrapy.selector import Selector

test_html = """
<html><body>
<strong class="subject">
<div class="rankBg"> </div>
<p class="rankNum">1</p>
    오늘)공식자막 완전판 (( 매 갈 로 됸 2 )) 마지막완전판 초고화질BluRay5.1
    <span style="font-size:11px; color:#ff3000;">[12]</span>
</strong>
</body>
</html>
"""
def innertext_quick(elements, delimiter=""):
    return list(delimiter.join(el.strip() for el in element.css('*::text').getall()) for element in elements)
#print("===============")
#print(test_html)

#print("===============")
#/div/text()[normalize-space()]
sel = Selector(text=test_html)
#target = sel.xpath('/strong[not(*)]')
#print("===============")
#print(target)
#print("===============")

target = sel.css('strong.subject')   
tmp_str = innertext_quick(target, delimiter="")
print(type(tmp_str[0]))
print(tmp_str[0])
#replaced = re.sub('2', '****', tmp_str)

#print(replaced)



#for i in target.xpath('//*[name()="div" or name()="p" or name()="span"]'):
#    print(i.get())
#target.xpath('//strong[@class="subject"]//text()').re('(\w+)')

#test_str = '/disk/2/111068774?page=2'
##            idx = bbs_line.xpath("a/@href").re("\?m=(.+?)&")
##phoneNumRegex = re.compile(r'disk\/\d.+?\/(\d.+?\?)\/')
#phoneNumRegex = re.compile(r'/(\d+)\?')
#mo = phoneNumRegex.search(test_str)
#print('Phone number found: ' + mo.group(1))
