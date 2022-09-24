import re
import json
import furl
import copy
from datetime import datetime
from lxml import etree

from spider.base import BaseSpider
from utils.httpclient import HttpClient
from utils.time import Time
from utils.settings import SAVE, OverSea
from utils.config import Config
from utils.decorators import retry


class RankRecord(BaseSpider):
    duplicates = []
    rank_tag = None
    rank_mask = None

    def duplicate(self):
        url = "http://127.0.0.1:8000/api/rank_record/?type=distinct&rank_mask=HV,ST"
        response = HttpClient.get(url=url)
        content = json.loads(response.text)
        if content.get('data'):
            self.duplicates = [x.get('rank_tag') for x in content.get('data')]

    def crawl(self):
        self.duplicate()
        if not self.content:
            response = HttpClient.get(self.session, url=self.url)
            self.content = response.text
        html = etree.HTML(self.content)
        args = furl.furl(self.url).args
        if args.get('Racecourse'):
            self.rank_mask = args.get('Racecourse')
        if not args:
            self.single(self.content)
            self.record(self.content)
        elif 'para' in args:
            pass
        elif 'RaceNo' in args:
            self.single(self.content)
        elif 'RaceDate' in args:
            self.single(self.content)
            self.record(self.content)
        if self.info.get('flag'):
            options = html.xpath('//*[@id="selectId"]/option[@value]/@value')
            for opt in options:
                opt_time = Time.convert_time_format_by_string(opt, '%d/%m/%Y', '%Y/%m/%d')
                if opt_time.replace('/', '') not in OverSea:
                    url = f"https://racing.hkjc.com/racing/information/chinese/Racing/LocalResults.aspx?RaceDate={opt_time}"
                    self.href.append(url)
        self.status = True

    def single(self, content):
        html = etree.HTML(content)
        rank_tag = re.search(r'/(\d{8})', content).group(1)
        string = html.xpath('string(//span[@class="f_fl f_fs13"])')
        string = string.replace('\r\n', '').replace(' ', '')
        patt = r'賽事日期:[0-9/]+\s+(\S+)'
        find = re.search(patt, string)
        field = dict()
        if find:
            field['place'] = find.group(1)
            if not self.rank_mask:
                if find.group(1) == '沙田':
                    self.rank_mask = 'ST'
                elif find.group(1) == '跑馬地':
                    self.rank_mask = 'HV'
        string = html.xpath('string(//div[@class="race_tab"])')
        string = string.replace('\r\n', '').replace(' ', '')
        patt = r'第(\d+)場\((\d+)\)(第.*?班)-(\d+)米-\((.*?)\)場地狀況:(.*?地)(.*?)賽道:(.*?)HK\$(.*?)時間'
        find = re.search(patt, string)
        if find:
            self.rank_tag = rank_tag + find.group(1)
            field['rank_tag'] = self.rank_tag
            field['rank_mask'] = self.rank_mask
            field['number'] = find.group(1)
            field['rank_id'] = find.group(2)
            field['name'] = find.group(7)
            tracks = find.group(8).split('-')
            field['field'] = tracks[0]
            field['track'] = tracks[-1] if len(tracks) == 2 else ''
            field['route'] = find.group(4)
            field['site_condition'] = find.group(6)
            field['reward'] = find.group(9)
            field['score'] = find.group(5)
            field['race_class'] = find.group(3)
            self.result['field'] = field
            rank_id = find.group(2)
            trs = html.xpath("//tbody[@class='f_fs12 fontFam']/tr")
            data = []
            for tr in trs:
                text = []
                for x in tr.xpath('./td'):
                    text.append(x.xpath('string(.)').replace('\r\n', '').strip())
                hrefs = tr.xpath('.//a[@href]/@href')
                _data = Config.get_url_val(hrefs)
                single = copy.deepcopy(_data)
                single['rank_tag'] = self.rank_tag
                single['rank_mask'] = self.rank_mask
                single['rank_id'] = rank_id
                single['order'] = text[0]
                single['number'] = text[1]
                single['horse'] = text[2].split('(')[0]
                single['horse_no'] = text[2].split('(')[-1].replace(')', '')
                single['jockey'] = text[3]
                single['trainer'] = text[4]
                single['actual_pound'] = text[5]
                single['position_weight'] = text[6]
                single['position'] = text[7]
                single['head_distance'] = text[8]
                single['blocking'] = re.sub(r'\s+', ' ', text[9])
                single['finish_time'] = text[10]
                if len(text) >= 12:
                    single['single_win'] = text[11]
                data.append(single)
            self.result['rank_record'] = data
        else:
            print(self.info)

    def record(self, content):
        html = etree.HTML(content)
        hrefs = html.xpath("//table[@class='f_fs12 f_fr js_racecard']//a[@href]/@href")
        for href in hrefs:
            if "RaceNo" in href:
                url = f"https://racing.hkjc.com{href}"
                args = furl.furl(url).args
                rank_tag = f"{Time.convert_time_format_by_string(args['RaceDate'], '%Y/%m/%d', '%Y%m%d')}{args['RaceNo']}"
                if rank_tag not in self.duplicates:
                    self.href.append(url)

    @retry(times=3)
    def data_duplicate(self):
        tmp = {}
        for key, val in self.result.items():
            if isinstance(val, list) and key in SAVE:
                info = SAVE.get(key)
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
        import json
        print(json.dumps(self.result))


if __name__ == '__main__':
    info = {'url': 'https://racing.hkjc.com/racing/information/Chinese/Racing/LocalResults.aspx?RaceDate=2018/04/15',
            'task_id': '20200710', 'tags': '20200710'}
    rank = RankRecord(**info)
    rank.get_data()