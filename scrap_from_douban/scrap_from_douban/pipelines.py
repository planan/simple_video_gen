# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request
import os
from urllib.parse import urlparse


class ScrapFromDoubanPipeline:
    def process_item(self, item, spider):
        return item
        
class SaveImagePipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['imgurl']:
            yield Request(image_url)

    # def item_completed(self, results, item, info):
    #     # 是一个元组，第一个元素是布尔值表示是否成功
    #     if not results[0][0]:
    #         raise DropItem('下载失败')
    #     return item

    # 重命名，若不重写这函数，图片名为哈希，就是一串乱七八糟的名字
    def file_path(self, request, response=None, info=None, *, item=None):
        return os.path.basename(urlparse(request.url).path)