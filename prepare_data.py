import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

def split_data(data, target, test_size = 0.25):
    """
    Split data into: train_x, train_y, test_x, test_y. 
    Args:
        data (pd.DataFrame):    dataframe loaded from the table "prodiq_mft_value_lab"
        target (str):           target column
        test_size (float):      size (between 0-1) of the test set
    Returns:
        train_x (pd.DataFrame): a dataframe that contains the train data with all posible predictor variables.
        train_y (np.array): an array that contains the train data with target variable.
        test_x (pd.DataFrame): a dataframe that contains the test data with predictor variables.
        test_y (np.array): an array that contains the test data with target variable.
    """
    print("- Splitting the data with test proportion: {}% ...".format(test_size*100))
    print ('    Size prior to train-test split: {}'.format(data.shape))
    # Split the data into training and test sets
    train, test = train_test_split(data, test_size = test_size)

    # Split the data into predictor and target variables
    train_x = train.drop([target], axis=1)
    test_x = test.drop([target], axis=1)
    train_y = np.array(train[[target]]).reshape(-1)
    test_y = np.array(test[[target]]).reshape(-1)
    print('    Sizes of train_x, train_y, test_x, test_y sets: {}, {}, {}, {}'.format(train_x.shape, train_y.shape, test_x.shape, test_y.shape ))

    return train_x, train_y, test_x, test_y



def cross_validation(df, target, model, n_splits = 10, scoring = 'r2' ):
    print('Performing {}-fold cross validation for model:\n{} \nScoring used: {}'.format(n_splits, model, scoring))
    y = df['rating']
    X = df.drop('rating', axis = 1).copy()
    
    kfold = KFold(n_splits = n_splits)
    scores = cross_val_score(model, X, y, cv=kfold, verbose = 1, 
                             scoring = scoring)

    print("Cross-validation scores:\n{}".format(scores))
    print("Number of cv iterations: ", len(scores))
    print("Mean {}: {:.2f}".format(scoring, scores.mean()))