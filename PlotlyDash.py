# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',style={'textAlign': 'center', 'color': '#503D36','font-size': 40}),
# TASK 1: Add a dropdown list to enable Launch Site selection
# The default select value is for ALL sites
# dcc.Dropdown(id='site-dropdown',...)
dcc.Dropdown(id='site-dropdown',options=spacex_df['Launch Site'].unique(), placeholder= 'All Sites',searchable= True),
html.Div(id='dd-output-container'),                              
html.Br(),

# TASK 2: Add a pie chart to show the total successful launches count for all sites
# If a specific launch site was selected, show the Success vs. Failed counts for the site
html.Div(dcc.Graph(id='success-pie-chart')),
html.Br(),


html.P("Payload range (Kg):"),
# TASK 3: Add a slider to select payload range
#dcc.RangeSlider(id='payload-slider',...)
dcc.RangeSlider(id='payload-slider',min=0, max=10000, step=1000,
                marks={0:'0', 2500:'2500',5000:'5000', 7500:'7500',10000:'10000' },
                value=[min_payload, max_payload]),


# TASK 4: Add a scatter chart to show the correlation between payload and launch success
html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    
    filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
    #print(filtered_df['class'])
    if entered_site == 'CCAFS LC-40' or entered_site == 'VAFB SLC-4E' or  entered_site == 'KSC LC-39A' or entered_site == 'CCAFS SLC-40' :
        fig = px.pie(data_frame=filtered_df, 
        names='class', 
        title='Total Success Launches for Site: '+ str(entered_site))
        return fig
    else:
        fig = px.pie(spacex_df, values='class', 
        names='Launch Site', 
        title='Total Success Launches By Site')
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
              Input(component_id="payload-slider", component_property="value")])
def get_scatterPlot(entered_site, limiters):    
      filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
      User_df= filtered_df[(filtered_df['Payload Mass (kg)']>=limiters[0]) & (filtered_df['Payload Mass (kg)']<=limiters[1])]
      print(User_df)

      if entered_site == 'CCAFS LC-40' or entered_site == 'VAFB SLC-4E' or  entered_site == 'KSC LC-39A' or entered_site == 'CCAFS SLC-40':
          plot = px.scatter(User_df,x='Payload Mass (kg)', y='class', color='Booster Version Category',  
          title='Correlation between Payload and Success for site: '+ str(entered_site))
          return plot
     
      else:
        #print(entered_site,limiters)
        plot = px.scatter(spacex_df,x='Payload Mass (kg)', y='class', color='Booster Version Category',  
        title='Correlation between Payload and Success')
        return plot





# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)