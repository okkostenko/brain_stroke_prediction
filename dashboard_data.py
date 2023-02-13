import pandas as pd

#load data
df=pd.read_csv('full_data.csv')

#preprocess data 
del df['ever_married']
del df['avg_glucose_level']
del df['Residence_type']
del df['heart_disease']
del df['hypertension']

df['work_type']=df['work_type'].replace(['Govt_job', 'children'], ['Goverment job', 'Taking care of children'])
underweight=df[df['bmi']<18.5]
normal=df[df['bmi'].between(18.5, 24.9)]
pre=df[df['bmi'].between(25.0, 29.9)]
obesity1=df[df['bmi'].between(30, 34.9)]
obesity2=df[df['bmi'].between(35, 39.9)]
obesity3=df[df['bmi']>=40]

underweight.loc[:, 'bmi']='below 18.5'
normal.loc[:, 'bmi']='18.5-24.9'
pre.loc[:, 'bmi']='25.0-29.9'
obesity1.loc[:, 'bmi']='30.0-34.9'
obesity2.loc[:, 'bmi']='35.0-39.9'
obesity3.loc[:, 'bmi']='above 40'

df=pd.concat([underweight, normal, pre, obesity3, obesity1, obesity2])



