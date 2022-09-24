import json
import pandas as pd
import numpy as np
import time
import pickle
from datetime import datetime, timedelta



chdriver = '/usr/bin/chromedriver'
capabilities = {
  'browserName': 'chrome',
  'chromeOptions':  {
    'useAutomationExtension': False,
    'forceDevToolsScreenshot': True,
    'args': [
        '--headless', 
        '--disable-infobars', '--profile-directory=Default'
        ,'--disable-dev-shm-usage', '--dns-prefetch-disable'
        ,"--user-agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'"
    ]
  }
}

# def get0(driver):
#     from selenium import webdriver
#     from datetime import datetime
#     from selenium.webdriver.support.select import Select
#     from selenium.common.exceptions import NoSuchElementException
#     from selenium.webdriver.support import expected_conditions as EC
#     from selenium.webdriver.support.ui import WebDriverWait
#     from selenium.webdriver.common.by import By

#     import time
#     import re

# #     time.sleep(5)
# #    b = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '/html/body')))
#     b = WebDriverWait(driver, 30).until(EC.url_matches('venue='))

#     try:
# # 20191019 amended
# #         elem = driver.find_element_by_xpath('//*[@id="OddsTable"]/tbody/tr[2]/td[2]/table/tbody/tr/td[2]/table[1]/tbody/tr[2]/td/div/table/tbody/tr/td[1]/select')
#         elem = driver.find_element_by_xpath('/html/body/div[7]/div/div[2]/table[1]/tbody/tr[2]/td/div/table/tbody/tr/td[1]/select')
#         select_fr = Select(elem)
#         yt=[opt.text  for opt in elem.find_elements_by_tag_name('option') ]
#         yt2=[re.match (r'(.*)Sha Tin(.*)|(.*)Happy Valley(.*)',ytt) is not None for ytt in yt]
#         select_fr.select_by_visible_text(yt[yt2.index(True)])
#         b = WebDriverWait(driver, 30).until(EC.url_matches('venue='+yt[yt2.index(True)].split(' ')[-2][0]+yt[yt2.index(True)].split(' ')[-1][0]))
#     except NoSuchElementException: 
#         pass

#     currentlink=driver.current_url
# #    print(currentlink)
# #    print(driver.page_source)
#     from bs4 import BeautifulSoup
#     soup = BeautifulSoup(driver.page_source, 'html.parser')

#     import re
#     racePostTimex=[]
#     for i, xxx in enumerate(soup.findAll('script')):
#         r1 = re.findall(r'racePostTime(.*)',xxx.text)
#         if r1!=[]: racePostTimex = list(set(r1[0].split("'")[1].split('@@@'))-set(['']))

#     racePostTimex=[datetime.strptime(xx, "%Y-%m-%d %H:%M:%S") for xx in racePostTimex]
#     racePostTimex=sorted(racePostTimex)


#     vv= re.search(r'venue=\w\w', currentlink).group()
#     dd= re.search(r'date=\d\d\d\d-\d\d-\d\d',currentlink).group()
#     nn=len(racePostTimex)
# #     try:
# #         nn= re.search(r'raceno=\d+',currentlink).group()
# #     except :
# #         nn='raceno=1'


#     return racePostTimex,dd, vv, nn
# def get0(driver):
    
#     import requests
#     import json
#     a =requests.get('https://bet.hkjc.com/racing/script/rsdata.js?lang=en&CV=L3.05R1c').text
#     #"https://bet.hkjc.com/racing/script/rsstr.js?lang=en&CV=L3.05R1c" another js for reference
#     b={x.split("=")[0].strip():x.split("=")[1].strip() for x in a.replace('var ','').replace("'",'').split(';\n')[:-1] }
#     print(b)
#     racePostTimex=[datetime.strptime(xx, "%Y-%m-%d %H:%M:%S") for xx in json.loads(b['racePostTime']) if xx !='']
#     vv=f"venue={b['mtgVenue']}"
#     dd=f"date={b['mtgDate']}"
#     nn=len(racePostTimex)
#     assert nn==int(b['mtgTotalRace'])
#     return racePostTimex,dd, vv, nn
    
# def get0(driver):
    
#     import requests
#     import json
#     import pickle
#     import time
#     a =requests.get('https://bet.hkjc.com/racing/script/rsdata.js?lang=en&CV=L3.05R1c').text
#     #"https://bet.hkjc.com/racing/script/rsstr.js?lang=en&CV=L3.05R1c" another js for reference
#     b={x.split("=")[0].strip():x.split("=")[1].strip() for x in a.replace('var ','').replace("'",'').split(';\n')[:-1] }
#     print(b.keys())
#     ncount=0
#     while(1):
#         try:
#             ncount = ncount +1
#             print('>>>',ncount)
#             if ncount >10: break  
#             b['racePostTime']=[datetime.strptime(xx, "%Y-%m-%d %H:%M:%S") for xx in json.loads(b['racePostTime']) if xx !='']
#             racePostTimex=b['racePostTime']
#             vv=f"venue={b['mtgVenue']}"
#             dd=f"date={b['mtgDate']}"
#             nn=len(racePostTimex)
#             assert nn==int(b['mtgTotalRace'])
#             pth=gethomedir()
#             with open(pth+pth.split('/')[-2]+'_'+getptime()+'_rawi.pickle', 'wb') as outfile:
#                     pickle.dump(b, outfile)
#             break
#         except:
#             time.sleep(np.random.uniform()*10)
#             a =requests.get('https://bet.hkjc.com/racing/script/rsdata.js?lang=en&CV=L3.05R1c').text
#             b={x.split("=")[0].strip():x.split("=")[1].strip() for x in a.replace('var ','').replace("'",'').split(';\n')[:-1] }
#     if ncount > 10 : 
#         return 
#     else: 
#         return racePostTimex,dd, vv, nn


# def get0(driver):
    
#     import requests
#     import json
#     import pickle
#     import time
#     import os
#     a =[requests.get('https://bet.hkjc.com/racing/script/rsdata.js?lang=en&CV=L3.05R1c').text for i in range(10)]
#     #"https://bet.hkjc.com/racing/script/rsstr.js?lang=en&CV=L3.05R1c" another js for reference
#     aa=[{x.split("=")[0].strip():x.split("=")[1].strip() for x in ii.replace('var ','').replace("'",'').split(';\n')[:-1] } for ii in a]
    
#     c={i['mtgVenue']:i for i in aa if 'mtgVenue' in i.keys()}
#     b=[c[x] for x in c.keys() if x in ['ST','HV']][0]
#     b['racePostTime']=[datetime.strptime(xx, "%Y-%m-%d %H:%M:%S") for xx in json.loads(b['racePostTime']) if xx !='']
#     racePostTimex=b['racePostTime']
#     vv=f"venue={b['mtgVenue']}"
#     dd=f"date={b['mtgDate']}"
#     nn=len(racePostTimex)
#     assert nn==int(b['mtgTotalRace'])
    
#     pth = f'/home/ec2-user/hrpgm/meetings/{datetime.strptime(b["mtgDate"], "%Y-%m-%d").strftime("%Y%m%d")}/'
#     if not os.path.exists(pth):
#         os.makedirs(pth, exist_ok=True)
#         print(f'create a path {pth}')

    
#     with open(pth+pth.split('/')[-2]+'_'+getptime()+'_rawi.pickle', 'wb') as outfile:
#             pickle.dump(b, outfile)
    
#     return racePostTimex,dd, vv, nn

def get0(driver):
    
    import requests
    import json
    import pickle
    import time
    import os
    #"https://bet.hkjc.com/racing/script/rsstr.js?lang=en&CV=L3.05R1c" another js for reference
    #20200223 change to CV=L3.05R1g_1
    #20210105 change to CV=L3.08R1a
    def getkey():
        return {y['mtgVenue']:y for y in 
            [{x.split("=")[0].strip():x.split("=")[1].strip()   
            for x in ii.replace('var ','').replace("'",'').split(';\n')[:-1]}
            for ii in [requests.get('https://bet.hkjc.com/racing/script/rsdata.js?lang=en&CV=L3.08R1a').text for i in range(10)]
            ] if ('mtgVenue' in y.keys())}
    cnt = 0
    while(1):
        cnt+=1
        a=getkey()
        rin= list(set(['ST','HV']).intersection(set(a.keys()))) 
        if rin != []: 
            print(cnt,">>>", rin)
            b=a[rin[0]]
            break
        if cnt > 10: break

    b['racePostTime']=[datetime.strptime(xx, "%Y-%m-%d %H:%M:%S") for xx in json.loads(b['racePostTime']) if xx !='']
    racePostTimex=b['racePostTime']
    vv=f"venue={b['mtgVenue']}"
    dd=f"date={b['mtgDate']}"
    nn=len(racePostTimex)
    assert nn==int(b['mtgTotalRace'])
    
    pth = f'/home/ec2-user/hrpgm/meetings/{datetime.strptime(b["mtgDate"], "%Y-%m-%d").strftime("%Y%m%d")}/'
    if not os.path.exists(pth):
        os.makedirs(pth, exist_ok=True)
        print(f'create a path {pth}')

    
    with open(pth+pth.split('/')[-2]+'_'+getptime()+'_rawi.pickle', 'wb') as outfile:
            pickle.dump(b, outfile)
    
    return racePostTimex,dd, vv, nn



# def get_timeinfo(outvalue='all'):
#     import time
# #     from selenium.webdriver.support import expected_conditions as EC
# #     from selenium.webdriver.support.ui import WebDriverWait
# #     from selenium.webdriver.common.by import By

#     driver=createdriver()
#     driver.get('https://bet.hkjc.com/racing/index.aspx?lang=en')
# #     b = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/table/tbody/tr[1]/td')))

# #     time.sleep(5)
#     racePostTimex,dd, vv, nn=get0(driver)

#     quitdriver(driver)

#     if outvalue=='all' :
#         print(racePostTimex, dd, vv, nn)
#     if outvalue=='1race' :
#         print(racePostTimex[0].strftime("%Y-%m-%dT%H:%M:%S"))
#     if outvalue=='date' :
#         print(dd.split('=')[1])
#     if outvalue=='venue' :
#         print(vv.split('=')[1])
#     if outvalue=='1racevenue' :
#         print(racePostTimex[0].strftime("%Y-%m-%dT%H:%M:%S")," ",vv.split('=')[1])
# #     driver.quit()

#     return racePostTimex,dd, vv, nn



def createdriver():
    from selenium import webdriver
    driver = webdriver.Chrome(chdriver, desired_capabilities=capabilities) 
    return driver

def quitdriver(x):
    x.quit()

def getdriverinfo(x):
    return [x.command_executor._url, x.session_id]

# def hookdriver(tm):
#     from selenium import webdriver

#     executor_url, session_id = tm
#     driver = webdriver.Remote(command_executor=executor_url, desired_capabilities=capabilities)
#     driver.session_id = session_id

#     return driver

def hookdriver(tm):
    executor_url, session_id = tm
    from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
    from selenium import webdriver

    # Save the original function, so we can revert our patch
    org_command_execute = RemoteWebDriver.execute

    def new_command_execute(self, command, params=None):
        if command == "newSession":
            # Mock the response
            return {'success': 0, 'value': None, 'sessionId': session_id}
        else:
            return org_command_execute(self, command, params)

    # Patch the function before creating the driver object
    RemoteWebDriver.execute = new_command_execute

    new_driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
    new_driver.session_id = session_id

    # Replace the patched function with original function
    RemoteWebDriver.execute = org_command_execute

    return new_driver


def getptime():
    from datetime import datetime
    return datetime.now().strftime("%Y%m%d%H%M%S")

def gethomedir():
    import pickle
    from datetime import datetime
    with open('/home/ec2-user/hrpgm/meetings/outtar.pickle', 'rb') as infile:
        outtar= pickle.load(infile)
    return '/home/ec2-user/hrpgm/meetings/'+datetime.strptime(outtar[1].split('=')[1], "%Y-%m-%d").strftime('%Y%m%d')+'/'

def getdriver(pth, worker):
    import pickle
    with open(pth+f'drivers{worker}.pickle', 'rb') as infile:
        dr = pickle.load(infile)
    return dr[worker]

def gettask(pth, worker):
    import pickle
    with open(pth+'task.pickle', 'rb') as infile:
        dr = pickle.load(infile)
    return dr[worker]

def gettarget(pth, worker):
    import pickle
    with open(pth+'target.pickle', 'rb') as infile:
        dr = pickle.load(infile)
    return dr[worker]

def getlatest(pth, ele):
    from glob import glob
    import pickle
    return pickle.load(open(sorted(glob(pth+'/*_'+ele+'.pickle'))[-1], 'rb'))

def getsecond(pth, ele):
    from glob import glob
    import pickle
    return pickle.load(open(sorted(glob(pth+'/*_'+ele+'.pickle'))[-2], 'rb'))


def get2(y):
    from selenium import webdriver
    from datetime import datetime
    from selenium.webdriver.support.select import Select
    from selenium.common.exceptions import NoSuchElementException
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.by import By

    import numpy as np
    import pandas as pd
    from bs4 import BeautifulSoup
    
    b = WebDriverWait(y, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="oddsContentMain"]/table/tbody/tr[4]/td')))


    table_id = y.find_element_by_xpath('//*[@id="oddsContentMain"]/table/tbody/tr[4]/td')

    Page_Source = table_id.get_attribute("outerHTML").encode('utf-8')

    soup = BeautifulSoup(Page_Source, 'html.parser')
    lab=[]
    b={}
    labx=[]
    trl = soup.findAll('tr')
    for ii,xx in enumerate(trl):
        for jj, yy in enumerate(xx.findAll('td', recursive=False )):
            if ii == 0:
                lab.append(yy.text.strip())
            else:
                b[lab[jj]]=yy.text
        if (b!={}):
    #         print(b)
            if (b['Race']!='') & (b['No.']!='') & (b['Win']!= 'SCR'):
                labx.append(b.copy())
    labx=pd.DataFrame(labx)
    labx['Race']=labx['Race'].astype(int)
    labx['disable']=[int(y.find_element_by_xpath('//*[@id="wipCell'+str(r) +'_'+n+'"]/input').get_attribute("disabled")=='true') for r, n in zip(labx['Race'], labx['No.'])]
    return labx

# def getnextrace(pth, src):
#     import pandas as pd
#     if src=='hkjc':
#         try:
#             labx=getlatest(pth, src+'_wp')
#             completed= labx.groupby(['Race']).agg(['sum', 'count'])['disable'].reset_index()
#             try:
#                 return sorted(list(set(list(labx.Race.unique())) - set(list(completed[completed['sum']==completed['count']]['Race']))))[0]
#             except :
#                 return 0
#         except:
#             return 0

# def getnextrace(pth, src):
#     import pandas as pd
#     if src=='hkjc':
#         try:
#             completed=getlatest(pth, 'hkjc'+'_wp').groupby(['Race']).agg(['sum', 'count'])['disable'].reset_index()
#             completed=completed.drop(completed.index[completed['sum'] ==completed['count']])
#             if completed.empty:
#                 return getlatest(pth, 'info')[-1]
#             else:
#                 return completed.Race.min()
#         except:
#             return 1

def getnextrace(pth, src):
    if src=='hkjc':
        a =getlatest(pth, 'rawi')
        return min(int(a['mtgRanRace'])+1, int(a['mtgTotalRace']))
    elif src in ['skk','ctb']:
        return getlatest(pth, 'nrtime')['Race'].unique().min()
    

def get3(driver, btype):
    import pandas as pd
    from bs4 import BeautifulSoup
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.by import By

    
    b = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="combOddsTable'+btype+'"]/table/tbody')))

    table_id = driver.find_element_by_xpath('//*[@id="combOddsTable'+btype+'"]/table/tbody')


    # table_id = driver.find_element_by_xpath('//*[@id="oddsContentMain"]/table/tbody/tr[3]/td[1]/table')
    Page_Source = table_id.get_attribute("outerHTML").encode('utf-8')
    # print(table_id.text)

    soup = BeautifulSoup(Page_Source, 'html.parser')
    # a=[]
    b=[]
    for ii,xx in enumerate(soup.findAll('tr')):
        a=[]
        for jj, yy in enumerate(xx.findAll('td', recursive=False )):
            a.append(yy.text)
        b.append(a.copy())
    c={}
    for i in range(1, 8):
        for j in range(i+1, 15):
            c[(i,j)]=b[i][j+1]
    for i in range(8,15):
        for j in range(i+1, 15):
            c[(i,j)]=b[j-7][i-7]
    return pd.DataFrame({'combination':list(c.keys()), 'odds':list(c.values())})

def get4(driver, pth, current_race):
    import json
    import numpy as np
    import pandas as pd
    from datetime import datetime
    x = driver.find_element_by_tag_name('html').text
    y=json.loads(x)


    jc= y['S'].split('@@@')[2].split('|')[1:] 
#     lo=np.array([float(iii) for iii in [ii.replace('LSE','999999999') if ii== 'LSE' else ii for ii in [i.replace('','0') if i== '' else i for i in y['S'].split('@@@')[7].split('|')[1:]  ]]])
#     co=np.array([float(iii) for iii in [ii.replace('LSE','999999999') if ii== 'LSE' else ii for ii in [i.replace('','0') if i== '' else i for i in y['S'].split('@@@')[8].split('|')[1:]  ]]])
    lo=np.array([float(iii) for iii in [ii.replace('LSE','999999999').replace('RFD','999999999') if ii in ['LSE','RFD'] else ii for ii in [i.replace('','0') if i== '' else i for i in y['S'].split('@@@')[7].split('|')[1:]  ]]])
    co=np.array([float(iii) for iii in [ii.replace('LSE','999999999').replace('RFD','999999999') if ii in ['LSE','RFD'] else ii for ii in [i.replace('','0') if i== '' else i for i in y['S'].split('@@@')[8].split('|')[1:]  ]]])

    jkc_lo={a: b for a,b in zip(jc, lo)}
    jkc_co={a: b for a,b in zip(jc, co)}
    jkc_diff={a: b for a,b in zip(jc, lo-co)}

    labx=getlatest(pth, 'hkjc_wp')

    cr_race_info=pd.DataFrame(columns=['Draw', 'Horse', 'Jockey', 'No.', 'Place', 'Race', 'Trainer', 'Win',
           'Win & Place', 'Wt.', 'disable', 'last_jkc_odd', 'curr_jkc_odd',
           'diff_jkc_odd', 'jkc_upddt'])

    # cr_race_info=labx.copy()
    cr_race_info=labx.merge(cr_race_info, how='left')

#     cr_race_info=labx[labx['Race']==current_race].copy()
    if datetime.now() > datetime.strptime(y['EXP_START_DT'],'%Y%m%d%H%M%S'):
        if 'Others' in jc:
            cr_race_info['last_jkc_odd']=cr_race_info['Jockey'].map(jkc_lo).fillna(jkc_lo['Others'])
            cr_race_info['curr_jkc_odd']=cr_race_info['Jockey'].map(jkc_co).fillna(jkc_co['Others'])
            cr_race_info['diff_jkc_odd']=cr_race_info['Jockey'].map(jkc_diff).fillna(jkc_diff['Others'])
        else:
            cr_race_info['last_jkc_odd']=cr_race_info['Jockey'].map(jkc_lo).fillna(0)
            cr_race_info['curr_jkc_odd']=cr_race_info['Jockey'].map(jkc_co).fillna(0)
            cr_race_info['diff_jkc_odd']=cr_race_info['Jockey'].map(jkc_diff).fillna(0)

        cr_race_info['jkc_upddt']=y['ODDS_UPD_DT']
    return cr_race_info

def get5(driver):
    import json
    import numpy as np
    import pandas as pd
    from datetime import datetime
    x = driver.find_element_by_tag_name('html').text
    y=json.loads(x)

    c={yy.split('=')[0]: yy.split('=')[1] for yy in y['OUT'].replace('|',';').split(';') if len(yy.split('='))>1}
    return pd.DataFrame({'combination':list(c.keys()), 'odds':list(c.values())})

def get6(driver):
    import json
    import numpy as np
    import pandas as pd
    
    pdf=pd.DataFrame()
    x=driver.find_element_by_tag_name('html').text
    x1 = json.loads(x[2:-2], strict=False)
    if x1['pendingData'] !='': 
        pdf =pd.read_csv(pd.compat.StringIO(x1['pendingData']), sep='\t', header=None)
        pdf['upddt']=x1['dateTime']
    return pdf    

# def get6(driver):
#     import json
#     import numpy as np
#     import pandas as pd
#     import requests

#     import urllib.request
#     url =driver
#     try:
#         with urllib.request.urlopen(url) as response:

#             html = response.read().decode('utf-8')#use whatever encoding as per the webpage
#     except urllib.request.HTTPError as e:
#         if e.code==404:
#             print(f"{url} is not found")
#         elif e.code==503:
#             print(f'{url} base webservices are not available')
#             ## can add authentication here 
#         else:
#             print('http error',e)

#     pdf=pd.DataFrame()
#     x=html
# #     x=requests.get(driver,timeout=10).text
# #     x=driver.find_element_by_tag_name('html').text
#     x1 = json.loads(x[2:-2], strict=False)
#     if x1['pendingData'] !='': 
#         pdf =pd.read_csv(pd.compat.StringIO(x1['pendingData']), sep='\t', header=None)
#         pdf['upddt']=x1['dateTime']
#     return pdf    
  
def get7(driver):
    return get6(driver)

def get8(driver):
    import json
    import numpy as np
    import pandas as pd
    from datetime import datetime
    x = driver.find_element_by_tag_name('html').text
    y=json.loads(x)

    return pd.DataFrame(y['inv'])

def get9(y):
    from selenium import webdriver
    from datetime import datetime
    from selenium.webdriver.support.select import Select
    from selenium.common.exceptions import NoSuchElementException

    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.by import By

    import numpy as np
    import pandas as pd
    from bs4 import BeautifulSoup
    
    b = WebDriverWait(y, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="oddsContentMain"]/table/tbody/tr[4]/td')))


    table_id = y.find_element_by_xpath('//*[@id="oddsContentMain"]/table/tbody/tr[4]/td')

    Page_Source = table_id.get_attribute("outerHTML")
    soup = BeautifulSoup(Page_Source, 'html.parser')
    lab=[]
    b={}
    labx=[]
    trl = soup.findAll('tr')
    for ii,xx in enumerate(trl):
        for jj, yy in enumerate(xx.findAll('td', recursive=False )):
            if ii == 0:
                lab.append(yy.text.strip())
            else:
                b[lab[jj]]=yy.text
        if (b!={}):
            if (b['場次']!='') & (b['馬號']!='') & (b['獨贏']!= '退出'):
                labx.append(b.copy())
    labx=pd.DataFrame(labx)
    labx['場次']=labx['場次'].astype(int)
    labx['disable']=[int(y.find_element_by_xpath('//*[@id="wipCell'+str(r) +'_'+n+'"]/input').get_attribute("disabled")=='true') for r, n in zip(labx['場次'], labx['馬號'])]
    
    return labx

def pid_srch():
    import sys, os
    import pandas as pd
    import numpy as np
    import re

    f1 = os.popen(f'ps -efx -o pid=')
    f2 = os.popen(f'ps -efx -o cmd=')

    xx=pd.concat([pd.read_csv(pd.compat.StringIO(f1.read()),  header=None, names=['pid'], sep='\n', engine='python'),
               pd.read_csv(pd.compat.StringIO(f2.read()),  header=None, names=['cmd'], sep='\n', engine='python')], axis=1)
    xx.dropna(inplace=True)
    xx['pid']=xx['pid'].astype(int)

#     xx['pos']=np.minimum(np.array(xx['cmd'].apply(lambda s: s.find('\\\'))), np.array(xx['cmd'].apply(lambda s: s.find('|'))))
    xx['pos2']=xx['cmd'].apply(lambda x: re.search("\\\_|\|", x).start() if re.search("\\\_|\|", x) else -1)
    xx['pos']=xx['cmd'].apply(lambda s: re.search('/usr/bin/chromedriver --port=\d\d\d\d\d', s).start()
                              if re.search('/usr/bin/chromedriver --port=\d\d\d\d\d', s) else -1)

    xx['chromedrive']=xx['cmd'].apply(lambda s: s[re.compile(r'port=\d\d\d\d\d').search(s).span()[0]:re.compile(r'port=\d\d\d\d\d').search(s).span()[1]] 
                                      if re.compile(r'port=\d\d\d\d\d').search(s) else "0=0")
#     print(xx[xx['chromedrive']!= '0=0'])
#     print(xx)
#     xx.to_csv('/home/ec2-user/abc.csv')
    kk={}
    l=[]
    aaa=''
    for index, row in xx.iterrows():

        if row['pos'] ==0:
            l=[]
            aaa='http://127.0.0.1:'+row['chromedrive'].split('=')[1]
            l.append(int(row['pid']))
#             print('-1', aaa, l)

        elif row['pos2'] >0:
            l.append(int(row['pid']))

            kk[aaa]=l
        elif row['pos2'] <0:
            aaa=''
            l=[]
#             print('sub', aaa, l)
    
    kk.pop('')
#     print(kk)
    return kk


def worker1():
    
    pth = gethomedir()
    workno=1
#     hdinfo=hookdriver(getdriver(pth, workno))
    for i, x in enumerate(gettask(pth, workno)):
#         hdinfo.get(x)
#         hdinfo.refresh()
#         abc=get0(hdinfo)
        abc=get0(None)
        if not abc[0]==[]:
            with open(pth+gettarget(pth, workno)[i].format(ptime=getptime()), 'wb') as outfile:
                    pickle.dump(abc, outfile)






def worker2():
    pth = gethomedir()
    workno=2
    hdinfo=hookdriver(getdriver(pth, workno))
    for i, x in enumerate(gettask(pth, workno)):
    #     print(x)
        hdinfo.get(x)
        hdinfo.refresh()
        abc=get2(hdinfo)
        if not abc.empty:
            with open(pth+gettarget(pth, workno)[i].format(ptime=getptime(), raceno=getnextrace(pth, 'hkjc')), 'wb') as outfile:
                    pickle.dump(abc, outfile)








def worker3():
    pth = gethomedir()
    workno=3
    hdinfo=hookdriver(getdriver(pth, workno))
    for i, x in enumerate(gettask(pth, workno)):
        noor= getlatest(gethomedir(), 'info')[-1]+1
        raceno=max(getnextrace(pth, 'hkjc'),1)
        races= np.random.permutation(range(raceno, noor))
        for race in races: 
            raceno=race
            hdinfo.get(x.format(raceno=raceno))
            hdinfo.refresh()
            qin=get3(hdinfo, 'QIN')
            qpl=get3(hdinfo, 'QPL')
            outo= qin.merge(qpl, on='combination', suffixes =('_qin','_qpl'))
            outo['raceno']=raceno
            if not outo.empty:
                with open(pth+gettarget(pth, workno)[i].format(ptime=getptime(), raceno=raceno), 'wb') as outfile:
                        pickle.dump(outo, outfile)







def worker4():
    pth = gethomedir()
    workno=4
    hdinfo=hookdriver(getdriver(pth, workno))
    for i, x in enumerate(gettask(pth, workno)):
        raceno=getnextrace(pth, 'hkjc')
        if raceno == 0: raceno = 1 
        hdinfo.get(x.format(raceno=raceno))
        hdinfo.refresh()
        time.sleep(2)
        outo=get4(hdinfo, pth, raceno)
        if not outo.empty:
            with open(pth+gettarget(pth, workno)[i].format(ptime=getptime(), raceno=raceno), 'wb') as outfile:
                    pickle.dump(outo, outfile)









def worker5():
    pth = gethomedir()
    workno=5
    hdinfo=hookdriver(getdriver(pth, workno))

    for i, x in enumerate(gettask(pth, workno)):
        raceno=getnextrace(pth, 'hkjc')
        if raceno == 0: raceno = 1 
        hdinfo.get(x.format(raceno=raceno))
        hdinfo.refresh()
        time.sleep(1)
        outo=get5(hdinfo)
        if not outo.empty:
            with open(pth+gettarget(pth, workno)[i].format(ptime=getptime(), raceno=raceno), 'wb') as outfile:
                    pickle.dump(outo, outfile)





# def worker6():
#     pth = gethomedir()
#     workno=6
#     hdinfo=hookdriver(getdriver(pth, workno))
#     for i, x in enumerate(gettask(pth, workno)):
        
#         noor= getlatest(gethomedir(), 'info')[-1]+1
#         raceno=max(getnextrace(pth, 'hkjc'),1)
#         races= np.random.permutation(range(raceno, noor))
#         for race in races: 
#             raceno=race
#             hdinfo.get(x.format(raceno=raceno))
#             hdinfo.refresh()
#             outo=get6(hdinfo)
#             if not outo.empty:
#                 with open(pth+gettarget(pth, workno)[i].format(ptime=getptime(), raceno=raceno), 'wb') as outfile:
#                     pickle.dump(outo, outfile)


def worker6():
    import requests
    pth = gethomedir()
    workno=6
#     hdinfo=hookdriver(getdriver(pth, workno))
    for i, x in enumerate(gettask(pth, workno)):
        
        noor= getlatest(gethomedir(), 'info')[-1]+1
        raceno=max(getnextrace(pth, 'hkjc'),1)
        races= np.random.permutation(range(raceno, noor))
        for race in races: 
            tmp=requests.get(x.format(raceno=race)).text
            x1 = json.loads(tmp[2:-2], strict=False)
            outo=pd.DataFrame()
            if x1['pendingData'] !='': 
                outo =pd.read_csv(pd.compat.StringIO(x1['pendingData']), sep='\t', header=None)
                outo['upddt']=x1['dateTime']
#                 print(f'race {race} in {races}', outo.empty)
                
            if not outo.empty:
                with open(pth+gettarget(pth, workno)[i].format(ptime=getptime(), raceno=race), 'wb') as outfile:
                    pickle.dump(outo, outfile)

                    
def worker10():
    import requests
    pth = gethomedir()
    workno=10
#     hdinfo=hookdriver(getdriver(pth, workno))
    for i, x in enumerate(gettask(pth, workno)):
        
        noor= getlatest(gethomedir(), 'info')[-1]+1
        raceno=max(getnextrace(pth, 'hkjc'),1)
        races= np.random.permutation(range(raceno, noor))
        for race in races: 
            tmp=requests.get(x.format(raceno=race)).text
            x1 = json.loads(tmp[2:-2], strict=False)
            outo=pd.DataFrame()
            if x1['pendingData'] !='': 
                outo =pd.read_csv(pd.compat.StringIO(x1['pendingData']), sep='\t', header=None)
                outo['upddt']=x1['dateTime']
#                 print(f'race {race} in {races}', outo.empty)
                
            if not outo.empty:
                with open(pth+gettarget(pth, workno)[i].format(ptime=getptime(), raceno=race), 'wb') as outfile:
                    pickle.dump(outo, outfile)


def worker7():
    import requests
    pth = gethomedir()
    workno=7
#     hdinfo=hookdriver(getdriver(pth, workno))
    for i, x in enumerate(gettask(pth, workno)):
        
        noor= getlatest(gethomedir(), 'info')[-1]+1
        raceno=max(getnextrace(pth, 'hkjc'),1)
        races= np.random.permutation(range(raceno, noor))
        for race in races: 
            tmp=requests.get(x.format(raceno=race)).text
            x1 = json.loads(tmp[2:-2], strict=False)
            outo=pd.DataFrame()
            if x1['pendingData'] !='': 
                outo =pd.read_csv(pd.compat.StringIO(x1['pendingData']), sep='\t', header=None)
                outo['upddt']=x1['dateTime']
#                 print(f'race {race} in {races}', outo.empty)
                
            if not outo.empty:
                with open(pth+gettarget(pth, workno)[i].format(ptime=getptime(), raceno=race), 'wb') as outfile:
                    pickle.dump(outo, outfile)




# def worker7():
#     pth = gethomedir()
#     workno=7
#     hdinfo=hookdriver(getdriver(pth, workno))
#     for i, x in enumerate(gettask(pth, workno)):
        
#         noor= getlatest(gethomedir(), 'info')[-1]+1
#         raceno=max(getnextrace(pth, 'hkjc'),1)
#         races= np.random.permutation(range(raceno, noor))
#         for race in races: 
#             raceno=race
#             hdinfo.get(x.format(raceno=raceno))
#             hdinfo.refresh()
#             outo=get7(hdinfo)
#             if not outo.empty:
#                 with open(pth+gettarget(pth, workno)[i].format(ptime=getptime(), raceno=raceno), 'wb') as outfile:
#                     pickle.dump(outo, outfile)

# def worker8():
#     pth = gethomedir()
#     workno=8
#     hdinfo=hookdriver(getdriver(pth, workno))
# 
#     for i, x in enumerate(gettask(pth, workno)):
#         raceno=getnextrace(pth, 'hkjc')
#         if raceno == 0: raceno = 1 
#         hdinfo.get(x.format(raceno=raceno))
#         hdinfo.refresh()
#         outo=get8(hdinfo)
#         if not outo.empty:
#             with open(pth+gettarget(pth, workno)[i].format(ptime=getptime(), raceno=raceno), 'wb') as outfile:
#                     pickle.dump(outo, outfile)


def worker8():
    pth = gethomedir()
    workno=8
    hdinfo=hookdriver(getdriver(pth, workno))

    for i, x in enumerate(gettask(pth, workno)):
        noor= getlatest(gethomedir(), 'info')[-1]+1
        raceno=max(getnextrace(pth, 'hkjc'),1)
        races= np.random.permutation(range(raceno, noor))
        for race in races: 
            hdinfo.get(x.format(raceno=race))
            hdinfo.refresh()
            outo=get8(hdinfo)
            if not outo.empty:
                with open(pth+gettarget(pth, workno)[i].format(ptime=getptime(), raceno=race), 'wb') as outfile:
                        pickle.dump(outo, outfile)


def worker9():
    pth = gethomedir()
    workno=9
    hdinfo=hookdriver(getdriver(pth, workno))
    for i, x in enumerate(gettask(pth, workno)):
        hdinfo.get(x)
        hdinfo.refresh()
        outo=get9(hdinfo)
        if not outo.empty:
            with open(pth+gettarget(pth, workno)[i].format(ptime=getptime(), raceno=getnextrace(pth, 'hkjc')), 'wb') as outfile:
                    pickle.dump(outo, outfile)
                    
def get12(driver):
    import json
    import numpy as np
    import pandas as pd
    from datetime import datetime
    x = driver.find_element_by_tag_name('html').text
    y=json.loads(x)
    y1=[ [{yyy.split(';')[0]:yyy.split(';')[1:]} for ii, yyy in enumerate(yy.split('#'))] for i, yy in enumerate(y['OUT'].replace('|',';').split('@@@'))]
#     print(y1)
    win=pd.DataFrame({race: {int(yy.split('=')[0]):yy.split('=')[1] for yy in y1[race][0]['WIN']} for race in range(1,len(y1))}).unstack().reset_index().rename(columns={'level_0':'raceno', 'level_1':'No.', 0:'WIN'})
#     print(len(y1))
    pla=pd.DataFrame({race: {int(yy.split('=')[0]):yy.split('=')[1] for yy in y1[race][1]['PLA']} for race in range(1,len(y1))}).unstack().reset_index().rename(columns={'level_0':'raceno', 'level_1':'No.', 0:'PLA'})
    winpla=win.merge(pla, on=['raceno','No.'])
    winpla['updatedt']=int(list(y1[0][0].keys())[0])
    return winpla

def worker12():
    pth = gethomedir()
    workno=12
    hdinfo=hookdriver(getdriver(pth, workno))
    for i, x in enumerate(gettask(pth, workno)):
#         print(x.format(noofrace=getlatest(pth, 'info')[-1]))
        hdinfo.get(x.format(noofrace=getlatest(pth, 'info')[-1]))
        hdinfo.refresh()
        abc=get12(hdinfo)
        if not abc.empty:
            with open(pth+gettarget(pth, workno)[i].format(ptime=getptime(), raceno=getnextrace(pth, 'hkjc')), 'wb') as outfile:
                    pickle.dump(abc, outfile)
                    

# def get13(driver):
#     import json
#     import numpy as np
#     import pandas as pd
#     from datetime import datetime
#     from selenium import webdriver
#     from datetime import datetime
#     from selenium.webdriver.support.select import Select
#     from selenium.common.exceptions import NoSuchElementException
#     from selenium.webdriver.support import expected_conditions as EC
#     from selenium.webdriver.support.ui import WebDriverWait
#     from selenium.webdriver.common.by import By

#     import numpy as np
#     import pandas as pd
#     from bs4 import BeautifulSoup
    
#     b = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="racecard"]/div[8]/table')))

#     table_id = driver.find_element_by_xpath('//*[@id="racecard"]/div[8]/table')
#     rosx = table_id.find_elements_by_tag_name("tr")[1].find_elements_by_tag_name('td')
#     ly=[]
#     for i in range(1, len(rosx)+1, 25):
#         colx=[col.text for col in rosx[i:i+25]]
#         if i == 1:
#             rcard = pd.DataFrame()
#             columns=colx.copy()
#         else:
#             yy= {k:v for k, v in zip(columns, colx) if k !=''}
#             ly.append(yy)
#     return pd.DataFrame(ly).dropna(axis=0)

def get13(driver):
    import json
    import numpy as np
    import pandas as pd
    from datetime import datetime
    from selenium import webdriver
    from datetime import datetime
    from selenium.webdriver.support.select import Select
    from selenium.common.exceptions import NoSuchElementException
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.by import By

    import numpy as np
    import pandas as pd
    from bs4 import BeautifulSoup
    
    b = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="racecardlist"]')))
# //*[@id="racecardlist"]/tbody/tr/td/table/thead/tr
# //*[@id="racecardlist"]/tbody/tr/td/table/tbody
    table_id = driver.find_element_by_xpath('//*[@id="racecardlist"]/tbody/tr/td/table')
    c = table_id.find_elements_by_tag_name("thead")[0]
    colx=[col.text for col in c.find_elements_by_tag_name('td')]
    d = table_id.find_elements_by_tag_name("tbody")[0].find_elements_by_tag_name("tr")
    
    e = pd.DataFrame([[col.text for col in f.find_elements_by_tag_name('td')] for f in d ], columns=colx)
#     print(e)
# add race info 
    g=driver.find_element_by_xpath("/html/body/div/div[4]/div[2]").text 
    h={'Raceinfo':pd.read_csv(pd.compat.StringIO(g), sep='\n', header=None)[0].to_list()} 
    return e, h

def worker13():
    pth = gethomedir()
    workno=13
    hdinfo=hookdriver(getdriver(pth, workno))
    for i, x in enumerate(gettask(pth, workno)):
        noor= getlatest(gethomedir(), 'info')[-1]+1
        raceno=max(getnextrace(pth, 'hkjc'),1)
        races= np.random.permutation(range(raceno, noor))
        for race in races: 
            raceno=race
            hdinfo.get(x.format(raceno=raceno))
            hdinfo.refresh()
#             outo= get13(hdinfo)
# add race info
            outo, out1= get13(hdinfo)
            if not outo.empty:
                outo['raceno']=raceno
                with open(pth+gettarget(pth, workno)[i].format(ptime=getptime(), raceno=raceno, itype='card'), 'wb') as outfile:
                        pickle.dump(outo, outfile)
                with open(pth+gettarget(pth, workno)[i].format(ptime=getptime(), raceno=raceno, itype='info'), 'wb') as outfile:
                        pickle.dump(out1, outfile)
                    

                    
def get14(driver):
    import json
    import numpy as np
    import pandas as pd
    from datetime import datetime
    x = driver.find_element_by_tag_name('html').text
    y=json.loads(x)
    polling_uptime = y['OUT'].split('@@@')[0].replace('#CWA', "")
    y1=[ [i]+[yyyy.split("=")[1] for yyyy in yyy.split(';')[1:]] 
        for i, yy in enumerate(y['OUT'].replace('|',';').split('@@@')) 
       for ii, yyy in enumerate(yy.split('#'))
       if i >0]
    cwa=pd.DataFrame(y1).rename(columns={0:'raceno'}).set_index('raceno').unstack().reset_index().rename(columns={'level_0':'combination', 0:'odds'})
    return cwa, polling_uptime

def get14_2(driver):
    import json
    import numpy as np
    import pandas as pd
    from datetime import datetime
    import re
    x = driver.find_element_by_tag_name('html').text
    y=json.loads(x)
    try:
        yyy=pd.concat([pd.DataFrame({"raceno":y['CWA']['raceNo'],
                                     "combination":re.sub("\D", "", yy['SelStr']), 
                                     "RunnerNos":yy['RunnerNos']})
                       for yy in y['CWA']['CwinSels']]).reset_index(drop=True).astype(int)
    except:
        #for the race without CWA
        yyy=pd.DataFrame()
    return yyy

def worker14():
    import json
    pth = gethomedir()
    workno=14
    hdinfo=hookdriver(getdriver(pth, workno))
    for i, x in enumerate(gettask(pth, workno)):
        noor= getlatest(gethomedir(), 'info')[-1]+1
        raceno=1
        races= np.random.permutation(range(raceno, noor))
        if i == 0:
            hdinfo.get(x.format(noofrace=getlatest(pth, 'info')[-1]))
            hdinfo.refresh()
            abc,polling_uptime=get14(hdinfo)
        elif i == 1 and not abc.empty:
            allouto=[]
            for j, race in enumerate(races): 
                raceno=race
                hdinfo.get(x.format(raceno=raceno))
                hdinfo.refresh()
                outo= get14_2(hdinfo)
                if not outo.empty:
                    allouto.append(outo)
                    xx = hdinfo.find_element_by_tag_name('html').text
                    yy=json.loads(xx)
#                     print(yy, pth+gettarget(pth, workno)[i].format(ptime=getptime(), raceno=raceno))
                    with open(pth+gettarget(pth, workno)[i].format(ptime=getptime(), raceno=raceno), 'wb') as outfile:
                            pickle.dump(yy, outfile)
            abc=abc.merge(pd.concat(allouto), how='outer', on=['raceno','combination'])
            abc=abc[['raceno','RunnerNos','combination','odds']].sort_values(by=['raceno','RunnerNos']).reset_index(drop=True)
#             print("******",allouto)
#             print(abc, pth+gettarget(pth, workno)[0].format(ptime=getptime(), raceno=getnextrace(pth, 'hkjc')))
            with open(pth+polling_uptime+"_"+gettarget(pth, workno)[0].format(ptime=getptime(), raceno=getnextrace(pth, 'hkjc')), 'wb') as outfile:
                    pickle.dump(abc, outfile)
            



#### Updated @ 20211011

# def worker14():
#     pth = gethomedir()
#     workno=14
#     hdinfo=hookdriver(getdriver(pth, workno))
#     for i, x in enumerate(gettask(pth, workno)):
# #         print(x.format(noofrace=getlatest(pth, 'info')[-1]))
#         hdinfo.get(x.format(noofrace=getlatest(pth, 'info')[-1]))
#         hdinfo.refresh()
#         abc=get14(hdinfo)
#         if not abc.empty:
#             with open(pth+gettarget(pth, workno)[i].format(ptime=getptime(), raceno=getnextrace(pth, 'hkjc')), 'wb') as outfile:
#                     pickle.dump(abc, outfile)
 


def wipeall():
    import os
    yy = pid_srch()
    for ii in list(yy.keys()):
        for i, x in enumerate(yy[ii]):
            if i <=2:
                os.popen(f'kill {x}')

            
            
#def getracejkc(pth):
#    from glob import glob
#    import numpy as np
#    zza =pd.DataFrame()
#    for y in sorted(list(set([x.split('_')[-3] for x in glob(pth+'/*_'+'R*hkjc_jkc'+'.pickle')]))):
#        zz= getlatest(pth, f'{y}_hkjc_jkc')
#        if np.array(zz['diff_jkc_odd'].tolist()).sum()==0:
#            zz= getsecond(pth, f'{y}_hkjc_jkc')
#        zz=zz[zz['Race']==int(y[1:])]
#        zz.reset_index(inplace=True)
#        zza=pd.concat([zza, zz], axis=0)
#    return zza[['Race','No.','diff_jkc_odd']].reset_index(drop=True)

def getgtzero(pth, ele):
    from glob import glob
    import pandas as pd
    for xy in sorted(glob(pth+'/*_'+ele+'*_jkc.pickle'), reverse=True):
        x=pd.read_pickle(xy)
        if x['diff_jkc_odd'].get_values().sum() != 0.0:
            break
    return x[x['Race']==int(ele[1:-1])]
            
def getracejkc(pth):
    from glob import glob
    import numpy as np
    zza =pd.DataFrame()
    for y in sorted(list(set([x.split('_')[-3] for x in glob(pth+'/*_'+'R*hkjc_jkc'+'.pickle')]))):
        zz=getgtzero(pth, y+'_')
        zz.reset_index(inplace=True)
        zza=pd.concat([zza, zz], axis=0)
    return zza[['Race','No.','diff_jkc_odd']].reset_index(drop=True)



# def getclosest(pth, ele, ts):
#     from glob import glob
#     import bisect
#     s=sorted(list(set([x.split('_')[1] for x in glob(pth+'/*_'+ele+'.pickle')])))
#     i = bisect.bisect_left(s, ts)
#     mini = min(s[max(0, i-1): i+2], key=lambda t: abs(datetime.strptime(ts,'%Y%m%d%H%M%S') - datetime.strptime(t,'%Y%m%d%H%M%S')))
#     return getlatest(pth, mini+'*hkjc_jkc')


def getclosest(pth, ele, ts):
    from glob import glob
    import bisect
    s=sorted(list(set([x.split('_')[1] for x in glob(pth+'/*_'+ele+'.pickle')])))
    i = bisect.bisect_left(s, ts)
    mini = min(s[max(0, i-1): i+2], key=lambda t: abs(datetime.strptime(ts,'%Y%m%d%H%M%S') - datetime.strptime(t,'%Y%m%d%H%M%S')))
    print(mini)
    return getlatest(pth, mini+'*'+ele)


def get11(driver):
    from selenium import webdriver
    from datetime import datetime
    from selenium.webdriver.support.select import Select
    from selenium.common.exceptions import NoSuchElementException

    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.by import By

    import numpy as np
    import pandas as pd
    from bs4 import BeautifulSoup
    
    b = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="contentContainer"]/div[1]')))

#     from bs4 import BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    racedate = soup.find('div',{'class':'rowDiv5'}).findAll('td')[0].text.split(':')[-1]

    res=[]
    res_2=[]
    key=['Pool', 'Winning Combination', 'Dividend (HK$)']
    key_2=['Pla.','H.No', 'Horse','Jockey','Trainer','Actual Wt.','Dr']
    table = soup.findAll('table')
    for x in table:
        y = x.findAll('tr')
        for z in y:
            zz = z.findAll('td')
            for z2 in zz:
                z3 = z2.findAll('table')
                race = z2.findAll('div',{"class":"boldFont13 color_white trBgBlue clearDivFloat lineH20"})
                race_oversea= z2.findAll('div',{"class":"boldFont13 color_white trBgGreen clearDivFloat lineH20"})
                race=race+race_oversea
                if race !=[]: 
#                     race=race[0].text.replace('\xa0','').split(' ')[1]
                    race=' '.join(race[0].text.replace('\xa0','').split(' ')[1:]).strip()
                    kex={}
                    kex['raceno']=race
                    kex['racedate']=racedate
                    kex_2={}
                    kex_2['raceno']=race
                    kex_2['racedate']=racedate
                for z4 in z3:
                    z5 = z4.findAll('tr')
                    for z6 in z5:
                        z7_2 = z6.findAll('td', {'style':"font-weight: normal;font-size:13px"}) #FP
                        z7 = z6.findAll('td',{'style':"font-weight: normal;font-size:13px;padding-top:0px;padding-bottom:0px;"})
                        if z7!=[]:
                            z9= [z8.text for z8 in z7]
                            if len(z9) == 3: 
                                type = z9[0]
                            elif len(z9) == 2:
                                z9=[type, z9[0], z9[1]]
                            kex[key[0]]=z9[0].replace('\xa0','')
                            kex[key[1]]=z9[1].replace('\xa0','')
                            kex[key[2]]=z9[2].replace('\xa0','')
                            res.append(kex.copy())
                        if z7_2!=[]:
                            kex_2.update({i:j for i, j in zip(key_2, [z8.text for z8 in z7_2])})
                            res_2.append(kex_2.copy())

    dividend=pd.DataFrame(res)
    
    if not dividend.empty:
        dividend=dividend[dividend['raceno'].str.isnumeric()]
        dividend=dividend[~dividend['Winning Combination'].isin(['Winning Combination',''])].reset_index(drop=True)
    fp=pd.DataFrame(res_2).reset_index(drop=True)
    
    return fp,dividend

def worker11():
    import pandas as pd
    pth = gethomedir()
    workno=11
    hdinfo=hookdriver(getdriver(pth, workno))
    hdinfo.get(list(set(gettask(pth, workno)))[0])
    hdinfo.refresh()
    y=get11(hdinfo)
    for i ,j in zip(y, gettarget(pth, workno)):
        if not i.empty:
            i.to_pickle(pth+j.format(ptime=getptime()))



# def workertab():
#     from datetime import timedelta, time
#     import os
    
#     jtmap={'莫雷拉': '雷', '潘頓': '潘', '田泰安': '田 ', '利敬國': '利', '何澤堯': '堯', '史卓豐': '史', '陳嘉熙': '熙', '蔡明紹': '紹', '杜美爾': '爾', '沈拿': '拿', '楊明綸': '楊', '薛恩': '薛', '巫顯東': '顯', '梁家俊': '家', '貝力斯': '斯', '黃皓楠': '楠', '潘明輝': '明', '郭能': '郭', '李寶利': '李', '蘇狄雄': '狄', '希威森': '希', '黎海榮': '海', '黃俊': '俊', '告東尼': '東', '沈集成': '沈', '呂健威': '呂', '姚本輝': '姚', '丁冠豪': '丁', '韋達': '韋', '苗禮德': '苗', '方嘉柏': '方', '約翰摩亞': '摩', '徐雨石': '徐', '蘇偉賢': '賢', '羅富全': '羅', '文家良': '文', '高伯新': '高', '蘇保羅': '蘇', '容天鵬': '容', '葉楚航': '葉', '何良': '何', '鄭俊偉': '鄭', '蔡約翰': '蔡', '霍利時': '時', '賀賢': '賀'}
#     pth=gethomedir()
#     nr= getnextrace(pth,'hkjc')
# #     nr=11
#     print(pth, nr)
# #     11pm snapshot
#     if (datetime.now() > previous11()) :
#         if os.path.exists(f'{pth}skk_eat_11.pickle'):
#             allrx=pd.read_pickle(f'{pth}skk_eat_11.pickle')
#         else:
#             allr=pd.DataFrame()
#             for xx in range(1, getlatest(pth, 'info')[-1]+1):
#                 xb2=getlatest(pth, 'R'+str(xx)+'_skk'+'_eat')
#             #     print(xb2)
#                 c1 = list(xb2[(xb2[4]==3.8) & (xb2[5]=='120/30')][1])
#                 c2 = list(xb2[(xb2[4]==3.8) & (xb2[5]=='120/0')][1])
#                 c3 = list(xb2[(xb2[4]==3.8) & (xb2[5]=='0/30')][1])
#                 allc= list(set(c1) & set(c2) & set(c3))
#             #     print(allc)
#                 allr=allr.append(xb2[(xb2[1].isin(allc)) & (xb2[4]==3.8)])
#             # xb2[(xb2[1].isin([9])) & (xb2[4]==3.8)]
#             allr=allr[[0,1]].reset_index(drop=True)
#             allr[1]=allr[1].astype(str)
#             allrx= allr.groupby([0])[1].apply(set).apply(list).reset_index()
#             allrx.to_pickle(f'{pth}skk_eat_11.pickle')        
#     else:
#         allr=pd.DataFrame()
#         for xx in range(1, getlatest(pth, 'info')[-1]+1):
#             xb2=getlatest(pth, 'R'+str(xx)+'_skk'+'_eat')
#         #     print(xb2)
#             c1 = list(xb2[(xb2[4]==3.8) & (xb2[5]=='120/30')][1])
#             c2 = list(xb2[(xb2[4]==3.8) & (xb2[5]=='120/0')][1])
#             c3 = list(xb2[(xb2[4]==3.8) & (xb2[5]=='0/30')][1])
#             allc= list(set(c1) & set(c2) & set(c3))
#         #     print(allc)
#             allr=allr.append(xb2[(xb2[1].isin(allc)) & (xb2[4]==3.8)])
#         # xb2[(xb2[1].isin([9])) & (xb2[4]==3.8)]
#         allr=allr[[0,1]].reset_index(drop=True)
#         allr[1]=allr[1].astype(str)
#         allrx= allr.groupby([0])[1].apply(set).apply(list).reset_index()

        
# #         ts = datetime.combine(getlatest(gethomedir(), 'info')[0][0]-timedelta(days=1), time(23,0,0)).strftime('%Y%m%d%H%M%S')
# #         getclosest(gethomedir(), 'R1_*'+'ctb_eat', ts)        
    
#     labx=pd.concat([getlatest(pth, 'hkjc_jkc'),getlatest(pth, 'hkjc_wpchi')], axis=1)
#     labx=pd.merge(labx, getracejkc(pth), how='left', on=['Race','No.'], suffixes=('_old', ''))
    
#     for r, n in zip(allrx[0], allrx[1]):
#         labx.loc[(labx['Race']==r) & (labx['No.'].isin(n)), 'dead']=chr(128128)
#         labx['dead']=labx['dead'].fillna('')
# #         labx.loc[(labx['Race']==r) & (labx['No.'].isin(n)), 'dead']='死'
# #         labx['dead']=labx['dead'].fillna('生')
#     if 'diff_jkc_odd' in labx.columns:
#         labx['diff_jkc_odd']=labx['diff_jkc_odd'].apply(lambda x: np.round(x, 2))
#     else:
#         labx['diff_jkc_odd']=0
    
#     #result
#     labx['Res']=''
#     winmap={'1':chr(127942),'2':'Q','3':'T','4':'4th'}
# #     winmap={'1':'W','2':'Q','3':'T','4':'4th'}
# #     chr(128512)
#     try:
#         res=getlatest(pth, 'result')
#         for r, n, p in zip(res['raceno'], res['H.No'], res['Pla.']):
#             labx.loc[(labx['Race']==int(r)) & (labx['No.']==n), 'Res']='***'+winmap[p]
#     except:
#         pass

    
# #     ctb eat info
#     labx['eat']=''
# #     print(labx.dtypes)
#     try:
#         lctbeat=getlatest(pth, 'lctb')[['Race','No.','WP eat']]
#         lctbeat['eat']=lctbeat['WP eat'].apply(lambda x: x.split(' ')[1]).apply(lambda x:x.strip())
#         lctbeat=lctbeat[lctbeat['eat']=='76'] #new added

#         histccc=getlatest(pth, 'hist_ccc')
# #         for r, n, p in zip(lctbeat['Race'], lctbeat['No.'], lctbeat['eat']):
#         for r, n in zip(lctbeat['Race'].append(histccc['Race']), lctbeat['No.'].append(histccc['No.'])):
# #             if p.strip() == '76':
#             labx.loc[(labx['Race']==r) & (labx['No.']==str(n)), 'eat']=chr(128169)
# #             labx.loc[(labx['Race']==r) & (labx['No.']==str(n)), 'eat']=p.strip()
#     except:
#         pass
    

    
#     labxx=labx
#     keyxs = ['練馬師', '騎師']
#     for keyx in keyxs:
#         tag=''.join(set(keyxs) ^ set([keyx]))
# #         if keyx= '練馬師':
#         labxx['cc'] = labxx.groupby([keyx, 'Race'])[keyx].cumcount()
# #         yyxx=labxx[labxx['cc']>0][['Race',keyx]].drop_duplicates()
# #         yyxx['cc_new']=99
# #         labxx=pd.merge(labxx, yyxx, how='left', on=['Race',keyx])
#         yyxx=labxx.groupby(['練馬師', '騎師'])['Horse'].count()
#         yyxx=pd.DataFrame(yyxx[yyxx>1])
#         yyxx.rename(columns={'Horse': 'cc'+keyx}, inplace=True)
#         labxx=pd.merge(labxx, yyxx, how='left', on=['練馬師', '騎師'])


# #         if keyx =='騎師': labxx['cc_new']=0
        
#         labxx['nohorse']=np.where(labxx['cc'+keyx]>0 , '('+labxx['馬號']+')'+labxx['馬名']+'('+labxx[tag].map(jtmap).apply(lambda x: x[0])+chr(128108)+')'
#                                   ,'('+labxx['馬號']+')'+labxx['馬名']+'('+labxx[tag].map(jtmap).apply(lambda x: x[0])+')')
        
        
#         p11 = getclosest(pth, 'wp', previous9().strftime('%Y%m%d%H%M%S'))['Win'].apply(lambda x: float(x) if isfloat(x) else 0)
#         if nightrace():
#             t11 = getclosest(pth, 'wp', today5().strftime('%Y%m%d%H%M%S'))['Win'].apply(lambda x: float(x) if isfloat(x) else 0)
#         else:
#             t11 = getclosest(pth, 'wp', today12().strftime('%Y%m%d%H%M%S'))['Win'].apply(lambda x: float(x) if isfloat(x) else 0)

#         labxx['win_sym']=np.where((p11 - t11)/p11 > 0.2, labxx['Win']+chr(9196), labxx['Win'])

#         labxx['R']=labxx[['dead','nohorse','win_sym','diff_jkc_odd','eat','Res']].apply(lambda y: y.astype(str), axis=1).apply(lambda x: '/ '.join(x), axis=1)
        
# #         labxx['R']=labxx[['dead','nohorse','Win','diff_jkc_odd','eat','Res']].apply(lambda y: y.astype(str), axis=1).apply(lambda x: '/ '.join(x), axis=1)

#         xx=labxx
# #         print(xx.columns)
# #     for keyx in ['練馬師', '騎師']:        
# #         xx['cc'] = xx.groupby([keyx, 'Race'])['R'].cumcount()
#         dd = pd.DataFrame()
#         for ijk in xx['cc'].unique():
#             xy= xx[xx['cc']==ijk].pivot(index=keyx, columns='Race', values=['R']).reset_index().fillna('')
#             xy.set_axis(xy.columns.map('{0[0]}{0[1]}'.format) , axis=1, inplace=True)
#             dd=dd.append(xy, sort=False)

#         dd=dd.reset_index(drop=True).fillna('')
#         cc=dd.copy()
#         cc['sv']=cc[f'R{nr}'].apply(lambda x: float(x.split('/')[-3]) if x !='' else -9999999999.0)
#         dd=dd.reindex(cc.sort_values(by='sv', ascending=False).index)
#         pth.split('/')[-1]
#         if not dd.empty:
#             if keyx=='練馬師': 
#                 key='trainer'
# #                 return dd
#             elif keyx=='騎師':
#                 key='jockey'
# #                return dd
#             dd.to_pickle(pth+pth.split('/')[-2]+'_'+key+'.pickle')
#     return 



# def workertab():
#     from datetime import timedelta, time
#     import os
#     import re
    
#     jtmap={'莫雷拉': '雷', '潘頓': '潘', '田泰安': '田 ', '利敬國': '利', '何澤堯': '堯', '史卓豐': '史', '陳嘉熙': '熙', '蔡明紹': '紹', '杜美爾': '爾', '沈拿': '拿', '楊明綸': '楊', '薛恩': '薛', '巫顯東': '顯', '梁家俊': '家', '貝力斯': '斯', '黃皓楠': '楠', '潘明輝': '明', '郭能': '郭', '李寶利': '李', '蘇狄雄': '狄', '希威森': '希', '黎海榮': '海', '黃俊': '俊', '告東尼': '東', '沈集成': '沈', '呂健威': '呂', '姚本輝': '姚', '丁冠豪': '丁', '韋達': '韋', '苗禮德': '苗', '方嘉柏': '方', '約翰摩亞': '摩', '徐雨石': '徐', '蘇偉賢': '賢', '羅富全': '羅', '文家良': '文', '高伯新': '高', '蘇保羅': '蘇', '容天鵬': '容', '葉楚航': '葉', '何良': '何', '鄭俊偉': '鄭', '蔡約翰': '蔡', '霍利時': '時', '賀賢': '賀'}
#     pth=gethomedir()
#     nr= getnextrace(pth,'hkjc')
# #     nr=11
#     print(pth, nr)
# #     11pm snapshot
#     if (datetime.now() > previous11()) :
#         if os.path.exists(f'{pth}skk_eat_11.pickle'):
#             allrx=pd.read_pickle(f'{pth}skk_eat_11.pickle')
#         else:
#             allr=pd.DataFrame()
#             for xx in range(1, getlatest(pth, 'info')[-1]+1):
#                 xb2=getlatest(pth, 'R'+str(xx)+'_skk'+'_eat')
#             #     print(xb2)
#                 c1 = list(xb2[(xb2[4]==3.8) & (xb2[5]=='120/30')][1])
#                 c2 = list(xb2[(xb2[4]==3.8) & (xb2[5]=='120/0')][1])
#                 c3 = list(xb2[(xb2[4]==3.8) & (xb2[5]=='0/30')][1])
#                 allc= list(set(c1) & set(c2) & set(c3))
#             #     print(allc)
#                 allr=allr.append(xb2[(xb2[1].isin(allc)) & (xb2[4]==3.8)])
#             # xb2[(xb2[1].isin([9])) & (xb2[4]==3.8)]
#             allr=allr[[0,1]].reset_index(drop=True)
#             allr[1]=allr[1].astype(str)
#             allrx= allr.groupby([0])[1].apply(set).apply(list).reset_index()
#             allrx.to_pickle(f'{pth}skk_eat_11.pickle')        
#     else:
#         allr=pd.DataFrame()
#         for xx in range(1, getlatest(pth, 'info')[-1]+1):
#             xb2=getlatest(pth, 'R'+str(xx)+'_skk'+'_eat')
#         #     print(xb2)
#             c1 = list(xb2[(xb2[4]==3.8) & (xb2[5]=='120/30')][1])
#             c2 = list(xb2[(xb2[4]==3.8) & (xb2[5]=='120/0')][1])
#             c3 = list(xb2[(xb2[4]==3.8) & (xb2[5]=='0/30')][1])
#             allc= list(set(c1) & set(c2) & set(c3))
#         #     print(allc)
#             allr=allr.append(xb2[(xb2[1].isin(allc)) & (xb2[4]==3.8)])
#         # xb2[(xb2[1].isin([9])) & (xb2[4]==3.8)]
#         allr=allr[[0,1]].reset_index(drop=True)
#         allr[1]=allr[1].astype(str)
#         allrx= allr.groupby([0])[1].apply(set).apply(list).reset_index()

        
# #         ts = datetime.combine(getlatest(gethomedir(), 'info')[0][0]-timedelta(days=1), time(23,0,0)).strftime('%Y%m%d%H%M%S')
# #         getclosest(gethomedir(), 'R1_*'+'ctb_eat', ts)        
    
#     labx=pd.concat([getlatest(pth, 'hkjc_jkc'),getlatest(pth, 'hkjc_wpchi')], axis=1)
#     labx=pd.merge(labx, getracejkc(pth), how='left', on=['Race','No.'], suffixes=('_old', ''))
    
#     for r, n in zip(allrx[0], allrx[1]):
#         labx.loc[(labx['Race']==r) & (labx['No.'].isin(n)), 'dead']=chr(128128)
#         labx['dead']=labx['dead'].fillna('')
# #         labx.loc[(labx['Race']==r) & (labx['No.'].isin(n)), 'dead']='死'
# #         labx['dead']=labx['dead'].fillna('生')
#     if 'diff_jkc_odd' in labx.columns:
#         labx['diff_jkc_odd']=labx['diff_jkc_odd'].apply(lambda x: np.round(x, 2))
#     else:
#         labx['diff_jkc_odd']=0
    
#     #result
#     labx['Res']=''
#     winmap={'1':chr(127942),'2':'Q','3':'T','4':'4th'}
# #     winmap={'1':'W','2':'Q','3':'T','4':'4th'}
# #     chr(128512)
#     try:
#         res=getlatest(pth, 'result')
#         for r, n, p in zip(res['raceno'], res['H.No'], res['Pla.'].apply(lambda x: re.sub("\D", "", x))  ):
#             labx.loc[(labx['Race']==int(r)) & (labx['No.']==n), 'Res']='***'+winmap[p]
#     except:
#         pass

    
# #     ctb eat info
#     labx['eat']=''
# #     print(labx.dtypes)
#     try:
#         lctbeat=getlatest(pth, 'lctb')[['Race','No.','WP eat']]
#         lctbeat['eat']=lctbeat['WP eat'].apply(lambda x: x.split(' ')[1]).apply(lambda x:x.strip())
#         lctbeat=lctbeat[lctbeat['eat']=='76'] #new added

#         histccc=getlatest(pth, 'hist_ccc')
# #         for r, n, p in zip(lctbeat['Race'], lctbeat['No.'], lctbeat['eat']):
#         for r, n in zip(lctbeat['Race'].append(histccc['Race']), lctbeat['No.'].append(histccc['No.'])):
# #             if p.strip() == '76':
#             labx.loc[(labx['Race']==r) & (labx['No.']==str(n)), 'eat']=chr(128169)
# #             labx.loc[(labx['Race']==r) & (labx['No.']==str(n)), 'eat']=p.strip()
#     except:
#         pass
    

# #         win drop
#     p11base = getclosest(pth, 'wp', previous9(pth).strftime('%Y%m%d%H%M%S'))
#     p11base['Win']=p11base['Win'].apply(lambda x: float(x) if isfloat(x) else 0)
#     if nightrace():
#         t11base=getclosest(pth, 'wp', today5(pth).strftime('%Y%m%d%H%M%S'))
#     else:
#         t11base=getclosest(pth, 'wp', today12(pth).strftime('%Y%m%d%H%M%S'))

#     t11base['Win'] = t11base['Win'].apply(lambda x: float(x) if isfloat(x) else 0)
#     t11base2= p11base[['No.','Race','Horse','Win']].merge(t11base[['No.','Race','Horse', 'Win']], 
#                                                         how='outer', on=['No.','Race','Horse'])
#     t11base2['win_sym']=np.where((t11base2['Win_x'] - t11base2['Win_y'])/t11base2['Win_x'] > 0.2, 1, 0)
# #         print(t11base2['win_sym'])
#     labx=labx.merge(t11base2[['No.','Race','Horse','win_sym']], how='left', on=['No.','Race','Horse'])
#     labx['win_sym']=np.where(labx['win_sym'], labx['Win']+chr(9196), labx['Win'])

    
#     labxx=labx
#     keyxs = ['練馬師', '騎師']
#     for keyx in keyxs:
#         tag=''.join(set(keyxs) ^ set([keyx]))
# #         if keyx= '練馬師':
#         labxx['cc'] = labxx.groupby([keyx, 'Race'])[keyx].cumcount()
# #         yyxx=labxx[labxx['cc']>0][['Race',keyx]].drop_duplicates()
# #         yyxx['cc_new']=99
# #         labxx=pd.merge(labxx, yyxx, how='left', on=['Race',keyx])
#         yyxx=labxx.groupby(['練馬師', '騎師'])['Horse'].count()
#         yyxx=pd.DataFrame(yyxx[yyxx>1])
#         yyxx.rename(columns={'Horse': 'cc'+keyx}, inplace=True)
#         labxx=pd.merge(labxx, yyxx, how='left', on=['練馬師', '騎師'])


# #         if keyx =='騎師': labxx['cc_new']=0
        
# #         labxx['nohorse']=np.where(labxx['cc'+keyx]>0 , '('+labxx['馬號']+')'+labxx['馬名']+'('+labxx[tag].map(jtmap).apply(lambda x: x[0])+chr(128108)+')'
# #                                   ,'('+labxx['馬號']+')'+labxx['馬名']+'('+labxx[tag].map(jtmap).apply(lambda x: x[0])+')')
#         labxx['nohorse']=np.where(labxx['cc'+keyx]>0 , '('+labxx['馬號']+')'+labxx['馬名']+'('+labxx[tag].map(jtmap).fillna(labxx[tag]).apply(lambda x: x[0])+chr(128108)+')'
#                                   ,'('+labxx['馬號']+')'+labxx['馬名']+'('+labxx[tag].map(jtmap).fillna(labxx[tag]).apply(lambda x: x[0])+')')

# #         print(labxx[])

        
# #         p11 = getclosest(pth, 'wp', previous9().strftime('%Y%m%d%H%M%S'))['Win'].apply(lambda x: float(x) if isfloat(x) else 0)
# #         if nightrace():
# #             t11 = getclosest(pth, 'wp', today5().strftime('%Y%m%d%H%M%S'))['Win'].apply(lambda x: float(x) if isfloat(x) else 0)
# #         else:
# #             t11 = getclosest(pth, 'wp', today12().strftime('%Y%m%d%H%M%S'))['Win'].apply(lambda x: float(x) if isfloat(x) else 0)

# #         labxx['win_sym']=np.where((p11 - t11)/p11 > 0.2, labxx['Win']+chr(9196), labxx['Win'])

#         labxx['R']=labxx[['dead','nohorse','win_sym','diff_jkc_odd','eat','Res']].apply(lambda y: y.astype(str), axis=1).apply(lambda x: '/ '.join(x), axis=1)
        
# #         labxx['R']=labxx[['dead','nohorse','Win','diff_jkc_odd','eat','Res']].apply(lambda y: y.astype(str), axis=1).apply(lambda x: '/ '.join(x), axis=1)

#         xx=labxx
# #         print(xx.columns)
# #     for keyx in ['練馬師', '騎師']:        
# #         xx['cc'] = xx.groupby([keyx, 'Race'])['R'].cumcount()
#         dd = pd.DataFrame()
#         for ijk in xx['cc'].unique():
#             xy= xx[xx['cc']==ijk].pivot(index=keyx, columns='Race', values=['R']).reset_index().fillna('')
#             xy.set_axis(xy.columns.map('{0[0]}{0[1]}'.format) , axis=1, inplace=True)
#             dd=dd.append(xy, sort=False)

#         dd=dd.reset_index(drop=True).fillna('')
#         cc=dd.copy()
#         cc['sv']=cc[f'R{nr}'].apply(lambda x: float(x.split('/')[-3]) if x !='' else -9999999999.0)
#         dd=dd.reindex(cc.sort_values(by='sv', ascending=False).index)
#         pth.split('/')[-1]
#         if not dd.empty:
#             if keyx=='練馬師': 
#                 key='trainer'
# #                 return dd
#             elif keyx=='騎師':
#                 key='jockey'
# #                 return dd
#             dd.to_pickle(pth+pth.split('/')[-2]+'_'+key+'.pickle')
#     return 

###### corona virus shutdown of Singapore #####
###### change from 3.8 to 3.9 at 1 dec 2020 #####
def workertab():
    from datetime import timedelta, time
    import os
    import re
    
    jtmap={'莫雷拉': '雷', '潘頓': '潘', '田泰安': '田 ', '利敬國': '利', '何澤堯': '堯', '史卓豐': '史', '陳嘉熙': '熙', '蔡明紹': '紹', '杜美爾': '爾', '沈拿': '拿', '楊明綸': '楊', '薛恩': '薛', '巫顯東': '顯', '梁家俊': '家', '貝力斯': '斯', '黃皓楠': '楠', '潘明輝': '明', '郭能': '郭', '李寶利': '李', '蘇狄雄': '狄', '希威森': '希', '黎海榮': '海', '黃俊': '俊', '告東尼': '東', '沈集成': '沈', '呂健威': '呂', '姚本輝': '姚', '丁冠豪': '丁', '韋達': '韋', '苗禮德': '苗', '方嘉柏': '方', '約翰摩亞': '摩', '徐雨石': '徐', '蘇偉賢': '賢', '羅富全': '羅', '文家良': '文', '高伯新': '高', '蘇保羅': '蘇', '容天鵬': '容', '葉楚航': '葉', '何良': '何', '鄭俊偉': '鄭', '蔡約翰': '蔡', '霍利時': '時', '賀賢': '賀'}
    pth=gethomedir()
    nr= getnextrace(pth,'hkjc')
#     nr=11
    print(pth, nr)
#     11pm snapshot
    if (datetime.now() > previous11()) :
        if os.path.exists(f'{pth}skk_eat_11.pickle'):
            allrx=pd.read_pickle(f'{pth}skk_eat_11.pickle')
        else:
            allr=pd.DataFrame()
            for xx in range(1, getlatest(pth, 'info')[-1]+1):
                xb2=getlatest(pth, 'R'+str(xx)+'_skk'+'_eat')
#                 xb2=getlatest(pth, 'R'+str(xx)+'_ctb'+'_eat')
            #     print(xb2)
                c1 = list(xb2[(xb2[4]==3.9) & (xb2[5]=='120/30')][1])
                c2 = list(xb2[(xb2[4]==3.9) & (xb2[5]=='120/0')][1])
                c3 = list(xb2[(xb2[4]==3.9) & (xb2[5]=='0/30')][1])
#                 c1 = list(xb2[(xb2[4]==3.8) & (xb2[5]=='150/50')][1])
#                 c2 = list(xb2[(xb2[4]==3.8) & (xb2[5]=='150/0')][1])
#                 c3 = list(xb2[(xb2[4]==3.8) & (xb2[5]=='0/50') & (xb2[3]>=500)][1])
                allc= list(set(c1) & set(c2) & set(c3))
            #     print(allc)
                allr=allr.append(xb2[(xb2[1].isin(allc)) & (xb2[4]==3.9)])
            # xb2[(xb2[1].isin([9])) & (xb2[4]==3.8)]
            allr=allr[[0,1]].reset_index(drop=True)
            allr[1]=allr[1].astype(str)
            allrx= allr.groupby([0])[1].apply(set).apply(list).reset_index()
            allrx.to_pickle(f'{pth}skk_eat_11.pickle')        
    else:
        allr=pd.DataFrame()
        for xx in range(1, getlatest(pth, 'info')[-1]+1):
            xb2=getlatest(pth, 'R'+str(xx)+'_skk'+'_eat')
#             xb2=getlatest(pth, 'R'+str(xx)+'_ctb'+'_eat')
#             print(xb2)
            c1 = list(xb2[(xb2[4]==3.9) & (xb2[5]=='120/30')][1])
            c2 = list(xb2[(xb2[4]==3.9) & (xb2[5]=='120/0')][1])
            c3 = list(xb2[(xb2[4]==3.9) & (xb2[5]=='0/30')][1])
#             c1 = list(xb2[(xb2[4]==3.8) & (xb2[5]=='150/50')][1])
#             c2 = list(xb2[(xb2[4]==3.8) & (xb2[5]=='150/0')][1])
#             c3 = list(xb2[(xb2[4]==3.8) & (xb2[5]=='0/50') & (xb2[3]>=500)][1])
            allc= list(set(c1) & set(c2) & set(c3))
        #     print(allc)
            allr=allr.append(xb2[(xb2[1].isin(allc)) & (xb2[4]==3.9)])
        # xb2[(xb2[1].isin([9])) & (xb2[4]==3.8)]
        allr=allr[[0,1]].reset_index(drop=True)
        allr[1]=allr[1].astype(str)
        allrx= allr.groupby([0])[1].apply(set).apply(list).reset_index()
#         print(allrx)

# '''        
        
#         ts = datetime.combine(getlatest(gethomedir(), 'info')[0][0]-timedelta(days=1), time(23,0,0)).strftime('%Y%m%d%H%M%S')
#         getclosest(gethomedir(), 'R1_*'+'ctb_eat', ts)        
    
    labx=pd.concat([getlatest(pth, 'hkjc_jkc'),getlatest(pth, 'hkjc_wpchi')], axis=1)
    labx=pd.merge(labx, getracejkc(pth), how='left', on=['Race','No.'], suffixes=('_old', ''))
    
    labx['dead']=''
    for r, n in zip(allrx[0], allrx[1]):
        labx.loc[(labx['Race']==r) & (labx['No.'].isin(n)), 'dead']=chr(128128)
        labx['dead']=labx['dead'].fillna('')
#         labx.loc[(labx['Race']==r) & (labx['No.'].isin(n)), 'dead']='死'
#         labx['dead']=labx['dead'].fillna('生')
    if 'diff_jkc_odd' in labx.columns:
        labx['diff_jkc_odd']=labx['diff_jkc_odd'].apply(lambda x: np.round(x, 2))
    else:
        labx['diff_jkc_odd']=0
    
    #result
    labx['Res']=''
    winmap={'1':chr(127942),'2':'Q','3':'T','4':'4th'}
#     winmap={'1':'W','2':'Q','3':'T','4':'4th'}
#     chr(128512)
    try:
        res=getlatest(pth, 'result')
        for r, n, p in zip(res['raceno'], res['H.No'], res['Pla.'].apply(lambda x: re.sub("\D", "", x))  ):
            labx.loc[(labx['Race']==int(r)) & (labx['No.']==n), 'Res']='***'+winmap[p]
    except:
        pass

    #wdg
    labx['WDG']=''
    try:
        wdg=getlatest(pth, 'betall')
        wdg=wdg[(wdg['ema_wdg_h7']>0) & (wdg['Pool']=='WIN')]
        for r, n in zip(wdg['Race'], wdg['No._x']  ):
            labx.loc[(labx['Race']==int(r)) & (labx['No.']==n), 'WDG']=chr(129412)
    except:
        pass

    
#     ctb eat info
    labx['eat']=''
#     print(labx.dtypes)
    try:
        lctbeat=getlatest(pth, 'lctb')[['Race','No.','WP eat']]
        lctbeat['eat']=lctbeat['WP eat'].apply(lambda x: x.split(' ')[1]).apply(lambda x:x.strip())
#        lctbeat=lctbeat[lctbeat['eat']=='76'] #new added
        lctbeat=lctbeat[lctbeat['eat']=='78'] #20201206 change from 76 to 78

        histccc=getlatest(pth, 'hist_ccc')
#         for r, n, p in zip(lctbeat['Race'], lctbeat['No.'], lctbeat['eat']):
        for r, n in zip(lctbeat['Race'].append(histccc['Race']), lctbeat['No.'].append(histccc['No.'])):
#             if p.strip() == '76':
            labx.loc[(labx['Race']==r) & (labx['No.']==str(n)), 'eat']=chr(128169)
#             labx.loc[(labx['Race']==r) & (labx['No.']==str(n)), 'eat']=p.strip()
    except:
        pass
    
    #place_drop
    labx['place_drop']=''
    o7, t7=getclosest_v2(pth, '*wp', previous7(pth).strftime('%Y%m%d%H%M%S'))
#     print(t7)
    o7['Place']=o7['Place'].astype(float)

    o7=o7[o7['Place']==o7['Race'].map(o7.groupby('Race')['Place'].min().to_dict())].reset_index(drop=True)
    for r, n in zip(o7['Race'], o7['No.']  ):
        labx.loc[(labx['Race']==int(r)) & (labx['No.']==n), 'place_drop']=chr(128051)


#         win drop
    p11base = getclosest(pth, 'wp', previous9(pth).strftime('%Y%m%d%H%M%S'))
    p11base['Win']=p11base['Win'].apply(lambda x: float(x) if isfloat(x) else 0)
    if nightrace():
        t11base=getclosest(pth, 'wp', today5(pth).strftime('%Y%m%d%H%M%S'))
    else:
        t11base=getclosest(pth, 'wp', today12(pth).strftime('%Y%m%d%H%M%S'))

    t11base['Win'] = t11base['Win'].apply(lambda x: float(x) if isfloat(x) else 0)
    t11base2= p11base[['No.','Race','Horse','Win']].merge(t11base[['No.','Race','Horse', 'Win']], 
                                                        how='outer', on=['No.','Race','Horse'])
    t11base2['win_sym']=np.where((t11base2['Win_x'] - t11base2['Win_y'])/t11base2['Win_x'] > 0.2, 1, 0)
#         print(t11base2['win_sym'])
    labx=labx.merge(t11base2[['No.','Race','Horse','win_sym']], how='left', on=['No.','Race','Horse'])
    labx['win_sym']=np.where(labx['win_sym'], labx['Win']+chr(9196), labx['Win'])

    
    labxx=labx
    keyxs = ['練馬師', '騎師']
    for keyx in keyxs:
        tag=''.join(set(keyxs) ^ set([keyx]))
#         if keyx= '練馬師':
        labxx['cc'] = labxx.groupby([keyx, 'Race'])[keyx].cumcount()
#         yyxx=labxx[labxx['cc']>0][['Race',keyx]].drop_duplicates()
#         yyxx['cc_new']=99
#         labxx=pd.merge(labxx, yyxx, how='left', on=['Race',keyx])
        yyxx=labxx.groupby(['練馬師', '騎師'])['Horse'].count()
        yyxx=pd.DataFrame(yyxx[yyxx>1])
        yyxx.rename(columns={'Horse': 'cc'+keyx}, inplace=True)
        labxx=pd.merge(labxx, yyxx, how='left', on=['練馬師', '騎師'])


#         if keyx =='騎師': labxx['cc_new']=0
        
#         labxx['nohorse']=np.where(labxx['cc'+keyx]>0 , '('+labxx['馬號']+')'+labxx['馬名']+'('+labxx[tag].map(jtmap).apply(lambda x: x[0])+chr(128108)+')'
#                                   ,'('+labxx['馬號']+')'+labxx['馬名']+'('+labxx[tag].map(jtmap).apply(lambda x: x[0])+')')
        labxx['nohorse']=np.where(labxx['cc'+keyx]>0 , '('+labxx['馬號']+')'+labxx['馬名']+'('+labxx[tag].map(jtmap).fillna(labxx[tag]).apply(lambda x: x[0])+chr(128108)+')'
                                  ,'('+labxx['馬號']+')'+labxx['馬名']+'('+labxx[tag].map(jtmap).fillna(labxx[tag]).apply(lambda x: x[0])+')')

#         print(labxx[])

        
#         p11 = getclosest(pth, 'wp', previous9().strftime('%Y%m%d%H%M%S'))['Win'].apply(lambda x: float(x) if isfloat(x) else 0)
#         if nightrace():
#             t11 = getclosest(pth, 'wp', today5().strftime('%Y%m%d%H%M%S'))['Win'].apply(lambda x: float(x) if isfloat(x) else 0)
#         else:
#             t11 = getclosest(pth, 'wp', today12().strftime('%Y%m%d%H%M%S'))['Win'].apply(lambda x: float(x) if isfloat(x) else 0)

#         labxx['win_sym']=np.where((p11 - t11)/p11 > 0.2, labxx['Win']+chr(9196), labxx['Win'])

        labxx['R']=labxx[['dead','nohorse','win_sym','diff_jkc_odd','eat','WDG','place_drop','Res']].apply(lambda y: y.astype(str), axis=1).apply(lambda x: '/ '.join(x), axis=1)
        
#         labxx['R']=labxx[['dead','nohorse','Win','diff_jkc_odd','eat','Res']].apply(lambda y: y.astype(str), axis=1).apply(lambda x: '/ '.join(x), axis=1)

        xx=labxx
#         print(xx.columns)
#     for keyx in ['練馬師', '騎師']:        
#         xx['cc'] = xx.groupby([keyx, 'Race'])['R'].cumcount()
        dd = pd.DataFrame()
        for ijk in xx['cc'].unique():
            xy= xx[xx['cc']==ijk].pivot(index=keyx, columns='Race', values=['R']).reset_index().fillna('')
            xy.set_axis(xy.columns.map('{0[0]}{0[1]}'.format) , axis=1, inplace=True)
            dd=dd.append(xy, sort=False)

        dd=dd.reset_index(drop=True).fillna('')
        cc=dd.copy()
        cc['sv']=cc[f'R{nr}'].apply(lambda x: float(x.split('/')[-5]) if x !='' else -9999999999.0)
        dd=dd.reindex(cc.sort_values(by='sv', ascending=False).index)
        pth.split('/')[-1]
        if not dd.empty:
            if keyx=='練馬師': 
                key='trainer'
#                 return dd
            elif keyx=='騎師':
                key='jockey'
#                 return dd
            dd.to_pickle(pth+pth.split('/')[-2]+'_'+key+'.pickle')
            if key=='jockey':
                tabtipprocessing(dd)
            
    return 






def get_ctb_wp(rdate, raceno, loc):
    from datetime import datetime
    import requests
    rdate=datetime.strptime(rdate.split('=')[1], "%Y-%m-%d").strftime('%d-%m-%Y')
    s = requests.Session()
    ###original###
#     with s.get(f'http://pending.skk268.com/{loc}data?race_date={rdate}&race_type=3S&rc={raceno}&m=HK&c=0&lu=0', stream=True) as r:
    ### replacement because of coronavirus shutdown of singapore ###
    with s.get(f'http://pending.zas789.com/{loc}data?race_date={rdate}&race_type=3H&rc={raceno}&m=HK&c=0&lu=0', stream=True) as r:
        x=r.text
#     x=requests.get(f'http://pending.skk268.com/{loc}data?race_date={rdate}&race_type=3S&rc={raceno}&m=HK&c=0&lu=0').text
#     print(x)
    x1 = json.loads(x[2:-2], strict=False)
    pdf=pd.DataFrame()
    if x1['pendingData'] !='':
        pdf =pd.read_csv(pd.compat.StringIO(x1['pendingData']), sep='\t', header=None)
        pdf['upddt']=x1['dateTime']
    return pdf



def getctb(position):
    allr=pd.DataFrame()
    for xx in range(1, getlatest(gethomedir(), 'info')[-1]+1):
#         xb2=getlatest(gethomedir(), 'R'+str(xx)+'_ctb'+'_'+position)
        xb2=pd.DataFrame()
        try:
            xb2=get_ctb_wp(getlatest(gethomedir(), 'info')[1], xx, position[0])
        except:
            pass
        #print(xb2)
        if not xb2.empty:
            allr=allr.append(xb2)
    allr.loc[(allr[5].apply(lambda x: x.split('/')[0].replace('!','')).astype(float)>0),'ind']='W'
    allr.loc[(allr[5].apply(lambda x: x.split('/')[1].replace('!','')).astype(float)>0),'ind']='P'
    allr.loc[(allr[5].apply(lambda x: x.split('/')[0].replace('!','')).astype(float)>0) &
             (allr[5].apply(lambda x: x.split('/')[1].replace('!','')).astype(float)>0)
             ,'ind']='WP'

#      0   1     2     3     4       5                upddt ind
# 0    1   1     0   817  4.35    0/12  29-05-2019 19:15:17   P
# 1    1   1     0    52  4.35    0/14  29-05-2019 19:15:17   P
# 2    1   1     0   107  4.30    0/12  29-05-2019 19:15:17   P
# 3    1   1    47    47  4.25   28/13  29-05-2019 19:15:17  WP
        
    allr=allr[(allr[2]>10) | (allr[3]>10)]
#     allr=allr[allr[3]>10]
#     allr=allr[allr[3]>10]
#     allr.reset_index(inplace=True)
#     print(allr)
    if position=='eat':
        return pd.pivot_table(allr,index=[0, 1 ],columns=['ind'],values=[2, 3,4], aggfunc={2: np.sum,3: np.sum, 4:np.min})\
        .sort_index(axis=1, level=[1,0], ascending=[False, True]).reset_index().fillna(0)
    elif position=='bet':
        return pd.pivot_table(allr,index=[0, 1 ],columns=['ind'],values=[2, 3,4], aggfunc={2: np.sum,3: np.sum, 4:np.max})\
        .sort_index(axis=1, level=[1,0], ascending=[False, True]).reset_index().fillna(0)


# def workerlctb():
#     pth =gethomedir()
#     xxx=getctb('bet')
#     yyy=getctb('eat')
    
#     zzz=xxx[[0,1]].merge(yyy, on=[0,1], how='outer', sort =True).fillna(0)
#     xxx=zzz[[0,1]].merge(xxx, on=[0,1], how='outer', sort =True).fillna(0)

# #     print(zzz)
# #     print(xxx)
#     aa={'Race':xxx.iloc[:,0], 'No.':xxx.iloc[:,1],
#     'WP bet':[str(int(x))+' '+ str(int(y)) for x,y in zip(xxx.iloc[:,3],xxx.iloc[:,4])],
#     'WP eat':[str(int(x))+' '+ str(int(y)) for x,y in zip(zzz.iloc[:,3],zzz.iloc[:,4])],
#     'W bet':[str(int(x))+' '+ str(int(y)) for x,y in zip(xxx.iloc[:,5],xxx.iloc[:,7])],
#     'W eat':[str(int(x))+' '+ str(int(y)) for x,y in zip(zzz.iloc[:,5],zzz.iloc[:,7])],
#     'P bet':[str(int(x))+' '+ str(int(y)) for x,y in zip(xxx.iloc[:,9],xxx.iloc[:,10])],
#     'P eat':[str(int(x))+' '+ str(int(y)) for x,y in zip(zzz.iloc[:,9],zzz.iloc[:,10])]
#    }
#     bb=pd.DataFrame(aa)
#     if not bb.empty:
        
#         bb.to_pickle(pth+pth.split('/')[-2]+'_lctb.pickle')
#     return



# def workerlctb():
#     pth =gethomedir()
#     xxx=getctb('bet')
#     yyy=getctb('eat')
    
#     zzz=xxx[[0,1]].merge(yyy, on=[0,1], how='outer', sort =True).fillna(0)
#     xxx=zzz[[0,1]].merge(xxx, on=[0,1], how='outer', sort =True).fillna(0)
#     xxx=xxx.reindex(columns=zzz.columns).fillna(0)


# #     print(zzz)
# #     print(xxx)
#     aa={'Race':xxx.iloc[:,0], 'No.':xxx.iloc[:,1],
#     'WP bet':[str(int(x))+' '+ str(int(y)) for x,y in zip(xxx.iloc[:,3],xxx.iloc[:,4])],
#     'WP eat':[str(int(x))+' '+ str(int(y)) for x,y in zip(zzz.iloc[:,3],zzz.iloc[:,4])],
#     'W bet':[str(int(x))+' '+ str(int(y)) for x,y in zip(xxx.iloc[:,5],xxx.iloc[:,7])],
#     'W eat':[str(int(x))+' '+ str(int(y)) for x,y in zip(zzz.iloc[:,5],zzz.iloc[:,7])],
#     'P bet':[str(int(x))+' '+ str(int(y)) for x,y in zip(xxx.iloc[:,9],xxx.iloc[:,10])],
#     'P eat':[str(int(x))+' '+ str(int(y)) for x,y in zip(zzz.iloc[:,9],zzz.iloc[:,10])]
#    }
#     bb=pd.DataFrame(aa)
#     if not bb.empty:
#         jkc_all=pd.concat([getlatest(pth, 'hkjc_jkc'),getlatest(pth, 'hkjc_wpchi')], axis=1)
#         jkc_all['No.']=jkc_all['No.'].astype('int')
#         bb=pd.merge(jkc_all[[ 'Race', 'No.','馬名','騎師','練馬師','獨贏','位置']],bb
#                  , how='right', on=['Race','No.'], suffixes=('_old', ''))

#         cc=getlatest_remote('getlatest(gethomedir(), '"'betfile'"')')
        
#         if not cc.empty:
#             cc=cc.round(4)
#             cc['Race']=cc['racekey'].astype(str).apply(lambda x: int(x[-2:]))
#             cc.drop(['racekey'], axis=1, inplace=True)

#             if "/".join(gethomedir().split("/")[3:]) == "/".join(getlatest_remote('pd.DataFrame({0:[gethomedir()]})').iloc[0,0].split("/")[3:]):
#                 bb=pd.merge(bb, cc, how='left', on=['Race','No.'])
        
#         bb.to_pickle(pth+pth.split('/')[-2]+'_lctb.pickle')

#         bb.to_pickle(pth+pth.split('/')[-2]+'_'+getptime()+'_lctb.pickle')

#     return


def workerlctb():
    pth =gethomedir()
    xxx=getctb('bet')
    yyy=getctb('eat')
    
    zzz=xxx[[0,1]].merge(yyy, on=[0,1], how='outer', sort =True).fillna(0)
    xxx=zzz[[0,1]].merge(xxx, on=[0,1], how='outer', sort =True).fillna(0)
    xxx=xxx.reindex(columns=zzz.columns).fillna(0)
#     print(zzz)
#     print(xxx)
    aa={'Race':xxx.iloc[:,0], 'No.':xxx.iloc[:,1],
    'WP bet':[str(int(x))+' '+ str(int(y)) for x,y in zip(xxx.iloc[:,3],xxx.iloc[:,4])],
    'WP eat':[str(int(x))+' '+ str(int(y)) for x,y in zip(zzz.iloc[:,3],zzz.iloc[:,4])],
    'W bet':[str(int(x))+' '+ str(int(y)) for x,y in zip(xxx.iloc[:,5],xxx.iloc[:,7])],
    'W eat':[str(int(x))+' '+ str(int(y)) for x,y in zip(zzz.iloc[:,5],zzz.iloc[:,7])],
    'P bet':[str(int(x))+' '+ str(int(y)) for x,y in zip(xxx.iloc[:,9],xxx.iloc[:,10])],
    'P eat':[str(int(x))+' '+ str(int(y)) for x,y in zip(zzz.iloc[:,9],zzz.iloc[:,10])]
   }
    bb=pd.DataFrame(aa)
    bb.to_pickle(pth+pth.split('/')[-2]+'_nrtime.pickle')
    
    if not bb.empty:
        jkc_all=pd.concat([getlatest(pth, 'hkjc_jkc'),getlatest(pth, 'hkjc_wpchi')], axis=1)
        jkc_all['No.']=jkc_all['No.'].astype('int')
        bb=pd.merge(jkc_all[[ 'Race', 'No.','馬名','騎師','練馬師','獨贏','位置']],bb
                 , how='right', on=['Race','No.'], suffixes=('_old', ''))
        try:
            
            cc=getlatest(pth, '2stages')
#             cc['Race']=cc['racekey'].astype(str).apply(lambda x: int(x[-2:]))
#             cc['No.']=cc['combinations'].astype(int)
            

# #             if "/".join(getlatest_remote('pd.DataFrame({0:[gethomedir()]})').iloc[0,0].split("/")[3:])=="/".join(gethomedir().split("/")[3:]):
#             ab=f'getlatest( \'"{"/".join(pth.split("/")[3:])}"\'  , \'"betfile"\')'
#             cc=getlatest_remote(ab)
# #             cc=getlatest_remote('getlatest(gethomedir(), '"'betfile'"')')
#             cc['Race']=cc['racekey'].astype(str).apply(lambda x: int(x[-2:]))
#             cc['No.']=cc['No.'].astype(str)
#             cc=getlatest(gethomedir(),'wp').merge(cc, how='left', on=['Race','No.'])
#             betsize=50000

#             k_formula=lambda x: (np.maximum((x[0]-1)*x[1], 0)-(1-x[1]))/x[0]
#             amt_formula=lambda x:np.maximum(np.around(x*betsize,-1),0)
#             cc['k_win']=cc[['Win','Winprob']].astype(float).apply(k_formula, axis=1)
#             cc['k_plc']=cc[['Place','Plcprob']].astype(float).apply(k_formula, axis=1)
#             cc['betamt_win']=cc['k_win'].apply(amt_formula)
#             cc['betamt_plc']=cc['k_plc'].apply(amt_formula)/2
#             ind=cc['Win'].astype(float)>100
#             cc['betamt_win']=np.where(ind, 0,cc['betamt_win'])
#             cc['betamt_plc']=np.where(ind, 0,cc['betamt_plc'])
#             cc['adv_win']=cc['Winprob']*cc['Win'].astype('float')
#             cc['adv_plc']=cc['Plcprob']*cc['Place'].astype('float')

#             cc=cc[['Race','No.', 'Winprob', 'Plcprob', 'adv_win', 'adv_plc', 'betamt_win', 'betamt_plc']]
#             cc['No.']=cc['No.'].astype(int)
#             cc=cc.round(4)
    #         cc['Race']=cc['racekey'].astype(str).apply(lambda x: int(x[-2:]))
    #         cc.drop(['racekey'], axis=1, inplace=True)

            bb=pd.merge(bb, cc, how='left', on=['Race','No.'])
#             print(bb)
        except:
            pass
            

        bb.to_pickle(pth+pth.split('/')[-2]+'_lctb.pickle')
        bb.to_pickle(pth+pth.split('/')[-2]+'_'+getptime()+'_R'+str(bb['Race'].min())+'_lctb.pickle')
#     bb.to_pickle(pth+pth.split('/')[-2]+'_lctb.pickle')

#     bb.to_pickle(pth+pth.split('/')[-2]+'_'+getptime()+'_lctb.pickle')

    return 

def previous7(pth=gethomedir()):
    from datetime import timedelta, time
    return datetime.combine(getlatest(pth, 'info')[0][0]-timedelta(days=1), time(19,0,0))


def previous11(pth=gethomedir()):
    from datetime import timedelta, time
    return datetime.combine(getlatest(pth, 'info')[0][0]-timedelta(days=1), time(23,0,0))

def previous9(pth=gethomedir()):
    from datetime import timedelta, time
    return datetime.combine(getlatest(pth, 'info')[0][0]-timedelta(days=1), time(21,0,0))

def today11(pth=gethomedir()):
    from datetime import timedelta, time
    return datetime.combine(getlatest(pth, 'info')[0][0], time(11,0,0))

def today12(pth=gethomedir()):
    from datetime import timedelta, time
    return datetime.combine(getlatest(pth, 'info')[0][0], time(12,0,0))

def today5(pth=gethomedir()):
    from datetime import timedelta, time
    return datetime.combine(getlatest(pth, 'info')[0][0], time(17,0,0))

def workerhistccc(pth=gethomedir()):
    import pandas as pd
    from glob import glob
    def getgtzerolctb(pth, times):
        import numpy as np
#         print(times)
        zza =pd.DataFrame(columns=['Race','No.'])
        fds= sorted(glob(pth+'/*_*_*lctb.pickle'), reverse=True)
        for k, v in times.items():
            if int(k[1:]) < getnextrace(pth,'hkjc'):
                for xy in fds:            
                    if xy.split('_')[1]<v:
                        x=pd.read_pickle(xy)
#                         print(k, v, xy.split('_')[1])
                        yyy=getlatest(pth, 'wp')
                        checkno=np.array(yyy[yyy['Race']==int(k[1:])]['No.'].unique(), dtype=np.int32 )
                        checkagnt=np.array(x[x['Race']==int(k[1:])]['No.'].unique(), dtype=np.int32 )
                        if (int(k[1:]) == x['Race'].min()) & (np.array_equal(checkno,checkagnt)):
                            x['eat']=x['WP eat'].apply(lambda x: x.split(' ')[1]).apply(lambda x:x.strip())
#                            zz=x[(x['Race']==int(k[1:])) & (x['eat']=='76')]
# change from 76 to 78 
                            zz=x[(x['Race']==int(k[1:])) & (x['eat']=='78')]
                            zz.reset_index(inplace=True, drop=True)
                            zza=pd.concat([zza, zz], axis=0, sort=True)
                            break
        return zza[['Race','No.']]
    yy=getgtzerolctb(pth, {xy.split('_')[2]: xy.split('_')[1] for xy in sorted(glob(f'{pth}/*ctb_bet.pickle'))})
#     print(yy)
#     print(yy, pth+pth.split('/')[-2]+'_hist_ccc.pickle')
    yy.to_pickle(pth+pth.split('/')[-2]+'_hist_ccc.pickle')
    

def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
    
def nightrace(pth=gethomedir()):
    from datetime import time
    return getlatest(pth,'info')[0][0].time() > time(17,0,0)


def extrlatest_windrop():
    from datetime import time
    allrec=pd.DataFrame()

    ll=gethomedir()
    p11base = getclosest_v2(ll, 'wp', previous9(ll).strftime('%Y%m%d%H%M%S'))[0]
    p11base['Win']=p11base['Win'].apply(lambda x: float(x) if isfloat(x) else 0)
    if nightrace(ll):
        t11base=getclosest_v2(ll, 'wp', today5(ll).strftime('%Y%m%d%H%M%S'))[0]
    else:
        t11base=getclosest_v2(ll, 'wp', today12(ll).strftime('%Y%m%d%H%M%S'))[0]

    t11base['Win'] = t11base['Win'].apply(lambda x: float(x) if isfloat(x) else 0)
    t11base2= p11base[['No.','Race','Horse','Jockey', 'Trainer','Win']].merge(t11base[['No.','Race','Horse', 'Win']], 
                                                        how='outer', on=['No.','Race','Horse'])
    t11base2['windrop']=np.where((t11base2['Win_x'] - t11base2['Win_y'])/t11base2['Win_x'] > 0.2, 1, 0)
    t11base2['racekey']=(ll.split('/')[-2]+t11base2['Race'].astype(str).apply(lambda x: x.zfill(2))).astype('int')

    rmap = {a:b for a, b in zip(sorted(t11base2['racekey'].unique()),getlatest(ll, 'info')[0])}
    t11base2['racedt']= t11base2['racekey'].map(rmap)

    allrec=allrec.append(t11base2.copy())

    return allrec


def getclosest_v2(pth, ele, ts):
    from glob import glob
    import bisect
    s=sorted(list(set([x.split('_')[1] for x in glob(pth+'/*_'+ele+'.pickle')])))
    i = bisect.bisect_left(s, ts)
    mini = min(s[max(0, i-1): i+2], key=lambda t: abs(datetime.strptime(ts,'%Y%m%d%H%M%S') - datetime.strptime(t,'%Y%m%d%H%M%S')))
    return getlatest(pth, mini+'*'+ele), mini


def getlatest_remote(func,USER = "xyz", HOST = "202.64.141.146", PORT=2233):
    
    '''
    examples:
    extra=getlatest_remote('getlatest(gethomedir(), '"'dividend'"')')

    examples:
    extra=getlatest_remote('extrlatest_windrop()')

    '''
    import os
    import subprocess
    import pandas as pd

#    PRIVATE_KEY_LOCATION = "Downloads/learnability.pem"
#     USER = "ec2-user"
#     HOST = "18.141.10.15"
    COMMAND=str.encode(f'python -c "from hrpgm.utilities import *;print({func}.to_json())"')
#     print(COMMAND)
    ssh = subprocess.Popen(["/usr/bin/ssh", f"{USER}@{HOST}", '-p',f'{PORT}'],
                           stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)

    std_data = ssh.communicate(COMMAND)
#     print(std_data)

#     return pd.read_json(std_data[0]).sort_index()
    return pd.read_json(std_data[0].decode().split('\n')[-2]).sort_index()

def sshcmd(USER, HOST, PORT, COMMAND):
    import os
    import subprocess
    import pandas as pd
    ssh = subprocess.Popen(["/usr/bin/ssh", f"{USER}@{HOST}", '-p',PORT],
                           stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)

    std_data = ssh.communicate(COMMAND)
    print(std_data)
    return 

def workertempjkc():
    import requests
    import json
    pth = gethomedir()
    workno=4
#     hdinfo=hookdriver(getdriver(pth, workno))
    for i, x in enumerate(gettask(pth, workno)):
        raceno=getnextrace(pth, 'hkjc')
        if raceno == 0: raceno = 1 
#         hdinfo.get(x.format(raceno=raceno))
#         hdinfo.refresh()
#         time.sleep(2)
        outo=json.loads(requests.get(x.format(raceno=raceno)).text)
#         if not outo.empty:
        with open(pth+gettarget(pth, workno)[i].format(ptime=getptime(), raceno=raceno), 'wb') as outfile:
                pickle.dump(outo, outfile)
            
            
def workerwp():
    for lang in ['eng','chi']:
        pth=gethomedir()
#         from functools import reduce
        src = pd.DataFrame({'key':getlatest(pth,'rawi')['scratchList'].split(';')[1:]})
        if lang=='eng':

            alllist=pd.concat([getlatest(pth, f'*R{xy}_*rcard_{lang}').drop('',axis=1) for xy in range(1,getlatest(pth, 'info')[-1]+1) ], axis=0)
            alllist['No.']=alllist['Horse No.']
            alllist['key']=alllist['raceno'].astype(str)+'#'+alllist['No.'].apply(lambda x: x.strip())
            alllist['Jockey']=alllist['Jockey'].apply(lambda x: x.split('(')[0].strip())
            alllist['Race']=alllist['raceno'].astype(int)
            alllist=pd.merge(alllist,src,on=['key'],how="outer",indicator=True)
            alllist=alllist[alllist['_merge']=='left_only'].drop('_merge', axis=1)
            wpodds=getlatest(pth, 'wpodds').rename(columns={'WIN':'Win','PLA':'Place'}).dropna(axis=0)
            wpodds['key']=wpodds['raceno'].astype(str)+'#'+wpodds['No.'].astype(str)
            wpodds=wpodds[wpodds['Win']!='SCR'].reset_index()
            wpodds=wpodds.dropna() #patch

            alllist=pd.merge(alllist, wpodds[['key','Win','Place']], how='outer', on=['key'])[['Horse','Jockey','No.','Place','Race','Trainer','Win']]
            if not alllist.empty:
                with open(f'{pth}{pth.split("/")[-2]}_{getptime()}_R{getnextrace(pth, "skk")}_hkjc_wp.pickle', 'wb') as outfile:
                    pickle.dump(alllist, outfile)
        elif lang=='chi':
            alllist=pd.concat([getlatest(pth, f'*R{xy}_*rcard_{lang}').drop('',axis=1) for xy in range(1,getlatest(pth, 'info')[-1]+1) ], axis=0)
            alllist['馬號']=alllist['馬匹編號']
            alllist['key']=alllist['raceno'].astype(str)+'#'+alllist['馬匹編號'].apply(lambda x: x.strip())
            alllist['騎師']=alllist['騎師'].apply(lambda x: x.split('(')[0].strip())
            alllist['場次']=alllist['raceno'].astype(int)
            alllist=pd.merge(alllist,src,on=['key'],how="outer",indicator=True)
            alllist=alllist[alllist['_merge']=='left_only'].drop('_merge', axis=1)
            wpodds=getlatest(pth, 'wpodds').rename(columns={'WIN':'獨贏','PLA':'位置'}).dropna(axis=0)
            wpodds['key']=wpodds['raceno'].astype(str)+'#'+wpodds['No.'].astype(str)
            wpodds=wpodds[wpodds['獨贏']!='SCR'].reset_index()
            wpodds=wpodds.dropna()
            alllist=pd.merge(alllist, wpodds[['key','獨贏','位置']], how='outer', on=['key'])[['位置','場次','獨贏','練馬師','馬名','馬號','騎師']]
            if not alllist.empty:
                with open(f'{pth}{pth.split("/")[-2]}_{getptime()}_R{getnextrace(pth, "skk")}_hkjc_wpchi.pickle', 'wb') as outfile:
                    pickle.dump(alllist, outfile)

    return
                          
                          
def workerjkc():
    import json
    import numpy as np
    import pandas as pd
    from datetime import datetime
    pth=gethomedir()
#     x = driver.find_element_by_tag_name('html').text
    y=getlatest(pth, 'rawj')


    jc= y['S'].split('@@@')[2].split('|')[1:] 
#     lo=np.array([float(iii) for iii in [ii.replace('LSE','999999999') if ii== 'LSE' else ii for ii in [i.replace('','0') if i== '' else i for i in y['S'].split('@@@')[7].split('|')[1:]  ]]])
#     co=np.array([float(iii) for iii in [ii.replace('LSE','999999999') if ii== 'LSE' else ii for ii in [i.replace('','0') if i== '' else i for i in y['S'].split('@@@')[8].split('|')[1:]  ]]])
    lo=np.array([float(iii) for iii in [ii.replace('LSE','999999999').replace('RFD','999999999') if ii in ['LSE','RFD'] else ii for ii in [i.replace('','0') if i== '' else i for i in y['S'].split('@@@')[7].split('|')[1:]  ]]])
    co=np.array([float(iii) for iii in [ii.replace('LSE','999999999').replace('RFD','999999999') if ii in ['LSE','RFD'] else ii for ii in [i.replace('','0') if i== '' else i for i in y['S'].split('@@@')[8].split('|')[1:]  ]]])

    jkc_lo={a: b for a,b in zip(jc, lo)}
    jkc_co={a: b for a,b in zip(jc, co)}
    jkc_diff={a: b for a,b in zip(jc, lo-co)}

    labx=getlatest(pth, 'hkjc_wp')

    cr_race_info=pd.DataFrame(columns=['Draw', 'Horse', 'Jockey', 'No.', 'Place', 'Race', 'Trainer', 'Win',
           'Win & Place', 'Wt.', 'disable', 'last_jkc_odd', 'curr_jkc_odd',
           'diff_jkc_odd', 'jkc_upddt'])

    # cr_race_info=labx.copy()
    cr_race_info=labx.merge(cr_race_info, how='left')

#     cr_race_info=labx[labx['Race']==current_race].copy()
    if datetime.now() > datetime.strptime(y['EXP_START_DT'],'%Y%m%d%H%M%S'):
        if 'Others' in jc:
            cr_race_info['last_jkc_odd']=cr_race_info['Jockey'].map(jkc_lo).fillna(jkc_lo['Others'])
            cr_race_info['curr_jkc_odd']=cr_race_info['Jockey'].map(jkc_co).fillna(jkc_co['Others'])
            cr_race_info['diff_jkc_odd']=cr_race_info['Jockey'].map(jkc_diff).fillna(jkc_diff['Others'])
        else:
            cr_race_info['last_jkc_odd']=cr_race_info['Jockey'].map(jkc_lo).fillna(0)
            cr_race_info['curr_jkc_odd']=cr_race_info['Jockey'].map(jkc_co).fillna(0)
            cr_race_info['diff_jkc_odd']=cr_race_info['Jockey'].map(jkc_diff).fillna(0)

        cr_race_info['jkc_upddt']=y['ODDS_UPD_DT']
        
#         20191201_20191201134223_R4_hkjc_jkc.pickle
    if not cr_race_info.empty:
        with open(f'{pth}{pth.split("/")[-2]}_{getptime()}_R{getnextrace(pth, "skk")}_hkjc_jkc.pickle', 'wb') as outfile:
            pickle.dump(cr_race_info, outfile)
    return 

def only_numerics(seq):
    seq_type= type(seq)
    return seq_type().join(filter(seq_type.isdigit, seq))

def ocgetraces(driver, raceId, raceno):
    from selenium import webdriver
    from datetime import datetime
    from selenium.webdriver.support.select import Select
    from selenium.common.exceptions import NoSuchElementException
    import numpy as np
    import pandas as pd
    import time
    import re
    from bs4 import BeautifulSoup
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.by import By
    import json
    print(raceno, f'//*[@id="oc{raceId}"]')
    rind=raceId
#     javaScript = f'document.querySelector("#pageContent > div > div.component-wrapper.odds-event-navigation > ul > li:nth-child({raceindex+1}) > a").click();'
#     driver.execute_script(javaScript)
    b = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, f'//*[@id="oc{rind}"]')))
#     a=BeautifulSoup(driver.page_source, 'html.parser').find('div',{"data-api-params":'{"eventId":"'+rind+'","showHeader":true,"includeOdds":1,"includeTote":true}'} )
    a=BeautifulSoup(driver.page_source, 'html.parser').find('div',{"data-api-params":re.compile(f'.*"eventId":\"{rind}\".*') })
    bs=a.find('div',{"data-event":f"{rind}"}).findAll('div',{"class":"oc-table-tr gutter"})
    
#     print(bs)
    bs=[only_numerics(i['id']) for i in bs]
    alloc=[]
    for b in bs:
        #### find next b for the other horse
#         print(b)
        d=a.find('div',{'id':f'ocSelection_{b}'}).find('span',{"class":"competitor-info__horse-name"} )

        oc={}

        oc['horseId']=d['data-sid']
        oc['race_no']=raceno
        oc['horse_no']=only_numerics(d.find('a' ).text.split('\n')[1])
        oc['horse']=eval(re.sub(r"(e\.\\xa0\\n)", '', repr(d.find('a').text))).split('\n')[2].strip()

#         oc['horse']=d.find('a' ).text.split('\n')[2].strip()
        oc['barrier']=only_numerics(d.find('a' ).text.split('\n')[3])
        oc['link']=d.find('a' )['href']
        oc['betId']=b
        cs=a.find('div',{'id':f'ocSelection_{b}'}).find_next('div',{'id':f'ocSelection_{b}'}).findAll('div',{'data-key':re.compile(f'{b}.*')})
        oc['odds']={c['data-key'][len(b)+1:]:c.text.replace('\n','').replace('bet','').strip() for c in cs}
#         print(a.find('span', {'data-key':f'{b}-Average-FixedWin'}) if b=='9844010' else '')
        es=json.loads(a.find('span', {'data-key':f'{b}-Average-FixedWin'})['data-prices'] or 'null')
#         print(">>>>",es,"<<<<")
        oc['odds_avg']={e:f for e,f in es} if es else []
#         print(oc)
        alloc.append(oc)
    return alloc,  datetime.fromtimestamp(int(a.find('abbr',{"class":"oc-table__countdown"})['data-utime']))

def ocgetmeetinginfo(driver):
                  
    from selenium import webdriver
    from datetime import datetime
    from selenium.webdriver.support.select import Select
    from selenium.common.exceptions import NoSuchElementException
    import numpy as np
    import pandas as pd
    import time
    import re
    from bs4 import BeautifulSoup
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.by import By
    import json
                  
    b = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="pageContent"]/footer')))

    ele = driver.find_element_by_xpath('//*[@id="pageContent"]').get_attribute("outerHTML")
    bspc =BeautifulSoup(ele,'html.parser').find('div',{"class":"component-wrapper odds-event-navigation"})
    meetinginfo=json.loads(bspc['data-api-params'])
    meetinginfo['races']=[{'raceId':x.find('a')['data-eventid'], 'title':x.find('a')['title'], 
                                                         'data-title':x.find('a')['data-title'] } 
                            for x in bspc.findAll('li') if x.find('a')['data-eventid'] !='']
    meetinginfo['info']=json.loads(BeautifulSoup(ele,'html.parser').find('div',{"class":"component-wrapper odds-comparison-header"})['data-api-params'])
    meetinginfo['url']=BeautifulSoup(ele,'html.parser').find('div',{"class":"oc-header-inner"})['data-current-url']

    races=[i['raceId'] for i in meetinginfo['races']]
#     pmraces= np.random.permutation(races)
#     print(races)
#     for race in pmraces:
    for race in races:
#         print(race)
        hrs, racet = ocgetraces(driver, race, races.index(race)+1)
        meetinginfo['races'][races.index(race)].update({ 'race_time':racet, 'horse': hrs})
    meetinginfo['update_time']=driver.execute_script("return Date.now()")
    
#     ace=pd.concat([pd.DataFrame(j)  for i in  meetinginfo['races'] for j in i['horse'] ]).reset_index().rename(columns={'index':'bet'})
#     ace=a[~a['odds'].isna()].reset_index(drop=True)

    return meetinginfo

def ocdicttopd(meetingdict):
    ace=pd.concat([pd.DataFrame(j)  for i in  meetingdict['races'] for j in i['horse'] ]).reset_index().rename(columns={'index':'bet'})
    return ace[~ace['odds'].isna()].reset_index(drop=True)
                  
                  
                  
                  
def worker15():
    pth = gethomedir()
    workno=15
    hdinfo=hookdriver(getdriver(pth, workno))
    for i, x in enumerate(gettask(pth, workno)):
        if hdinfo.current_url!=x:
            hdinfo.get(x)
        outo= ocgetmeetinginfo(hdinfo)
        if outo:
            with open(pth+gettarget(pth, workno)[i].format(ptime=getptime(), raceno=getnextrace(pth, 'skk')), 'wb') as outfile:
                    pickle.dump(outo, outfile)

def drivergoblank(pth , workno):
    hdinfo=hookdriver(getdriver(pth, workno))
    hdinfo.get('about:blank')
    return {str(workno)+'blank': hdinfo.current_url == 'about:blank'}
                  
def workertip():
    from glob import glob
    import numpy as np
    pd.options.mode.chained_assignment = None
    pth=gethomedir()

    a=pd.concat([getlatest(pth, f'*R{i}_skk_eat') for i in range(1, getlatest(pth, 'info')[-1]+1)])
    b=a.groupby([0,1])[2].count().reset_index().rename(columns={2:'count'}).astype(int)
    c=pd.concat([getlatest(pth, f'*R{i}_skk_bet') for i in range(1, getlatest(pth, 'info')[-1]+1)])
    d=c.groupby([0,1])[2].count().reset_index().rename(columns={2:'count'}).astype(int)
    e=b.merge(d, how='outer', on=[0,1], suffixes=['_eat', '_bet']).fillna(0)
    #1=betting on 0= no betting
    c1=np.where(e.count_eat< 20, 1, 0).astype(bool)
    c2=np.where(e.count_bet>28, 1, 0).astype(bool)
    t1=e.iloc[~c2].groupby(0)['count_bet'].nlargest(3).reset_index()\
    .groupby(0)['count_bet'].sum().reset_index()
    c3=~e[0].isin(t1[t1['count_bet']<28][0].tolist())
    e['Race']=e[0].astype(int)
    e['No.']=e[1].astype(int)
    e['外圍']=''
    e.loc[((c1)|(~c1)*c2)*c3, '外圍']=chr(128175)
    e=e.drop([0,1], axis=1)

    # cwa
    # fixing the buges
    path_list = []
    for path in sorted(glob(pth+'/*R'+str(getnextrace(pth, 'hkjc'))+'*_cwa.pickle'), reverse=True):
        if(path.count("_") > 4):
            path_list.append(path)

    t11base = path_list[0]
    current_uptime = t11base.split("/")[-1].split("_")[0]
    for path in path_list[1:]:
        if path.split("/")[-1].split("_")[0]!=current_uptime:
            p11base = path
            break

    p11base = pd.read_pickle(p11base)
    p11base['odds']=p11base['odds'].astype(float).fillna(0)

    t11base=pd.read_pickle(t11base)
    t11base['odds'] = t11base['odds'].astype(float).fillna(0)

    t11base2= p11base[['raceno','RunnerNos', 'combination', 'odds']].merge(t11base[['raceno','RunnerNos','combination', 'odds']], how='outer', on=['raceno','RunnerNos', 'combination'])

    t11base2['cwa_sym']=np.where((t11base2['odds_x'] - t11base2['odds_y']) > 0, 1, 0)
    t11base2 = t11base2.loc[:, ["raceno", "RunnerNos", "cwa_sym"]].rename(columns={"raceno": "Race", "RunnerNos": "No.", "cwa_sym": "3選1"})
    t11base2['3選1'] = t11base2['3選1'].apply(lambda x: "3️⃣" if x == 1 else "")

    e = e.merge(t11base2, on=['Race', 'No.'], how='left')
    # fixing the buges                  
                  
    # jkc
    path = sorted(glob(pth+'/*R'+str(getnextrace(pth, 'hkjc'))+'*_hkjc_jkc.pickle'), reverse=True)[0]
    jkc = pd.read_pickle(path)
    jkc = jkc[jkc.diff_jkc_odd > 0].loc[:, ['No.', 'Race']].reset_index(drop=True)
    jkcTips = []
    for index, row in e.iterrows():
        if len(jkc[(jkc["No."] == str(row["No."])) & (jkc["Race"] == row["Race"])]) > 0:
            jkcTips.append("🐎")
        else:
            jkcTips.append("")
    e.loc[:, "騎師王"] = jkcTips
    e.to_pickle(pth+pth.split('/')[-2]+'_'+getptime()+'_2stages.pickle')

    ctbTip=chr(128175)
    e.loc[:, "tips"] = e["外圍"].apply(lambda x: True if x == ctbTip else False)
    cwaDrop="3️⃣"
    e.loc[:, "cwaDropTips"] = e["3選1"].apply(lambda x: True if x == cwaDrop else False)
    jkcDrop="🐎"
    e.loc[:, "jkcDropTips"] = e["騎師王"].apply(lambda x: True if x == jkcDrop else False)
    e.loc[:, "No."] = e["No."].apply(lambda x:str(x))
    e = e.loc[:, ["Race", "No.", "tips", "cwaDropTips", "jkcDropTips"]]
    e.loc[:, "date"]=datetime.strptime(gethomedir().split("/")[-2], "%Y%m%d")
    e.loc[:, "timeCut"]=round_minutes(datetime.now(), 5)
    e = e.rename(columns={"Race": "race", "No.": "no", "tips":"ctbTip"})

    if len(e) > 0:
        dfWriteMongoDB(e, "indicator")
    return
                  
def round_minutes(dt, resolution):
    new_minute = (dt.minute // resolution * resolution)
    new_minute = dt + timedelta(minutes=new_minute - dt.minute)
    new_minute = new_minute.replace(second=0, microsecond=0)
    return datetime.timestamp(new_minute)
  
def dfWriteMongoDB(df, collection):
    import pymongo
    from pymongo import UpdateOne
    from pymongo.errors import BulkWriteError
    client = pymongo.MongoClient("mongodb://xyz:abcd@202.64.141.146:60288")
    db = client["ABCD"]
    db_collection = db[collection]

    if collection == "indicator":
        df.loc[:, "no"] = df.loc[:, "no"].apply(lambda x: int(x))
        df.loc[:, "race"] = df.loc[:, "race"].apply(lambda x: int(x))
        
        operations = []
        for index, row in df.iterrows():
            operations.append(UpdateOne(
                filter={"date": row["date"], 
                        "race": row["race"], 
                        "no": row["no"],
                        "timeCut": row["timeCut"]
                       },
                update={"$set": row.to_dict()},
                upsert=True)
            )

        
    if collection == "rcard":
        df.loc[:, "no"] = df.loc[:, "no"].apply(lambda x: int(x))
        df.loc[:, "race"] = df.loc[:, "race"].apply(lambda x: int(x))
        df.loc[:, "drawNo"] = df.loc[:, "drawNo"].apply(lambda x: int(x))
        df.loc[:, "weight"] = df.loc[:, "weight"].apply(lambda x: int(x))
        operations = []
        for index, row in df.iterrows():
            operations.append(UpdateOne(
                filter={"date": row["date"], 
                        "race": row["race"], 
                        "no": row["no"],
                       },
                update={"$set": row.to_dict()},
                upsert=True)
            )
                  
    if collection == "raceInfo":
        df.loc[:, "totalRaceNo"] = df.loc[:, "totalRaceNo"].apply(lambda x: int(x))
        operations = []
        for index, row in df.iterrows():
            operations.append(UpdateOne(
                filter={"date": row["date"]},
                update={"$set": row.to_dict()},
                upsert=True)
            )

    try:
        db_collection.bulk_write(operations)
    except BulkWriteError as bwe:
        print(bwe.details)
        raise

    client.close()
                  
def workerjkctip():
    from glob import glob
    import numpy as np
    import pandas as pd
    import pymongo

    pth=gethomedir()
    zza =pd.DataFrame()
    for y in sorted(list(set([x.split('_')[-3] for x in glob(pth+'/*_'+'R*hkjc_jkc'+'.pickle')]))):
        zz=getgtzero(pth, y+'_')
        zz.reset_index(inplace=True, drop=True)
        zza=pd.concat([zza, zz], axis=0)
    zza['racekey']=(pth.split('/')[-2]+zza['Race'].astype(str).apply(lambda x: x.zfill(2))).astype('int')
    rmap = {a:b for a, b in zip(sorted(zza['racekey'].unique()),getlatest(pth,'info')[0])}
    zza['racedt']= zza['racekey'].map(rmap)
    zza = zza.reset_index(drop=True)

    zza['jkc_ind']=(zza['diff_jkc_odd']>0).astype(int)
    zza['jkc_ind']=zza['jkc_ind'].fillna(0)
    zza['jkcTip']=False
    zza.loc[zza['jkc_ind'] == 1, 'jkcTip'] = True
    zza = zza.loc[:, ["Race", "No.", "jkcTip"]].rename(columns={"Race": "race", "No.": "no"})
    zza.loc[:, "date"]=datetime.strptime(gethomedir().split("/")[-2], "%Y%m%d")
    zza.loc[:, "timeCut"]=round_minutes(datetime.now(), 5)
                  
    if len(zza) > 0:
        dfWriteMongoDB(zza, "indicator")
    zza.to_pickle(pth+pth.split('/')[-2]+'_'+getptime()+'_jkc_ind.pickle')
    return
                  
def workermoneyflowtip():
    def moneyFlowTip(wp, qqpl, pool, race, discount = 0.825):
        wp["Win"] = wp["Win"].astype(float)
        qqpl['horse_1'] = qqpl.combination.apply(lambda x: x[0])
        qqpl['horse_2'] = qqpl.combination.apply(lambda x: x[1])

        wp = wp[wp.Race == race].reset_index(drop=True)

        qin = qqpl.loc[:, ["odds_qin", "raceno", "horse_1", "horse_2"]]
        qin.odds_qin = pd.to_numeric(qin.odds_qin, downcast='float' , errors='coerce').dropna()

        qpl = qqpl.loc[:, ["odds_qpl", "raceno", "horse_1", "horse_2"]]
        qpl.odds_qpl = pd.to_numeric(qpl.odds_qpl, downcast='float' , errors='coerce').dropna()

        wp.loc[:, "winMoney"] = float(pool.loc[pool["pool"] == "WIN", "value"]) * discount / wp["Win"].astype(float)
        wp.loc[:, "winMoney"] = wp.loc[:, "winMoney"].apply(lambda x: int(round(x)))
        wp.loc[:, "placeMoney"] = float(pool.loc[pool["pool"] == "PLA", "value"]) * discount / wp["Place"].astype(float)
        wp.loc[:, "placeMoney"] = wp.loc[:, "placeMoney"].apply(lambda x: int(round(x)))
        qin.loc[:, "qMoney"] = float(pool.loc[pool["pool"] == "QIN", "value"]) * discount / (qin["odds_qin"].astype(float)*2)
        qpl.loc[:, "qpMoney"] = float(pool.loc[pool["pool"] == "QPL", "value"]) * discount / (qpl["odds_qpl"].astype(float)*2)

        total_q_money = []
        total_qp_money = []
        for index, row in wp.iterrows():
            No = int(row["No."])
            total_q_money.append(qin[(qin.horse_1 == No) | (qin.horse_2 == No)].qMoney.sum())
            total_qp_money.append(qpl[(qpl.horse_1 == No) | (qpl.horse_2 == No)].qpMoney.sum())

        wp.loc[:, "qMoney"] = total_q_money
        wp.loc[:, "qMoney"] = wp.loc[:, "qMoney"].apply(lambda x: int(round(x)))
        wp.loc[:, "qpMoney"] = total_qp_money
        wp.loc[:, "qpMoney"] = wp.loc[:, "qpMoney"].apply(lambda x: int(round(x)))
        # Handle Place 
        wp.loc[:, "placeMoney"]  = wp.loc[:, "placeMoney"] / 3
        wp.loc[:, "qpMoney"] = wp.loc[:, "qpMoney"] / 3
        wp.loc[:, "TotalMoney"] = wp.loc[:, "winMoney"] + wp.loc[:, "placeMoney"] + wp.loc[:, "qMoney"] + wp.loc[:, "qpMoney"]

        # Weighted Pool
        wp.loc[:, "winMoneyRatio"] = wp.loc[:, "winMoney"] * (wp.loc[:, "winMoney"].sum() / wp.loc[:, "TotalMoney"].sum())
        wp.loc[:, "placeMoneyRatio"] = wp.loc[:, "placeMoney"] * (wp.loc[:, "placeMoney"].sum() / wp.loc[:, "TotalMoney"].sum())
        wp.loc[:, "qMoneyRatio"] = wp.loc[:, "qMoney"] * (wp.loc[:, "qMoney"].sum() / wp.loc[:, "TotalMoney"].sum())
        wp.loc[:, "qpMoneyRatio"] = wp.loc[:, "qpMoney"] * (wp.loc[:, "qpMoney"].sum() / wp.loc[:, "TotalMoney"].sum())
        wp.loc[:, "TotalMoney"] = wp.loc[:, "winMoneyRatio"] + wp.loc[:, "placeMoneyRatio"] + wp.loc[:, "qMoneyRatio"] + wp.loc[:, "qpMoneyRatio"]

        wp = wp.fillna(0)
        wp.loc[:, "TotalMoney"] = wp["TotalMoney"].apply(lambda x: int(round(x)))
        wp = wp.loc[:, ["Race", "No.", "Win", "winMoney", "placeMoney", "qMoney", "qpMoney", "TotalMoney"]].sort_values(by = ["Win"]).reset_index(drop=True)

        moneyFlowTip = [False, False, False]
        for row in range(3, len(wp)):
            if wp.loc[row, "TotalMoney"] > wp.loc[row - 1, "TotalMoney"]:
                moneyFlowTip.append(True)
            else:
                moneyFlowTip.append(False)
        wp["moneyFlowTip"] = moneyFlowTip
        wp["moneyPoolIndex"] = (wp.loc[:, "TotalMoney"] / wp.loc[:, "TotalMoney"].sum()) * 1000
        return wp

    from glob import glob
    import numpy as np
    pd.options.mode.chained_assignment = None
    pth=gethomedir()

    Final_moneyFlowTip = pd.DataFrame([])
    noor= getlatest(gethomedir(), 'info')[-1]+1
    raceno=max(getnextrace(pth, 'hkjc'),1)
    races= np.random.permutation(range(raceno, noor))
    for race in races: 
        wp = pd.read_pickle(sorted(glob(pth+'*_hkjc_wp.pickle'), reverse=True)[0])
        wp = wp[wp.Race == race]
        qqpl = pd.read_pickle(sorted(glob(pth+'/*_R'+ str(race) +'_hkjc_qqpl.pickle'), reverse=True)[0])
        if len(sorted(glob(pth+'/*_R'+ str(race) +'_hkjc_pool.pickle'), reverse=True)) > 0:
            pool = pd.read_pickle(sorted(glob(pth+'/*_R'+ str(race) +'_hkjc_pool.pickle'), reverse=True)[0])
            temp_moneyFlowTip = moneyFlowTip(wp, qqpl, pool, race)
            Final_moneyFlowTip = pd.concat([Final_moneyFlowTip, temp_moneyFlowTip])

    Final_moneyFlowTip.loc[:, "date"]=datetime.strptime(gethomedir().split("/")[-2], "%Y%m%d")
    Final_moneyFlowTip.loc[:, "timeCut"]=round_minutes(datetime.now(), 5)
    Final_moneyFlowTip = Final_moneyFlowTip.rename(
        columns={"Race": "race", "No.": "no", "Win":"win", "TotalMoney": "moneyPool"}).reset_index(drop=True)

    if len(Final_moneyFlowTip) > 0:
        dfWriteMongoDB(Final_moneyFlowTip, "indicator")
    Final_moneyFlowTip.to_pickle(pth+pth.split('/')[-2]+'_'+getptime()+'_money_flow_ind.pickle')
    return

def workeremamoney():
    import datetime
    from glob import glob
    pth=gethomedir()
    info = pd.read_pickle(sorted(glob(pth+'/*_rawi.pickle'), reverse=True)[0])
    raceStartTime = info['racePostTime']

    time_decay = 1
    time_cut = time_decay * 4

    money_flow_list = sorted(glob(pth+'/*_money_flow_ind.pickle'), reverse=True)
    money_flow_list_with_time = []
    for pickle_file in money_flow_list:
        money_flow_list_with_time.append(datetime.datetime.strptime(pickle_file.split("_")[1], '%Y%m%d%H%M%S'))

    final_race_time = []
    race_no = 1
    for StartTime in raceStartTime:
        race_time = {}
        race_time["race"] = race_no
        race_no += 1

        temp_money_flow_list_with_time = list(filter(lambda x: x < StartTime, money_flow_list_with_time))
        latest_time = temp_money_flow_list_with_time[0]
        race_time["latest_time"] = latest_time
        temp_money_flow_list_with_time = list(filter(lambda x: x > (latest_time - datetime.timedelta(minutes = time_cut)), 
                                                     temp_money_flow_list_with_time))
        race_time["select_time"] = temp_money_flow_list_with_time
        final_race_time.append(race_time)

    final_result = pd.DataFrame([])

    for race in final_race_time:
        final_temp = pd.DataFrame([])
        total_weighted = 0
        for temp_time in race["select_time"]:
            temp = pd.read_pickle(pth+pth.split('/')[-2]+'_'+temp_time.strftime('%Y%m%d%H%M%S')+'_money_flow_ind.pickle')
            temp = temp[temp.race == race["race"]]
            temp = temp.loc[:, ["race", "no", "moneyPoolIndex"]]

            temp.loc[:, "time"] = temp_time
            decay = 60*time_decay
            timeweight = np.exp([
                (-(race["latest_time"]-temp_time).total_seconds())/decay
            ])
            temp.loc[:, "timeweight"] = timeweight
            total_weighted += timeweight

            if len(final_temp) == 0:
                final_temp = temp
            else:  
                final_temp = final_temp.append(temp, sort=True)

            final_temp["timeWeightedMoneyIndex"] = final_temp["moneyPoolIndex"] * final_temp["timeweight"] / total_weighted[0]

        final_result = pd.concat([final_result, final_temp], sort=False)

    final_result = pd.DataFrame(final_result.groupby(['race','no'])['timeWeightedMoneyIndex'].sum()).reset_index()

    current_index_data = pd.DataFrame([])
    for race in final_race_time:
        temp = pd.read_pickle(pth+pth.split('/')[-2]+'_'+race["latest_time"].strftime('%Y%m%d%H%M%S')+'_money_flow_ind.pickle')
        temp = temp[temp.race == race["race"]]
        temp = temp.loc[:, ["race", "no", "moneyPoolIndex"]]
        current_index_data = pd.concat([current_index_data, temp], sort=False)

    final_result = pd.merge(final_result, current_index_data, on=['race', 'no'])
    final_result["moneyPoolDiff"] = (final_result["moneyPoolIndex"] - final_result["timeWeightedMoneyIndex"]) * 100

    final_result = final_result.loc[:, ["race", "no", "timeWeightedMoneyIndex", "moneyPoolDiff"]]

    final_result.loc[:, "date"]=datetime.datetime.strptime(gethomedir().split("/")[-2], "%Y%m%d")
    final_result.loc[:, "timeCut"]=round_minutes(datetime.datetime.now(), 5)
    if len(final_result) > 0:
        dfWriteMongoDB(final_result, "indicator")
    final_result.to_pickle(pth+pth.split('/')[-2]+'_'+getptime()+'_EMA_money_ind.pickle')
    return
                  
def workercwatip():
    from glob import glob
    import numpy as np
    pd.options.mode.chained_assignment = None
    pth=gethomedir()

    cwa = pd.read_pickle(sorted(glob(pth+'/*_R1_hkjc_cwa.pickle'), reverse=True)[0])
    cwa.odds = pd.to_numeric(cwa.odds, downcast='float' , errors='coerce').dropna()
    cwa.odds = cwa.odds.apply(lambda x: round(x, 1))
    cwa.loc[:, "cwaTip"] = False
    cwa.loc[cwa.odds <= 1.9, "cwaTip"] = True
    cwa.loc[:, "date"]=datetime.strptime(gethomedir().split("/")[-2], "%Y%m%d")
    cwa.loc[:, "timeCut"]=round_minutes(datetime.now(), 5)
    cwa.loc[:, "RunnerNos"] = cwa.loc[:, "RunnerNos"].astype(str)
    cwa = cwa.rename(columns={"raceno": "race", "RunnerNos": "no", "odds": "cwaOdds", "combination": "cwaCombination"})

    if len(cwa) > 0:
        dfWriteMongoDB(cwa, "indicator")
    cwa.to_pickle(pth+pth.split('/')[-2]+'_'+getptime()+'_cwa_ind.pickle')
    return
                
def tabtipprocessing(tab):
    winDropTip=chr(9196)
    placeDropTip=chr(128051)
    deadHorseTip=chr(128128)
    wdgTip=chr(129412)
    ctbEatTip=chr(128169)
    partnerTip=chr(128108)

    race_list = []
    no_list = []
    winDropTip_list = []
    placeDropTip_list = []
    deadHorseTip_list = []
    wdgTip_list = []
    ctbEatTip_list = []
    partnerTip_list = []

    for column in tab:
        for index, row in tab.iterrows():
            if "R" in column:
                if row[column] != "":
                    temp_row = row[column].split('/')
                    race_list.append(int(column.replace("R", "")))
                    no_list.append(temp_row[1].replace(" ", "").replace("(", "").split(")")[0])

                    if winDropTip in row[column]:
                        winDropTip_list.append(True)
                    else:
                        winDropTip_list.append(False)

                    if placeDropTip in row[column]:
                        placeDropTip_list.append(True)
                    else:
                        placeDropTip_list.append(False)

                    if deadHorseTip in row[column]:
                        deadHorseTip_list.append(True)
                    else:
                        deadHorseTip_list.append(False)

                    if wdgTip in row[column]:
                        wdgTip_list.append(True)
                    else:
                        wdgTip_list.append(False)

                    if ctbEatTip in row[column]:
                        ctbEatTip_list.append(True)
                    else:
                        ctbEatTip_list.append(False)

                    if partnerTip in row[column]:
                        partnerTip_list.append(True)
                    else:
                        partnerTip_list.append(False)

    indicator_df = pd.DataFrame(race_list, columns = ["race"])
    indicator_df.loc[:, "no"] = no_list
    indicator_df.loc[:, "winDropTip"] = winDropTip_list
    indicator_df.loc[:, "placeDropTip"] = placeDropTip_list
    indicator_df.loc[:, "deadHorseTip"] = deadHorseTip_list
    indicator_df.loc[:, "wdgTip"] = wdgTip_list
    indicator_df.loc[:, "ctbEatTip"] = ctbEatTip_list
    indicator_df.loc[:, "partnerTip"] = partnerTip_list
    indicator_df.loc[:, "date"]=datetime.strptime(gethomedir().split("/")[-2], "%Y%m%d")
    indicator_df.loc[:, "timeCut"]=round_minutes(datetime.now(), 5)
                  
    if len(indicator_df) > 0:
        dfWriteMongoDB(indicator_df, "indicator")
    return

def workerrcard():
    from glob import glob
    import numpy as np
    pd.options.mode.chained_assignment = None
    pth=gethomedir()
    final_rcard = pd.DataFrame([])
    for y in sorted(list(set([x.split('_')[-4] for x in glob(pth+'/*_'+'R*hkjc_rcard_chi'+'.pickle')]))):
        rcard_chi = pd.read_pickle(sorted(glob(pth+'/*_'+ y +'_hkjc_rcard_chi.pickle'), reverse=True)[0])
        rcard_eng = pd.read_pickle(sorted(glob(pth+'/*_'+ y +'_hkjc_rcard_eng.pickle'), reverse=True)[0])

        selected_col = ["馬匹編號", "馬名", "騎師", "練馬師"]
        rcard_chi = rcard_chi.loc[:, selected_col]
        rcard_chi = rcard_chi.rename(columns={"馬匹編號": "no", 
                                              "馬名": "horseChiName", 
                                              "騎師": "jockyChiName", 
                                              "練馬師": "trainerChiName"})
        rcard_chi.loc[:, "jockyChiName"] = rcard_chi.loc[:, "jockyChiName"].apply(lambda x: x.split("(")[0] if "(" in x else x)

        selected_col = ["Horse No.", "Horse", "Jockey", "Trainer", "Wt.", "Draw", "raceno"]
        rcard_eng = rcard_eng.loc[:, selected_col]
        rcard_eng = rcard_eng.rename(columns={"Horse No.": "no", 
                                              "Horse": "horseEngName", 
                                              "Jockey": "jockyEngName", 
                                              "Trainer": "trainerEngName",
                                              "Wt.": "weight",
                                              "Draw": "drawNo",
                                              "raceno": "race"
                                             })
        rcard_eng.loc[:, "jockyEngName"] = rcard_eng.loc[:, "jockyEngName"].apply(lambda x: x.split("(")[0] if "(" in x else x)

        temp_rcard = rcard_eng.join(rcard_chi.set_index('no'), on='no')
        final_rcard = pd.concat([final_rcard, temp_rcard])

    final_rcard = final_rcard.reset_index(drop=True)
    final_rcard.loc[:, "date"]=datetime.strptime(gethomedir().split("/")[-2], "%Y%m%d")
    final_rcard = final_rcard[final_rcard.no != "-"].reset_index(drop=True)
    final_rcard = final_rcard[final_rcard.race != "-"].reset_index(drop=True)

    # Result
    res = pd.DataFrame([])
    try:
        res=getlatest(pth, 'result')
        for r, n, p in zip(res['raceno'], res['H.No'], res['Pla.'].apply(lambda x: re.sub("\D", "", x))  ):
            labx.loc[(labx['Race']==int(r)) & (labx['No.']==n), 'Res']='***'+winmap[p]
    except:
        pass

    if len(res) > 0:
        res = res.loc[:, ["Pla.", "H.No", "raceno"]].rename(columns={"Pla.": "rank", "H.No": "no", "raceno": "race"})
        res["race"] = res["race"].apply(lambda x: int(x) if isfloat(x) else 0)
        final_rcard = pd.merge(final_rcard, res, how="left", on=["no", "race"]).fillna("")

    number_of_horse = final_rcard.groupby(['race']).size().reset_index().rename(columns={0: "numberOfHorse"})
    final_rcard = pd.merge(final_rcard,number_of_horse, on=['race','race'])
    final_rcard["numberOfHorse"] =  1 + ((final_rcard["numberOfHorse"] - 10) * 0.1)
    final_rcard['drawNo'].loc[(final_rcard['drawNo'] == "-")] = -1
    final_rcard['weight'].loc[(final_rcard['weight'] == "-")] = -1
                  
    if len(final_rcard) > 0:
        dfWriteMongoDB(final_rcard, "rcard")
    return
                  
def workerraceinfo():
    from glob import glob
    import numpy as np
    pd.options.mode.chained_assignment = None
    pth=gethomedir()

    info = pd.read_pickle(sorted(glob(pth+'/*_rawi.pickle'), reverse=True)[0])
    date = datetime.strptime(gethomedir().split("/")[-2], "%Y%m%d")
    venueEngName = info['venueLong']
    venueChiName = info['venueLongCh']
    totalRaceNo = info['mtgTotalRace']
    raceStartTime = info['racePostTime']

    raceDetail = []
    raceSurfaceChi = []

    for y in sorted(list(set([x.split('_')[-4] for x in glob(pth+'/*_'+'R*hkjc_rinfo_chi'+'.pickle')]))):
        rcard_chi = pd.read_pickle(sorted(glob(pth+'/*_'+ y +'_hkjc_rinfo_chi.pickle'), reverse=True)[0])
        rcard_eng = pd.read_pickle(sorted(glob(pth+'/*_'+ y +'_hkjc_rinfo_eng.pickle'), reverse=True)[0])

        temp_detail = {}
        temp_detail["raceNo"] = y
        temp_detail["raceNameEng"] = rcard_eng["Raceinfo"][0]
        temp_detail["raceNameChi"] = rcard_chi["Raceinfo"][0]
        if rcard_chi["Raceinfo"][2].split(", ")[0] != "全天候跑道":
            temp_detail["raceDistanceEng"] = rcard_eng["Raceinfo"][2].split(", ")[2]
            temp_detail["raceDistanceChi"] = rcard_chi["Raceinfo"][2].split(", ")[2]
        else:
            temp_detail["raceDistanceEng"] = rcard_eng["Raceinfo"][2].split(", ")[1]
            temp_detail["raceDistanceChi"] = rcard_chi["Raceinfo"][2].split(", ")[1]
        temp_detail["raceClassEng"] = rcard_eng["Raceinfo"][3].split(", ")[2]
        temp_detail["raceClassChi"] = rcard_chi["Raceinfo"][3].split(", ")[2]
        temp_detail["raceSurfaceEng"] = rcard_eng["Raceinfo"][2].split(", ")[0]
        temp_detail["raceSurfaceChi"] = rcard_chi["Raceinfo"][2].split(", ")[0]
        raceDetail.append(temp_detail)
        raceSurfaceChi.append(temp_detail["raceSurfaceChi"])

    data = pd.DataFrame(
        [date, venueEngName, venueChiName, totalRaceNo, raceStartTime, raceDetail, raceSurfaceChi]
    ).transpose()
    data = data.rename(columns={0:"date", 1:"venueEngName", 2:"venueChiName", 3:"totalRaceNo", 
                                4:"raceStartTime", 5:"raceDetail", 6:"raceSurfaceChi"})
    if len(data) > 0:
        dfWriteMongoDB(data, "raceInfo")
    return
                  
def workerctbstatus():
    import numpy as np
    pth=gethomedir()

    final_ctb = pd.DataFrame([])
    ctb = pd.read_pickle(pth+pth.split('/')[-2] + '_lctb.pickle')
    if len(ctb) > 0:
        WPBet = pd.DataFrame(item for item in (ctb.loc[:, "WP bet"].apply(lambda x: x.split(" ")).values))
        WPBet = WPBet.rename(columns={0: "WPBet", 1: "WPBetDiscount"})

        WPEat = pd.DataFrame(item for item in (ctb.loc[:, "WP eat"].apply(lambda x: x.split(" ")).values))
        WPEat = WPEat.rename(columns={0: "WPEat", 1: "WPEatDiscount"})

        WBet = pd.DataFrame(item for item in (ctb.loc[:, "W bet"].apply(lambda x: x.split(" ")).values))
        WBet = WBet.rename(columns={0: "WBet", 1: "WBetDiscount"})

        WEat = pd.DataFrame(item for item in (ctb.loc[:, "W eat"].apply(lambda x: x.split(" ")).values))
        WEat = WEat.rename(columns={0: "WEat", 1: "WEatDiscount"})

        PBet = pd.DataFrame(item for item in (ctb.loc[:, "P bet"].apply(lambda x: x.split(" ")).values))
        PBet = PBet.rename(columns={0: "PBet", 1: "PBetDiscount"})

        PEat = pd.DataFrame(item for item in (ctb.loc[:, "P eat"].apply(lambda x: x.split(" ")).values))
        PEat = PEat.rename(columns={0: "PEat", 1: "PEatDiscount"})

        temp_ctb = ctb.loc[:, ["Race", "No.", "count_eat", "count_bet"]]
        temp_ctb = temp_ctb.join(WPBet).join(WPEat).join(WBet).join(WEat).join(PBet).join(PEat)
        temp_ctb = temp_ctb.rename(columns={
            "Race": "race", "No.": "no", "count_eat": "countEat", "count_bet": "countBet"})
        temp_ctb.loc[:, "date"]=datetime.strptime(gethomedir().split("/")[-2], "%Y%m%d")
        temp_ctb.loc[:, "timeCut"]=round_minutes(datetime.now(), 5)

        if len(temp_ctb) > 0:
            dfWriteMongoDB(temp_ctb, "indicator")
    return
                
def sshcmd_horsedataserver(COMMAND):
    import os
    import subprocess
    import pandas as pd
    ssh = subprocess.Popen(["/usr/bin/ssh", '-p', '22', '-i', 
                            '/home/ec2-user/horsedataserver.pem', 
                            'twortert@202.155.233.90'],
                           stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)

    std_data = ssh.communicate(COMMAND)
    print(std_data)
    return 

###### corona virus shutdown of Singapore #####
### changes on get_ctb_wp of workerlctb : from skk to ctb ####
### changes on workertab   : from skk to ctb ####
