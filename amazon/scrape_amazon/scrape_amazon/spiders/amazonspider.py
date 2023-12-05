import scrapy
from urllib.parse import urljoin
import json
import re
from ..items import AmazonProductItem

class AmazonSearchSpider(scrapy.Spider):
    name = 'amazonsearch'

    def start_requests(self):
        keyword_list = ['desktop monitor']
        for keyword in keyword_list:
            amazon_search_url = f'https://www.amazon.com/s?k={keyword}&page=1'
            yield scrapy.Request(url=amazon_search_url, callback=self.discover_product_urls, meta={'keyword': keyword, 'page': 1})

    def discover_product_urls(self, response):
        page = response.meta['page']
        keyword = response.meta['keyword']

        products = response.css("div.s-result-item[data-component-type=s-search-result]")
        for product in products:

            relative_url = product.css("h2>a::attr(href)").get()
            product_url = urljoin('https://www.amazon.com/', relative_url).split("?")[0]
            yield scrapy.Request(url=product_url, callback=self.parse_product_data,
                                 meta={'keyword': keyword, 'page': page})

            ## Get All Pages
            if page == 1:
                # available_pages = response.xpath(
                #     '//*[contains(@class, "s-pagination-item")][not(has-class("s-pagination-separator"))]/text()'
                # ).getall()
                #
                # last_page = available_pages[-1] # ,int(last_page)
                custom_pg = 5
                for page_num in range(2, custom_pg):
                    amazon_search_url = f'https://www.amazon.com/s?k={keyword}&page={page_num}'
                    yield scrapy.Request(url=amazon_search_url, callback=self.discover_product_urls,
                                         meta={'keyword': keyword, 'page': page_num})
    def parse_product_data(self, response):

        product_item = AmazonProductItem()
        description = []
        desc = response.xpath('//*[@id="feature-bullets"]/ul/li/span/text()')
        description = ', '.join(desc.getall())

        product_item['title'] = response.xpath('//span[@id="productTitle"]/text()').get()
        product_item['price'] = response.xpath('//span[@class="a-offscreen"]/text()').get()
        product_item['brand'] = response.xpath('//span[@class="a-size-base po-break-word"]/text()').get()
        product_item['image'] = response.xpath('//img[@class="a-dynamic-image"]/@src').get()
        product_item['description'] = description
        product_item['table_name'] = 'Desktop_monitors'

        yield product_item
