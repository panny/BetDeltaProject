import re
import json
from lxml import etree
from urllib.parse import urlencode

from spider.base import BaseSpider
from utils.httpclient import HttpClient
from utils.config import Config
from utils.settings import JOCKEY, PLACE, SAVE
from utils.decorators import retry


class Jockey(BaseSpider):
    jockey_id = None
    name = None
    records = []
    Season = 'Current'

    @retry(times=2, delay=1)
    def crawl(self):
        if not self.content:
            response = HttpClient.get(self.session, url=self.url)
            self.content = response.text
        if '沒有相關資料' in self.content:
            self.Season = 'Previous'
            if 'Season' not in self.url:
                self.url = f"{self.url}&Season={self.Season}"
            self.content = None
            raise Exception(f"Jockey {self.url} 沒有相關資料")
        html = etree.HTML(self.content)
        self.jockey_id = re.search(r'JockeyId=(.*?)&', self.content).group(1)
        self.name = html.xpath('string(//p[@class="tit"])').replace('\r\n', '').strip()
        trs = html.xpath('//div[@class="trainer_right f_ffChinese trainer_right_filecontent_ch"]/table/tr')
        jockey = dict()
        jockey['jockey_id'] = self.jockey_id
        jockey['name'] = self.name
        jockey['url'] = self.url
        for tr in trs:
            text = tr.xpath('string(.)').replace('\r\n', '').strip()
            if "：" in text:
                words = text.split('：', 1)
                key = words[0].strip()
                val = words[-1].strip()
                key_ = Config.get_key(key, JOCKEY)
                if key_:
                    jockey[key_] = val
        trs = html.xpath('//div[@class="seasonTab"]/table/tbody/tr/td[contains(text(), ":")]')
        text = []
        for tr in trs:
            text.append(tr.xpath('string(.)').strip())
        jockey['ten_rank_times'] = text[0].replace(':', '').strip()
        jockey['ten_head_horse'] = text[2].replace(':', '').replace('$', '').strip()
        jockey['ten_win_score'] = text[4].replace(':', '').strip()
        jockey['ten_position_times'] = text[1].replace(':', '').strip()
        jockey['ten_position_score'] = text[3].replace(':', '').strip()
        self.result['jockey'] = jockey
        trs = html.xpath('//div[@class="performance"]/table/tbody/tr')
        data = []
        place, track = None, None
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
                    place, track = text[0], None
                else:
                    track = text[0]
            single = dict()
            single['jockey_id'] = self.jockey_id
            single['name'] = self.name
            single['place'] = place
            single['track'] = track
            single['route'] = text[-5]
            single['first'] = text[-4]
            single['second'] = text[-3]
            single['third'] = text[-2]
            single['rank_times'] = text[-1]
            data.append(single)
        self.result['jockey_rank'] = data
        self.rank_record()
        self.status = True

    def rank_record(self, url=None):
        if not url:
            params = {'JockeyId': self.jockey_id, 'Season': self.Season}
            url = f"https://racing.hkjc.com/racing/information/chinese/Jockey/JockeyPastRec.aspx?{urlencode(params)}"
        response = HttpClient.get(self.session, url=url)
        html = etree.HTML(response.text)
        jockey = dict()
        jockey['jockey_id'] = self.jockey_id
        trs = html.xpath('//div[@class="seasonTab"]/table/tbody/tr/td[contains(text(), ":")]')
        text = []
        for tr in trs:
            text.append(tr.xpath('string(.)').strip())
        jockey['country'] = text[0].replace(':', '').strip()
        jockey['reward'] = text[3].replace(':', '').replace('$', '').strip()
        jockey['rank_times'] = text[2].replace(':', '').strip()
        jockey['win_score'] = text[5].replace(':', '').strip()
        jockey['first'] = text[1].replace(':', '').strip()
        jockey['second'] = text[4].replace(':', '').strip()
        if len(text) == 10:
            jockey['win_times'] = text[6].replace(':', '').strip()
            jockey['avg_score'] = text[8].replace(':', '').strip()
            jockey['third'] = text[7].replace(':', '').strip()
            jockey['forth'] = text[9].replace(':', '').strip()
        elif len(text) == 8:
            jockey['third'] = text[6].replace(':', '').strip()
            jockey['forth'] = text[7].replace(':', '').strip()
        self.result = Config.edit_dict({'jockey': jockey}, self.result)
        trs = html.xpath('//div[@class="ridingRec"]/table/tbody/tr')
        data = []
        date, place = None, None
        for tr in trs:
            text = []
            for x in tr.xpath('./td'):
                text.append(x.xpath('string(.)').replace('\r\n', '').strip())
            if len(text) == 1:
                date, place = text[0].split('  ')
            elif len(text) == 13:
                single = dict()
                single['jockey_id'] = self.jockey_id
                single['name'] = self.name
                single['rank_date'] = date
                single['place'] = place.split(" ")[0]
                single['rank_id'] = text[0]
                single['ranking'] = text[1]
                single['track'] = text[2]
                single['route'] = text[3]
                single['race_class'] = text[4]
                single['site_condition'] = text[5]
                single['horse'] = text[6]
                single['position'] = text[7]
                single['score'] = text[8]
                single['trainer'] = text[9]
                single['equipment'] = text[10]
                single['horse_weight'] = text[11]
                single['actual_pound'] = text[12]
                data.append(single)
        self.records.extend(data)
        self.result['jockey_record'] = self.records
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
                response = HttpClient.get(url=info.get('url'), params={'jockey_id': self.jockey_id})
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
    info = {'url': 'https://racing.hkjc.com/racing/information/chinese/Jockey/JockeyWinStat.aspx?JockeyId=WD',
            'task_id': '20200710', 'tags': '20200710'}
    rank = Jockey(**info)
    rank.get_data()
