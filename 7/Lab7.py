import numpy as np
import pandas as pd
import csv
from pgmpy.estimators import MaximumLikelihoodEstimator
from pgmpy.models import BayesianModel
from pgmpy.inference import VariableElimination

lines = list(csv.reader(open('heart_disease.csv','r')))

attribute = lines[0]
heartDisease = pd.read_csv('heart_disease.csv')
heartDisease = heartDisease.replace('?',np.nan)



#print("Few examples from dataset are :-")
#print(heartDisease.head())
print("Attributes and datatypes")
print(heartDisease.dtypes)

model = BayesianModel([('age','trestbps'),('age','fbs'),('sex', 'trestbps'), ('sex', 'trestbps'), ('exang', 'trestbps'),('trestbps','heartdisease'),('fbs','heartdisease'),
('heartdisease','restecg'),('heartdisease','thalach'),('heartdisease','chol')])

print("Learning CPDs using max lilelihood estimatos")
model.fit(heartDisease,estimator = MaximumLikelihoodEstimator)

print("Inferencing with bayesian network")
HeartDisease_infer = VariableElimination(model)

q = HeartDisease_infer.query(variables = ['heartdisease'], evidence = {'age':28})
print(q)
print(q['heartdisease'])

print("2. Probability of Heart disease given chol = 100")
q = HeartDisease_infer.query(variables = ['heartdisease'], evidence =  {'chol':100})
print(q['heartdisease'])
