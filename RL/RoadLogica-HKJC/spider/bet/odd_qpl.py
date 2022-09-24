import re
import json
import copy
import datetime

from spider.bet.odd import OddSpider, django
from utils.httpclient import HttpClient
from utils.decorators import retry
from utils.config import Config


class OddQplSpider(OddSpider):
    type = 'qpl'

    @retry(times=3, delay=3)
    def get_data(self):
        rank_time = self.get_odds()
        if not rank_time:
            return
        self.init_url()
        rank_date = self.params.get('date').replace('-', '')
        response = HttpClient.get(url=self.url, proxies=self.proxies)
        content = json.loads(response.content)
        out = content.get("OUT").split("@@@")
        for i, win in enumerate(out):
            if "WIN" in win and 'PLA' in win:
                tmp = {}
                words = re.split(r';|#', win)
                tag = None
                for word in words:
                    if word in ['WIN', 'PLA']:
                        tag = word.lower()
                    else:
                        find = re.search(r'(\d+)=([0-9\.]+)=\d+', word)
                        if find and rank_time[i - 1] >= datetime.datetime.now():
                            _tmp = {tag: float(find.group(2)), 'number': int(find.group(1)), 'raceno': i}
                            _tmp.update({
                                'rank_tag': f"{rank_date}{i}",
                                'date': rank_time[i - 1].strftime('%Y-%m-%d %H:%M:%S'),
                                'venue': self.params.get('venue'),
                            })
                            if tmp.get(find.group(1)):
                                tmp[find.group(1)].update(_tmp)
                            else:
                                tmp[find.group(1)] = _tmp
                self.data.extend(tmp.values())
        # self.save()

    def save(self):
        from bet.models import BetOdds
        for dt in self.data:
            tmp = copy.deepcopy(dt)
            tmp.pop('win')
            tmp.pop('pla')
            values = 'rank_tag,raceno,number,win,pla'
            val = BetOdds.objects.filter(**tmp).values(*values.split(',')).order_by('-create_date').first()
            if val and Config.cmp_dict(val, dt, False):
                continue
            BetOdds.objects.create(**dt)
        self.data.clear()


if __name__ == '__main__':
    info = {}
    odd_wp = OddQplSpider(info)
    while True:
        odd_wp.get_data()
        import time

        time.sleep(60)
