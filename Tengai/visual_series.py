import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Any

def lineplot_features(data:pd.DataFrame) -> Any:
    """
    this function for visual line from data
    Args:
        data (pd.DataFrame): _description_
    """
    n_col = len(data.columns)
    n_row = min(data.shape[1],1)
    
    fig, ax = plt.subplots(n_row,n_col,figsize=(12,6))
    
    for i,feat in enumerate(data.columns):
        sns.lineplot(data[feat],ax=ax[i])
        ax[i].set_xlabel(f"{feat}")
    plt.suptitle("Line Plot feature dataFrames")


def lineplot_resample_feature(data: pd.DataFrame, on_feat: str, rule: str) -> None:
    # Resample data
    resample_data = data.resample(rule, on=on_feat).sum()

    # Calculate the number of features
    n_features = len(data.columns) - 1  # Subtract 1 for 'on_feat'
    n_col = min(n_features, 2)
    n_row = n_features // (n_col)

    # Setting up the figure for plotting
    fig, ax = plt.subplots(n_row + 1, n_col, figsize=(15, 6))

    for i, feat in enumerate(data.columns.drop(on_feat)):
        sns.lineplot(x=resample_data.index, y=resample_data[feat], ax=ax[i // 2, i % 2])
        ax[i // 2, i % 2].set_xlabel(on_feat)
        ax[i // 2, i % 2].set_ylabel(f"{feat}")

    # deactivate plot no useage
    for i in range(n_features, (n_row + 1) * n_col):
        fig.delaxes(ax[i // n_col, i % n_col])

    # Adjust the layout and title
    plt.tight_layout()
    plt.suptitle("Line Plot Resampled Dataframes", fontsize=15)
    plt.show()
    

def avarange_genarating_barplot(data:pd.DataFrame,on_feat:str):
    # how to mean in Dataframe order by on_feat
    numeric_feat = data.columns.drop(on_feat)
    mean_data = data.groupby(data[on_feat].dt.hour)[numeric_feat].mean().reset_index()
    # setting figure
    n_features = len(data.columns) - 1
    n_col = min(n_features, 2)
    n_row = n_features // (n_col)

    fig, ax = plt.subplots(n_row + 1, n_col, figsize=(20, 10))

    for i, feat in enumerate(numeric_feat):
        ax[i // 2, i % 2].bar(mean_data[on_feat].astype(str), mean_data[feat])
        # Find maximum value and its index
        max_val = mean_data[feat].max()
        max_idx = mean_data[mean_data[feat] == max_val].index[0]  # Use .index[0] to get the first occurrence
        rects = ax[i // 2, i % 2].containers[0]
        
        for j, rect in enumerate(rects):
            if j == max_idx:
                rect.set_color('red')
            else:
                rect.set_color('skyblue')
            ax[i // 2, i % 2].annotate(f'{mean_data[feat][j]:.2f}', 
                                       xy=(rect.get_x() + rect.get_width() / 2, rect.get_height()),
                                       xytext=(0, 3), textcoords='offset points', ha='center', va='bottom',
                                       color='black')
        ax[i // 2, i % 2].set_xlabel(on_feat)
        ax[i // 2, i % 2].set_ylabel(f"Mean of {feat}")
        ax[i // 2, i % 2].grid(axis='y', linestyle='--', alpha=0.7)
    # Turn off empty subplots
    for i in range(n_features, n_row * n_col):
        fig.delaxes(ax[i // n_col, i % n_col])

    # Rotate x-axis labels for readability
    plt.xticks(rotation=45)  
    plt.tight_layout()
    plt.show()