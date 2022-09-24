#!/usr/bin/python
# coding: utf-8



from utilities import *
import pandas as pd
a = pd.read_csv('/home/ec2-user/hrpgm/download_log_template.csv')




# from datetime import datetime
# hdinfo=hookdriver(getdriverinfo(c[0]))
# hdinfo.get(a.link[0])
# hdinfo.refresh()
# time.sleep(5)
outtar = get0(None)
pt, rdate, rvenue, _ = outtar
dater=datetime.strptime(rdate.split('=')[1], "%Y-%m-%d").strftime('%d-%m-%Y')
brdate=datetime.strptime(rdate.split('=')[1], "%Y-%m-%d").strftime('%Y%m%d')
rcarddate=datetime.strptime(rdate.split('=')[1], "%Y-%m-%d").strftime('%Y/%m/%d')

brvenue=rvenue.split('=')[1]

pvenue={'HV':'happy-valley','ST':'sha-tin'}[brvenue]
pdate=rdate.split('=')[1]

ptime='{ptime}'
raceno='{raceno}'
noofrace='{noofrace}'
itype='{itype}'

c=[createdriver() for b in a.driverno.unique()]


# import os
pth = f'/home/ec2-user/hrpgm/meetings/{brdate}/'
# os.makedirs(pth.format(**locals()), exist_ok=True)




d=[]
for i in a.link:
    d.append(str(i.format(**locals())))
a['new_link']=d




d=[]
for i in a.outtarget:
    d.append(str(i.format(**locals())))
a['new_target']=d




task={}
target={}
for b in a.driverno.unique():
    task[b]=list(a[a.driverno==b]['new_link'])
    target[b]=list(a[a.driverno==b]['new_target'])



d={i+1:getdriverinfo(e) for i, e in enumerate(c)}




import pickle
ptime=getptime()
with open('/home/ec2-user/hrpgm/meetings/outtar.pickle', 'wb') as outfile:
    pickle.dump(outtar, outfile)
with open(pth.format(**locals())+target[1][0].format(**locals()), 'wb') as outfile:
    pickle.dump(outtar, outfile)
for ii,b in enumerate(a.driverno.unique()):
    d={b:getdriverinfo(c[ii])}
    with open(pth.format(**locals())+f'drivers{b}.pickle', 'wb') as outfile:
        pickle.dump(d, outfile)
with open(pth.format(**locals())+'task.pickle', 'wb') as outfile:
    pickle.dump(task, outfile)
with open(pth.format(**locals())+'target.pickle', 'wb') as outfile:
    pickle.dump(target, outfile)



# import time
# ttt = int(abs((pt[-1]-datetime.now()).total_seconds())+30*60)
# print(ttt)
# time.sleep(ttt)




# for x in c:
#     quitdriver(x)




# os.system('ps -awx | grep chromedriver')





