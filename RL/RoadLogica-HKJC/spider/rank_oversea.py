import re
import copy
import furl
from lxml import etree

from spider.base import BaseSpider
from utils.httpclient import HttpClient
from utils.settings import SAVE
from utils.config import Config
from utils.decorators import retry


class RankOversea(BaseSpider):
    rank_tag = None
    rank_mask = None

    def crawl(self):
        if not self.content:
            response = HttpClient.get(self.session, url=self.url)
            self.content = response.text
        if '請稍後重試' in self.content:
            self.status = True
            return
        html = etree.HTML(self.content)
        hrefs = html.xpath("//div[@class='raceNum clearfix']//a[contains(@href, 'overseas')]/@href")
        # 判断是否存在历史数据
        args = furl.furl(self.url).args
        match_id = args.get('match_id')
        if match_id:
            find = re.search(r'(\d+)/([A-Z0-9]+)/(\d+)/', match_id)
            if find:
                self.rank_tag = find.group(1)+find.group(3)
                self.rank_mask = find.group(2)
                if find.group(3) == '1':
                    self.href.extend(hrefs)
        # 解析页面
        self.single(self.content)
        self.status = True

    def single(self, content):
        html = etree.HTML(content)
        row_div = html.xpath('//p[@class="info"]')
        string = row_div[0].xpath('string(.)')
        string = string.replace('\r\n', '')
        patt = r'(.*?)\s+-\s+(\d+)米 (.*?地) (|.*?地)(\d{4}年\d+月\d+日), .*第(\d+)場, ([\d:]+)'
        find = re.search(patt, string)
        if find:
            field = dict()
            if not self.rank_tag:
                self.rank_tag = find.group(7).replace('年', '').replace('月', '').replace('日', '') + find.group(8)
            field['rank_tag'] = self.rank_tag
            field['rank_mask'] = self.rank_mask
            field['place'] = find.group(1).split('馬場')[0].split(',')[-1].strip()+'馬場'
            field['number'] = find.group(6)
            field['name'] = find.group(1).split('馬場')[-1].split(',')[-1].strip()
            field['rank_date'] = find.group(5) + " " + find.group(7)
            field['field'] = find.group(3)
            field['route'] = find.group(2)
            field['site_condition'] = find.group(4)
            self.result['field'] = field
        trs = html.xpath("//table[@class='draggable']/tbody/tr[@class]")
        data = []
        for tr in trs:
            text = []
            for x in tr.xpath('./td'):
                text.append(x.xpath('string(.)').replace('\r\n', '').strip())
            single = dict()
            single['rank_tag'] = self.rank_tag
            single['rank_mask'] = self.rank_mask
            single['number'] = text[1]
            single['horse'] = text[3]
            single['position'] = text[4]
            single['jockey'] = text[5]
            single['weight_bear'] = text[6]
            single['trainer'] = text[7]
            single['score'] = text[8]
            single['horse_age'] = text[9]
            single['sex'] = text[10]
            single['equipment'] = text[11]
            single['classify'] = '参赛'
            data.append(single)
        self.result['rank'] = data
        import json
        print(json.dumps(self.result))

    @retry(times=3)
    def data_duplicate(self):
        tmp = {}
        for key, val in self.result.items():
            if isinstance(val, list) and key in SAVE:
                info = SAVE[key]
                response = HttpClient.get(url=info.get('url'), params={'rank_tag': self.rank_tag})
                content = response.json()
                if content.get('status') == '200' and content.get('data'):
                    data = Config.get_filter_dict(val, content.get('data'), info.get('keys'))
                else:
                    data = val
                tmp[key] = data
            else:
                tmp[key] = val
        self.result = tmp


if __name__ == '__main__':
    info = {'url': 'https://racing.hkjc.com/racing/SystemDataPage/racing/overseas/RaceCard-SystemDataPage.aspx?match_id=20200705/S2/1/0&lang=Chinese', 'task_id': '20200702', 'tags': '20200702'}
    rank = RankOversea(**info)
    rank.get_data()