import re
import json
import furl
from lxml import etree

from spider.base import BaseSpider
from utils.httpclient import HttpClient
from utils.config import Config
from utils.decorators import retry
from utils.settings import JOCKEY, PLACE, SAVE


class Trainer(BaseSpider):
    trainer_id = None
    name = None

    records = []

    def crawl(self):
        if not self.content:
            response = HttpClient.get(self.session, url=self.url)
            self.content = response.text
        if '沒有相關資料' in self.content:
            self.status = True
            return
        html = etree.HTML(self.content)
        self.trainer_id = re.search(r'TrainerId=(.*?)&', self.content).group(1)
        self.name = html.xpath('string(//p[@class="tit"])').replace('\r\n', '').strip()
        trainer = dict()
        trainer['trainer_id'] = self.trainer_id
        trainer['name'] = self.name
        trainer['url'] = self.url
        trs = html.xpath('//div[@class="trainer_right f_ffChinese trainer_right_filecontent_ch"]/table/tr')
        for tr in trs:
            text = tr.xpath('string(.)').replace('\r\n', '').strip()
            if "：" in text:
                words = text.split('：', 1)
                key = words[0].strip()
                val = words[-1].strip()
                key_ = Config.get_key(key, JOCKEY)
                if key_:
                    trainer[key_] = val
        trs = html.xpath('//div[@class="seasonTab"]/table/tbody/tr/td[contains(text(), ":")]')
        text = []
        for tr in trs:
            text.append(tr.xpath('string(.)').strip())
        trainer['ten_rank_times'] = text[0].replace(':', '').strip()
        trainer['ten_win_times'] = text[1].replace(':', '').strip()
        trainer['ten_win_score'] = text[2].replace(':', '').strip()
        trainer['ten_position_times'] = text[3].replace(':', '').strip()
        trainer['ten_position_score'] = text[4].replace(':', '').strip()
        self.result['trainer'] = trainer
        trs = html.xpath('//div[@class="performance"]/table/tbody/tr')
        data = []
        place, track = '', ''
        for tr in trs:
            text = []
            for x in tr.xpath('./td'):
                text.append(x.xpath('string(.)').replace('\r\n', '').strip())
            if text[0] == '合計':
                continue
            if len(text) == 7:
                place, track = text[0], text[1]
            elif len(text) == 6:
                if text[0] in PLACE:
                    place, track = text[0], ''
                else:
                    track = text[0]
            single = dict()
            single['name'] = self.name
            single['trainer_id'] = self.trainer_id
            single['place'] = place
            single['track'] = track
            single['route'] = text[-5]
            single['first'] = text[-4]
            single['second'] = text[-3]
            single['third'] = text[-2]
            single['rank_times'] = text[-1]
            data.append(single)
        self.result['trainer_rank'] = data
        self.rank_record()
        self.status = True

    def rank_record(self, url=None):
        if not url:
            url = "https://racing.hkjc.com/racing/information/Chinese/Trainers/TrainerPastRec.aspx?TrainerId=" + self.trainer_id
        response = HttpClient.get(self.session, url=url)
        html = etree.HTML(response.text)
        trainer = dict()
        trainer['trainer_id'] = self.trainer_id
        trs = html.xpath('//div[@class="seasonTab"]/table/tbody/tr/td[contains(text(), ":")]')
        text = []
        for tr in trs:
            text.append(tr.xpath('string(.)').strip())
        trainer['rank_times'] = text[1].replace(':', '').strip()
        trainer['first'] = text[0].replace(':', '').strip()
        trainer['second'] = text[2].replace(':', '').strip()
        trainer['third'] = text[4].replace(':', '').strip()
        trainer['reward'] = text[3].replace(':', '').replace('$', '').strip()
        self.result = Config.edit_dict({'trainer': trainer}, self.result)
        trs = html.xpath('//div[@class="performance"]/table/tbody/tr')
        data = []
        for tr in trs:
            text = []
            for x in tr.xpath('./td'):
                text.append(x.xpath('string(.)').replace('\r\n', '').strip())
            single = dict()
            single['name'] = self.name
            single['trainer_id'] = self.trainer_id
            single['rank_id'] = text[0]
            single['horse'] = text[1]
            single['ranking'] = text[2]
            single['rank_date'] = text[3]
            single['track'] = text[4]
            single['route'] = text[5]
            single['site_condition'] = text[6]
            single['position'] = text[7]
            single['score'] = text[8]
            single['odds'] = text[9]
            single['jockey'] = text[10]
            single['equipment'] = text[11]
            single['horse_weight'] = text[12]
            single['actual_pound'] = text[13]
            single['first'] = text[14]
            single['second'] = text[15]
            single['third'] = text[16]
            data.append(single)
        self.records.extend(data)
        self.result['trainer_record'] = self.records
        if self.info.get('flag', 0) == 1 and html.xpath("//a[text()='下一頁']"):
            hrefs = html.xpath("//a[text()='下一頁']/@href")
            href = f"https://racing.hkjc.com/{hrefs[0]}"
            self.rank_record(href)

    @retry(times=3)
    def data_duplicate(self):
        tmp = {}
        for key, val in self.result.items():
            if isinstance(val, list) and key in SAVE:
                info = SAVE[key]
                response = HttpClient.get(url=info.get('url'), params={'trainer_id': self.trainer_id})
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
    info = {'url': 'https://racing.hkjc.com/racing/information/Chinese/Trainers/TrainerWinStat.aspx?TrainerId=MKL',
            'task_id': '20200710', 'tags': '20200710'}
    rank = Trainer(**info)
    rank.get_data()
