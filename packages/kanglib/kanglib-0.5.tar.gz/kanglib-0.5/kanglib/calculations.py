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


    这个函数计算一个DataFrame中的加权值。

    参数:
    df (pd.DataFrame): 输入的DataFrame。
    columns (list): 需要被乘的列的名称列表。
    weights_column (str): 权重列的名称。
    result_column (str): 结果列的名称。

    返回:
    pd.DataFrame: 更新了结果列的DataFrame。

    示例:
    >>> import pandas as pd
    >>> import kanglib
    >>> import matplotlib.pyplot as plt
    >>> import numpy as np
    >>> dates = pd.date_range(start='2022-01-01', periods=365*2)
    >>> activity_levels_df = pd.DataFrame({
    >>>     'date': dates,
    >>>     'activity_level': np.random.rand(len(dates))
    >>> })
    >>> weights_df = pd.DataFrame({
    >>>     'date': dates,
    >>>     'weight': np.random.rand(len(dates))
    >>> })
    >>> df = pd.merge(activity_levels_df, weights_df, on='date')
    >>> df = kanglib.calculate_weighted_value(df, ['activity_level'], 'weight', 'result')
    >>> print(df)
    """
    
    # calculate_weighted_value 计算加权值

    df[result_column] = df[columns].prod(axis=1) * df[weights_column]
    return df
