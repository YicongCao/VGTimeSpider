# -*- coding: utf-8 -*-
# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import scrapy
import urllib.parse
from VGTimeSpider.items import GameItem, TopicItem
from scrapy.selector import HtmlXPathSelector
import html2text


class GameSpider(scrapy.Spider):
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
    name = 'game'
    #url = 'https://www.vgtime.com/game/4446.jhtml'
    #start_urls = ['https://www.vgtime.com/game/4446.jhtml']

    url = 'https://www.vgtime.com/game/index.jhtml'
    start_urls = ['https://www.vgtime.com/game/index.jhtml']
    seen_urls = set()

    converter = html2text.HTML2Text()
    converter.ignore_images = True
    converter.ignore_emphasis = True
    converter.ignore_links = True
    converter.ignore_tables = True
    converter.strong_mark = ''

    def parse(self, response):
        selector = scrapy.Selector(response)
        '''
        示例游戏页面: https://www.vgtime.com/game/4446.jhtml
        对游戏页面，爬取游戏内容。
        '''
        game = selector.xpath('//section[@class="game_main"]')
        if game:
            game_item = GameItem()
            game_name = game.xpath(
                'div[@class="game_box main"]/h2/a/text()').extract_first(default='')
            game_nickname = game.xpath(
                'div[@class="game_box main"]/p/text()').extract_first(default='')
            game_score = game.xpath(
                '//span[@class="game_score showlist"]//text()').extract_first(default='-1')
            game_count = game.xpath(
                '//span[@class="game_count showlist"]//text()').extract_first(default="-1")
            game_descri = game.xpath(
                '//div[@class="game_descri"]/div[@class="descri_box"]')
            game_imgs = selector.xpath(
                '//img/@src').extract()

            if game_name != '':
                game_item['name'] = game_name
                game_item['nickname'] = game_nickname
                game_item['score'] = float(game_score)
                game_count = str(game_count).replace(
                    "位玩家评分", "").replace(" ", "")
                game_item['count'] = int(game_count)
                game_item['img'] = ''
                for game_img in game_imgs:
                    if (any(x in game_img for x in ['cover', 'photo', 'w_300'])) and (any(x in game_img for x in ['.jpg', '.png'])):
                        game_img = urllib.parse.urljoin(self.url, game_img)
                        suffix_idx = str(game_img).find('.jpg')
                        if suffix_idx == -1:
                            suffix_idx = str(game_img).find('.png')
                        if suffix_idx == -1:
                            continue
                        game_img = str(game_img)[:suffix_idx+4]
                        game_item['img'] = game_img
                        break

                if str(game_item['img']) == '' or not game_item['img']:
                    print(game_name + ' find no img')

                if game_descri:
                    for game_sub_descri in game_descri:
                        caption = game_sub_descri.xpath(
                            'p/text()').extract_first(default='')
                        if caption == '平台':
                            game_platform = game_sub_descri.xpath(
                                'div[@class="jizhong_tab"]/span/text()').extract()
                        elif caption == '最早发售':
                            game_date = game_sub_descri.xpath(
                                'span/text()').extract_first(default='1970-1-1')
                        elif caption == '游戏基因':
                            game_dna = game_sub_descri.xpath(
                                'div[@class="game_gene"]/span/text()').extract()
                        elif caption == '开发商':
                            game_company = game_sub_descri.xpath(
                                'span/text()').extract_first()
                            if not game_company:
                                game_company = game_sub_descri.xpath(
                                    'a/text()').extract_first()

                    game_item['platform'] = game_platform
                    game_item['date'] = game_date
                    game_item['dna'] = game_dna
                    game_item['company'] = game_company

                game_tags = game.xpath(
                    '//div[@class="game_gene"]/span/a/text()').extract()
                game_item['tag'] = game_tags
                game_item['url'] = response.url

                yield game_item
        '''
        示例文章页面: http://www.vgtime.com/topic/1042146.jhtml
        爬取article标签下的所有文本，用于NLU分析
        '''
        if 'topic' in response.url:
            articles_raw = selector.select("//article").extract()
            article = ''
            for article_raw in articles_raw:
                para = self.converter.handle(article_raw)
                if len(str(para)) > 50:
                    article = article + para + '\r\n'
            bypass = any(x in article for x in [
                         'VG聊天室', '本期听点', '新游月谈', '网易云音乐'])
            if len(article) > 50 and not bypass:
                topic_item = TopicItem()
                article = response.url + '\r\n' + article + '\r\n===\r\n\r\n'
                topic_item['article'] = article
                yield topic_item
        '''
        抓取剩下的游戏详情页面链接
        '''
        next_pages = selector.xpath('//a/@href').extract()
        for page in next_pages:
            if any(x in page for x in ['topic', 'game', 'forum']):
                page = urllib.parse.urljoin(self.url, page)
                if page not in self.seen_urls and 'vgtime.com' in page:
                    self.seen_urls.add(page)
                    yield scrapy.Request(page, callback=self.parse)
