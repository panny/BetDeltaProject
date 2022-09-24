from lxml import etree

from spider.base import BaseSpider
from utils.httpclient import HttpClient


class JockeyRank(BaseSpider):

    def crawl(self):
        response = HttpClient.get(self.session, url=self.url)
        html = etree.HTML(response.text)
        hrefs = html.xpath("//div[@id='JKC']//a[@href]/@href")
        self.href.extend(hrefs)


if __name__ == '__main__':

    info = {'url': 'https://racing.hkjc.com/racing/information/chinese/Racing/JockeysRides.aspx'}
    rank = JockeyRank(**info)
    rank.get_data()
