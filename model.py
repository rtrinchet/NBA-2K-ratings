import numpy as np 
import pandas as pd 
from scipy import stats

import matplotlib.pyplot as plt
import seaborn as sns

sns.set() # use Seaborn styles
sns.color_palette("Blues")
plt.style.use('fivethirtyeight')


from sklearn import preprocessing, metrics
from sklearn.model_selection import cross_val_score, train_test_split, KFold
from sklearn.ensemble import RandomForestRegressor

# import xgboost as xgb

import warnings; warnings.simplefilter('ignore')



# Data import
df = pd.read_csv('2019_ratings_stats.csv')



