import numpy as np
from dash import Dash, html, dcc, Input, Output, State, ctx
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px

import dashboard_data as dd
import brain_stroke_prediction as bsp

#create dashboard
app=Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

#import preprocessed data
df=dd.df

#create dashboard layout
app.layout=html.Div(id='app', children=[
    
    #side bar controls
    html.Div(id='controls', children=[
        html.H1(children='Brain Stroke Data Visualization'),
        html.Img(src='/assets/brain_stroke.jpg'),
        html.Br(),

        #radiobuttons
        html.Label('Gender'),
        dcc.RadioItems(
            id='radiobutton',
            options={
                'Female':'Female', 
                'Male':'Male', 
                'All':'All'}, 
            value='All')
    ]),

    #main sectiion
    html.Div(id='container', children=[
        
        #visualization section
        html.Div(id='visualization', children=[
            
            #Number of people who has experienced brain stroke by age 
            html.Div(id='age', children=[
                html.H4(children='Number of people who has experienced brain stroke by age'),
                dcc.Graph(
                    id='age_graph',
                    figure={}
                )
            ]),

            #Number of people who has experienced brain stroke by BMI
            html.Div(id='bmi', children=[
                html.H4(children='Number of people who has experienced brain stroke by BMI'),
                dcc.Graph(
                    id='bmi_graph',
                    figure={}
                )
            ]),

            #Percent of people who has experienced brain stroke by work type
            html.Div(id='work_type', children=[
                html.H4(children='Percent of people who has experienced brain stroke by work type'),
                dcc.Graph(
                    id='work_type_graph',
                    figure={}
                )
            ]),

            #Percent of people who has experienced brain stroke by smoking status
            html.Div(id='smoking_status', children=[
                html.H4(children='Percent of people who has experienced brain stroke by smoking status'),
                dcc.Graph(
                    id='smoking_status_graph',
                    figure={}
                )
            ])
        ]),

        #prediction section
        html.Div(id='prediction', children=[
            html.H2('Input your indicators:'),

            #create inputs 
            html.Div(id='indicators', children=[
                html.Label('Gender'),
                dcc.Dropdown(id='gender_indicator', 
                    options={0:'Male', 1:'Female'}, 
                    value=1, style={'color':'#ffffff', 'background-color':'#0a0a0a'}),
                html.Br(),

                html.Label('Age', className='input'),
                dcc.Input(id='age_indicator', type='number', placeholder=f'Your age'),
                html.Br(),
                
                html.Label('Do you have hypertension?'),
                dcc.Dropdown(id='hypertension', 
                    options={1:'Yes', 0:'No'}, 
                    value=0, style={'color':'#ffffff', 'background-color':'#0a0a0a'}),
                html.Br(),
                
                html.Label('Do you have any heart diseases?'),
                dcc.Dropdown(id='heart_disease', 
                    options={1:'Yes', 0:'No'}, 
                    value=0, style={'color':'#ffffff', 'background-color':'#0a0a0a'}),
                html.Br(),
                
                html.Label('Work type'),
                dcc.Dropdown(id='work_type_indicator', 
                    options={3:'Privat', 4:'Self-employed', 1:'Goverment job', 0:'Taking care of children'},
                    value=4, style={'color':'#ffffff', 'background-color':'#0a0a0a'}),
                html.Br(),
                
                html.Label('Average glucose level in blood', className='input'),
                dcc.Input(id='avg_glucose_lvl', type='number', placeholder=f'Glucose level'),
                html.Br(),

                html.Label('BMI'),
                dcc.Dropdown(id='bmi_indicator', 
                    options={0:'below 18.5', 1:'18.5-24.9', 2:'25.0-29.9', 3:'30.0-34.9', 4:'35.0-39.9', 5:'above 40'},
                    value=1, style={'color':'#ffffff', 'background-color':'#0a0a0a'}),
                html.Br(),

                html.Label('Smoking status'),
                dcc.Dropdown(id='smoking_status_indicator', 
                    options={1:'formerly smoked', 0:'never smoked', 2:'smoke'},
                    value=0, style={'color':'#ffffff', 'background-color':'#0a0a0a'}),
                html.Br(),

                html.Label('Residence type'),
                dcc.Dropdown(id='residence_type_indicator', 
                    options={1:'Urbar', 0:'Rural'},
                    value=0, style={'color':'#ffffff', 'background-color':'#0a0a0a'}),
                html.Br()
            ]),

            #button
            html.Button('Submit', id='submit'),

            #prediction result 
            html.Div(id='msg')
        ])
    ])
    
])

#visualization callback: calls update_figure() function when radio button value is changed
@app.callback(
    #Visualization Output
    [Output(component_id='age_graph', component_property='figure'), 
    Output(component_id='bmi_graph', component_property='figure'), 
    Output(component_id='work_type_graph', component_property='figure'), 
    Output(component_id='smoking_status_graph', component_property='figure')],
    #visualization Input
    Input(component_id='radiobutton', component_property='value'))

#function that updates graphs when radio button value is changed
def update_figure(selected_gender):

    #change condition
    if selected_gender!='All':
        filtered_df=df[df['gender']==selected_gender] 
    else:
        filtered_df=df  

    #define new age figure
    age_df=filtered_df[filtered_df['stroke']==1].groupby('age')['work_type'].count().reset_index().rename(columns={'work_type':'count'})  
    age_fig=px.bar(data_frame=age_df, x='age', y='count', color_discrete_sequence=px.colors.sequential.Plasma_r)
    age_fig.update_layout()
    
    #define new bmi figure
    bmi_df=filtered_df[filtered_df['stroke']==1].groupby('bmi')['work_type'].count().reset_index().rename(columns={'work_type':'count'})
    bmi_fig=px.bar(data_frame=bmi_df, x='bmi', y='count', color_discrete_sequence=px.colors.sequential.Plasma_r)

    #define new work type figure
    work_total=filtered_df.groupby('work_type')['age'].count().reset_index().rename(columns={'age':'count'})
    work_stroke=filtered_df[filtered_df['stroke']==1].groupby('work_type')['age'].count().reset_index().rename(columns={'age':'count'})
    work_stroke['percent']=[i/j*100 for i, j in zip(work_stroke['count'], work_total['count'])]
    
    #condition used since there are no male in dataFrame who has experienced brain stroke and had no job
    if selected_gender=='Male':
        work_stroke.loc[len(work_stroke.index)]=['Taking care of children',0, 0]

    work_total['percent']=[i/j*100-k for i, j, k in zip(work_total['count'], work_total['count'], work_stroke['percent'])]
    work_stroke=pd.concat([work_stroke, work_total])
    work_fig=px.bar(data_frame=work_stroke, x='work_type', y='percent', color='percent', color_discrete_sequence=px.colors.sequential.Plasma_r)

    #define new smoking status figure
    smoking_total=filtered_df.groupby('smoking_status')['age'].count().reset_index().rename(columns={'age':'count'})
    smoking_stroke=filtered_df[filtered_df['stroke']==1].groupby('smoking_status')['age'].count().reset_index().rename(columns={'age':'count'})
    smoking_stroke.drop(smoking_stroke[smoking_stroke['smoking_status']=='Unknown'].index, inplace=True)
    smoking_total.drop(smoking_total[smoking_total['smoking_status']=='Unknown'].index, inplace=True)
    smoking_stroke['percent']=[i/j*100 for i, j in zip(smoking_stroke['count'], smoking_total['count'])]
    smoking_total['percent']=[i/j*100-k for i, j, k in zip(smoking_total['count'], smoking_total['count'], smoking_stroke['percent'])]
    smoking_stroke=pd.concat([smoking_stroke, smoking_total])
    smoking_fig=px.bar(data_frame=smoking_stroke, x='smoking_status', y='percent', color='percent', color_discrete_sequence=px.colors.sequential.Plasma_r)

    #update graphs and their layouts
    age_fig.update_layout(transition_duration=300, paper_bgcolor='#1f1f1f',
    plot_bgcolor='#1f1f1f', font=dict(color='#ffffff'))
    age_fig.update_yaxes(gridcolor='rgba(0,0,0,0.4)', showline=False)
    bmi_fig.update_layout(transition_duration=300, paper_bgcolor='#1f1f1f',
    plot_bgcolor='#1f1f1f', font=dict(color='#ffffff'))
    bmi_fig.update_yaxes(gridcolor='rgba(0,0,0,0.4)', showline=False)
    work_fig.update_layout(transition_duration=300, paper_bgcolor='#1f1f1f',
    plot_bgcolor='#1f1f1f', font=dict(color='#ffffff'))
    work_fig.update_yaxes(gridcolor='rgba(0,0,0,0.4)', showline=False)
    smoking_fig.update_layout(transition_duration=300, paper_bgcolor='#1f1f1f',
    plot_bgcolor='#1f1f1f', font=dict(color='#ffffff'))
    smoking_fig.update_yaxes(gridcolor='rgba(0,0,0,0.4)', showline=False)

    return age_fig, bmi_fig, work_fig, smoking_fig

#prediction callback: calls prediction_update() function when button is clicked
@app.callback(
    #Prediction Output
    Output(component_id='msg', component_property='children'),
    #Prediction Input
    Input(component_id='submit', component_property='n_clicks'), 
    #Prediction States
    [State(component_id='gender_indicator', component_property='value'),
    State(component_id='age_indicator', component_property='value'),
    State(component_id='hypertension', component_property='value'),
    State(component_id='heart_disease', component_property='value'),
    State(component_id='work_type_indicator', component_property='value'),
    State(component_id='avg_glucose_lvl', component_property='value'),
    State(component_id='bmi_indicator', component_property='value'),
    State(component_id='smoking_status_indicator', component_property='value'),
    State(component_id='residence_type_indicator', component_property='value')])

#function that predicts wether you are at risk of getting brain stroke using Decicission Tree model
def prediction_update(n_clicks, gender_ind, age_ind, hypertension_ind, heart_disease_ind, work_type_ind, avg_glucose_lvl_ind, bmi_ind, smoking_status_ind, residence_type_ind):
    
    x_df=pd.DataFrame(np.array([gender_ind, age_ind, hypertension_ind, heart_disease_ind, work_type_ind, residence_type_ind, avg_glucose_lvl_ind, bmi_ind, smoking_status_ind]).reshape((1, 9)))
    print(x_df)
    prediction_result=bsp.tree_model.predict(x_df)

    #converting result into text
    if prediction_result==0:
        msg='You are fine!'
    else:
        msg='You are at risk of getting brain stroke'

    return msg

#start app
if __name__=='__main__':
    app.run_server(debug=True)