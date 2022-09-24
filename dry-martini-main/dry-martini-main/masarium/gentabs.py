import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
# from app import application as app
# from app import app
import re



def cell_style(value):
    COLORS = [
    {
        'background': '#333333',
        'text': 'rgb(255, 255, 255)'
    },
    {
        'background': '#FF336E',
        'text': 'rgb(30, 30, 30)'
    },
    {
        'background': '#fdcc8a',
        'text': 'rgb(30, 30, 30)'
    },
    {
        'background': '#fc8d59',
        'text': 'rgb(30, 30, 30)'
    },
    {
        'background': '#d7301f',
        'text': 'rgb(30, 30, 30)'
    },
    {
        'background': '#00FA9A',
        'text': 'rgb(30, 30, 30)'
    },
    ]

    regex_pattern = r' [0-9]+\.[0-9]+'
    p = re.compile(regex_pattern)

    style = {
            'backgroundColor': COLORS[2]['background'],
            'color': COLORS[2]['text'],
        }

    if len(value.split('/'))>2:
        if bool(p.search(value.split('/')[-5])):
#             chr(128128)
#             if (value.split('/')[0]=='死') & (float(p.search(value.split('/')[-2                                                                                                              ])[0]) >0):
            if (value.split('/')[0]==chr(128128)) & (float(p.search(value.split('/')[-5                                                                                                             ])[0]) >0):
                style = {
                    'backgroundColor': COLORS[1]['background'],
                    'color': COLORS[1]['text'],
                    'text-decoration': 'line-through',
                }
            elif float(p.search(value.split('/')[-5])[0]) >0:
                style = {
                    'backgroundColor': COLORS[1]['background'],
                    'color': COLORS[1]['text']
                }
            else:
                style = {
                        'backgroundColor': COLORS[2]['background'],
                        'color': COLORS[2]['text']
                    }
#         elif value.split('/')[0]=='死':
        elif value.split('/')[0]==chr(128128):
            style = {
                'backgroundColor': COLORS[0]['background'],
                'color': COLORS[0]['text'],
                'text-decoration': 'line-through',
            }

    return style
def generate_table(dataframe, max_rows=100):
    rows = []
    for i in range(min(len(dataframe), max_rows)):
        row = []
        for col in dataframe.columns:
            value = dataframe.iloc[i][col]
            style = cell_style(value)
            row.append(html.Td(value, style=style))
        rows.append(html.Tr(row))

    return [html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        rows)]
