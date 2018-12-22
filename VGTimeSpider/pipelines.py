# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import json
import csv
import codecs
from scrapy.exporters import JsonItemExporter
from VGTimeSpider.items import GameItem, TopicItem
from VGTimeSpider.settings import PROJECT_DIR
from VGTimeSpider.tools.asynctask import download_pic


class VgtimespiderPipelineGeneral(object):
    # 自定义导出csv
    def __init__(self):
        self.json_file = codecs.open('gamedata.json', 'w', encoding='utf-8')
        self.csv_file = open('gamedata.csv', 'w', encoding='utf-8')
        self.title_file = open('gametitle.txt', 'w', encoding='utf-8')
        self.writer = csv.writer(self.csv_file)
        self.writer.writerow(["name", "nickname", "score", "count",
                              "platform", "date", "dna", "company", "tag", "url", "img"])
        self.nlu_file = codecs.open('gametopic.txt', 'w', encoding='utf-8')
        self.img_dir = os.path.join(PROJECT_DIR, 'gameimg')
        if not os.path.exists(self.img_dir):
            os.mkdir(self.img_dir)

    # 处理结束后关闭文件IO流
    def close_spider(self, spider):
        self.csv_file.close()
        self.json_file.close()
        self.nlu_file.close()
        self.title_file.close()

    # 将Item实例导出到csv文件
    def process_item(self, item, spider):
        if isinstance(item, GameItem):
            self.writer.writerow([item["name"], item["nickname"], item["score"], item["count"], item["platform"],
                                  item["date"], item["dna"], item["company"], item["tag"], item["url"], item["img"]])
            lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
            self.json_file.write(lines)
            self.title_file.write(item["name"] + '\r\n')
            image_url = item["img"]
            if image_url and item["name"]:
                image_suffix = ""
                if ".jpg" in image_url:
                    image_suffix = ".jpg"
                elif ".png" in image_url:
                    image_suffix = ".png"
                else:
                    image_suffix = ".bin"
                image_path = os.path.join(
                    self.img_dir, item["name"] + image_suffix)
                download_pic.delay(image_url, image_path)
        elif isinstance(item, TopicItem):
            self.nlu_file.write(item["article"] + '\r\n===\r\n')
        return item
