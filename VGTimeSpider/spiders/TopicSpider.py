# -*- coding: utf-8 -*-
# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import scrapy
import urllib.parse
from scrapy.selector import HtmlXPathSelector
from VGTimeSpider.items import TopicItem
import html2text


class TopicSpider(scrapy.Spider):
    """
    name:用于区别spider,名字必须唯一
    allowed_domains: 允许扒取的域名
    start_urls: Spider在启动时进行爬取的url列表,
                后续的url可从初始的url获取的数据中提取
    parse():是spider的一个方法。 被调用时，每个初始URL完成下载后生成的 
            Response 对象将会作为唯一的参数传递给该函数。 该方法负责解
            析返回的数据(response data)，提取数据(生成item)以及生成需
            要进一步处理的URL的 Request 对象。
    """
    name = 'topic'

    url = 'https://www.vgtime.com/'
    start_urls = ['https://www.vgtime.com/']
    seen_urls = set()
    converter = html2text.HTML2Text()
    converter.ignore_images = True
    converter.ignore_emphasis = True
    converter.ignore_links = True
    converter.ignore_tables = True
    converter.strong_mark = ''

    def parse(self, response):
        selector = HtmlXPathSelector(response)
        '''
        示例文章页面: http://www.vgtime.com/topic/1042146.jhtml
        爬取article标签下的所有文本，用于NLU分析
        '''

        articles_raw = selector.select("//article").extract()
        article = ''
        for article_raw in articles_raw:
            para = self.converter.handle(article_raw)
            if len(str(para)) > 50:
                article = article + para + '\r\n'
        if len(article) > 50:
            item = TopicItem()
            item['article'] = article
            yield item
        '''
        抓取剩下的游戏详情页面链接
        '''
        next_pages = selector.xpath('//a/@href').extract()
        for page in next_pages:
            if any(x in page for x in ['topic', 'forum', 'game', 'shop', 'video']):
                page = urllib.parse.urljoin(self.url, page)
                if page not in self.seen_urls:
                    self.seen_urls.add(page)
                    yield scrapy.Request(page, callback=self.parse)
