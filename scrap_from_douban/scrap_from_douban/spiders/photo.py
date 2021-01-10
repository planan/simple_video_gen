import scrapy
from scrap_from_douban.items import ScrapFromDoubanItem


class PhotoSpider(scrapy.Spider):
    name = 'photo'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/celebrity/1371979/photos/']

    def parse(self, response):
        item = ScrapFromDoubanItem()
        imgurls = response.css(".cover img::attr(src)").extract()
        item['imgurl'] = [imgurl.replace("photo/m", "photo/l") for imgurl in imgurls ]
        yield item
        next_url = response.xpath("//span[@class='next']/a/@href").extract()
        if next_url:
            yield scrapy.Request(next_url[0],callback=self.parse)

    def parse_next(self, response):
        item = ScrapFromDoubanItem()
        imgurls = response.css(".cover img::attr(src)").extract()
        item['imgurl'] = [imgurl.replace("photo/m", "photo/l") for imgurl in imgurls ]
        yield item
