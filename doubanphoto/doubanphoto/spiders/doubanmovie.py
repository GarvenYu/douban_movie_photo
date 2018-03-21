# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest
import re


class DoubanmovieSpider(scrapy.Spider):
    name = 'doubanmovie'
    # allowed_domains = ['douban.movie.com']
    start_urls = ['https://movie.douban.com/subject/1418640/photos?type=S']
    login_url = 'https://www.douban.com/accounts/login'
    photo_per_page = 30
    next_page_url = "https://movie.douban.com/subject/1418640/photos?" \
                    "type=S&start=%s&sortby=like&size=a&subtype=a"

    def start_requests(self):
        yield Request(self.login_url, callback=self.login)

    def login(self, response):
        fd = {'form_email': '18615013834', 'form_password': 'ykbyt13142'}
        yield FormRequest.from_response(response, formdata=fd, callback=self.parse_login, dont_filter=True)

    def parse_login(self, response):
        if response.status == 200:
            yield from super().start_requests()

    def parse(self, response):
        page_url_list = response.css('div.paginator>a::attr(href)').extract()
        page_start_re = re.compile(r'start=(\d+)')
        page_start_end = page_start_re.findall(page_url_list[len(page_url_list) - 1])[0]  # 最后一页的起始start
        page = int(page_start_end) // self.photo_per_page  # 页数
        for i in range(0, page+1):  # 要包含最后一页
            if i == 0:
                yield scrapy.Request(self.start_urls[0], callback=self.parse_test)
            else:
                yield scrapy.Request(self.next_page_url % (self.photo_per_page*i), callback=self.parse_test)

    def parse_test(self, response):
        for div in response.css('ul.clearfix li'):
            link = div.css('a::attr(href)').extract_first()
            yield scrapy.Request(link, callback=self.download_images)

    def download_images(self, response):
        link_ls = []
        link_ls.append(response.css(
            'a.mainphoto img::attr(src)').extract_first())
        yield {'image_urls': link_ls}
