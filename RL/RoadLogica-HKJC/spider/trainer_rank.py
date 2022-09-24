from lxml import etree

from spider.base import BaseSpider
from utils.httpclient import HttpClient


class TrainerRank(BaseSpider):

    def crawl(self):
        response = HttpClient.get(self.session, url=self.url)
        html = etree.HTML(response.text)
        hrefs = html.xpath("//table[@id='trainerEntryInfo']//a[@href]/@href")
        self.href.extend(hrefs)
        self.dispatch()


if __name__ == '__main__':

    info = {'url': 'https://racing.hkjc.com/racing/Info/meeting/TrainerEntry/chinese/Local/'}
    rank = TrainerRank(**info)
    rank.get_data()
