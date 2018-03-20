# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest


class DoubanmovieSpider(scrapy.Spider):
    name = 'doubanmovie'
    # allowed_domains = ['douban.movie.com']
    start_urls = ['https://movie.douban.com/subject/1418640/all_photos']
    login_url = 'https://www.douban.com/accounts/login'

    def start_requests(self):
        yield Request(self.login_url, callback=self.login)

    def login(self, response):
        fd = {'form_email': '18615013834', 'form_password': 'ykbyt13142'}
        yield FormRequest.from_response(response, formdata=fd, callback=self.parse_login, dont_filter=True)

    def parse_login(self, response):
        if response.status == 200:
            yield from super().start_requests()

    def parse(self, response):
        link_ls = []
        for div in response.css('div.mod:nth-child(1) ul li'):
            link = div.css('img::attr(src)').extract_first()
            link_ls.append(link)
        yield {'image_urls': link_ls}

    # def download_images(self, response):
    #     link_ls = []
    #     link_ls.append(response.css(
    #         'span.magnifier a::attr(href)').extract_first())
    #     yield {'image_urls': link_ls}
