# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class TryScrapyPipeline(object):
    def process_item(self, item, spider):
        return item

import json

class JsonWriterPipeline(object):

    def __init__(self):
        self.file = open('output.json', 'wb')

    def open_spider(self,spider):
        self.file.write("[\n")

    def close_spider(self,spider):
        self.file.write("]")

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + ",\n"
        self.file.write(line)
        return item
