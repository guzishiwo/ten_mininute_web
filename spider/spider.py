import os
import requests
from bs4 import BeautifulSoup


class Spider(object):
    def __init__(self, *arg):
        self.url = url
        self.save_file = save_file
        self.photo_num = page_num
        self.img_urls = []

    def get_img_url(self):
        for num in (1, self.photo_num):
            # http://www.umei.cc/katongdongman/dongmantupian/1.htm
            _url = self.url + '{0}.htm'.format(num)
            html = requests.get(_url)
            soup = BeautifulSoup(html.text, "html.parser")
            self.img_urls.extend([x['src'] for x in soup.find_all('img')])
        self.write_all_urls_text()

    def write_url_to_text(self, data):
        with open(self.save_file, 'a+') as text_file:
            text_file.write('{}\n'.format(data))

    def write_all_urls_text(self):
        list(map(self.write_url_to_text, self.img_urls))


url = 'http://www.umei.cc/katongdongman/dongmantupian/'
# current_path = os.path.dirname(os.path.abspath(__file__))
# save_file = current_path + 'img_url_output.txt'
save_file = 'img_urls.txt'
page_num = 3
spider = Spider(url, save_file, page_num)
spider.get_img_url()
