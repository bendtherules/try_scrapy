from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from try_scrapy.items import LyndaItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.shell import inspect_response
import urlparse,urllib
# from scrapy import log

base_url=r"http://www.lynda.com"
items=[]
# log.start()

def do_nothing(*args,**kwargs):
    pass

class lynda_spider(CrawlSpider):
    name="get_lynda"
    # allowed_domains = ["dmoz.org"]  
    start_urls=[urlparse.urljoin(base_url,"allcourses")]
    
    

    def  parse(self,response):
        sel = Selector(response)

        next_page =sel.xpath("//a[contains(@class,'see-more-results')]/@data-url").extract()
        if next_page:
            next_page=next_page[0]

            next_page=urlparse.urljoin(base_url,next_page)
            parsed_url=urlparse.urlparse(next_page)
            parsed_qs=urlparse.parse_qs(parsed_url.query)
            parsed_qs.pop("ajax")
            for tmp_qs in parsed_qs:
                parsed_qs[tmp_qs]=parsed_qs[tmp_qs][0]
            qs=urllib.urlencode(parsed_qs)
            parsed_url=list(parsed_url)
            parsed_url[-2]=qs
            final_url=urlparse.urlunparse(parsed_url)

            print final_url
        #     if int(parsed_qs["page"])<=4:
        #         return Request(final_url, self.parse)

        # sel = Selector(response)
        course_a=sel.xpath(r'//*[@class="course-list"]//li//a')
        # print course_a.extract()
        titles=course_a.xpath("text()").extract()
        links=course_a.xpath("@href").extract()
        for i in range(len(titles)):
            tmp_item=LyndaItem()
            tmp_item["course_title"]=titles[i].strip()
            tmp_item["course_link"]=links[i]
            items.append(tmp_item)
            # print titles[i].strip()
            # print links[i]
        print len(items)
        if int(parsed_qs["page"])<=4:
            return Request(url=final_url)
        else:
            return items


# class NextPageLinkExtractor(SgmlLinkExtractor):
#     # allow_domains=[r"http://www.lynda.com/"]
#     attrs=["href","data-url"]
#     allow=[r".*?page=\d+.*"]
