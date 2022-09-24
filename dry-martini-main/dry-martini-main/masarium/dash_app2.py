
import dash
from flask import Flask
from server import server
from flask import request as flask_request  

import app_pivot
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from hrpgm.utilities import *
from app_p import app as dash_app2
from glob import glob
import os
import platform
import dash_table

def htmltopd(html):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(open(html).read(), 'html.parser')
    data2 = []
    for a in soup.find_all('div',{'class': ['betcon_itemTable']}):
        rows = a.find_all('tr')
        data=[]
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele]) # Get rid of empty values
        data2.append({data[1][0]:data[1][1], 'bet':data[-3][0]})
    return pd.DataFrame(data2)

def pdtopd(a):
    import re
    rx_dict = {
        'Pool': re.compile(r'(Quinella Place|Win|Place|Quinella)'),
        'raceno': re.compile(r'(Race \d+)'),
        'combinations': re.compile(r'(\d+\s+[a-zA-Z]+)'),
        'betamt': re.compile(r'(\$\d+)'),
    }
    def _parse_line(line):
        return { key: "+".join(rx.findall(line)) for key, rx in rx_dict.items() if rx.search(line)}
    b= pd.DataFrame(a[a['Status']=='BET ACCEPTED']['bet'].apply(lambda x: _parse_line(x)).tolist(), columns=list(rx_dict))
    for c in list(b.columns):
        if c=='Pool': 
            b[c] = b[c].apply(lambda x: x.upper())
        else:
            b[c] = b[c].apply(lambda x: re.sub("[a-zA-Z\$]", "", x).replace(" ",""))
    return b

# dash_app2 = dash.Dash(__name__, server = server)

# dash_app2 = dash.Dash(__name__, server = server, url_base_pathname='/reports/')
# _app_route = '/reports'

dash_app2.config.suppress_callback_exceptions = True
dash_app2.css.config.serve_locally = True
dash_app2.scripts.config.serve_locally = True

dash_app2.layout = html.Div([
        dcc.Tabs(id="tabs", value='own', children=[
            dcc.Tab(label='own', value='own'),
            dcc.Tab(label='sim', value='sim')
        ]),
        html.Form([
            dcc.Input(id="capital1",
                            type='number',
                            placeholder="WIN",min=1000, max=1000000, step=100),
            dcc.Input(id="capital2",
                            type='number',
                            placeholder="PLC",min=1000, max=1000000, step=100),
            dcc.Input(id="capital3",
                            type='number',
                            placeholder="QIN",min=1000, max=1000000, step=100),
            dcc.Input(id="capital4",
                            type='number',
                            placeholder="QPL",min=1000, max=1000000, step=100),
        ], style={'display':'inline-block'})

        ,html.Div(id='tabs-content')
    ])


@dash_app2.callback(dash.dependencies.Output('tabs-content', 'children'),
              [dash.dependencies.Input('tabs', 'value'), 
               dash.dependencies.Input('capital1', 'value'), 
               dash.dependencies.Input('capital2', 'value'), 
               dash.dependencies.Input('capital3', 'value'), 
               dash.dependencies.Input('capital4', 'value'), 
              ])
def render_content(tab, cap1, cap2, cap3, cap4):
    pth = gethomedir()
    if tab =='own':
        ba_pth = 'hrpgm/betaccounts/'
        ba_ip= "xx"+flask_request.environ.get('HTTP_X_REAL_IP', flask_request.remote_addr)
    #     if not os.path.isfile(ba_pth+ba_ip+'_'+pth.split('/')[-2]+'_total_invest.pickle'):

        conbet=pd.DataFrame()

        if glob(ba_pth+ba_ip+'_'+pth.split('/')[-2]+'*_betconfirm.html')!=[]:
            conbet=pd.concat([htmltopd(i) for i in glob(ba_pth+ba_ip+'_'+pth.split('/')[-2]+'*_betconfirm.html')], axis=0).reset_index(drop=True)
            conbet=pdtopd(conbet)
            conbet['betamt']=conbet['betamt'].astype(float)
            conbet['date']=pth.split('/')[-2]
    #             print(conbet)
            if glob(pth+'*dividend*.pickle')!=[]:
                dividend=getlatest(pth, 'dividend')
                dividend['combinations']=dividend['Winning Combination'].apply(lambda x: x.replace(",","+"))
                conbet=conbet.merge(dividend, on =['raceno','combinations','Pool'], how='left').fillna(0)
                conbet['revenue']=(conbet['Dividend (HK$)'].apply(lambda x: str(x).replace(',','')).astype(float)/10)*conbet['betamt'].astype(float)
                conbet['net']=conbet['revenue']-conbet['betamt'].astype(float).fillna(0)
                conbet=conbet[['date','raceno','Pool','combinations','betamt','revenue','net']]
        conbet.to_pickle(ba_pth+ba_ip+'_'+pth.split('/')[-2]+'_total_invest.pickle')
        allbet=pd.DataFrame()
        for ab in glob(ba_pth+ba_ip+'_*_total_invest.pickle'):
            t1=pd.read_pickle(ab)
            allbet=allbet.append(t1).reset_index(drop=True)
        xxx=app_pivot.pivot(allbet)
        return xxx

    elif tab=='sim':
#     if tab=='sim':
        cc=getlatest(gethomedir(), 'betfile')
#         if platform.node() == 'biscoveryubuntu':
#             cc=getlatest(gethomedir(), 'betfile')
#         else:
#             cc=getlatest_remote('getlatest(gethomedir(), '"'betfile'"')')
#         cc['Race']=cc['racekey'].astype(str).apply(lambda x: int(x[-2:]))
#         cc['No.']=cc['No.'].astype(str)
#         cc=getlatest(gethomedir(),'wp').merge(cc, how='left', on=['Race','No.'])
#         betsize=[]
#         for ii in [cap1, cap2, cap3, cap4]:
#             if ii == None: ii = 10000
#             betsize.append(ii)
# #         betsize=[cap1, cap2, cap3, cap4]
# #         if betsize==[None, None, None, None]: betsize=[10000,10000,10000,10000]
        
#         k_formula=lambda x: (np.maximum((x[0]-1)*x[1], 0)-(1-x[1]))/x[0]
#         amt_formula0=lambda x:np.maximum(np.around(x*betsize[0],-1),0)
#         amt_formula1=lambda x:np.maximum(np.around(x*betsize[1],-1),0)
#         amt_formula2=lambda x:np.maximum(np.around(x*betsize[2],-1),0)
#         amt_formula3=lambda x:np.maximum(np.around(x*betsize[3],-1),0)
#         cc['k_win']=cc[['Win','Winprob']].astype(float).apply(k_formula, axis=1)
#         cc['k_plc']=cc[['Place','Plcprob']].astype(float).apply(k_formula, axis=1)
#         cc['betamt_win']=cc['k_win'].apply(amt_formula0)
#         cc['betamt_plc']=cc['k_plc'].apply(amt_formula1)/2
#         ind=cc['Win'].astype(float)>100
#         cc['betamt_win']=np.where(ind, 0,cc['betamt_win'])
#         # cc['betamt_plc']=np.where(ind, 0,cc['betamt_plc'])
#         cc['No.']=cc['No.'].astype(str)

#         cc[['Race','No.', 'Winprob', 'Plcprob', 'k_win', 'k_plc', 'betamt_win', 'betamt_plc']]
#         dividend=getlatest(gethomedir(), 'dividend')
#         dividend['racekey']=(dividend['racedate'].apply(lambda x: datetime.strptime(x.strip(), "%d/%m/%Y").strftime('%Y%m%d'))+dividend['raceno'].astype('str').apply(lambda x: x.zfill(2))).astype(int)
#         dividend['No.']=dividend['Winning Combination']            
#         tempresult=cc.merge(dividend[dividend['Pool']=='WIN'], on =['racekey','No.'], how='left').merge(dividend[dividend['Pool']=='PLACE'], on =['racekey','No.'], how='left').fillna(0)
#         tempresult['revenue_win']=(tempresult['Dividend (HK$)_x'].astype(float)/10)*tempresult['betamt_win']
#         tempresult['revenue_plc']=(tempresult['Dividend (HK$)_y'].astype(float)/10)*tempresult['betamt_plc']
#         res_wp=tempresult.copy()
        
#         if platform.node() == 'biscoveryubuntu':
#             cc=getlatest(gethomedir(), 'qinfile').\
#             merge(getlatest(gethomedir(), 'qplfile'), 
#                   on=['racekey', 'combinations'], suffixes = ("_qin","_qpl"))
#         else:
#             cc=getlatest_remote('getlatest(gethomedir(), '"'qinfile'"')').\
#             merge(getlatest_remote('getlatest(gethomedir(), '"'qplfile'"')'), 
#                   on=['racekey', 'combinations'], suffixes = ("_qin","_qpl"))
            
#         cc['raceno']=cc['racekey'].astype(str).apply(lambda x: int(x[-2:]))
#         qqpl=pd.DataFrame()
#         for r in cc.raceno.unique():
#             qqpl=qqpl.append(getlatest(gethomedir(),f'R{r}_*qqpl'))
#         qqpl=qqpl.reset_index(drop=True)
#         qqpl['combinations']=qqpl['combination'].apply(lambda x: str(x).strip().replace('(','').replace(')','').replace(' ',''))
#         cc=qqpl.merge(cc, on=['raceno','combinations'], how='right')
#         cc['odds_qin']=cc['odds_qin'].replace("SCR",'0')
#         cc['odds_qpl']=cc['odds_qpl'].replace("SCR",'0')        
# #         betsize=10000

# #         k_formula=lambda x: (np.maximum((x[0]-1)*x[1], 0)-(1-x[1]))/x[0]
# #         amt_formula=lambda x:np.maximum(np.around(x*betsize,-1),0)
#         cc['k_qin']=cc[['odds_qin','prob_qin']].astype(float).apply(k_formula, axis=1)
#         cc['k_qpl']=cc[['odds_qpl','prob_qpl']].astype(float).apply(k_formula, axis=1)
#         cc['betamt_qin']=cc['k_qin'].apply(amt_formula2)
#         cc['betamt_qpl']=cc['k_qpl'].apply(amt_formula3)

# dividend
        dividend=getlatest(gethomedir(), 'dividend')
        
        dividend['racekey']=(dividend['racedate'].apply(lambda x: datetime.strptime(x.strip(), '%d/%m/%Y').strftime('%Y%m%d'))+\
                dividend['raceno'].apply(lambda x: x.zfill(2)).astype(str)).astype(int)
        dividend['dividend']=dividend['Dividend (HK$)'].astype(str).apply(lambda x: x.replace(',',"") if any(i.isdigit() for i in x) else "0.0").astype(float)/10
        dividend['combinations']=dividend['Winning Combination'].apply(lambda x: x.strip())

        allbet=cc[['racekey', 'combinations','Pool', 'prob','odds','betamt','k','ema_wdg_h']]\
.merge(dividend[['racekey', 'combinations','Pool', 'dividend']], 
       on=['racekey', 'combinations','Pool'], how='left').fillna(0)
        allbet['revenue']=allbet['dividend']*allbet['betamt']
        allbet['net']=allbet['revenue']-allbet['betamt']


#         dividend['racekey']=(dividend['racedate'].apply(lambda x: datetime.strptime(x.strip(), "%d/%m/%Y").strftime('%Y%m%d'))+dividend['raceno'].astype('str').apply(lambda x: x.zfill(2))).astype(int)
#         dividend['combinations']=dividend['Winning Combination']

#         tempresult=cc.merge(dividend[dividend['Pool']=='QUINELLA'], on =['racekey','combinations'], how='left').merge(dividend[dividend['Pool']=='QUINELLA PLACE'], on =['racekey','combinations'], how='left').fillna(0)
#         tempresult['revenue_qin']=(tempresult['Dividend (HK$)_x'].apply(lambda x: str(x).replace(',','')).astype(float)/10)*tempresult['betamt_qin']
#         tempresult['revenue_qpl']=(tempresult['Dividend (HK$)_y'].apply(lambda x: str(x).replace(',','')).astype(float)/10)*tempresult['betamt_qpl']
        
#         allbet=pd.DataFrame()
#         for btype in ['WIN', 'PLC','QIN','QPL']:
#             conbet=pd.DataFrame()
#             if btype in ['WIN', 'PLC']:
#                 conbet['raceno'], conbet['combinations']= res_wp['racekey'].apply(lambda x: int(str(x)[-2:])), res_wp['No.']
#                 conbet['betamt'] = res_wp[f'betamt_{btype.lower()}']
#                 conbet['revenue'] = res_wp[f'revenue_{btype.lower()}']
#                 conbet['net']=res_wp[f'revenue_{btype.lower()}']-res_wp[f'betamt_{btype.lower()}']
#                 conbet['Pool']=btype
#                 conbet['date']=pth.split('/')[-2]


#             if btype in ['QIN', 'QPL']:
           
#                 conbet['raceno'], conbet['combinations']= tempresult['racekey'].apply(lambda x: int(str(x)[-2:])), tempresult['combinations']
#                 conbet['betamt'] = tempresult[f'betamt_{btype.lower()}']
#                 conbet['revenue'] = tempresult[f'revenue_{btype.lower()}']
#                 conbet['net']=tempresult[f'revenue_{btype.lower()}']-tempresult[f'betamt_{btype.lower()}']
#                 conbet['Pool']=btype
#                 conbet['date']=pth.split('/')[-2]
#             conbet=conbet[['date','raceno','Pool','combinations','betamt','revenue','net']]
#             allbet=allbet.append(conbet)
#         xxx2=app_pivot2.pivot(allbet)
#         print(xxx2)
#         return xxx2
        out=pd.pivot_table(allbet, index=['date','raceno'], columns=['Pool'], values=[ 'betamt','revenue','net'], aggfunc=np.sum,
                       fill_value='',
                       margins=True,
                       margins_name='Total')


        out.set_axis(out.columns.map('{0[0]}{0[1]}'.format) , axis=1, inplace=True)
#        out=out.reset_index()
        out=out.round(2)
        out=out.reset_index()
        return dash_table.DataTable(
                        columns=[{"name": i, "id": i} for i in out.columns],
                        data=out.to_dict('records'))
    
    
dash_app2.title="ABCD"      
if __name__ == '__main__':
    dash_app2.run_server(host="0.0.0.0", port=8050)

