from collections import namedtuple

import pandas as pd
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

categories = ['const', 'mintempm_1', 'mintempm_2', 'mintempm_3',
              'maxdewptm_1', 'maxdewptm_3', 'mindewptm_1', 'maxtempm_1']

daily_summary = namedtuple("DailySummary", categories)
reg = LinearRegression()


def init():
    df = pd.read_csv('weather_dataset.csv').set_index('date')

    predictors = ['meantempm_1', 'meantempm_2', 'meantempm_3',
                  'mintempm_1', 'mintempm_2', 'mintempm_3',
                  'meandewptm_1', 'meandewptm_2', 'meandewptm_3',
                  'maxdewptm_1', 'maxdewptm_2', 'maxdewptm_3',
                  'mindewptm_1', 'mindewptm_2', 'mindewptm_3',
                  'maxtempm_1', 'maxtempm_2', 'maxtempm_3']

    df2 = df[['meantempm'] + predictors]

    x, y = df2[predictors], df2['meantempm']

    x = sm.add_constant(x)
    x = x[['const', 'mintempm_1', 'mintempm_2', 'mintempm_3', 'maxdewptm_1',
           'maxdewptm_3', 'mindewptm_1', 'maxtempm_1']]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1, random_state=12)
    reg.fit(x_train, y_train)


def get_prediction(coefficients):
    return reg.predict([coefficients])[0]
