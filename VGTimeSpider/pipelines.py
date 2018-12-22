# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import csv
import codecs
from scrapy.exporters import JsonItemExporter


class VgtimespiderPipelineJson(object):
    # 自定义导出json
    def __init__(self):
        self.file = codecs.open('gamedata.json', 'w', encoding='utf-8')

    # 处理结束后关闭文件IO流
    def close_spider(self, spider):
        self.file.close()

    # 将Item实例导出到json文件
    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item


class VgtimespiderPipelineCsv(object):
    # 自定义导出csv
    def __init__(self):
        self.file = open('gamedata.csv', 'w', encoding='utf-8')
        self.writer = csv.writer(self.file)
        self.writer.writerow(["name", "nickname", "score", "count",
                              "platform", "date", "dna", "company", "tag", "url", "img"])

    # 处理结束后关闭文件IO流
    def close_spider(self, spider):
        self.file.close()

    # 将Item实例导出到csv文件
    def process_item(self, item, spider):
        self.writer.writerow([item["name"], item["nickname"], item["score"], item["count"], item["platform"],
                              item["date"], item["dna"], item["company"], item["tag"], item["url"], item["img"]])
        return item


class VgtimespiderPipelineTopicTxt(object):
    # 语料导出（单文本），用于NLU
    def __init__(self):
        self.file = codecs.open('gametopic.txt', 'w', encoding='utf-8')

    # 处理结束后关闭文件IO流
    def close_spider(self, spider):
        self.file.close()

    # 将Item实例导出到json文件
    def process_item(self, item, spider):
        self.file.write(item["article"] + '\r\n===\r\n')
        return item
