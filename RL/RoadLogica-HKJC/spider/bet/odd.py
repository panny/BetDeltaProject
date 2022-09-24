from utils.config import Config
from utils.httpclient import HttpClient
from utils.time import Time
from spider.base import BaseSpider
import furl
import re
import os
import json
import time
import django
import datetime
from selenium import webdriver
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hkjc.settings')
django.setup()


class OddSpider(BaseSpider):

    def __init__(self, info: dict = dict()):
        self.proxies = {
            'http': 'http://127.0.0.1:10808',
            'https': 'https://127.0.0.1:10808'
        }
        self.data = []
        self.params = info.get('params', {})
        super(OddSpider, self).__init__(info=info)

    def init_url(self):
        if self.info.get("url"):
            self.url = self.info.get("url")
            self.params = furl.furl(self.url).args
        elif self.params:
            url = "https://bet.hkjc.com/racing/getJSON.aspx"
            params = "&".join(
                [f"{key}={val}" for key, val in self.params.items()])
            self.url = f"{url}?{params}"

    def init_cookie(self):
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("–ignore-certificate-errors")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument(f'--proxy-server=http://127.0.0.1:1080')
        browser = webdriver.Chrome(chrome_options=chrome_options)
        browser.get("https://bet.hkjc.com/racing/index.aspx?lang=ch")
        if not browser.get_cookies():
            time.sleep(3)
        time.sleep(10)
        cookie = ";".join(
            [f"{x.get('name')}={x.get('value')}" for x in browser.get_cookies()])
        redis_client = Config.get_redis_client()
        redis_client.set('Cookie', cookie)
        self.session.headers['Cookie'] = cookie
        browser.close()
        browser.quit()

    def save(self):
        pass

    def get_odds(self, rank_mask='HV,ST'):
        url = f"http://127.0.0.1:8000/api/field/?type=odds&rank_mask={rank_mask}"
        response = HttpClient.get(url=url)
        content = json.loads(response.content)
        rank_times = {}
        start, end = 0, 0
        date, venue = None, None
        for data in content.get('data'):
            rank_date = datetime.datetime.strptime(
                data.get('rank_date'), '%Y年%m月%d日 %H:%M')
            if not self.params:
                date, num = data.get('rank_tag')[:8], data.get('rank_tag')[8:]
                date = Time.convert_time_format_by_string(
                    date, '%Y%m%d', '%Y-%m-%d')
                venue = data.get('rank_mask')
                if int(num) < start or start == 0:
                    start = int(num)
                if int(num) > end or start == 0:
                    end = int(num)
                rank_times[num] = rank_date
        if start and end and date and venue:
            self.params.update({
                'type': self.type,
                'date': date,
                'venue': venue,
                'start': start,
                'end': end,
            })
        return rank_times
