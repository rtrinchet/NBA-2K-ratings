import pandas as pd
import numpy as np

def missing_pct(df):
    '''
    Gets a dataframe with the percentage of missing values for each value of the original dataframe
    Args:
        df (dataframe): original df
        
    Returns:
        missing_value_df (dataframe): df with NA info
    '''
    percent_missing = df.isnull().sum() * 100 / len(df)
    missing_value_df = pd.DataFrame({'percent_missing': percent_missing})
    missing_value_df.sort_values('percent_missing', ascending = False, inplace=True)
    return missing_value_df

def get_NA_interval(df, col, filter_value = 5):
    '''
    Gets a dataframe with information about intervals where a given variable takes NA values
    
    Args:
        df (dataframe): initial dataframe
        col (str): name of the column to be analyzed
        filter_value (int): number of minimum seconds an interval must have to be considered
        
    Returns: 
        out_df (dataframe): dataframe with information about the NA intervals. 
                            Contains the columns start & end with the interval ends
                            and duration with the duration of the interval in seconds
    '''
    a = df[col].values  # Extract out relevant column from dataframe as array
    m = np.concatenate(( [False], np.isnan(a), [False] ))  # Mask
    ss = np.flatnonzero(m[1:] != m[:-1]).reshape(-1,2)   # Instantes de cambio entre null y no-null

    try: 
        # fecha de cambios entre null y no null
        tiempos = df.index[ss].reshape(-1,2)
    except:
        # if the last element of ss is not accesible
        if ss[-1,1] == len(df):
            ss = np.delete(ss, -1, axis=0)
        # fecha de cambios entre null y no null
        tiempos = df.index[ss].reshape(-1,2)

    # df con información de intervalos
    out_df = pd.DataFrame(0, index=np.arange(len(tiempos)), columns=['start', 'end'])
    out_df["start"], out_df["end"] = tiempos[:,0], tiempos[:,1]
    out_df['duration'] = (out_df.end - out_df.start).dt.seconds
    out_df = out_df.sort_values('duration', ascending = False).reset_index(drop=True)
    out_df = out_df.loc[out_df.duration > filter_value].reset_index(drop=True)

    return out_df



def get_zeroes_interval(df, col, filter_time = 1):
    '''
    Gets a dataframe with information about intervals where a given variable takes 
    isolated zero values (or values in intervals of zeroes).
    
    Args:
        df (dataframe): initial dataframe
        col (str): name of the column to be analyzed
        filter_time (int): maximum length in seconds of the intervals with zeroes
        
    Returns: 
        out_df (dataframe): dataframe with information about the zeroes intervals. 
                            Contains the columns start & end with the interval ends
                            and duration with the duration of the interval in seconds
    '''
    a = df[col].values  # Extract out relevant column from dataframe as array
    m = np.concatenate(( [False], a == 0, [False] ))  # Mask
    ss = np.flatnonzero(m[1:] != m[:-1]).reshape(-1,2)   # Instantes de cambio entre null y no-null
    #if the last element of ss is the 
    if ss[-1,1] == len(df):
        ss = np.delete(ss, -1, axis=0)
    # fecha de cambios entre null y no null
    tiempos = df.index[ss].reshape(-1,2)
    # df con información de intervalos
    out_df = pd.DataFrame(0, index=np.arange(len(tiempos)), columns=['start', 'end'])
    out_df["start"], out_df["end"] = tiempos[:,0], tiempos[:,1]
    out_df['duration'] = (out_df.end - out_df.start).dt.seconds
    out_df = out_df.sort_values('duration', ascending = False)
    out_df = out_df.loc[out_df.duration < filter_time].reset_index(drop=True)
    return out_df