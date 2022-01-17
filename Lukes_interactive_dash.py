import dash_auth
import dash
from dash import dcc
from dash import html
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

# Subset dataframe to show some specific columns in dash web app

#51.56569468252655, -0.40344721931807725, 67_Lynmouth_Dr_Ruislip_HA4_9BY_UK
lat_center = 53.34035434171382
long_center = -6.189352520464214
geo_coord_str = "Lat: " + str(lat_center) +", Long:" + str(long_center)

app = dash.Dash(external_stylesheets=['https://codepen.io/amyoshino/pen/jzXypZ.css'])
app.title = 'Open Street Map'

app.layout = html.Div(
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

if __name__ == '__main__':
    app.run_server(debug=True)