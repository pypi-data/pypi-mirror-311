import os
import json
import random
import pandas as pd
import numpy as np
from fastai.tabular.all import torch


def set_seed(random_seed: int = 123456):
    random.seed(random_seed)
    np.random.seed(random_seed)
    torch.manual_seed(random_seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(random_seed)


def makedirs(dirname: str):
    os.makedirs(dirname, exist_ok=True)


def exists(path: str):
    return os.path.exists(path)


def load_json_dict(filepath: str) -> dict:
    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            loaded_dict = json.load(file)
            return loaded_dict
    return {}


def rel_to_abs_path(rel_path):
    return os.path.abspath(rel_path)


def check_high_correlation(df, threshold=0.9):
    """
    Check if any features in the DataFrame are strongly correlated.

    Parameters:
    df (pd.DataFrame): Input DataFrame
    threshold (float): Correlation threshold to consider as strong (default=0.9)

    Returns:
    None: Prints a warning with strongly correlated features if any are found.
    """
    numeric_df = df.select_dtypes(include=["number"])

    # Compute the correlation matrix
    corr_matrix = numeric_df.corr().abs()  # Use absolute correlation values

    # Create a mask to ignore the diagonal and duplicate pairs
    mask = np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)

    # Extract strongly correlated feature pairs
    high_corr_pairs = [
        (numeric_df.columns[i], numeric_df.columns[j], corr_matrix.iloc[i, j])
        for i in range(len(corr_matrix.columns))
        for j in range(len(corr_matrix.columns))
        if mask[i, j] and corr_matrix.iloc[i, j] > threshold
    ]

    # Display warnings if high correlations are found
    if high_corr_pairs:
        print("Warning: The following features are strongly correlated:")
        for f1, f2, corr_value in high_corr_pairs:
            print(f"  - {f1} and {f2} (Correlation: {corr_value:.2f})")
    else:
        print("No strong correlations found.")
