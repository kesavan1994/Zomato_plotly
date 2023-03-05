import pandas as pd
from plotly.subplots import make_subplots
import plotly.express as px 
import plotly.graph_objects as go
fig=go.Figure()
import dash

from dash import Dash, dcc, Input, Output,ctx
import dash_html_components as html
import dash_bootstrap_components as dbc

#Zomato CSV File Path
zomato=pd.read_csv('zomato.csv')

#Country dropdown dta
options=[]
for col in zomato['Country'].unique():
            options.append({'label':'{}'.format(col, col), 'value':col})
            
            
            
tap_style={'margin-bottom':'10px','padding':'5px','margin':'10px','color':'black','font-size':'20px'} 
           
app = dash.Dash("__name__",prevent_initial_callbacks=True, suppress_callback_exceptions=True)
server= app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=True),
    #html.Img(src=r"\Users\91909\Downloads\Ayyappa_Swamy.jpg"),
    html.Div(id='page-content')
],style={'background-color':'#94618E',})

#home page
index_page = html.Div(children=[

     
    html.Div( style={'background-color':'#94618E','height':'30px'},children=[
    dcc.Link('Home', href='/home',style=tap_style),
    dcc.Link('Country', href='/page-1',style=
             tap_style),
    dcc.Link('City', href='/page-2',style=tap_style),

   ]),
    
    html.Div(children=[
        dcc.Graph(id='graph9',style={'width':'900px','margin-left':'100px','margin-top':'30px','padding':'70px'})
        
        ])
    
],id='index',style={'background-color':'#94618E'})    

#country Page
page_1_layout = html.Div(children=[
    html.Div( style={'background-color':'#94618E','height':'30px'},children=[
    dcc.Link('Home', href='/home',style=tap_style),
    dcc.Link('Country', href='/page-1',style= tap_style),
    dcc.Link('City', href='/page-2',style=tap_style),
    ]),
      html.Div(children=[
      html.Label('Country',style={'margin':'18px'}), dcc.Dropdown(
      options=options,id='Country-Dropdown2' ,value='India',style={'width': '200px','margin-left':'5px','margin-right':'5px','padding':'3px'}),
      html.Br(),
      dcc.RangeSlider(id='ranger_slider1',
                   min=50, max=31000,
                   #marks={str(h) : h for h in range(50,31001)},
                   value=[50,31000],
                 #  tooltip={"placement": "bottom", "always_visible": True}
                   
                   )    
    ],),
   html.Br(),
   html.Div(children=[
      
      dcc.Graph(id='graph4',style={'padding':'10px'}),
      dcc.Graph(id='graph6',style={'padding':'10px'})
      ]),
          
   html.Div(children=[   
      dcc.Graph(id='graph7',style={'padding':'5px','margin':'5px'}),
      dcc.Graph(id='graph8',style={'padding':'5px','margin':'5px'}),
   ],style={
         'display': 'flex', 
       'flex-direction': 'row',
       'padding':'5 px'
       }),
       
    html.Div(children=[
    dcc.RadioItems(['UAE', 'India'],'India',style={'width': '200px','margin-left':'5px','margin-right':'5px','padding':'3px'}
                   ,id='radio_btn'),
    dcc.RadioItems(['UAE', 'India','Philippines','Qatar','South Africa','United Kingdom'],'India',
         style={'width': '500px','margin-left':'320px','margin-right':'5px','padding':'3px'},id='radio_btn_1'),
    ],style={
          'display': 'flex', 
          'flex-direction': 'row'}),
    html.Br(),
    html.Br(),    
    
])

#City page 
page_2_layout = html.Div([
    html.Div(children=[
       html.Div( style={'background-color':'#94618E','height':'30px'},children=[
       dcc.Link('Home', href='/home',style=tap_style),
       dcc.Link('Country', href='/page-1',style= tap_style),
       dcc.Link('City', href='/page-2',style=tap_style),
       ]),
          html.Div(children=[
          html.Label('Country',style={'margin':'14px'}), dcc.Dropdown(
              options=options,id='Country-Dropdown' ,value='India',style={'width': '200px','margin-left':'5px','margin-right':'5px','padding':'3px'}),
        
          html.Label('City',style={'margin':'14px'}),dcc.Dropdown(
              id='City-Dropdown',options={'label':' ','value':' '},value=' ',
              style={'width': '200px','margin-left':'5px','margin-right':'5px','padding':'3px'} ),   

        ],style={
            
            'margin-left':'300px',
              'display': 'flex', 
            'flex-direction': 'row'
        }),
          

          html.Br(),
          html.Div([
            dcc.Graph(id='graph'),
            
            dcc.Graph(id='graph2',style={'padding-left':'5px'}),
            
            ],style={
                'margin-left':'50px',
                'display': 'flex', 
                'flex-direction': 'row',
                'padding':'3px'
                

            }),
          html.Br(),   
          html.Div([
            dcc.Graph(id='graph3'),
            dcc.Graph(id='graph5',style={'padding':'5px','margin-top':'-4px'}),
           
            ],style={
                'paper_bgcolor':"LightSteelBlue",
                  'margin-left':'50px',
                  'display': 'flex', 
                  'flex-direction': 'row',
                  'padding':'3px'
            }),
        
      ],),
        
         
])
   
     


@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')],
              prevent_initial_call=True
              )
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    elif pathname == '/home':
        return index_page
    else:
        return index_page
# Country based filter
@app.callback(
    Output('graph4', 'figure'),
    Output('graph6', 'figure'),
    Output('graph7', 'figure'),
    Output('graph8', 'figure'),
    [Input('Country-Dropdown2', 'value'),
    Input('ranger_slider1', 'value'),
    Input('radio_btn','value'),
    Input('radio_btn_1','value')
    ],
    prevent_initial_call=True)

#To select the country , Range slider, radio btn
def country(selected_country1,slider_range1,radio_btn,radio_btn_1):
  low, high = slider_range1
  data=zomato[zomato['Country']==selected_country1]
  mask = (data['Avg_price_for_two'] > low) & (data['Avg_price_for_two'] < high)
 
  
  fig4=px.scatter(data[mask],y='Cuisines',x='Avg_price_for_two',hover_data=['Restaurant Name'],color='City',title='Which is costlier cuisine')
  
  fig6=px.scatter(data, x="Votes",y='Restaurant Name',hover_data=['Cuisines','City'],color='Price range',title='Which cuisine gets high votes')
  c=zomato[zomato['Country']==radio_btn]
  Currency_=c[c["Has Online delivery"]=='Yes']
  Currency_=Currency_.groupby(['City'],sort=True)['Has Online delivery','City'].aggregate('count')
  d1=Currency_.sort_values(by='Has Online delivery',ascending=False)
  fig7=px.bar(x=d1['City'].index,y=d1['Has Online delivery'],text_auto=True,title=f'Online Delivery in {radio_btn}')

  c=zomato[zomato['Country']==radio_btn_1]
  Currency_=c[c["Has Table booking"]=='Yes']
  Currency_=Currency_.groupby(['City'],sort=True)['Has Table booking','City'].aggregate('count')
  d1=Currency_.sort_values(by='Has Table booking',ascending=False)
  fig8=px.bar(x=d1['City'].index,y=d1['Has Table booking'],text_auto=True,title=f'Table booking {radio_btn_1}')
  
  
  
  fig4.update_layout(
      autosize=False,
      paper_bgcolor="LightSteelBlue",
      width=1100,
      height=500,
      plot_bgcolor='black'
            )
  fig6.update_layout(
      autosize=False,
      paper_bgcolor="LightSteelBlue",
      width=1100,
      height=500,
      plot_bgcolor='black'
            )
  fig7.update_layout(
      autosize=False,
      paper_bgcolor="LightSteelBlue",
      width=500,
      height=500,
      )
  fig8.update_layout(
      autosize=False,
      paper_bgcolor="LightSteelBlue",
      width=500,
      height=500,
     
      )
  return fig4,fig6,fig7,fig8


# City Page

@app.callback(
   Output('City-Dropdown','options')
 ,Input('Country-Dropdown','value'),
 prevent_initial_call=True)

def set_cities_options(selected_country):      # To selcet country and City
     data=zomato[zomato['Country']==selected_country]
     return [{'label': i, 'value': i} for i in data['City'].unique()]

@app.callback(
     Output('City-Dropdown', 'value'),
     Input('City-Dropdown', 'options'),
     prevent_initial_call=True)
def set_cities_value(available_options):
     return available_options[0]['value']


@app.callback(
     Output('graph', 'figure'),
     Output('graph2', 'figure'),
     Output('graph3', 'figure'),   
     Output('graph5', 'figure'),  
     Input('Country-Dropdown', 'value'),
     Input('City-Dropdown', 'value'),
     prevent_initial_call=True,)

def set_display_country(selected_country,selected_city):
 #selected=zomato[value]
   data=zomato[zomato['Country']==selected_country]
   data=data[data['City']==selected_city]
   pie=data['Has Online delivery'].value_counts()
   fig=px.pie(data,labels='Cuisines',values='Avg_price_for_two',names='Restaurant Name',color='Cuisines',width=500, 
               height=300,title=f'What are Cuisines in the {selected_country},{selected_city}')

   
   data1 = data.groupby(['Aggregate rating','Rating color', 'Rating text']).size().reset_index().rename(columns={0:'Rating Count'})
   

   fig2=px.bar(data1,x=data1['Rating color'],color=data1['Rating color'], width=500, height=300)
   
   
   fig3=px.pie(data,values=data['Has Online delivery'].value_counts()/9952*100,title=f'Online Food Delivery in {selected_country},{selected_city}',
                width=500, height=300,names=data['Has Online delivery'].value_counts().index)
   fig5=px.pie(data,values=data['Has Table booking'].value_counts()/9952*100,title=f'Table booking in {selected_country},{selected_city}',
               names=data['Has Table booking'].value_counts().index, width=500, height=300)
   
   
   
   fig.update_layout(
       autosize=False,
       paper_bgcolor="LightSteelBlue",

       ),
   fig2.update_layout(
       autosize=False,
       paper_bgcolor="#FA77D9",

       )
   fig3.update_layout(
       autosize=False,
       paper_bgcolor="#F5D660",
       )
   fig5.update_layout(
       autosize=False,
       paper_bgcolor="#F5D660",
       )
   
   
   return fig,fig2,fig3,fig5


#world Page
@app.callback(
    Output('graph9','figure'),
    Input('index','value'),
    prevent_initial_call=False
    
    )

def index(y):
    
    ddd=zomato.groupby(by='Currency_')[['Currency','City','Currency_','Country','Avg_price_for_two','Latitude','Longitude']].aggregate('first')
   
    fig9= px.scatter_geo(ddd, lat='Latitude' , lon='Longitude',color='Country',size='Currency_',projection="natural earth",title='Currency')
    
    return fig9
    
    
if __name__ == '__main__':
    app.run_server(debug=True)

