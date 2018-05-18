# -*- coding: utf-8 -*-
import scrapy
from tapcomment.items import TapcommentItem
import requests

class CommentSpider(scrapy.Spider):
    name = 'comment'
    allowed_domains = ['taptap.com']
    #start_urls = ['https://www.taptap.com/review/2']
    def start_requests(self):
        start_id = 2442798
        for id in range(start_id,start_id+1000000):
            url = 'https://www.taptap.com/review/{}'.format(str(id))
            yield scrapy.Request(url=url,callback=self.parse)
    def parse(self, response):
        item = TapcommentItem()
        if "app" in response.xpath("//div[@class='main-app-text']/a/@href").extract_first():
            item['game_name'] = response.css('h2::text').extract_first()
            item['game_id'] = response.xpath("//a[@class='main-app-icon']/@href").extract_first().split('/')[-1]
            item['game_rate'] = response.css('p.main-app-score span::text').extract_first()
            item['comment_author'] = response.css('h1::text').extract_first()
            item['comment_id'] = response.xpath("//button[@data-value='up']/@data-id").extract_first()
            item['author_id'] = response.xpath("//a[@class='user-text-name']/@href").extract_first().split('/')[-1]
            item['author_verified'] = response.xpath("//p[@class='user-text-verified']/span/text()").extract_first()
            comment_rate = response.xpath("//div[@class='main-contents-score']/i[@class='colored']/@style").extract_first().split('/')[-1]
            item['comment_rate'] = self.convert_rate(comment_rate)
            item['comment_time'] = response.xpath("//li[@class='main-footer-time review-main-user-time']/span[1]/text()").extract_first()
            item['comment_phone'] = response.xpath("//li[@class='main-footer-time review-main-user-time']/span[2]/text()").extract_first()
            #item['comment_content'] =response.xpath("//div[@class='text']/p/text()").extract_first()
            item['comment_content'] = response.xpath("string(//div[@class='text'])").extract_first().replace('\n','')
            #item['comment_smile'] = response.xpath("//button[@data-value='funny']/span[@data-taptap-ajax-vote='count']/text()").extarct_first()
            item['comment_smile'] = response.css("button.vote-funny span[data-taptap-ajax-vote]::text").extract_first()
            item['comment_up'] = response.xpath("//button[@data-value='up']/span[@data-taptap-ajax-vote='count']/text()").extract_first()
            item['comment_down'] = response.xpath("//button[@data-value='down']/span[@data-taptap-ajax-vote='count']/text()").extract_first()
            item['comment_reply'] = response.xpath("//span[@id='review-detail-reply-button']/span/text()").extract_first()
           # print("------downloading----.{}".format(item['comment_id']))
            yield item
        else:
            pass

    def convert_rate(self,rate):
        if rate == "width: 100px":
            rate = 5
        elif rate == "width: 80px":
            rate = 4
        elif rate == "width: 60px":
            rate = 3
        elif rate =="width: 40px":
            rate = 2
        else:
            rate = 1
        return rate

