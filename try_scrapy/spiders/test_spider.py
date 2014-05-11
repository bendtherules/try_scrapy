from scrapy.spider import Spider
from scrapy.selector import Selector
from try_scrapy.items import LyndaItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

class lynda_spider(CrawlSpider):
    name="get_lynda"
    # allowed_domains = ["dmoz.org"]  
    start_urls=[r"file:///C:/Users/b/Downloads/Learn%20Web%20Development%20with%20Video%20Courses%20and%20Tutorials%20from%20lynda.com.htm"]
    rules = (
        Rule(SgmlLinkExtractor(attrs=["href","data-url"],allow=[r".*?page=\d+.*"])),
    )

    def  parse(self,response):
        sel = Selector(response)
        course_a=sel.xpath(r'//*[@class="course-list"]//li//*[@class="details-row"]/h3/a')
        # print course_a.extract()
        titles=course_a.xpath("text()").extract()
        links=course_a.xpath("@href").extract()
        items=[]
        for i in range(len(course_a)):
            tmp_item=LyndaItem()
            tmp_item["course_title"]=titles[i].strip()
            tmp_item["course_link"]=links[i]
            items.append(tmp_item)
            # print titles[i].strip()
            # print links[i]
        return items

# class NextPageLinkExtractor(SgmlLinkExtractor):
#     # allow_domains=[r"http://www.lynda.com/"]
#     attrs=["href","data-url"]
#     allow=[r".*?page=\d+.*"]
