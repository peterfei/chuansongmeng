# -*- coding: utf-8 -*-
import scrapy
import logging
import re
import json
import random
from wechatTop.top_type import TOP_TYPES
from scrapy.http import Request
from scrapy.spiders import CrawlSpider,Rule
from scrapy.selector import Selector
import requests
import pdb
from wechatTop.items import WechattopItem

class ChuansongSpider(scrapy.Spider):
    name = "chuansong"
    allowed_domains = ["chuansong.me"]
    host = 'http://chuansong.me/'
    start_urls = list(set(TOP_TYPES))
    # start_urls = ['http://chuansong.me/food']
    logging.getLogger("requests").setLevel(logging.WARNING)  # 将requests的日志级别设成WARNING
    logging.basicConfig(
        level=logging.DEBUG,
        format=
        '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S',
        filename='cataline.log',
        filemode='w')

    def start_requests(self):
    	for t_type in self.start_urls:
    		logging.debug('====t_type is '+t_type)
    		yield Request(url='http://chuansong.me/%s' % t_type,
                          callback=self.parse_ph_key)
    def parse_ph_key(self, response):
        selector = Selector(response)
        logging.debug('request url:------>' + response.url)
        divs = selector.xpath('//a[@class="question_link"]')
        for div in divs:
            urlkey = re.findall(r'href=[\'"]?([^\'" >]+)',div.extract())
            # logging.debug(viewkey)
            yield Request(url='http://chuansong.me%s' % urlkey[0],
                          callback=self.parse_ph_info)
    def parse_ph_info(self, response):
        wechatTop =  WechattopItem()
        selector = Selector(response)
        wechatTop['title'] = response.xpath('//*[@id="activity-name"]/text()').extract()
        # logging.debug("Title is ============%s"+title[0])
        content = response.xpath('//*[@id="js_content"]').extract()[0]
        wechatTop['content'] = re.sub(ur'(\s)\s+', ur'\1', content, flags=re.MULTILINE + re.UNICODE)
        # logging.debug("Content is ============%s"+content[0])
        # pdb.set_trace() 
        yield wechatTop