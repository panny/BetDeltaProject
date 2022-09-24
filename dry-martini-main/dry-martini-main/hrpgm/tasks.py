import sys
sys.path.append("/home/ec2-user/hrpgm/")
from utilities import *
import time
from datetime import datetime, timedelta
import os
import subprocess

# b=1
b=sys.argv[1]

bk=0
while(1):
    try:
        y=getlatest(gethomedir(), 'info') 
        getattr(sys.modules[__name__], f"worker{b}")()

#         worker1()
        bk=0
#         print(bk)
    except:
        bk = bk +1
        print(f'error => {b}, check {bk}!')
#        bk = bk+1

        if bk >3: 
    #         break

            cmd = f'/usr/bin/python /home/ec2-user/hrpgm/restartdriver.py {b}' 
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            c, err = p.communicate() 
            print(c)
            bk=0

    #         for i in pid_srch()[getdriver(gethomedir(), b)[0]]:
    #             os.popen(f'kill {i}')
    #         c=createdriver()
    #         d={b:getdriverinfo(c)}
    #         with open(gethomedir().format(**locals())+f'drivers{b}.pickle', 'wb') as outfile:
    #             pickle.dump(d, outfile)    


    time.sleep(int(sys.argv[2]))
    if (y[0][-1]-datetime.now()).total_seconds() <-900:
        break
