# Define here the models for your scraped items


import scrapy


class AmazonProductItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    brand = scrapy.Field()
    image = scrapy.Field()
    description = scrapy.Field()
    table_name = scrapy.Field()


