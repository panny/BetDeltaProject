import re
import copy
from lxml import etree

from spider.base import BaseSpider
from utils.httpclient import HttpClient
from utils.settings import HORSE, SAVE
from utils.config import Config
from utils.decorators import retry


class Horse(BaseSpider):
    name = None
    horse_no = None
    horse_id = None

    def crawl(self):
        if not self.content:
            response = HttpClient.get(self.session, url=self.url)
            self.content = response.text
        if '沒有相關資料' in self.content:
            self.status = True
            return
        html = etree.HTML(self.content)
        self.horse_id = re.search(r'HorseId=([0-9A-Z_]+)\"', self.content).group(1)
        horse = dict()
        title_text = html.xpath('string(//span[@class="title_text"])').strip()
        patt = r"(.*?)\((.*?)\)"
        find = re.search(patt, title_text)
        if find:
            self.name = find.group(1).strip()
            self.horse_no = find.group(2).strip()
        trs = html.xpath('//table[@class="table_top_right table_eng_text"]/tbody/tr')
        horse['name'] = self.name
        horse['horse_no'] = self.horse_no
        horse['horse_id'] = self.horse_id
        horse['url'] = self.url
        for tr in trs:
            text = tr.xpath('string(.)').replace('\r\n', '').strip()
            words = text.split(':')
            key = words[0].strip()
            val = words[-1].strip().replace('$', '')
            if key in HORSE:
                keys = HORSE.get(key)
                if "/" in keys:
                    key_ = keys.split('/')
                    if '(' in val:
                        val_ = val.replace(')', '').split('(')
                    else:
                        val_ = val.split('/')
                    horse[key_[0]] = val_[0].strip()
                    horse[key_[-1]] = val_[-1].strip()
                else:
                    horse[keys] = val
        self.result['horse'] = horse
        trs = html.xpath('//table[@class="bigborder"]/tr[@bgcolor]')
        data = []
        for tr in trs:
            string = []
            for x in tr.xpath('./td'):
                string_ = x.xpath('string(.)').replace('\r\n', '').strip()
                string.append(string_)
            single = dict()
            hrefs = tr.xpath("./td/a[@href]/@href")
            _data = Config.get_url_val(hrefs)
            single = copy.deepcopy(_data)
            single['name'] = self.name
            single['horse_no'] = self.horse_no
            single['horse_id'] = self.horse_id
            single['rank_id'] = string[0]
            single['ranking'] = string[1]
            single['rank_date'] = string[2]
            single['track'] = string[3]
            single['route'] = string[4]
            single['site_condition'] = string[5]
            single['race_class'] = string[6]
            single['position'] = string[7]
            single['score'] = string[8]
            single['trainer'] = string[9]
            single['jockey'] = string[10]
            single['head_distance'] = string[11]
            single['single_win'] = string[12]
            single['actual_pound'] = string[13]
            single['blocking'] = string[14]
            single['finish_time'] = string[15]
            single['position_weight'] = string[16]
            if len(string) >= 18:
                single['equipment'] = string[17]
            data.append(single)
        self.result['horse_rank'] = data
        self.status = True

    @retry(times=3)
    def data_duplicate(self):
        tmp = {}
        for key, val in self.result.items():
            if isinstance(val, list) and key in SAVE:
                info = SAVE[key]
                response = HttpClient.get(url=info.get('url'), params={'horse_no': self.horse_no})
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
    info = {'url': 'https://racing.hkjc.com/racing/information/Chinese/Horse/Horse.aspx?Horseno=V380',
            'task_id': '20200710', 'tags': '20200710'}
    rank = Horse(**info)
    rank.get_data()
