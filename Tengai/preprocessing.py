import numpy as np
import pandas as pd
from typing import Any,Union
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import statsmodels.api as sm

def detect_outlier(data:Union[pd.Series,np.array],
                   see_value:bool=None) -> np.array:
    see_value = False if see_value is None else see_value

    """
    ## Description

    this function detection outlier

    Args:
        data (Union[pd.Series,np.array]): input data a from Series or np.array

    Returns:
        np.array: result of index if see_value is True the element
                  is value
    """

    mean_val = data.mean()
    zscore = (data - mean_val) / data.std()
    if isinstance(data,pd.Series):
        if see_value:
            return data[abs(zscore)>3]
        else:
            return data.index[abs(zscore)>3]
    if isinstance(data,np.ndarray):
        if see_value:
            return data[abs(zscore)>3]
        else:
            return np.where(abs(zscore)>3)[0].tolist()
        
def undersampling_data(data:pd.DataFrame,ratio:float=.5)-> pd.DataFrame:
    """_summary_

    Args:
        data (pd.DataFrame): _description_
        ratio (float, optional): _description_. Defaults to .5.

    Returns:
        pd.DataFrame: _description_
    """
    n_samples = int(len(data)*ratio)
    undersampled_time_series = data.sample(n=n_samples,random_state=42)
    undersampled_time_series = undersampled_time_series.sort_index()
    return undersampled_time_series

def clustering_DataFrame(data:pd.DataFrame,name_time_feature:str,
                         rule:str="D")->pd.DataFrame:
    """_summary_
    this function about how to result dataframe ready to clustering
    Args:
        data (pd.DataFrame): _description_
        name_time_feature (str): _description_
        rule (str, optional): _description_. Defaults to "D".

    Returns:
        pd.DataFrame: _description_
    """
    # setting time features
    data[name_time_feature]=pd.to_datetime(data[name_time_feature])
    data.set_index(name_time_feature,inplace=True)
    
    return data.resample(rule).mean()

def Clustering_Optimalization(data:pd.DataFrame,
                              range_iterable:range,random_state:int=0):
    """
    this code deteck how many cluster group in data
    Args:
        data (pd.DataFrame): input data
        range_iterable (range): range of input value
        random_state (int, optional): this just lock data. Defaults to 0.
    """
    inertia = []
    for k in range_iterable:
        pipeline = make_pipeline(StandardScaler(),KMeans(n_clusters=k,random_state=random_state))
        # training model pipeline
        pipeline.fit(data)
        inertia.append(pipeline.named_steps['kmeans'].inertia_)
    # Plot the elbow graph
    diff_inertia = [inertia[i] - inertia[i - 1] for i in range(1, len(inertia))]
    plt.figure(figsize=(8, 6))
    plt.plot(range(1, 11), inertia, marker='o', linestyle='--')
    plt.xlabel('Number of clusters (k)')
    plt.ylabel('Inertia')
    plt.title('Elbow Method for Optimal k')
    plt.legend()
    plt.show()


def detect_outlier_zscore(data: Union[np.ndarray, pd.Series, pd.DataFrame], threshold: int = 3, change_outlier: bool = None) -> Union[np.array, pd.Series, pd.DataFrame]:
    """
    Detect and potentially modify outliers in data using Z-scores.

    Args:
        data (Union[np.ndarray, pd.Series, pd.DataFrame]): Input data.
        threshold (int, optional): Z-score threshold for outlier detection. Defaults to 3.
        change_outlier (bool, optional): If True, replace outliers with the median of the data. Defaults to None.

    Returns:
        Union[np.array, pd.Series, pd.DataFrame]: Data with outliers or modified outliers.
    """
    if change_outlier is None:
        change_outlier = False

    if isinstance(data, (pd.Series, np.ndarray)):
        if isinstance(data, pd.Series):
            # Convert to NumPy array
            data = data.values  

        mean_val = np.mean(data)
        std_val = np.std(data)
        z_score = np.abs((data - mean_val) / std_val)
        outliers = np.where(z_score>threshold)
        
        if change_outlier:
            # Create a copy of the data to avoid modifying the original
            new_data = data.copy()
            # Replace outliers with the median value
            median_val = np.median(data)
            new_data[outliers] = median_val
            return new_data
        else:
            # If not changing outliers, return the indices of outliers
            return outliers
    if isinstance(data, pd.DataFrame):
        new_data = data.copy()  # Create a copy of the DataFrame to avoid modifying the original

    if isinstance(data, pd.DataFrame):
        new_data = data.copy()  # Create a copy of the DataFrame to avoid modifying the original

        for col in data.columns:
            mean_val = np.mean(data[col])
            std_val = np.std(data[col])
            z_score = np.abs((data[col] - mean_val) / std_val)
            outliers = np.where(z_score > threshold)

            if change_outlier:
                # Replace outliers with the median value for this column
                median_val = np.median(data[col])
                new_data.loc[outliers, col] = median_val
        return new_data

def detect_pdq_different(data:pd.Series,
                         alpha:float=.05)->dict[str,np.number]:
    """_summary_

    Args:
        data (pd.Series): _description_
        alpha (float, optional): _description_. Defaults to .05.

    Returns:
        dict[str,np.number]: _description_
    """
    # for find p and q
    data_diff = data.copy()
    data_diff = data_diff.diff().dropna()
    best_aic = np.inf
    best_bic = np.inf
    best_p = 0
    best_q = 0

    # Define a range for p and q
    p_range = range(0, 4)  # Example range for p
    q_range = range(0, 4)  # Example range for q

    for p,q in zip(p_range,q_range):
        model = sm.tsa.ARIMA(data_diff, order=(p, 1, q))
        results = model.fit()
        aic = results.aic
        bic = results.bic

        if aic < best_aic and bic < best_bic:
            best_aic = aic
            best_bic = bic
            best_p = p
            best_q = q

    # to find value of d
    d = 0
    while True:
        # Uji stasioneritas menggunakan ADF
        result = sm.tsa.adfuller(data_diff)
        
        # Ambil nilai p-value dari hasil uji ADF
        p_value = result[1]
        
        # Cek apakah data sudah stasioner
        if p_value < alpha:
            break  # Keluar dari loop jika data sudah stasioner
        
        # Tambahkan 1 ke d
        d += 1
    return {
    "Best AIC": best_aic,
    "Best BIC": best_bic,
    "Best p": best_p,
    "Best q": best_q,
    "Best d": d}

if __name__ =="__main__":
    data = pd.DataFrame({'A': [1, 2, 3, 1000, 5], 'B': [10, 20, 30, 400, 50]})
    result = detect_outlier_zscore(data, threshold=2)
    print(result)