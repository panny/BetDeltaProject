
hkjc爬虫项目
=======


### 下载安装

* 安装依赖:

```shell
pip freeze > requirements.txt
pip install -r requirements.txt
```

* 配置hkjc/settings.py:

```shell
# api/tasks.py 项目配置文件

BROKER_URL='redis://127.0.0.1:6379/1',
CELERY_RESULT_BACKEND='redis://127.0.0.1:6379/2',


# 配置 celery服务
celery -A api.tasks beat -l info

celery -A api.tasks worker -l info -Q default

celery -A api.tasks worker -l info -Q save

celery -A api.tasks worker -l info -Q run

```

* 启动:

```shell
# 进入到项目根目录
python manage.py runserver 0.0.0.0:8000
```

### 使用

　1.通过api访问 http://127.0.0.1:8000/admin/

　账号/密码: admin/admin
    
　2.安装redis服务 

　3.安装chromedriver, 并添加到系统环境
　http://npm.taobao.org/mirrors/chromedriver/
    


* 任务添加

　　如果要添加新的celery任务, api/tasks.py 中新建一个方法 例如：

```python
from celery import shared_task

@shared_task
def add(x, y):
    return x + y
```

### 扩展爬虫
    项目默认爬虫基类为spider/base.py中BaseSpider类

* 创建一个新的Spider
 ```python
from spider.base import BaseSpider

class NewSpider(BaseSpider):
    
    def init_url(self):
        '''
        初始化info参数
        '''
        pass
    
    def check_cookie(self):
        '''
        检测cookie是否有效
        '''
        pass
        
    def crawl(self):
        '''
        数据接口请求逻辑，主逻辑程序
        '''
        pass
    
    def save(self):
        '''
        保存数据
        '''
        pass
        
    def dispatch(self):
        '''
        爬取下一层链接
        '''
        pass
    
    def finish(self):
        '''
        任务处理完响应
        '''
        pass

```
