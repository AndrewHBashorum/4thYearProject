import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import dash_auth
import dash

from dash.dependencies import Input, Output, State
import plotly.graph_objs as go

from houses_utils import geo_locate_houses_alt

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

USERNAME_PASSWORD_PAIRS = [
    ['JamesBond', '007'], ['LouisArmstrong', 'satchmo']
]




app = dash.Dash()
auth = dash_auth.BasicAuth(app,USERNAME_PASSWORD_PAIRS)
server = app.server


df = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/'
    'cb5392c35661370d95f300086accea51/raw/'
    '8e0768211f6b747c0db42a9ce9a0937dafcbd8b2/'
    'indicators.csv')

lat_center = 53.34035434171382
long_center = -6.189352520464214
geo_coord_str = "Lat: " + str(lat_center) +", Long:" + str(long_center)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


index_page = html.Div([
    dcc.Link('Go to Page 1', href='/page-1'),
    html.Br(),
    dcc.Link('Go to Page 2', href='/page-2'),
])




available_indicators = df['Indicator Name'].unique()


finderLayout = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Fertility rate, total (births per woman)'
            ),
            dcc.RadioItems(
                id='xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Life expectancy at birth, total (years)'
            ),
            dcc.RadioItems(
                id='yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic'),

    dcc.Slider(
        id='year--slider',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=df['Year'].max(),
        step=None,
        marks={str(year): str(year) for year in df['Year'].unique()}
    )
], style={'padding':10})

@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('xaxis-column', 'value'),
     Input('yaxis-column', 'value'),
     Input('xaxis-type', 'value'),
     Input('yaxis-type', 'value'),
     Input('year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name: object,
                 xaxis_type, yaxis_type,
                 year_value):
    dff = df[df['Year'] == year_value]
    return {
        'data': [go.Scatter(
            x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
            y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
            text=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }


mapLayout = html.Div(
    html.Div([
        html.H1(children='Load Map from Address'),
        html.H3('Enter address: (67 Lynmouth Drive Ruislip HA4 9BY)', style={'paddingRight': '30px'}),
        dcc.Input(id="input_address", type="text", placeholder="",
                  style={'paddingRight': '30px', 'width': 500}),
        html.Button(id='submit_button', n_clicks=0, children='Submit'),
        html.Div(id='print_info', children='hello'),

        html.Hr(),
        html.H3('Latitude and Longitude of House:', style={'paddingRight': '30px'}),
        html.H3(id='coords', children=geo_coord_str),

        html.Hr(),
        dcc.Graph(id='MapPlot1', figure={
            "data": [{"type": "scattermapbox", "lat": [lat_center], "lon": [long_center],
                    "hoverinfo": "text", "hovertext": 'Test',
                    "mode": "markers", "name": 'Shanes house',
                    "marker": {"size": 15, "opacity": 0.7, "color": '#F70F0F'}}],
            "layout": dict(autosize=True, height=500, width=500,
                font=dict(color="#191A1A"), titlefont=dict(color="#191A1A", size='14'),
                margin=dict(l=10, r=10, b=10, t=10), hovermode="closest",
                plot_bgcolor='#fffcfc', paper_bgcolor='#fffcfc',
                legend=dict(font=dict(size=10), orientation='h'),
                mapbox=dict(style="open-street-map", center=dict(lon=long_center, lat=lat_center), zoom=18)
                )}),

        html.Hr(),
        dcc.Graph(id='MapPlot2', figure={
            "data": [{"type": "scattermapbox", "lat": [lat_center], "lon": [long_center],
                      "hoverinfo": "text", "hovertext": 'Test',
                      "mode": "markers", "name": 'Shanes house',
                      "marker": {"size": 15, "opacity": 0.7, "color": '#F70F0F'}}],
            "layout": dict(autosize=True, height=500, width=500,
                           font=dict(color="#191A1A"), titlefont=dict(color="#191A1A", size='14'),
                           margin=dict(l=10, r=10, b=10, t=10), hovermode="closest",
                           plot_bgcolor='#fffcfc', paper_bgcolor='#fffcfc',
                           legend=dict(font=dict(size=10), orientation='h'),
                           mapbox=dict(style="open-street-map", center=dict(lon=long_center, lat=lat_center), zoom=18)
                           )})
    ])
)

@app.callback(
    Output('print_info', 'children'),
    [Input('submit_button', 'n_clicks')],
    [State('input_address', 'value')])
def geolocate_address(n_clicks, input_value):
    if input_value is not None:
        global long_center
        global lat_center
        id_house, house_number, postcode, xt, yt, long_center, lat_center = geo_locate_houses_alt(input_value)
        return 'House id: "{}", House number: "{}", Postcode: "{}", xt: "{}", yt: "{}", xd: "{}", yd: "{}"'.format(id_house, house_number, postcode, xt, yt, long_center, lat_center)

@app.callback(
    Output('coords', 'children'),
    [Input('print_info', 'children')])
def update_lat_long_div(value):
    return "latitude: " + str(lat_center) + ", longitude:" + str(long_center)

@app.callback(
    Output('MapPlot1', 'figure'),
    [Input('print_info', 'children')])
def update_map1(value):
    figure={
        "data": [{"type": "scattermapbox", "lat": [lat_center], "lon": [long_center],
            "hoverinfo": "text", "hovertext": 'Test',
            "mode": "markers", "name": 'Shanes house',
            "marker": {"size": 15, "opacity": 0.7, "color": '#F70F0F'}}],
        "layout": dict(autosize=True, height=500, width=500,
            font=dict(color="#191A1A"), titlefont=dict(color="#191A1A", size='14'),
            margin=dict(l=10, r=10, b=10, t=10), hovermode="closest",
            plot_bgcolor='#fffcfc', paper_bgcolor='#fffcfc',
            legend=dict(font=dict(size=10), orientation='h'),
            mapbox=dict(style="open-street-map", center=dict(lon=long_center, lat=lat_center), zoom=18)
            )}
    return figure

@app.callback(
    Output('MapPlot2', 'figure'),
    [Input('print_info', 'children')])
def update_map2(value):
    figure={
        "data": [{"type": "scattermapbox", "lat": [lat_center], "lon": [long_center],
            "hoverinfo": "text", "hovertext": 'Test',
            "mode": "markers+lines", "name": 'Shanes house',
            "marker": {"size": 15, "opacity": 0.7, "color": '#F70F0F'}}],
        "layout": dict(autosize=True, height=500, width=500,
            font=dict(color="#191A1A"), titlefont=dict(color="#191A1A", size='14'),
            margin=dict(l=10, r=10, b=10, t=10), hovermode="closest",
            plot_bgcolor='#fffcfc', paper_bgcolor='#fffcfc',
            legend=dict(font=dict(size=10), orientation='h'),
            mapbox=dict(style="open-street-map", center=dict(lon=long_center, lat=lat_center), zoom=18)
            )}
    box_x = [long_center - 0.001, long_center + 0.001, long_center + 0.001, long_center - 0.001]
    box_y = [lat_center - 0.001, lat_center - 0.001, lat_center + 0.001, lat_center + 0.001]
    figure.add_trace(go.Scattermapbox(
        mode="markers+lines",
        lon=box_x,
        lat=box_y,
        marker={'size': 10}))
    return figure

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])



def display_page(pathname):
    if pathname == '/page-1':
        return finderLayout
    elif pathname == '/page-2':
        return mapLayout
    else:
        return index_page

if __name__ == '__main__':
    app.run_server()
