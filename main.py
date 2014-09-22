#!/usr/bin/env python
from pymongo import MongoClient
from dragline.runner import main
from dragline.htmlparser import HtmlParser
from dragline.http import Request
import settings


class Spider:
    mydb = MongoClient(host ="localhost")["brainy"]
    def __init__(self, conf):
        self.name = "brainy"
        self.start = "http://www.brainyquote.com/quotes/topics.html"
        self.allowed_domains = ["www.brainyquote.com"]
        self.conf = conf

    def parse(self, response):
        parser = HtmlParser(response)
        for i in parser.extract_urls('//div[@class="bqLn"]/div[@class="bqLn"]/a'):
            yield Request(i,callback="parseCat")

    def parseCat(self, response):
        parser = HtmlParser(response)
        if 'Next' not in parser.xpath('//li/a/text()'):
            for i in parser.xpath('//span[@class="bqQuoteLink"]/a//text()'):
                self.mydb.quotes.insert({'quote':i})
        else:
            for i in parser.xpath('//span[@class="bqQuoteLink"]/a//text()'):
                self.mydb.quotes.insert({'quote':i})
            for url in parser.extract_urls('//li/a[contains(text(),"Next")]'):
                yield Request(url,callback="parseCat")


        #self.db.store_item('test', {'name': parser.find('head/title').text})


if __name__ == '__main__':
    main(Spider, settings)
