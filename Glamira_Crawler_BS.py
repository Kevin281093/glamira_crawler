import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# URL của trang chủ của Glamira
url = 'https://www.glamira.com/'

# Gửi yêu cầu HTTP GET để lấy nội dung của trang
response = requests.get(url)

# Kiểm tra xem yêu cầu thành công hay không
if response.status_code == 200:
    # Sử dụng BeautifulSoup để phân tích nội dung HTML
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Tìm tất cả các thẻ <img> để lấy đường dẫn ảnh
    img_tags = soup.find_all('img')
    
    # Lấy tất cả các đường dẫn ảnh
    image_urls = [urljoin(url, img['src']) for img in img_tags if 'src' in img.attrs]
    
    # In ra các đường dẫn ảnh
    for image_url in image_urls:
        print(image_url)
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")