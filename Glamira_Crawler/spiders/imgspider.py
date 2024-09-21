import scrapy
from urllib.parse import urljoin
import json
# from Glamira_Crawler.items import ImageItem # type: ignore

class ImagespiderSpider(scrapy.Spider):
    name = 'imagespider'
    allowed_domains = ['glamira.com'] # Chỉ lấy dữ liệu liên quan đến web tránh lấy dữ liệu bên thứ 3 nhúng vào web (các banner quảng cáo...)
    start_urls = ['https://www.glamira.com/']


    # Khởi tạo thuộc tính collected_images chứa urls ảnh đã crawled để và visited_urls chứa urls page đã truy cập tránh dupplicated crawl
    def __init__(self, *args, **kwargs):
            super(ImagespiderSpider, self).__init__(*args, **kwargs) # Khai báo kế thừ từ lớp cha scrapy.Spider để có thể tái sử dụng thuộc tính của lớp cha và đồng bộ với spider
            # Kiểm tra ảnh đã được tải để tránh tải trùng khi các pages khác nhau chứa cùng một ảnh
            self.collected_images = set() # Khai báo collected_images chứa urls của các ảnh đã tải
            # Kiểm tra page đã được truy cập chưa để tránh truy cập lại optimize thời gian và luồng
            self.visited_urls = set() # Khai báo visited_urls chứa urls của các trang đã truy cập
            try:
                # Mở files json chứa urls ảnh đã crawled và đưa vào set
                with open('collected_images.json', 'r') as f:
                    self.collected_images = set(json.load(f))
            except FileNotFoundError:
                pass # Nếu file không tồn tại sẽ bắt đầu với set rỗng

            try:
                # Mở files json chứa urls page đã truy cập và đưa vào set
                with open('visited_urls.json', 'r') as f:
                    self.visited_urls = set(json.load(f))
            except FileNotFoundError:
                pass # Nếu file không tồn tại sẽ bắt đầu với set rỗng

    """
    Để có thể tự động tải và lưu hình ảnh về chúng ta cần sử dụng Scrapy Image Pipeline
    với Scrapy Image Pipeline yêu cầu biến nhận diện để hoạt động có tên image_urls (là danh sách chứa tất cả urls)
    1. Mở file items.py và định nghĩa class ImageItem chứa biến image_urls
    2. Mở file settings.py và kích hoạt ITEM_PIPELINE
    """


    def parse(self, response):

        # Tìm và follow các liên kết trên trang để crawl thêm các trang khác khi trang web có nhiều trang
        # Lấy thẻ a có thuộc tính href thường sẽ là các nút next page hoặc các submenu...
        for href in response.css('a::attr(href)').getall(): 
            yield response.follow(href, self.parse)
            
        # Kiểm tra xem page đã được truy cập chưa
        if response.url in self.visited_urls:
            return
        self.visited_urls.add(response.url)

        # Tìm tất cả các thẻ <img> và lấy thuộc tính src bằng list comprehension dùng urljoin nối src với domain chính để nhận về full urls
        list_urls = [urljoin(response.url, src) for src in response.css('img::attr(src)').getall() if src]
        # Kiểm tra url có tồn tại trong danh sách đã crawl chưa
        image_urls = [url for url in list_urls if url not in self.collected_images]
        if image_urls:
            self.collected_images.update(image_urls) # Ghi vào danh sách chứa các urls đã được tải
            #item = ImageItem()  # Tạo biến item là class ImageItem
            # item['image_urls'] = new_urls  # Ghi vào biến image_urls trong class ImageItem
            yield {'image_urls' : image_urls}


    def close(self, reason):
        # Lưu urls ảnh đã crawled vào file colllected_image.json sau khi spider closed
        with open('collected_images.json', 'w') as f:
            json.dump(list(self.collected_images), f)

        # Lưu urls page đã truy cập vào file visited_image.json sau khi spider closed
        with open('visited_urls.json', 'w') as f:
            json.dump(list(self.visited_urls), f)