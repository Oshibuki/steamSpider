# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv


class SteamscrapyPipeline(object):
    def process_item(self, item, spider):
        return item


# class SteamGameInfoPipeline(object):
#     def open_spider(self, spider):
#         self.f = open('Steam.csv', 'w', encoding='utf-8', newline='')
#         csvWriter = csv.writer(self.f, delimiter=',', lineterminator='\n')
#         csvWriter.writerow(['名称', '当前价格', '初始价格', '折扣',
#                             '发行日期', '评分', '评测情况', '游戏主页'])
#
#     def close_spider(self, spider):
#         self.f.close()
#
#     def process_item(self, item, spider):
#         try:
#             csvWriter.writerow([item['name'], item['current_price'], item['original_price'],
#                                 item['discount'], item['releaseday'], item['score'],
#                                 item['review'], item['link']])
#         except:
#             pass
#         return item
