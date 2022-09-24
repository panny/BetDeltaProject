import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import pandas as pd
from flask import Flask, redirect
from server import server
from hrpgm.utilities import *
import os
from bs4 import BeautifulSoup
import requests
from flask import request as flask_request  
import hashlib
import numpy as np


header = html.Div(
    className='header',
    children=html.Div(
        className='container-width',
        style={'height': '100%'},
        children=[
            html.Img(
                src='assets/logo.png',
                className='logo'
            ),
            html.Div(className='links', children=[
                html.Div(id='user-name', className='link'),
                html.Div(id='logout', className='link')
            ])
        ]
    )
)


dash_app3 = dash.Dash(__name__, server = server, url_base_pathname='/register/')
dash_app3.layout=html.Div([ 
#                         header, 
                        html.Div(html.H1('This is a private application, please leave immediately')),

                            dcc.Input(
                            id="Login",
                            type="text",
                            placeholder="text",
                            ),
                           dcc.Input(
                            id="Password",
                            type="password",
                            placeholder="password",
                            ),
                           html.Button('Submit', id='login_', 
#                                        style ={'font-size': '25px', 'background-color': 'Yellow'}
                                      ),
                           html.Br(),
                           html.Br(),
                        dcc.Input(
                        id="q1",
                        type="text",
                        placeholder="",
                        style ={'width': '500px'},
                        ),
                        html.Button('Auth', id='q1_sub', hidden=False,
#                                     style ={'font-size': '25px', 'background-color': 'Green'}
                                   ),
                        html.Div(id='retrun_rc'),
                           html.Br(),
                           html.Br(),
                        html.Button('Logout', id='logout_', hidden=False,
#                                     style ={'font-size': '25px', 'background-color': 'Red'}
                                   ),
                        html.Div(id='logout_rc')
                        
          ])

dash_app3.config.suppress_callback_exceptions = True
dash_app3.css.config.serve_locally = True
dash_app3.scripts.config.serve_locally = True



















@dash_app3.callback(
#     [dash.dependencies.Output("q1", "placeholder"), dash.dependencies.Output("q1_sub", "hidden")],
    dash.dependencies.Output("q1", "placeholder"), 
    [ dash.dependencies.Input('login_', 'n_clicks')],
    [dash.dependencies.State("Login", "value"), dash.dependencies.State("Password", "value")])
# import numpy as np
# np.sum(np.array(['ans' in list(i.keys()) for i in list(account['auth'].values())])*1)


def response_to_lg(nc, lg, ps):
    if nc:
        ba_ip= "xx"+flask_request.environ.get('HTTP_X_REAL_IP', flask_request.remote_addr)
        ba_pth = 'hrpgm/betaccounts/'
        if os.path.isfile(ba_pth+f'{ba_ip}.pickle'):
            with open(ba_pth+f'{ba_ip}.pickle', 'rb') as infile:
                account=pickle.load(infile)
                account['login_info']={}
                account['currentQ']=''
                account['getin']=''
        else:
            os.makedirs(ba_pth, exist_ok=True)
            account={'login': f'{lg}', 
                  'pw':hashlib.sha1(f'{ps}'.encode()).hexdigest(),
                 'auth':{},
                   'login_info':{},
                    'currentQ':'',
                    'getin':{}}
            
        print(account)
        xxx= requests.get('https://iosbstxn02.hkjc.com/txnA/AOSBS/Login.ashx?Action=Login_Question&AccOrId='+account['login']+\
               '&Password='+account['pw']+\
               '&Lang=en-US&ActionType=1&IsDisplayNotice=1&ReturnXml=1&UDID=na')
    #         print(xxx.text)
        soup = BeautifulSoup(xxx.text, 'lxml')

        for message in soup.findAll('txn_xml'):
            login_info = dict(message.attrs)
            
        if login_info['errcode']!='0':
            return login_info['errmsg']
        else:
    #             print('Login_info', login_info)
            for message in soup.findAll('question'):
                question = dict(message.attrs)
    #         print(question)
            if question['text']: hid=False
            if question['questionid'] not in list(account['auth'].keys()):
                account['auth'].update({question['questionid']:question})
            else:
                if 'ans' in list(account['auth'][question['questionid']].keys()):
                    ans=account['auth'][question['questionid']]['ans']
                
            account['login_info']=login_info
            account['currentQ']=question['questionid']
            with open(ba_pth+f'{ba_ip}.pickle', 'wb') as outfile:
                pickle.dump(account, outfile)
    #         print(account['auth'])
    #         return (list(question['text']), list(True))
            return question['text']+f" *** press AUTH ****"

@dash_app3.callback(
    dash.dependencies.Output("retrun_rc", "children"),
    [dash.dependencies.Input("q1", "value"), 
     dash.dependencies.Input('q1_sub', 'n_clicks')],
)
def response_q1(ans, nc):
    if nc:
        ba_pth = 'hrpgm/betaccounts/'
        ba_ip= "xx"+flask_request.environ.get('HTTP_X_REAL_IP', flask_request.remote_addr)
        with open(ba_pth+f'{ba_ip}.pickle', 'rb') as infile:
            account=pickle.load(infile)
        question=account['auth'][account['currentQ']]
#         print(f"*************>>>{ans}<<*********")

        if 'ans' in list(account['auth'][account['currentQ']].keys()):
            if (ans is None) & (account['auth'][account['currentQ']]['ans']!=''):
    #             print(f"*************{ans}")

                ans=account['auth'][account['currentQ']]['ans']
        elif not ans is None:
            ans=hashlib.sha1(ans.upper().encode()).hexdigest().upper()

        login_info=account['login_info']
#         print(ans, account['auth'])
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
            account['getin']=getin
    #         print(account)
            account['auth'][account['currentQ']]['ans']=ans

            with open(ba_pth+f'{ba_ip}.pickle', 'wb') as outfile:
                pickle.dump(account, outfile)
        return 'Success'+ f"*** REC: {np.sum(np.array(['ans' in list(i.keys()) for i in list(account['auth'].values())])*1)} /3" if getin['errcode']== '0' else getin['errmsg']

@dash_app3.callback(
    dash.dependencies.Output("logout_rc", "children"),
    [dash.dependencies.Input("logout_", "n_clicks")],
)
def response_logout(nc):
    if nc:
        ba_pth = 'hrpgm/betaccounts/'
        ba_ip= "xx"+flask_request.environ.get('HTTP_X_REAL_IP', flask_request.remote_addr)
        if not os.path.isfile(ba_pth+f'{ba_ip}.pickle'): return [dcc.Location(pathname="/register", id="locate")]

        with open(ba_pth+f'{ba_ip}.pickle', 'rb') as infile:
            account=pickle.load(infile)
        login_info=account['login_info']
        getin=account['getin']
#         print(">>>>>>>"+getin+"<<<<<<")
        if (not getin)  : return [dcc.Location(pathname="/register", id="locate")]
        if (getin['errcode']!= '0') : return [dcc.Location(pathname="/register", id="locate")]

        xxx=    requests.get("https://iosbstxn.hkjc.com/txnA/AOSBS/Logout.ashx?" + "Guid=" + login_info['guid'] + "&BetAccount=" +\
            login_info['betaccount'] + "&SequenceNumber=" + getin['sequencenumber'] + "&SessionId=" + login_info['sessionid'] +\
            "&ServerId=" + login_info['serverid'] + "&Lang=en-US" + "&UDID=na" + "&ELVAEnabled=" + login_info['elvaenabled']+ \
            "&SSOCA=" + "&SSOFO=" + "&SSOAD=")
        soup = BeautifulSoup(xxx.text, 'lxml')
        for message in soup.findAll('txn_xml'):
            getout = dict(message.attrs)
        return ['Success Logout' if getout['errcode']=='0' else getout['errcode'], dcc.Location(pathname="/register", id="locate")]
