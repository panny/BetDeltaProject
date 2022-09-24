import re
import json
import copy
import datetime

from spider.bet.odd import OddSpider, django
from utils.httpclient import HttpClient
from utils.decorators import retry
from utils.config import Config


class OddWpSpider(OddSpider):
    type = 'winplaodds'

    @retry(times=3, delay=3)
    def get_data(self):
        rank_time = self.get_odds()
        if not rank_time:
            return
        self.init_url()
        rank_date = self.params.get('date').replace('-', '')
        response = HttpClient.get(self.session, url=self.url, proxies=self.proxies)
        if not Config.is_json(response.text):
            self.init_cookie()
            raise Exception("Cookie失效")
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
                        if find and rank_time.get(f"{i}") and rank_time.get(f"{i}") >= datetime.datetime.now():
                            _tmp = {tag: float(find.group(2)), 'number': int(find.group(1)), 'raceno': i}
                            _tmp.update({
                                'rank_tag': f"{rank_date}{i}",
                                'date': rank_time[f"{i}"].strftime('%Y-%m-%d %H:%M:%S'),
                                'venue': self.params.get('venue'),
                            })
                            if tmp.get(find.group(1)):
                                tmp[find.group(1)].update(_tmp)
                            else:
                                tmp[find.group(1)] = _tmp
                self.data.extend(tmp.values())
        self.save()

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
    odd_wp = OddWpSpider(info)
    # odd_wp.chrome()
    while True:
        try:
            odd_wp.get_data()
            # break
        except Exception:
            pass
        finally:
            import time
            time.sleep(60)
