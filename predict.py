import sklearn as sk
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import mean_squared_error
from sklearn.pipeline import Pipeline
import joblib
import numpy as np
import pandas as pd
from pprint import pprint
import numpy as np

# a function to take user input based on the columns in X and predict the salary
def predict_salary(gender, percent10th, board10th, percent12th, board12, 
                collegeTier, degree, specialization, collegeGPA, 
                CollegeCityTier, CollegeState, 
                English, Logical, Quant, Age):
    # create a dataframe with the user input
    udf = pd.DataFrame({
        'Gender': [gender],
        '10percentage': [percent10th],
        '10board': [board10th],
        '12percentage': [percent12th],
        '12board': [board12],
        'CollegeTier': [collegeTier],
        'Degree': [degree],
        'Specialization'    : [specialization],
        'collegeGPA': [collegeGPA],
        'CollegeCityTier': [CollegeCityTier],
        'CollegeState': [CollegeState],
        'English': [English],
        'Logical': [Logical],
        'Quant': [Quant],
        'Age' : [Age]
    })
    pprint(udf.to_dict())
    model = joblib.load('model.pkl')
    ans = model.predict(udf)
    return np.expm1(ans[0]).round(2)


