import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_auth
from firebase import Firebase
import pandas as pd
import math as mt
import numpy as np


#######################connetserver#######################################

from firebase import Firebase

config = {
  "apiKey": "AIzaSyCX2_DpYpZBrRDQYXdvk9doAXJZq3yK5qI",
  "authDomain": "analistainmobiliario-1aa61.firebaseapp.com",
  "databaseURL": "https://analistainmobiliario-1aa61.firebaseio.com/",
  "storageBucket": "analistainmobiliario-1aa61.appspot.com",
  "serviceAccount": "serviceAccountKey.json"
}

firebase = Firebase(config)

#################################################################

db = firebase.database()
all_users = db.child("/flat/34").get()
Flat= all_users.val()

################### desencripte###########################

rama= list(Flat.keys())
Data= pd.DataFrame()
Data2= pd.DataFrame()
for i in range(0, len(rama)):
  if type(Flat[rama[i]]) == list:
    for ky1 in Flat[rama[i]]:
      if type(ky1) == dict:
        for ramax in ky1.keys():
          train= pd.DataFrame.from_dict(ky1[ramax], orient= 'index')
          train.reset_index(level=0, inplace=True)
          Data= pd.concat([Data, train], axis= 0)

      elif type(ky1) == list:
        for ky2 in Flat[rama[i]][0]:
          if ky2 != None:
            train= pd.DataFrame.from_dict(ky2, orient= 'index')
            train.reset_index(level=0, inplace=True)
            Data= pd.concat([Data, train], axis= 0)
            continue


  else: 
    ramax= list(Flat[rama[i]].keys())
  #print(i)
    for e in range(0, len(ramax)):
      lista= len(Flat[rama[i]][ramax[e]])
      
    #print(type(Flat[rama[i]][ramax[e]]))
      if type(Flat[rama[i]][ramax[e]]) == list:
        for n in range(0, lista):
          if Flat[rama[i]][ramax[e]][n] != None:
            train= pd.DataFrame.from_dict(Flat[rama[i]][ramax[e]][n], orient= 'index')
            train.reset_index(level=0, inplace=True)
            Data= pd.concat([Data, train], axis= 0)
            continue
          
          elif type(Flat[rama[i]][ramax[e]]) == dict:
            ramac= list(Flat[rama[i]][ramax[e]].keys())
            for n in ramac:
              train= pd.DataFrame.from_dict(Flat[rama[i]][ramax[e]][n], orient= 'index')
              train.reset_index(level=0, inplace=True)
              Data= pd.concat([Data, train], axis= 0)



######################depuration###################
Data1= Data.loc[:, ['Title', 'Code', 'District', 'Country', 'Rooms' ,'Floor', 'Size', 'Price', 'Year', 'Url']]
Data1['Size']= Data1['Size'].astype('float')
Data1['Price']= Data1['Price'].astype('float')
Data1['Year'] = Data1['Year'].astype('int')
Data1= Data1.reset_index()


########################other fork#####################

#db = firebase.database()
all_users = db.child('/geolocation/district/34').get()
#Flat= all_users.val()
location= all_users.val()

#location['1266895767912705']['179604184'].keys()

rama1= list(location.keys())

#names= []
for i in range(0, len(rama1)):
  if type(location[rama1[i]]) == dict:
    rama2= list(location[rama1[i]].keys())
    
    for e in range(0, len(rama2)):
      Data1.loc[Data1['District'] == \
                location[rama1[i]][rama2[e]]['DistrictCode'],'District'] = \
                location[rama1[i]][rama2[e]]['District']
    continue


########################## App Dash #####################################

VALID_USERNAME_PASSWORD_PAIRS = {
    'Analista': 'Aa12345'
}

#Data1= Data1[Data1['Year'] != 0]
District= Data1['District'].unique().tolist()
Rooms= Data1['Rooms'].unique().tolist()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app= dash.Dash(__name__, external_stylesheets= external_stylesheets)

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

server= app.server

app.layout= html.Div([
    html.H1("Real estate analysis"),
    html.Div([
               html.Label('District'), 
               dcc.Dropdown(
                   id= 'District', 
                   options= [{'label': name, 'value': name} for name in District], 
                   value= 'Las Arenas' )],
              style={'width': '20%', 'display': 'inline-block'}), 
     
     html.Div([
               html.Label('Rooms'), 
               dcc.Dropdown(
                   id= 'Rooms', 
                   options= [{'label': name, 'value': name} for name in Rooms], 
                   value= 'All' )], 
              style={'width': '20%', 'display': 'inline-block'}), 
     
     html.Div([
               html.Label('Size: '),
               dcc.Input(
                   id= 'Size', type= 'number', value= '0')], 
               style={'width': '20%', 'display': 'inline-block'}),

     html.Div([
               html.Label('Price: '),
               dcc.Input(
                   id= 'Price', type= 'number', value= '0')], 
               style={'width': '20%', 'display': 'inline-block'}),  
  

     dcc.Graph(id= 'Corr', 
               hoverData={'points': [{'hovertext': 'https://www.idealista.com/inmueble/91887867/'}]}),  

     html.Div([
               html.Label('Year'), 
               dcc.Slider(
                   id= 'Year_s', 
                   min= Data1['Year'].min(),
                   max= Data1['Year'].max(),
                   value= Data1['Year'].max(), 
                   marks= {str(year): str(year) for year in range(Data1.Year.min(), Data1.Year.max(), int(round(1+3.322+mt.log(Data1.shape[0]), 0))*4)},
                   step= None

               )]), 
     html.H3('Resumen: '),

     html.Div(id='text'), 

     html.Div(id= 'URL')

    ])

@app.callback(
    Output('URL', 'children'), 
    Input('Corr', 'hoverData')
)

def disp_hover_data(hover_data):
  #return hover_data
  #lk= hover_data['points'][0]['hovertext']
  
  return (html.A('Selection point link', href= hover_data['points'][0]['hovertext']))

#@app.callback(
#    Output('URL', 'children')
#)
#def resetHoverData():
#    return None

@app.callback(
    Output('Corr', 'figure'), 
    Input('District', 'value'), 
    Input('Rooms', 'value'), 
    Input('Year_s', 'value'), 
    Input('Price', 'value'), 
    Input('Size', 'value'))

def update_graph(District_T, Rooms_T, Year_T, Price_T, Size_T):

  Datap= Data1[Data1['Year'] != Year_T]
  #Datap= Datap[(Datap['District'] == District_T) | (Datap['Rooms'] == Rooms_T)]
  #fig= go.Figure()
  #fig.add_trace(px.scatter(x= Datap['Size'], y= Datap['Price'], color= 'District', trendline='ols', \
   #               marginal_y= 'violin', marginal_x= 'violin', template="plotly_dark"))
  

  fig= px.scatter(Datap[(Datap['District'] == District_T) | (Datap['Rooms'] == Rooms_T)], x= 'Size', y= 'Price', color= 'District',trendline='lowess',\
                  template="plotly_dark", hover_name= 'Url') 
  fig.add_scatter(x= [Size_T], y= [Price_T], name= 'Reference', fillcolor= '#F1F7F7', line_color= '#F1F7F7')
  #x= np.mean(Datap[(Datap['District'] == District_T)]['Size'])
  #marginal_y= 'violin', marginal_x= 'violin', 
  return fig

@app.callback(
    Output('text', 'children'), 
    Input('District', 'value'), 
    Input('Year_s', 'value'),
    Input('Size', 'value'), 
    Input('Price', 'value')
    )

def update_output(District_T, Year_T, Size_T, Price_T):
  Datap= Data1[Data1['Year'] != Year_T]
  x= round(np.mean(Datap[(Datap['District'] == District_T)]['Size']), 3)
  x2= round(np.mean(Datap[(Datap['District'] == District_T)]['Price']), 3)
  x3= x- float(Size_T)
  x4= x2- float(Price_T)
    #return f'El distrito es {District_t}'
  #return u'La media de {} en Tamaño es {} y en Precio es {}.'.format(District_T, x, x2), '\n La diferencia con respecto a la referencia en tamaño es de {} y en Precio es de {}'.format(x3, x4)
  return (html.P(["La media de {} en Tamaño es {} y en Precio es {}".format(District_T, x, x2),html.Br(),"La diferencia con respecto a la referencia en tamaño es de {} y en Precio es de {}".format(x3, x4)]))


#app.run_server(debug= False)

if __name__ == '__main__':
    app.run_server(debug=True)
    
