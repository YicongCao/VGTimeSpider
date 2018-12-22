# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import csv
import codecs
from scrapy.exporters import JsonItemExporter
from VGTimeSpider.items import GameItem, TopicItem


class VgtimespiderPipelineGeneral(object):
    # 自定义导出csv
    def __init__(self):
        self.json_file = codecs.open('gamedata.json', 'w', encoding='utf-8')
        self.csv_file = open('gamedata.csv', 'w', encoding='utf-8')
        self.writer = csv.writer(self.csv_file)
        self.writer.writerow(["name", "nickname", "score", "count",
                              "platform", "date", "dna", "company", "tag", "url", "img"])
        self.nlu_file = codecs.open('gametopic.txt', 'w', encoding='utf-8')

    # 处理结束后关闭文件IO流
    def close_spider(self, spider):
        self.csv_file.close()
        self.json_file.close()
        self.nlu_file.close()

    # 将Item实例导出到csv文件
    def process_item(self, item, spider):
        if isinstance(item, GameItem):
            self.writer.writerow([item["name"], item["nickname"], item["score"], item["count"], item["platform"],
                                  item["date"], item["dna"], item["company"], item["tag"], item["url"], item["img"]])
            lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
            self.json_file.write(lines)
        elif isinstance(item, TopicItem):
            self.nlu_file.write(item["article"] + '\r\n===\r\n')
        return item
