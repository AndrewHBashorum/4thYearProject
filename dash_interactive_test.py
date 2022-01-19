import base64
import os
import pickle
from pathlib import Path

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import ssl
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import ssl

from site_finder import SiteFinder

ssl._create_default_https_context = ssl._create_unverified_context
import dash_auth
import dash

from dash.dependencies import Input, Output, State
import plotly.graph_objs as go

from houses_utils import geo_locate_houses_alt, find_id

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)
home = Path.home()
USERNAME_PASSWORD_PAIRS = [
    ['JamesBond', '007'], ['LouisArmstrong', 'satchmo']
]
ssl._create_default_https_context = ssl._create_unverified_context


def makePathFromInfoAndAddress(addressOrg, info = None):
    # / Users / andrewbashorm / Dropbox / auto_processing / aerial_images / BemptonDriveOdd / aerial_59_HA4_9DB.png
    #67 Lynmouth Drive Ruislip HA4 9BY
    address = addressOrg.split(' ')
    key = address[1] + address[2]

    if int(address[0]) % 2 == 0:
        key += 'Even'
    else:
        key += 'Odd'
        if 'ver' in address[1]:
            if int(address[0]) > 178:
                key += 'B'
            elif int(address[0]) < 178:
                key += 'A'
    id,num,postcode = find_id(addressOrg)
    path = str(home) + '/Dropbox/auto_processing/aerial_images/' + key + '/aerial_' + id + '.png'

    return path, key, id


def getPickleFiles(streetKeys):

    with open(str(home)+ '/Dropbox/auto_processing/pickle_files/' + streetKeys + '4.pickle', 'rb') as f:
            loadedDict = pickle.load(f)
    return loadedDict['house_dict']

def encode_image(image_file):
    encoded = base64.b64encode(open(image_file, 'rb').read())
    return 'data:image/png;base64,{}'.format(encoded.decode())

streetKeys = ['BemptonDriveOdd', 'LynmouthDriveEven','LynmouthDriveOdd','BemptonDriveEven','BeverleyRoadOddA','BeverleyRoadOddB','BeverleyRoadEven']
graphOptions = ['Height Data', 'Aerial','Street']

app = dash.Dash()
auth = dash_auth.BasicAuth(app,USERNAME_PASSWORD_PAIRS)
server = app.server
visibility_state = 'on'

lat_center = 53.34035434171382
long_center = -6.189352520464214
geo_coord_str = "Lat: " + str(lat_center) +", Long:" + str(long_center)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = dash.Dash(__name__,  external_stylesheets=external_stylesheets)


finderLayout = html.Div([

    html.Div([

    # dcc.Link('Go to Index page', href='/index_page'),
    html.Br(),
        html.Div([
            dcc.Dropdown(
                id='street_choice',
                options=[{'label': i, 'value': i} for i in streetKeys],
                value='Steet Side'
            ),

        ],
        style={'width': '20%', 'display': 'inline-block'}),

        html.Div([

        ], id='bb',style={'width': '20%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='house_choice',
                value='House'
            ),
        ],style={'width': '20%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='graph_choice',
                options=[{'label': i, 'value': i} for i in graphOptions],
                value='House'
            ),
        ], style={'width': '20%', 'float': 'right', 'display': 'inline-block'}),
        html.Hr(),
        html.Div([
            html.Img(id='display_image', src='children'),
            html.Img(id='display_imageMap', src='children')
        ],style={'float': 'centre', 'display': 'inline-block'} )

    ],
    ),
], style={'padding':10})




@app.callback(
    Output('house_choice', 'options'),
    Input('street_choice', 'value'))
def findHouseOptions(selected_street):
    print(selected_street)
    house_keys = getPickleFiles(selected_street)
    return [{'label': i, 'value': i} for i in house_keys.keys()]


@app.callback(
    Output('display_image', 'src'),
    [Input('house_choice', 'value'),
    Input('street_choice', 'value')],
    Input('graph_choice', 'value'))
def findHouseOptions2(selected_house, selected_street, selected_image):
    path = str(home) +'/Dropbox/auto_processing/'
    # / Users / andrewbashorm / Dropbox / auto_processing / aerial_images / BemptonDriveOdd / aerial_59_HA4_9DB.png
    if selected_image == 'Aerial':
       path += 'aerial_images/' + selected_street + '/aerial_' + selected_house + '.png'

    if selected_image == 'Height Data':
        path += 'height_data_images/' + selected_street + '/height_' + selected_house + '.png'

    return encode_image(path)

@app.callback(
    Output('display_imageMap', 'src'),
    [Input('street', 'value'),
     Input('houseID', 'value'),
     Input('graph_choice', 'value')])

def findHouseOptionsFromMap(selected_street,selected_house,selected_image ):
    path = str(home) +'/Dropbox/auto_processing/'
    # / Users / andrewbashorm / Dropbox / auto_processing / aerial_images / BemptonDriveOdd / aerial_59_HA4_9DB.png

    if selected_image == 'Aerial':
        path += 'aerial_images/' + selected_street + '/aerial_' + selected_house + '.png'

    if selected_image == 'Height Data':
        path += 'height_data_images/' + selected_street + '/height_' + selected_house + '.png'

    return encode_image(path)

mapLayout = html.Div(
    html.Div([
        #dcc.Link('Go to Index page', href='/index_page'),
        html.H1(children='Load Map from Address', id='maph1'),
        html.H3('Enter address: (67 Lynmouth Drive Ruislip HA4 9BY)', style={'paddingRight': '30px'}),
        dcc.Input(id="input_address", type="text", placeholder="",
                  style={'paddingRight': '30px', 'width': 500}),
        html.Button(id='submit_button', n_clicks=0, children='Submit'),
        html.Button(id='Generate_button', n_clicks=0, children='Generate'),
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
    Output('houseID', 'value'),
     [Input('input_address', 'value')])
def get_houseID(address):

    path, key, id = makePathFromInfoAndAddress(address)
    if os.path.exists(path):

        return id
    else:

        pass

@app.callback(
    Output('street', 'value'),
     Input('input_address', 'value'))
def check_if_house_is_input_else_display(address):

    path, key, id = makePathFromInfoAndAddress(address)
    if os.path.exists(path):
        return key
    else:
        pass

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


@app.callback(
    Output('maph1', 'children'),
    [Input('gg', 'value')])
def update_map2(value):
    return value

app.layout = html.Div([
    #dcc.Location(id='url', refresh=False),
    #dcc.Store(id='session', storage_type='session'),
    dcc.Store(id='path'),
    dcc.Store(id='temp'),
    dcc.Store(id='street'),
    dcc.Store(id='houseID'),
    dcc.Tabs(id="tabs-example-graph", value='tab-1-example-graph', children=[
        dcc.Tab(label='Map View', value='tab-1-example-graph', children=
                mapLayout),
        dcc.Tab(label='Graph View', value='tab-2-example-graph',children=
                finderLayout),
    ]),
    html.Div(id='page-content')
])
#
@app.callback(
   Output(component_id='display_imageMap', component_property='style'),
   [Input(component_id='street_choice', component_property='value')])
def show_hide_element(houseID):

    if houseID:
        return {'display': 'none'}
    else:
        return {'display': 'block'}
#sf = SiteFinder(pickle_file_folder, excel_file_folder)
#sf.main(4, pickle_file ,house_address)


@app.callback(Output('temp', 'value'),
    [Input('Generate_button', 'n_clicks')],
    [State('input_address', 'value')])
def get_houseID(n_clicks,address):

    sf = SiteFinder()
    sf.main(4 ,house_address=address)


# @app.callback(
#     Output(component_id='display_image', component_property='style'),
#     [Input(component_id='street_choice', component_property='value')])
# def show_hide_element(houseID):
#     if houseID:
#         return {'display': 'block'}
#     else:
#         return {'display': 'none'}
#
#
# @app.callback(
#     Output(component_id='display_image', component_property='style'),
#     [Input(component_id='house_choice', component_property='value')])
# def show_hide_element(houseID):
#     if houseID:
#         return {'display': 'block'}
#     else:
#         return {'display': 'none'}



# @app.callback(dash.dependencies.Output('page-content', 'children'),
#               dash.dependencies.Input('tabs-example-graph', 'value'))
# def render_content(tab):
#     print('lol')
#     if tab == 'tab-1-example-graph':
#         return finderLayout
#     elif tab == 'tab-2-example-graph':
#         return html.div('lol')
#     else:
#         return html.div('lol')
#



# @app.callback(dash.dependencies.Output('page-content', 'children'),
#               [dash.dependencies.Input('url', 'pathname')])
# def display_page(pathname):
#     if pathname == '/page-1':
#         return finderLayout
#     elif pathname == '/page-2':
#         return mapLayout
#     else:
#         return index_page




if __name__ == '__main__':
    app.run_server(debug=True)

