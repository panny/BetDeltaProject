import requests
import time
import copy
import json
import traceback
from selenium import webdriver
from utils.config import Config
from utils.httpclient import HttpClient
from utils.settings import SPIDER_UR
from utils.time import Time


class BaseSpider(object):

    def __init__(self, **kwargs):
        self.info = kwargs
        self.session = requests.Session()
        self.url = None
        self.result = {}
        self.href = []
        self.status = False
        self.content = None

    def init_url(self):
        if "url" in self.info and self.info.get("url"):
            self.url = self.info.get("url")
        elif self.info and self.info.get("params"):
            name = self.__class__.__name__
            if name in SPIDER_UR:
                params = "&".join(
                    [f"{key}={val}" for key, val in self.info.get("params").items()])
                self.url = f"{SPIDER_UR[name].get('url')}?{params}"
            self.info.pop("params")
        if self.url:
            info = Config.get_re_url(self.url)
            self.info.update(info)

    def duplicate(self):
        pass

    def check_cookie(self):
        redis_client = Config.get_redis_client()
        cookie = redis_client.get('Cookie')
        if cookie:
            self.session.headers['Cookie'] = cookie
            response = HttpClient.get(self.session, url=self.url)
            if 'GenericErrorMessageCookies' not in response.text:
                self.url = response.url
                self.content = response.text
                return True
        return False

    def chrome(self):
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
        browser = webdriver.Chrome(chrome_options=chrome_options)
        browser.get(self.url)
        if not browser.get_cookies():
            time.sleep(3)
        time.sleep(10)
        cookie = ";".join(
            [f"{x.get('name')}={x.get('value')}" for x in browser.get_cookies()])
        redis_client = Config.get_redis_client()
        redis_client.set('Cookie', cookie)
        self.session.headers['Cookie'] = cookie
        self.content = browser.page_source
        self.url = browser.current_url
        browser.close()
        browser.quit()

    def crawl(self):
        pass

    def get_data(self):
        self.init_url()
        if not self.url:
            return
        try:
            if not self.check_cookie():
                self.chrome()
            self.crawl()
            self.save()
        except Exception as ex:
            print(ex, traceback.format_exc())
        self.finish()
        self.dispatch()

    def data_duplicate(self):
        pass

    def save(self):
        if self.result:
            self.data_duplicate()
            from api import tasks
            for key, val in self.result.items():
                tasks.model_save.delay(tb_name=key, data=val)

    def dispatch(self):
        if self.href:
            from api import tasks
            for href in self.href:
                info = Config.get_re_url(href)
                if info and info.get("url"):
                    url = "http://127.0.0.1:8000/api/task/"
                    tmp = {
                        'url': info.get('url'),
                        'type': 'distinct',
                    }
                    tags = self.info.get(
                        'tags', Time.get_format_time(t_format='%Y%m%d'))
                    tmp['tags'] = tags
                    response = HttpClient.get(url=url, params=tmp)
                    content = json.loads(response.content)
                    if content and content.get("status") == "200" and content.get("data"):
                        continue
                    task_id = self.info.get(
                        'task_id', Time.get_format_time(t_format='%Y%m%d'))
                    info['task_id'] = task_id
                    info['tags'] = tags
                    info['finish'] = '0'
                    HttpClient.post(url=url, data=info)

    def finish(self):
        if self.info.get('url') and self.__class__.__name__ in SPIDER_UR:
            tmp = copy.deepcopy(self.info)
            if 'name' not in tmp:
                tmp.update(Config.get_url_info(self.url))
            if 'flag' in tmp:
                tmp.pop('flag')
            tmp['finish'] = '2' if self.status else '3'
            url = "http://127.0.0.1:8000/api/task/"
            task_id = self.info.get(
                'task_id', Time.get_format_time(t_format='%Y%m%d'))
            tmp['task_id'] = task_id
            tags = self.info.get(
                'tags', Time.get_format_time(t_format='%Y%m%d'))
            tmp['tags'] = tags
            HttpClient.post(url=url, data=tmp)
