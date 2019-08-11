from users.items import UsersItem
import scrapy
import json
import requests

class usersSpider(scrapy.Spider):
    name = 'users'
    allowed_domains = ['https://www.bilibili.com/']
    #start_url = ['https://api.bilibili.com/x/space/acc/info?mid=1&jsonp=jsonp']
    start_urls = (
            'https://api.bilibili.com/x/space/acc/info?mid=' + str(i) + '&jsonp=jsonp' for i in range(3100000,3210000)
            )

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url)

    def parse(self,response):
        info = json.loads(response.text)['data']
        item = UsersItem()
        item['name'] = info['name']
        item['mid'] = info['mid']
        item['coins'] = info['coins']
        item['sign'] = info['sign']
        item['birthday'] = info['birthday']
        item['level'] = info['level']
        item['sex'] = info['sex']
        item['face'] = info['face']
        yield item

