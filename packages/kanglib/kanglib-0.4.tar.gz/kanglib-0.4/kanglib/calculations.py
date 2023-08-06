import pandas as pd

def calculate_weighted_value(df: pd.DataFrame, columns: list, weights_column: str, result_column: str) -> pd.DataFrame:
    
    """
    This function calculates a weighted value in a DataFrame.

    Parameters:
    df (pd.DataFrame): The input DataFrame.
    columns (list): List of column names to be multiplied.
    weights_column (str): Column name for the weights.
    result_column (str): Column name for the result.

    Returns:
    pd.DataFrame: DataFrame with the result column updated.
    """
    # calculate_weighted_value 计算加权值

    df[result_column] = df[columns].prod(axis=1) * df[weights_column]
    return df
