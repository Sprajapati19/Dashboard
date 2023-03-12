import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import brickschema
import pymysql as m
import plotly.express as px
import jupyter_dash as dash
import plotly.graph_objects as go
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Connecting mysql server
mydb = m.connect(host = "127.0.0.5", user = 'Sp9644', password = 'Sp@@9644', db = 'nac_building')

# Creating a graph
g = brickschema.Graph(load_brick_nightly = True)
# loading ontology
g.load_file(filename = "C:\\Users\\Shubham\\Documents\\MTech Project\\Knowledge Graph\\Compiled NAC All Floors.ttl")

# function to convert sparql result to dataframe
def sparql_to_df(bldg, q):
    result = bldg.query(q)
    df = pd.DataFrame.from_records(list(result))
    df = df.applymap(str)
    df.drop_duplicates(inplace=True)
    return df

# creaating function to get data from database
def get_data(tablename):
    sql = "SELECT * FROM `{}`".format(tablename)
    df = pd.read_sql(sql, mydb)
    return df

# Creating a dictionary to store all uuids in floor and zone wise
uuid_types_ahu = {}

# First for loop for floors
for i in range(1, 7):
    
    # Creating a dictionary to store all uuids in zone wise
    ahu_floors_uuids = {}
    
    # This second for loop for zones
    for j in range(1, 5):
        
        # This list will contains all ahu variables uuids
        ahu_zones_uuids = []
        
        # Query to get auto manual status uuid of AHU
        q1 = '''
        select ?manualautostsuuid where {
            ?manualautosts a brick:Manual_Auto_Status ;
                brick:isPointOf ?ahu;
                brick:timeseries [ brick:hasTimeseriesId ?manualautostsuuid ] .
            ?ahu a brick:AHU;
                rdfs:label "%s".
        }''' % (f"Floor {i} Zone {j} AHU")
        uuid_variable_1 = sparql_to_df(g, q1)
        
        # Query to get On off command uuid of AHU
        q2 = '''
        select ?onoffcmduuid where {
            ?onoffcmd a brick:On_Off_Command ;
                brick:isPointOf ?ahu;
                brick:timeseries [ brick:hasTimeseriesId ?onoffcmduuid ] .
            ?ahu a brick:AHU;
                rdfs:label "%s".
        }''' % (f"Floor {i} Zone {j} AHU")
        uuid_variable_2 = sparql_to_df(g, q2)
        
        # Query to get On off status uuid of AHU
        q3 = '''
        select ?onoffstsuuid where {
            ?onoffsts a brick:On_Off_Status ;
                brick:isPointOf ?ahu;
                brick:timeseries [ brick:hasTimeseriesId ?onoffstsuuid ] .
            ?ahu a brick:AHU;
                rdfs:label "%s".
        }''' % (f"Floor {i} Zone {j} AHU")
        uuid_variable_3 = sparql_to_df(g, q3)
        
        # Query to get filter status uuid of AHU
        q4 = '''
        select ?filterstsuuid where {
            ?filtersts a brick:Filter_Status ;
                brick:isPointOf ?ahu;
                brick:timeseries [ brick:hasTimeseriesId ?filterstsuuid ] .
            ?ahu a brick:AHU;
                rdfs:label "%s".
        }''' % (f"Floor {i} Zone {j} AHU")
        uuid_variable_4 = sparql_to_df(g, q4)
        
        # Query to get supply and return air temperature uuid of AHU
        q5 = '''
        select ?satuuid ?ratuuid where {
            ?sat a brick:Supply_Air_Temperature_Sensor ;
                brick:isPointOf ?ahu;
                brick:timeseries [ brick:hasTimeseriesId ?satuuid] .
            ?rat a brick:Return_Air_Temperature_Sensor ;
                brick:isPointOf ?ahu;
                brick:timeseries [ brick:hasTimeseriesId ?ratuuid ] .
            ?ahu a brick:AHU;
                rdfs:label "%s".
        }''' % (f"Floor {i} Zone {j} AHU")
        uuid_variable_5 = sparql_to_df(g, q5)
        
        # Query to get Chilled water control and actual valve position uuid of AHU
        q6 = '''
        select ?chwvpcuuid ?chwvpuuid where {
            ?chwvpc a brick:Valve_Position_Command ;
                brick:isPointOf ?ahu;
                brick:timeseries [ brick:hasTimeseriesId ?chwvpcuuid ] .
            ?chwvp a brick:Valve_Position_Sensor ;
                brick:isPointOf ?ahu;
                brick:timeseries [ brick:hasTimeseriesId ?chwvpuuid ] .
            ?ahu a brick:AHU;
                rdfs:label "%s".
        }''' % (f"Floor {i} Zone {j} AHU")
        uuid_variable_6 = sparql_to_df(g, q6)
        
        # Query to get Chilled water Entering and Leaving temperature uuid of AHU
        q7 = '''
        select ?chwstuuid ?chwrtuuid where {
            ?chwst a brick:Entering_Chilled_Water_Temperature_Sensor ;
                brick:isPointOf ?ahu;
                brick:timeseries [ brick:hasTimeseriesId ?chwstuuid ] .
            ?chwrt a brick:Leaving_Chilled_Water_Temperature_Sensor ;
                brick:isPointOf ?ahu;
                brick:timeseries [ brick:hasTimeseriesId ?chwrtuuid ] .
            ?ahu a brick:AHU;
                rdfs:label "%s".
        }''' % (f"Floor {i} Zone {j} AHU")
        uuid_variable_7 = sparql_to_df(g, q7)
        
        # Query to get Return air temperature setpoint uuid of AHU
        q8 = '''
        select ?ratspuuid where {
            ?ratsp a brick:Return_Air_Temperature_Setpoint ;
                brick:isPointOf ?ahu;
                brick:timeseries [ brick:hasTimeseriesId ?ratspuuid ] .
            ?ahu a brick:AHU;
                rdfs:label "%s".
        }''' % (f"Floor {i} Zone {j} AHU")
        uuid_variable_8 = sparql_to_df(g, q8)
        
        # Query to get Return air relative humidity uuid of AHU
        q9 = '''
        select ?rarhuuid where {
            ?rarh a brick:Relative_Humidity_Sensor ;
                brick:isPointOf ?ahu;
                brick:timeseries [ brick:hasTimeseriesId ?rarhuuid ] .
            ?ahu a brick:AHU;
                rdfs:label "%s".
        }''' % (f"Floor {i} Zone {j} AHU")
        uuid_variable_9 = sparql_to_df(g, q9)
        
        # Query to get Return air Co2 level uuid of AHU
        q10 = '''
        select ?raco2uuid where {
            ?raco2 a brick:CO2_Sensor ;
                brick:isPointOf ?ahu;
                brick:timeseries [ brick:hasTimeseriesId ?raco2uuid ] .
            ?ahu a brick:AHU;
                rdfs:label "%s".
        }''' % (f"Floor {i} Zone {j} AHU")
        uuid_variable_10 = sparql_to_df(g, q10)
        
        # Storing all the uuids into a list
        ahu_zones_uuids.append(uuid_variable_1)
        ahu_zones_uuids.append(uuid_variable_2)
        ahu_zones_uuids.append(uuid_variable_3)
        ahu_zones_uuids.append(uuid_variable_4)
        ahu_zones_uuids.append(uuid_variable_5)
        ahu_zones_uuids.append(uuid_variable_6)
        ahu_zones_uuids.append(uuid_variable_7)
        ahu_zones_uuids.append(uuid_variable_8)
        ahu_zones_uuids.append(uuid_variable_9)
        ahu_zones_uuids.append(uuid_variable_10)
        
        # Storing list of all uuids into a dictionary in zone wise
        ahu_floors_uuids[j] = ahu_zones_uuids
        
    # Storing dictionary of zone wise uuids list into a outside dictionary in floor wise
    uuid_types_ahu[i] = ahu_floors_uuids

ahu_dataset = {}
for i in range(1, 7):
    zonewise_ahu_dataset = []
    for j in range(1, 5):
        tname_query = (
            f"select table_name from information_schema.columns where column_name like '{uuid_types_ahu[i][j][4].values[0][0]}' order by table_name ;")
        table_name = pd.read_sql(tname_query, mydb)
        
        # getting data from database
        df = get_data(table_name.values[0][0])
        
        # modifying data details
        data = df.copy()
        data['Time'] = data['Date'] + " " + data['Time']
        data.drop('Date', axis=1, inplace=True)
        data['Time'] = pd.to_datetime(data['Time'])
        data = data.sort_values("Time",ascending=True)
        data = data.reset_index(drop = True)
        
        # Storing dataframes into a list 
        zonewise_ahu_dataset.append(data)
    
    # Storing dataframes into dictionary flooor wise
    ahu_dataset[i] = zonewise_ahu_dataset

# Details of VAV in each floor zonewise
vav_dropdown_options = {
                    1 : {1 : [k for k in range(1, 13+1)],
                        2 : [k for k in range(14, 21+1)],
                        3 : [k for k in range(22, 27+1)],
                        4 : [k for k in range(28, 37+1)]},
                    2 : {1 : [k for k in range(1, 13+1)],
                        2 : [k for k in range(14, 21+1)],
                        3 : [k for k in range(22, 28+1)],
                        4 : [k for k in range(29, 38+1)]},
                    3 : {1 : [k for k in range(1, 13+1)],
                        2 : [k for k in range(14, 21+1)],
                        3 : [k for k in range(22, 28+1)],
                        4 : [k for k in range(29, 35+1)]},
                    4 : {1 : [k for k in range(1, 13+1)],
                        2 : [k for k in range(14, 21+1)],
                        3 : [k for k in range(22, 28+1)],
                        4 : [k for k in range(29, 35+1)]},
                    5 : {1 : [k for k in range(1, 13+1)],
                        2 : [k for k in range(14, 22+1)],
                        3 : [k for k in range(23, 29+1)],
                        4 : [k for k in range(30, 39+1)]},
                    6 : {1 : [k for k in range(1, 13+1)],
                        2 : [k for k in range(14, 19+1)],
                        3 : [k for k in range(20, 26+1)],
                        4 : [k for k in range(27, 38+1)]},
}

uuid_types_vav = {}
for i in range(1, 7):
    vav_floors_uuids = {}
    for j in range(1, 5):
        vav_zones_uuids = []
        for k in vav_dropdown_options[i][j]:
            q = '''
            select ?dpsenuuid where {
            ?vav  a  brick:VAV;
                rdfs:label "%s";
                brick:hasPoint ?dpsen.
            ?dpsen a brick:Damper_Position_Sensor;
                brick:timeseries [brick:hasTimeseriesId ?dpsenuuid ] .
            }''' % (f'Floor {i} VAV {k}')
            uuid = sparql_to_df(g, q)
            vav_zones_uuids.append(uuid[0][0])
        vav_floors_uuids[j] = vav_zones_uuids
    uuid_types_vav[i] = vav_floors_uuids

vav_dataset = {}
for i in range(1, 7):
    zonewise_vav_dataset = []
    for j in range(1, 5):
        tname_query = (
            f"select table_name from information_schema.columns where column_name like '{uuid_types_vav[i][j][4]}' order by table_name ;")
        table_name = pd.read_sql(tname_query, mydb)
        # getting data from database
        df = get_data(table_name.values[0][0])
        
        # modifying data details
        data = df.copy()
        data['Time'] = data['Date'] + " " + data['Time']
        data.drop('Date', axis=1, inplace=True)
        data['Time'] = pd.to_datetime(data['Time'])
        data = data.sort_values("Time",ascending=True)
        data = data.reset_index(drop = True)
        
        # Storing dataframes into a list 
        zonewise_vav_dataset.append(data)
    
    # Storing dataframes into dictionary flooor wise
    vav_dataset[i] = zonewise_vav_dataset

floor_dropdown_options = [
    {'label': 'Floor 1', 'value': 'Floor 1'},
    {'label': 'Floor 2', 'value': 'Floor 2'},
    {'label': 'Floor 3', 'value': 'Floor 3'},
    {'label': 'Floor 4', 'value': 'Floor 4'},
    {'label': 'Floor 5', 'value': 'Floor 5'},
    {'label': 'Floor 6', 'value': 'Floor 6'}]

zone_dropdown_options = [
    {'label': 'Zone 1', 'value': 'Zone 1'},
    {'label': 'Zone 2', 'value': 'Zone 2'},
    {'label': 'Zone 3', 'value': 'Zone 3'},
    {'label': 'Zone 4', 'value': 'Zone 4'}]

ahu_dropdown_options = ['Auto-Manual Status', 'On-Off Command', 'On-Off Status', 'Filter Status', 
                        'Supply and Return Air Temperature', 'Water Supply Control and Actual Valve Position', 
                        'Water Entering and Leaving Temperature', 'Return Air Temperature Setpoint',
                        'Return Air Relative Humidity', 'Return Air Co2 Level']

y_axis_title_ahu = ['0 - Off & 1 - On', '0 - Off & 1 - On', '0 - Off & 1 - On', '0 - Off & 1 - On',
                    f'Temperature ({chr(176)}C)', 'Valve Position (% Open)', f'Temperature ({chr(176)}C)',
                    'Return Air Temperature Setpoint', 'Return Air Relative Humidity (%)', 'Return Air Co2 Level (ppm)']

# Creating dash app server and layout

app = dash.JupyterDash(__name__)
app.layout = html.Div(
    children=[
        
#         This Div section is for heading design
        html.Div(
            children = [
                html.H1(
                    children=("HVAC System"),
                    style = {
                        'color': '#FFFFFF',
                        'margin' : '0 auto',
                        'textAlign' : 'center',
                        'font-size':'100px'}
                ),
                html.P(
                    children = ("NAC Building, IIT Madras, Chennai, Tamil Nadu 600036"),
                    style = {
                        'color': '#FFFFFF',
                        'margin' : '8px auto',
                        'textAlign' : 'center',
                        'font-size':'35px'}
                )
            ],
            style = {
                'background-color': '#1F3F49',
                'height': '200px',
                'padding': '16px 0 0 0'
            }
        ),
        
#         This Div section includes the selecting of dropdowns i.e. floor, zone date etc.
        html.Div(
            children = [
#                 Floor dropdown design
                html.Div(
                    children = [
                        html.P(
                            children = 'Floor',
                            style = {
                                'margin-bottom': '6px',
                                'font-weight': 'bold',
                                'color': '#036656'}
                        ),
                        dcc.Dropdown(
                            id = 'Floor',
                            options = floor_dropdown_options,
                            value = 'Floor 1',
                            clearable = False,
                            searchable = False,
                            style = {
                                'height' : '30px',
                                'width' : '96px'
                            }
                        )
                    ]
                ),
#                 Zone dropdown design
                html.Div(
                    children = [
                        html.P(
                            children = 'Zone',
                            style = {
                                'margin-bottom': '6px',
                                'font-weight': 'bold',
                                'color': '#036656'}
                        ),
                        dcc.Dropdown(
                            id = 'Zone',
                            options = zone_dropdown_options,
                            value = 'Zone 1',
                            clearable = False,
                            searchable = False,
                            style = {
                                'height' : '30px',
                                'width' : '96px'
                            }
                        )
                    ]
                ),
                
#                 AHU or VAV selection dropdown
                html.Div(
                    children = [
                        html.P(
                            children = 'AHU or VAV',
                            style = {
                                'margin-bottom': '6px',
                                'font-weight': 'bold',
                                'color': '#036656'}
                        ),
                        dcc.Dropdown(
                            id = 'AHU or VAV',
                            options = [
                                {'label':variable, 'value':variable}
                                for variable in ["AHU Variables", "VAV Variables"]
                            ],
                            value = 'AHU Variables',
                            clearable = False,
                            searchable = False,
                            style = {
                                'height' : '30px',
                                'width' : '250px'
                            }
                        )
                    ]
                ),
                
#                 Variable Selection
                html.Div(
                    children = [
                        html.P(
                            children = 'Variable',
                            style = {
                                'margin-bottom': '6px',
                                'font-weight': 'bold',
                                'color': '#036656'}
                        ),
                        dcc.Dropdown(
                            id = 'variable type',
                            clearable = False,
                            searchable = False,
                            value = 'Supply and Return Air Temperature',
                            style = {
                                'height' : '30px',
                                'width' : '250px'
                            }
                        )
                    ]
                ),
                
#                 Putting a date range section to data details
                html.Div(
                    children = [
                        html.P(
                            children = 'Date Range',
                            style = {
                                'margin-bottom': '6px',
                                'font-weight': 'bold',
                                'color': '#036656'}
                        ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed = ahu_dataset[1][0]["Time"].min(),
                            max_date_allowed = ahu_dataset[1][0]["Time"].max(),
                            start_date = ahu_dataset[1][0]["Time"].min(),
                            end_date = ahu_dataset[1][0]["Time"].max(),
                        )
                    ]
                )
                
            ],
            style = {
                'height': '112px',
                'width': '1500px',
                'display': 'flex',
                'justify-content': 'space-evenly',
                'padding-top': 'auto',
                'margin': '10px auto',
                'background-color': '#F4F5F8',
                'box-shadow': '0 0 10px 5px rgba(0, 0, 255, 0.25)'
            }
        ),
        html.Div(
            children = [
                html.Div(
                    children = dcc.Graph(
                        id = 'plot'
                    ),
                    style = {
                        'margin-bottom': '24px',
                        'box-shadow' : '0 0 10px 5px rgba(0, 0, 255, 0.25)',
                    }
                )
            ],
            style = {
                'height' : '600px',
                'width': '1200px',
                'margin-right': 'auto',
                'margin-left': 'auto',
                'padding-right': '5px',
                'padding-left': '5px',
                'padding-top': '10px',
                'padding-bottom': '5px',
                'margin-top': '32px'
            }
        )
    ],
    style = {
        'background-color': '#F4F9FA',
            }
)

@app.callback(
    Output('variable type', 'options'),
    [Input('AHU or VAV', 'value'),
    Input('Floor', 'value'),
     Input('Zone', 'value')]
)
def update_date_dropdown(name, floor, zone):
    if name == 'AHU Variables':
        dict_values = ['Auto-Manual Status', 'On-Off Command', 'On-Off Status', 'Filter Status',
                       'Supply and Return Air Temperature', 'Water Supply Control and Actual Valve Position',
                       'Water Entering and Leaving Temperature', 'Return Air Temperature Setpoint',
                       'Return Air Relative Humidity', 'Return Air Co2 Level']
        return [{'label': i, 'value': i} for i in dict_values]
    else :
        for i in range(1, 7):
            for j in range(1, 5):
                if floor == f"Floor {i}" and zone == f"Zone {j}":
                    return [{'label': "VAV " + str(k) + " Damper Position", 'value': k} for k in vav_dropdown_options[i][j]]
                    
# Defining a callback to autoselect first variable                    
@app.callback(
    Output('variable type', 'value'),
    [Input('AHU or VAV', 'value'),
     Input('variable type', 'options')]
)
def update_value(ahu_or_vav, options):
    if ahu_or_vav == "AHU Variables":
        return options[4]['value']
    else:
        return options[0]['value']
                    
# Define the callback function to update the graph based on the selected dropdown option
@app.callback(
    Output('plot', 'figure'),
    [Input('Floor', 'value'),
     Input('Zone', 'value'),
    Input('AHU or VAV', 'value'),
    Input('variable type', 'value'),
    Input(component_id ='date-range', component_property= 'start_date'),
    Input(component_id = 'date-range', component_property = 'end_date')])
def update_graph(floor, zone, ahu_or_vav, variable_type, start_date, end_date):
    
#     for loop for all six floors
    for i in range(1, 7):
        
#         for to cover all 4 zones of each floor
        for j in range(1, 5):
            
#             This if statement is for AHU Variables
            if ahu_or_vav == 'AHU Variables':
                for k in range(len(ahu_dropdown_options)):
                    
#                     This if statement is for ahu double line plots in single plot
                    if k >= 4 and k <= 6:
                        if floor == f'Floor {i}' and zone == f'Zone {j}' and variable_type == ahu_dropdown_options[k]:
                            
#                             Storing dataset as filtered data
                            filtered_data = ahu_dataset[i][j-1].query("Time >= @start_date and Time <= @end_date")
                            
#                             Checking if data available or not
                            if (uuid_types_ahu[i][j][k][0][0] not in filtered_data.columns or uuid_types_ahu[i][j][k][1][0] not in filtered_data.columns):
                                Value_figure = {
                                "layout": {
                                    'title': {'font': {'color': 'red',
                                                       'size' : 25,
                                                       'family': 'Times New Roman'},
                                              'yanchor' : 'bottom',
                                              'y' : 0.925,
                                              'xanchor' : 'center',
                                              'x' : 0.5,
                                              'bgcolor' : 'red',
                                              'text': f"Data is not available for this 'Floor {i} Zone {j} AHU' Variable!!"},
                                    },
                                }
                            else :
                                Value_figure = {
                                    "data": [
                                        {
                                            'hovertemplate': 'Time=%{x}<br>value=%{y}<extra></extra>',
                                            "x": filtered_data["Time"],
                                            "y": filtered_data[uuid_types_ahu[i][j][k][0][0]],
                                            "mode": "scatter",
                                            "name" : uuid_types_ahu[i][j][k][0][0]
                                        },
                                        {
                                            'hovertemplate': 'Time=%{x}<br>value=%{y}<extra></extra>',
                                            "x": filtered_data["Time"],
                                            "y": filtered_data[uuid_types_ahu[i][j][k][1][0]],
                                            "mode": "scatter",
                                            "name" : uuid_types_ahu[i][j][k][1][0]
                                        },
                                    ],
                                    "layout": {
                                        'xaxis':{
                                            'fixedrange':True,
                                            'mirror':True,
                                            'ticks':'outside',
                                            'showline':True,
                                            'title' : {'text':"Date"}
                                            },
                                        'yaxis':{
                                            'zeroline' : False,
                                            'fixedrange':True,
                                            'mirror':True,
                                            'ticks':'outside',
                                            'showline':True,
                                            'title' : y_axis_title_ahu[k]
                                            },
                                        "margin" : {"pad":0},
                                        "legend" : {"yanchor":"bottom",
                                                   "y" : 1.05,
                                                   "xanchor" : 'left',
                                                   "x" : 0,
                                                   "orientation" : 'h'},
                                        'title': {'font': {'color': 'black',
                                                           'size' : 20,
                                                           'family': 'Times New Roman'},
                                                  'yanchor' : 'bottom',
                                                  'y' : 0.91,
                                                  'xanchor' : 'center',
                                                  'x' : 0.5,
                                                  'text': floor + ' ' + zone + ' ' + ahu_dropdown_options[k]
                                        },
                                    },
                                }
                                
                            
#                     This else statement is for ahu single variable plots
                    else :
                        if floor == f'Floor {i}' and zone == f'Zone {j}' and variable_type == ahu_dropdown_options[k]:
                            
#                             Saving dataset as filtered data after filtering date details
                            filtered_data = ahu_dataset[i][j-1].query("Time >= @start_date and Time <= @end_date")
        
#                             Checking if data available or not
                            if uuid_types_ahu[i][j][k][0][0] not in filtered_data.columns:
                                Value_figure = {
                                "layout": {
                                    'title': {'font': {'color': 'red',
                                                       'size' : 25,
                                                       'family': 'Times New Roman'},
                                              'yanchor' : 'bottom',
                                              'y' : 0.925,
                                              'xanchor' : 'center',
                                              'x' : 0.5,
                                              'bgcolor' : 'red',
                                              'text': f"Data is not available for this 'Floor {i} Zone {j} AHU' Variable!!"},
                                    },
                                }
                            else :
                                Value_figure = {
                                    "data": [
                                        {
                                            'hovertemplate': 'Time=%{x}<br>value=%{y}<extra></extra>',
                                            "x": filtered_data["Time"],
                                            "y": filtered_data[uuid_types_ahu[i][j][k][0][0]],
                                            "mode": "lines"
                                        },
                                    ],
                                    "layout": {
                                        'xaxis':{
                                            'fixedrange':True,
                                            'mirror':True,
                                            'ticks':'outside',
                                            'showline':True,
                                            'title' : {'text':"Date"}
                                            },
                                        'yaxis':{
                                            'zeroline':False,
                                            'fixedrange':True,
                                            'mirror':True,
                                            'ticks':'outside',
                                            'showline':True,
                                            'title' : y_axis_title_ahu[k]
                                            },
                                        "margin" : {"pad":0},
                                        'title': {
                                            'font': {'color': 'black',
                                                     'size' : 20,
                                                     'family': 'Times New Roman'},
                                            'yanchor' : 'bottom',
                                            'y' : 0.875,
                                            'xanchor' : 'center',
                                            'x' : 0.5,
                                            'text': floor + ' ' + zone + ' ' + ahu_dropdown_options[k]
                                        },
                                    },
                                }
                        
#             This elif statement is for VAV Variables
            elif ahu_or_vav == "VAV Variables":
                for k in range(len(uuid_types_vav[i][j])):
                    if floor == f'Floor {i}' and zone == f'Zone {j}' and variable_type == vav_dropdown_options[i][j][k]:
                        filtered_data_vav = vav_dataset[i][j-1].query(
                                "Time >= @start_date and Time <= @end_date")
                        
                        if type(filtered_data_vav[uuid_types_vav[i][j][k]].values[0]) == str:
                            Value_figure = {
                                "layout": {
                                    'title': {'font': {'color': 'red',
                                                       'size' : 25,
                                                       'family': 'Times New Roman'},
                                              'yanchor' : 'bottom',
                                              'y' : 0.925,
                                              'xanchor' : 'center',
                                              'x' : 0.5,
                                              'bgcolor' : 'red',
                                              'text': "Data is not available for this VAV Damper position!!"},
                                    },
                                }
                        
                        else:
                        
                            Value_figure = {
                                "data": [
                                    {
                                        'hovertemplate': 'Time=%{x}<br>value=%{y}<extra></extra>',
                                        "x": filtered_data_vav["Time"],
                                        "y": filtered_data_vav[uuid_types_vav[i][j][k]],
                                        "mode": "lines"
                                    },
                                ],
                                "layout": {
                                    'xaxis':{'mirror':True,
                                             'ticks':'outside',
                                             'showline':True,
                                             'title' : {'text':"Date"}
                                            },
                                    'yaxis':{'fixedrange':True,
                                             'zeroline':False,
                                             'range':[-5, 105],
                                             'mirror':True,
                                             'ticks':'outside',
                                             'showline':True,
                                             'title' : {'text':"Damper Position (% Open)"}
                                            },
                                    "margin" : {"pad":0},
                                    'title': {'font': {'color': 'black',
                                                       'size' : 20,
                                                       'family': 'Times New Roman'},
                                              'yanchor' : 'bottom',
                                              'y' : 0.875,
                                              'xanchor' : 'center',
                                              'x' : 0.5,
                                              'text': floor + ' ' + 'VAV ' + str(vav_dropdown_options[i][j][k]) + ' Damper Position'},
                                    },
                                }     
    return Value_figure

if __name__ == '__main__':
    app.run_server(debug=True, port = 8052)