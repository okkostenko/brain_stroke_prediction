import pandas as pd
from sklearn import model_selection, tree
import numpy as np
from six import StringIO

#import dataset
df=pd.read_csv("full_data.csv")

#data preprocessing
df_prep=df

del df_prep['ever_married']
df_prep.drop(df_prep[df_prep['smoking_status']=='Unknown'].index, inplace=True)

underweight=df_prep[df_prep['bmi']<18.5]
normal=df_prep[df_prep['bmi'].between(18.5, 24.9)]
pre=df_prep[df_prep['bmi'].between(25.0, 29.9)]
obesity1=df_prep[df_prep['bmi'].between(30, 34.9)]
obesity2=df_prep[df_prep['bmi'].between(35, 39.9)]
obesity3=df_prep[df_prep['bmi']>=40]

underweight.loc[:, 'bmi']=0
normal.loc[:, 'bmi']=1
pre.loc[:, 'bmi']=2
obesity1.loc[:, 'bmi']=3
obesity2.loc[:, 'bmi']=4
obesity3.loc[:, 'bmi']=5

df_prep=pd.concat([underweight, normal, pre, obesity3, obesity1, obesity2])

##convert all string values into numbers
df_prep['gender']=list(map(lambda x: 1 if x=='Female' else 0 ,df_prep['gender']))
df_prep['work_type']=list(map(lambda x: 0 if x=='children' else 1 if x=='Govt_jov' else 2 if x=='Never_worked' else 3 if x=='Private' else 4 ,df_prep['work_type']))
df_prep['Residence_type']=list(map(lambda x: 1 if x=='Urban' else 0 ,df_prep['Residence_type']))
df_prep['smoking_status']=list(map(lambda x: 2 if x=='smokes' else 1 if x=='formerly smoked' else 0,df_prep['smoking_status']))

df=df_prep

#Decision Tree model
##devide data into train and test samples
var_columns=[i for i in df.columns if i not in ['stroke']]
X=df.loc[:, var_columns]
Y=df.loc[:, "stroke"]
ss=model_selection.ShuffleSplit(n_splits=np.random.randint(1, 21), test_size=.2, random_state=0)
for train_index, test_index in ss.split(X, Y):
    pass
train=df.iloc[train_index]
test=df.iloc[test_index]

x_train=train.loc[:, var_columns]
y_train=train.loc[:, 'stroke']
x_test=test.loc[:, var_columns]
y_test=test.loc[:, 'stroke']

##build model
tree_model=tree.DecisionTreeClassifier(max_depth=20, class_weight="balanced", criterion="gini")
tree_model=tree_model.fit(x_train, y_train)

##Decision Tree visualization
dot_data=StringIO()
tree.export_graphviz(tree_model, out_file="graph.dot", feature_names=var_columns, class_names="Class", filled=True, rounded=True, special_characters=True)






