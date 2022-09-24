
import dash
from flask import Flask
from server import server

import gentabs
import genctb
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from hrpgm.utilities import *
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
from app import app as dash_app1

dash_app1.layout = html.Div([
        dcc.Tabs(id="tabs", value='騎師', children=[
            dcc.Tab(label='騎師', value='騎師'),
            dcc.Tab(label='練馬師', value='練馬師'),
            dcc.Tab(label='CTB', value='CTB'),
#             dcc.Tab(label='BET', value='BET'),
        ])
        ,
        html.Div(id='tabs-content',
                 ),
         dcc.Interval(
         id='interval-component',
         interval=5*1000, # in milliseconds
         n_intervals=0
         ),
    ])

@dash_app1.callback([dash.dependencies.Output('tabs-content', 'children'),
#               dash.dependencies.Output('output-provider', 'children')
              ],
#               [dash.dependencies.Input('tabs', 'value')])
              [dash.dependencies.Input('tabs', 'value'), 
               dash.dependencies.Input('interval-component', 'n_intervals'),
#               dash.dependencies.Input('danger-danger-provider', 'submit_n_clicks')
              ])
def render_content(tab,n):
    pth = gethomedir()
    if tab =='騎師':
        df=pd.read_pickle(pth+pth.split('/')[-2]+'_jockey.pickle')
        return gentabs.generate_table(df)
    elif tab =='練馬師':
        df=pd.read_pickle(pth+pth.split('/')[-2]+'_trainer.pickle')
        return gentabs.generate_table(df)
    if tab in ['CTB']:
        df=pd.read_pickle(pth+pth.split('/')[-2]+'_lctb.pickle')
        return genctb.generate_ctbtable(df)
    
server.title="ABCD"

if __name__ == '__main__':
    dash_app1.run_server(host="0.0.0.0", port=60288)

