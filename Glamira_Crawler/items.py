# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GlamiraCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
# Định nghĩa class ImageItem với thuộc tính image_urls chứa danh sách các urls ảnh cần tải để Scrapy Image Pipeline nhận diện và tải ảnh về
class ImageItem(scrapy.Item):
    image_urls = scrapy.Field()  # Trường chứa danh sách URL hình ảnh
    images = scrapy.Field()  # Trường lưu trữ thông tin về các hình ảnh đã tải về