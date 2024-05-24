import pandas as pd


def preprocess_data(df):
    """
    Convert columns with mixed data types to numerical.

    Parameters:
    df (pandas DataFrame): DataFrame to preprocess.

    Returns:
    pandas DataFrame: DataFrame with columns converted to numerical.
    """
    df_processed = df.copy()

    # Replace non-numeric values with NaN
    for column in df_processed.columns:
        df_processed[column] = pd.to_numeric(df_processed[column], errors='coerce')

    return df_processed.fillna(0.0)
