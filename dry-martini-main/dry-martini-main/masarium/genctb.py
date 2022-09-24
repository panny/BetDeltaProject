import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app as app_ctb
import dash_table
import pandas as pd
from flask import Flask, redirect



def generate_ctbtable(dataframe):

    return [html.Div([
            html.Button('BET', id='buttonbet', style ={'font-size': '25px', 'background-color': 'Green'}),
            html.Button('REGISTER', id='buttonlogin', style ={'font-size': '25px', 'background-color': 'Blue'}),
            html.Button('REPORT', id='buttonreport', style ={'font-size': '25px', 'background-color': 'Yellow'}),
            html.Div(id='container-button-basic1'),
            html.Div(id='container-button-basic2'),
            html.Div(id='container-button-basic3'),
            html.Br(),
            html.Br(),
            dash_table.DataTable(
                    id='ctbtbl',
                    columns=[{"name": i, "id": i} for i in dataframe.columns],
                    data=dataframe.to_dict('records'),
                    style_table={'overflowX': 'scroll'},
                    style_cell={'width': '100px', 'font-size': 'large'},
                    style_cell_conditional=[
                        {'if': {'row_index': r},
                         'backgroundColor': '#edee9c'
                        }  for r in dataframe[dataframe['Race']%2==0].index
                    ]
                ),
#             dcc.ConfirmDialog(
#                 id='confirm',
#                 message='Danger danger! Are you sure you want to continue?',
#             ),

#             dcc.Dropdown(
#                 options=[
#                     {'label': i, 'value': i}
#                     for i in ['Safe', 'Danger!!']
#                 ],
#                 id='dropdown'
#             ),
#             html.Div(id='output-confirm')
        ])
           ]


@app_ctb.callback(dash.dependencies.Output('container-button-basic1', 'children'),
                  [dash.dependencies.Input('buttonbet', 'n_clicks')])
def update1(n_clicks):
    if n_clicks: return dcc.Location(pathname="/bet", id="id2")

@app_ctb.callback(dash.dependencies.Output('container-button-basic2', 'children'),
                  [dash.dependencies.Input('buttonlogin', 'n_clicks')])
def update2(n_clicks):
    if n_clicks: return dcc.Location(pathname="/register", id="id2")

@app_ctb.callback(dash.dependencies.Output('container-button-basic3', 'children'),
                  [dash.dependencies.Input('buttonreport', 'n_clicks')])
def update3(n_clicks):
    if n_clicks: return dcc.Location(pathname="/reports", id="id2")

    
    
#     return [dcc.Link('Navigate to "/"', href='/hello')]
#     redirect("/dash2") 
#     flask.redirect('/dash1')
#     return f"number of {n_clicks}"

# @app_ctb.callback(dash.dependencies.Output('confirm', 'displayed'),
#               [dash.dependencies.Input('dropdown', 'value')])
# def display_confirm(value):
#     if value == 'Danger!!':
#         return True
#     return False


# @app_ctb.callback(dash.dependencies.Output('output-confirm', 'children'),
#               [dash.dependencies.Input('confirm', 'submit_n_clicks')])
# def update_output(submit_n_clicks):
#     if submit_n_clicks:
#         return f'It wasnt easy but we did it {submit_n_clicks}'
