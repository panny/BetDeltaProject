import flask
from flask import request as flask_request  

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input, State
import dash_table
from server import server, User
from flask_login import logout_user, current_user, login_user, login_required, fresh_login_required, confirm_login
from werkzeug.security import check_password_hash
import os
import pickle
import urllib
import math
import requests

from hrpgm.utilities import *
import platform
from glob import glob
from datetime import datetime

# dash_app5 = dash.Dash(__name__, server = server)

dash_app5 = dash.Dash(__name__, server = server, url_base_pathname='/bet/')
_app_route = '/bet'

dash_app5.config.suppress_callback_exceptions = True
dash_app5.css.config.serve_locally = True
dash_app5.scripts.config.serve_locally = True

sd,d,rvenue, nrace =getlatest(gethomedir(), 'info')


dash_app5.layout = html.Div([
        dcc.Tabs(id="tabs", value='R1', children=[
            dcc.Tab(label=f'R{x+1}', value=f'R{x+1}') for x in range(nrace)
        ])
        ,
    
        html.Form([
#         html.Button('REFRESH', id='refresh', type='submit'),
        dcc.Input(id="capital",
                            type='number',
                            placeholder="Capital - 10,000 * 4 pools",min=100, max=10000000, step=100),
        dcc.Checklist(id='checkbtype',
                        options=[
                            {'label': 'WIN', 'value': 'WIN'},
                            {'label': 'PLA', 'value': 'PLA'},
                            {'label': 'QIN', 'value': 'QIN'},
                            {'label': 'QPL', 'value': 'QPL'},
                        ],
                        value=['WIN', 'PLA','QIN','QPL'],style={'display':'inline-block'},labelStyle={'display': 'inline-block'}),
        html.Button('Bet', id='Bet', type='submit', style={'background':'#eb94d0','color':'yello'},  n_clicks_timestamp=0)
#         html.Button('Reset', id='Reset', type='button', style = {display:'none'})

    ], style={'display':'inline-block'}),
    

        html.Div("Please place the bet"),
        html.Br(),
        html.Div(id='not_done'),
    
        html.Br(),
        html.Div(id='Betted'),
        html.Br(),
        html.Div(id='done'),
    
#          dcc.Interval(
#          id='interval-component',
#          interval=5*1000, # in milliseconds
#          n_intervals=0
#          ),
    ])
@dash_app5.callback(dash.dependencies.Output('not_done', 'children'),
                    [dash.dependencies.Input('tabs', 'value'), 
                    dash.dependencies.Input('checkbtype', 'value'),
#                     dash.dependencies.Input('Bet', 'n_clicks_timestamp'),
                    dash.dependencies.Input('Bet', 'n_clicks'),
#                     dash.dependencies.Input('refresh', 'n_clicks'),
                    dash.dependencies.Input('capital','value'),
#                  dash.dependencies.Input('interval-component', 'n_intervals')
              ])

# def abc(tabs, checkbtype, bet, capital, nint):
def abc(tabs, checkbtype, bet, capital):
    ba_pth = 'hrpgm/betaccounts/'
    ba_ip= "xx"+flask_request.environ.get('HTTP_X_REAL_IP', flask_request.remote_addr)
    pth = gethomedir()

    sd,d,rvenue, nrace =getlatest(gethomedir(), 'info')

    def jclogin():
    #     from selenium import webdriver
        import hashlib
        from bs4 import BeautifulSoup
        if os.path.isfile(ba_pth+f'{ba_ip}.pickle'):
            with open(ba_pth+f'{ba_ip}.pickle', 'rb') as infile:
                account=pickle.load(infile)
        xxx= requests.get('https://iosbstxn02.hkjc.com/txnA/AOSBS/Login.ashx?Action=Login_Question&AccOrId='+account['login']+\
               '&Password='+account['pw']+\
               '&Lang=en-US&ActionType=1&IsDisplayNotice=1&ReturnXml=1&UDID=na')
    #         print(xxx.text)
        soup = BeautifulSoup(xxx.text, 'lxml')

        for message in soup.findAll('txn_xml'):
            login_info = dict(message.attrs)
        for message in soup.findAll('question'):
            question = dict(message.attrs)
        if 'ans' in list(account['auth'][question['questionid']].keys()):
            ans=account['auth'][question['questionid']]['ans']

        xxx=    requests.get('https://iosbstxn.hkjc.com/txnA/AOSBS/LoginQuestion.ashx?' + "QuestionId=" + question['questionid']+ "&Answer="+ \
        ans+\
        "&WebAccount=" + login_info['webaccount'] + "&BetAccount=" + login_info['betaccount'] + "&Guid="+\
        login_info['guid'] + "&Lang=en-US" + "&ServerId=" +login_info['serverid'] + "&SessionId=" + login_info['sessionid']+\
        "&UDID=na" + "&Notify=" + "" + "&QuestionLang=" + question['questionlang'] + "&ELVAEnabled="+ \
        login_info['elvaenabled']  + "&WebAccountGUID=" + login_info['webaccountguid'])

        soup = BeautifulSoup(xxx.text, 'lxml')
        for message in soup.findAll('txn_xml'):
            getin = dict(message.attrs)

        if getin['errcode']== '0':
            return login_info, getin, ba_ip
    #     else:
    #         return getin['errmsg']

    def jclogout(login_info, getin):
        import hashlib
        from bs4 import BeautifulSoup

        xxx=    requests.get("https://iosbstxn.hkjc.com/txnA/AOSBS/Logout.ashx?" + "Guid=" + login_info['guid'] + "&BetAccount=" +\
        login_info['betaccount'] + "&SequenceNumber=" + getin['sequencenumber'] + "&SessionId=" + login_info['sessionid'] +\
        "&ServerId=" + login_info['serverid'] + "&Lang=en-US" + "&UDID=na" + "&ELVAEnabled=" + login_info['elvaenabled']+ \
        "&SSOCA=" + "&SSOFO=" + "&SSOAD=")
        soup = BeautifulSoup(xxx.text, 'lxml')

        for message in soup.findAll('txn_xml'):
            getout = dict(message.attrs)
        return getout['errcode']

    def genbet(btype):
        btype_map={'QIN':'QUINELLA', 'QPL':'QUINELLA PLACE','WIN':'WIN', 'PLA':'PLACE'}
        betstr=[]
        for bet in allbets[(allbets['Pool']==btype_map[btype]) & (allbets[f'betamt']>0)].to_dict('record'):
#             bet[f'betamt']=0 #for testing
            newstr = rvenue.split('=')[1]+" "+ sd[0].date().strftime('%a').upper()+" "+btype.upper()+" "\
            +str(bet['racekey']%100)+"*"+bet['combinations'].replace(',','+')+" $"+str(int(bet[f'betamt']))
#             print(newstr)
            betstr.append(urllib.parse.quote(newstr))

#         if btype in ['WIN', 'PLA']:
#             betstr=[]
#             for bet in cc.to_dict('record'):
#                 if (int(bet[f'betamt_{btype.lower()}'])>0) :
# #                     bet[f'betamt_{btype.lower()}']=0 #for testing
#                     btype2='PLA' if btype == 'PLA' else btype
#                     newstr = rvenue.split('=')[1]+" "+ sd[0].date().strftime('%a').upper()+" "+btype2.upper()+" "\
#                     +str(bet['raceno'])+"*"+bet['No.'].replace('-','+')+" $"+str(int(bet[f'betamt_{btype.lower()}']))
# #                     print(newstr)
#                     betstr.append(urllib.parse.quote(newstr))


#         if btype in ['QIN', 'QPL']:
#             betstr=[]
#             for bet in cc2.to_dict('record'):
#                 if (int(bet[f'betamt_{btype.lower()}'])>0):
# #                     bet[f'betamt_{btype.lower()}']=0 #for testing
#                     newstr = rvenue.split('=')[1]+" "+ sd[0].date().strftime('%a').upper()+" "+btype.upper()+" "\
#                     +str(bet['raceno'])+"*"+bet['combinations'].replace(',','+')+" $"+str(int(bet[f'betamt_{btype.lower()}']))
# #                     print(newstr)
#                     betstr.append(urllib.parse.quote(newstr))

        batch=20
        betstr2=[]
        for i in range(math.ceil(len(betstr)/batch)):
            betstr2.append("\\".join(betstr[i*batch:min((i+1)*batch, len(betstr))]))
        return betstr2

    def sendbet(login_info, getin, allbets):
        return requests.get("https://iosbstxn.hkjc.com/txnA/AOSBS/SendBet.ashx?"+ "Html=1" + "&BetAccount=" + login_info['betaccount']+\
        "&SequenceNumber=" + getin['sequencenumber'] + "&BetLines=" + allbets  +\
        "&ServerId=" + login_info['serverid']  + "&SessionId=" + login_info['sessionid'] + "&HNOfRow=2" + "&Lang=en-US"+\
        "&Dt=mobile" + "&Dpi=hdpi")


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
        #     print(c)
            if c=='Pool': 
                b[c] = b[c].apply(lambda x: x.upper())
            else:
                b[c] = b[c].apply(lambda x: re.sub("[a-zA-Z\$]", "", x).replace(" ",""))
        return b

    pd.options.display.float_format = '{:.4f}'.format
    
    try:
        allbets=getlatest(pth, f'{tabs}_*betfile')\
        .merge(getlatest(pth, f'{tabs}_*rcard_chi*').rename(columns={'馬匹編號':'combinations'}), on=['combinations'], how='left')[['racekey','Pool','combinations',  '馬名', '騎師', '練馬師','ema_wdg_h7','odds','prob','k','betamt']]
    except:
        allbets=pd.DataFrame(columns=['racekey','Pool','combinations',  '馬名', '騎師', '練馬師','ema_wdg_h7','odds','prob','k','betamt'])
    cc=allbets[allbets['Pool'].isin(['WIN','PLACE'])].reset_index(drop=True).copy()
    cc['ema_wdg_h7']=cc['ema_wdg_h7'].map('{:,.4f}'.format)
    cc['k']=cc['k'].map('{:,.4f}'.format)
    cc2x=allbets[allbets['Pool'].isin(['QUINELLA','QUINELLA PLACE'])]
    cc2x
    cc2x['horse1'] = cc2x['combinations'].apply(lambda x: x.split(',')[0].zfill(2))
    cc2x['horse2'] = cc2x['combinations'].apply(lambda x: x.split(',')[1].zfill(2))
    cc2x['Q']=cc2x['betamt'].replace(0, np.nan).fillna('').astype(str)
    cc2x_q=cc2x[cc2x['Pool']=='QUINELLA'].pivot(index='horse1', columns='horse2', values=['Q']).reset_index().fillna('')
    cc2x_q.set_axis(cc2x_q.columns.map('{0[0]}{0[1]}'.format) , axis=1, inplace=True)
#     display(cc2x_q)
    cc2x_qp=cc2x[cc2x['Pool']=='QUINELLA PLACE'].pivot(index='horse1', columns='horse2', values=['Q']).reset_index().fillna('')
    cc2x_qp.set_axis(cc2x_qp.columns.map('{0[0]}{0[1]}'.format) , axis=1, inplace=True)
#     display(cc2x_qp)


    conbet=pd.DataFrame()
    if glob(ba_pth+ba_ip+'_'+pth.split('/')[-2]+'_'+tabs+'_*_betconfirm.html')!=[]:
#     if os.path.isfile(ba_pth+ba_ip+'_'+pth.split('/')[-2]+'_'+tabs+'_*_betconfirm.html'):
        conbet=pd.concat([htmltopd(i) for i in glob(ba_pth+ba_ip+'_'+pth.split('/')[-2]+'_'+tabs+'_*_betconfirm.html')], axis=0).reset_index(drop=True)
        conbet=pdtopd(conbet)
        conbet['betamt']=conbet['betamt'].astype(float)
#         print(conbet)
        if glob(pth+'*dividend*.pickle')!=[]:
#         if os.path.isfile(pth+'*dividend*.pickle'):
            dividend=getlatest(pth, 'dividend')
            dividend['combinations']=dividend['Winning Combination'].apply(lambda x: x.replace(",","+"))
            conbet=conbet.merge(dividend, on =['raceno','combinations','Pool'], how='left').fillna(0)
            conbet['revenue']=(conbet['Dividend (HK$)'].apply(lambda x: str(x).replace(',','')).astype(float)/10)*conbet['betamt'].astype(float)
            conbet['net']=conbet['revenue']-conbet['betamt'].astype(float).fillna(0)




# #     print(bet)
#     if bet:
# #     if (datetime.now()-datetime.fromtimestamp(bet/1000)).total_seconds()<5:

#         for bt in checkbtype:
#             temp = genbet(bt)
# #             print(temp)
#             for xtemp in temp:
# #                 print(xtemp)
#                 login_info, getin, ba_ip=jclogin()
#                 ytemp = sendbet(login_info, getin, xtemp)
#                 print("ytemp", ytemp)
#                 err = jclogout(login_info, getin)
#                 with open(ba_pth+ba_ip+'_'+pth.split('/')[-2]+'_'+tabs+'_'+getptime()+'_betconfirm.html', 'w') as f:
#                     f.write(ytemp.text)
#             with open(ba_pth+ba_ip+'_'+pth.split('/')[-2]+'_'+tabs+'_'+getptime()+'_betconfirm.pickle', 'wb') as outfile:
#                 pickle.dump(temp, outfile)
#             temp=None


    return html.Div('WIN/PLA'), dash_table.DataTable(
                columns=[{"name": i, "id": i} for i in cc.columns],
                data=cc.to_dict('records')), \
                html.Div('QIN'), dash_table.DataTable(
                columns=[{"name": i, "id": i} for i in cc2x_q.columns],
                data=cc2x_q.to_dict('records')), \
                html.Div('QPL'), dash_table.DataTable(
                columns=[{"name": i, "id": i} for i in cc2x_qp.columns],
                data=cc2x_qp.to_dict('records')), \
                html.Div('BETS'), dash_table.DataTable(
                columns=[{"name": i, "id": i} for i in conbet.columns],
                data=conbet.to_dict('records'))



server.title="ABCD"

if __name__ == '__main__':
    dash_app5.run_server(host="0.0.0.0", port=60288)

