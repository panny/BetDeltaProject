import re
import copy
from lxml import etree
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hkjc.settings')
django.setup()
from api.models import Jockey, HorseRank, Trainer, Horse, TrainerRecord, JockeyRecord

from spider.base import BaseSpider
from utils.httpclient import HttpClient
from utils.settings import SAVE
from utils.config import Config
from utils.decorators import retry


class Rank(BaseSpider):
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
        hrefs_ = html.xpath("//div[@class='newBtnContainer']//a[@href]/@href")
        hrefs = html.xpath("//div[@class='raceNum clearfix']//a[@href]/@href")
        # 判断是否存在历史数据
        last = self.url.split('/')[-1]
        if not last or last == "1":
            if hrefs_:
                hrefs.extend(hrefs_)
            for href in hrefs:
                find = re.search(r'Simulcast/(\d+\/[A-Z0-9]+)', href)
                if find:
                    href = f'https://racing.hkjc.com/racing/overseas/chinese/racecard.aspx?para=/{find.group(1)}/1'
                self.href.append(href)
        # 添加赛马 骑师 练师链接
        hrefs = html.xpath("//div[@class='rowDiv10']//a[@href]/@href")
        self.href.extend(hrefs)
        # 解析页面
        self.single(self.content)
        self.status = True

    def single(self, content):
        html = etree.HTML(content)
        rank_tag = re.search(r'/(\d{8})/', content).group(1)
        row_div = html.xpath('//div[@class="rowDiv10"]/div[@class="rowDivLeft divWidth400"]')
        string = row_div[0].xpath('string(.)')
        string = string.replace('\r\n', '').replace(' ', '')
        patt = r'第(\d+)場 - (.*?)(\d{4}年\d+月\d+日),(星期.),(.*?),([0-9:]+)(.*?),(.*?)(\d+)米(.*)獎金:\$([0-9,]+),(.*?),(.*?)$'
        find = re.search(patt, string)
        if find:
            field = dict()
            self.rank_tag = rank_tag + find.group(1)
            field['rank_tag'] = self.rank_tag
            field['place'] = find.group(5)
            if find.group(5) == '沙田':
                self.rank_mask = 'ST'
            elif find.group(5) == '跑馬地':
                self.rank_mask = 'HV'
            field['rank_mask'] = self.rank_mask
            field['number'] = find.group(1)
            field['name'] = find.group(2)
            field['rank_date'] = find.group(3) + " " + find.group(6)
            field['field'] = find.group(7)
            field['track'] = find.group(8).replace(',', '') if find.group(8) else ''
            field['route'] = find.group(9)
            field['site_condition'] = find.group(10).replace(',', '')
            field['reward'] = find.group(11)
            field['score'] = find.group(12).replace('評分:', '')
            field['race_class'] = find.group(13)
            self.result['field'] = field
        trs = html.xpath(
            "//table[@class='draggable hiddenable']/tr[@class='font13 tdAlignC trBgWhite' or @class='font13 tdAlignC trBgGrey1']")
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
            single['number'] = text[0]
            single['performance'] = text[1]
            single['horse'] = text[3]
            single['stigma'] = text[4]
            single['weight_bear'] = text[5]
            single['jockey'] = text[6]
            single['is_over_weight'] = text[7]
            single['position'] = text[8]
            single['trainer'] = text[9]
            single['score'] = text[10]
            single['score_plus'] = text[11]
            single['position_weight'] = text[12]
            single['position_weight_plus'] = text[13]
            single['best_time'] = text[14]
            single['horse_age'] = text[15]
            single['horse_pound'] = text[16]
            single['sex'] = text[17]
            single['reward'] = text[18]
            single['priority_order'] = text[19]
            single['equipment'] = text[20]
            single['owner'] = text[21]
            single['father'] = text[22]
            single['mother'] = text[23]
            single['imported_type'] = text[24]
            single['classify'] = '参赛'
            data.append(single)
        trs = html.xpath("//table[@class='tableBorderBlue']/tbody/tr[@class='trBgWhite tdAlignV tdAlignC font13']")
        for tr in trs:
            text = []
            for x in tr.xpath('./td'):
                text.append(x.xpath('string(.)').replace('\r\n', '').strip())
            single = dict()
            single['rank_tag'] = self.rank_tag
            single['rank_mask'] = self.rank_mask
            single['number'] = text[0]
            single['performance'] = text[6]
            single['horse'] = text[1]
            single['stigma'] = ''
            single['weight_bear'] = text[3]
            single['jockey'] = ''
            single['is_over_weight'] = ''
            single['position'] = ''
            single['trainer'] = text[7]
            single['score'] = text[4]
            single['score_plus'] = ''
            single['position_weight'] = text[2]
            single['position_weight_plus'] = ''
            single['best_time'] = ''
            single['horse_age'] = text[5]
            single['horse_pound'] = ''
            single['sex'] = ''
            single['reward'] = ''
            single['priority_order'] = text[8]
            single['equipment'] = text[9]
            single['owner'] = ''
            single['father'] = ''
            single['mother'] = ''
            single['imported_type'] = ''
            single['classify'] = '后备'
            data.append(single)
        self.result['rank'] = data

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
    jockey_record = JockeyRecord.objects.all()
    for jockey in jockey_record:
        print(jockey.to_dict())
        _jockey = Jockey.objects.get(name=jockey.name)
        jockey.jockey_id = _jockey.jockey_id
        print(jockey.jockey_id)
        jockey.save()

