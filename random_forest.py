# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 00:50:53 2018

@author: Sakib Reza
"""
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble.forest import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
import numpy as np


test = pd.read_csv("test.csv")
test_shape = test.shape

train = pd.read_csv("train.csv")
train_shape = train.shape


#sex_pivot = train.pivot_table(index="Sex",values="Survived")
#sex_pivot.plot.bar()
#plt.show()

def process_age(df,cut_points,label_names):
    df["Age"] = df["Age"].fillna(-0.5)
    df["Age_categories"] = pd.cut(df["Age"],cut_points,labels=label_names)
    return df

cut_points = [-1, 0, 5, 12, 18, 35, 60, 100]
label_names = ["Missing", "Infant", "Child", "Teenager", "Young Adult", "Adult", "Senior"]

train = process_age(train,cut_points,label_names)
test = process_age(test,cut_points,label_names)

#age_plot = train.pivot_table(index="Age_categories", values="Survived")
#age_plot.plot.bar()
#plt.show()

def create_dummies(df,column_name):
    dummies = pd.get_dummies(df[column_name],prefix=column_name)
    df = pd.concat([df,dummies],axis=1)
    return df

train = create_dummies(train,"Pclass")
test = create_dummies(test,"Pclass")

train = create_dummies(train,"Sex")
test = create_dummies(test,"Sex")

train = create_dummies(train,"Age_categories")
test = create_dummies(test,"Age_categories")


columns = ['Pclass_1', 'Pclass_2', 'Pclass_3', 'Sex_female', 'Sex_male',
       'Age_categories_Missing','Age_categories_Infant',
       'Age_categories_Child', 'Age_categories_Teenager',
       'Age_categories_Young Adult', 'Age_categories_Adult',
       'Age_categories_Senior']


#lr = LogisticRegression()
#lr.fit(train[columns],train["Survived"])

holdout = test # from now on we will refer to this
               # dataframe as the holdout data

all_X = train[columns]
all_y = train['Survived']

train_X, test_X, train_y, test_y = train_test_split(all_X, all_y, test_size = 0.20, random_state = 0)


random_forest = RandomForestClassifier(n_estimators=100)
random_forest.fit(train_X, train_y)
Y_pred = random_forest.predict(test_X)
random_forest.score(train_X, train_y)
acc_random_forest = round(random_forest.score(train_X, train_y) * 100, 2)
print('train accuracy' + str(acc_random_forest))


scores = cross_val_score(random_forest, all_X, all_y, cv = 10)
accuracy = np.mean(scores)
print('Cross_val scores : ' + str(scores))
print('Cross_val accuracy : ' + str(accuracy))


random_forest.fit(all_X, all_y)
holdout_predictions = random_forest.predict(holdout[columns])


holdout_ids = holdout["PassengerId"]
submission_df = {"PassengerId": holdout_ids, "Survived": holdout_predictions}
submission = pd.DataFrame(submission_df)
submission.to_csv("submission.csv", index = False)
