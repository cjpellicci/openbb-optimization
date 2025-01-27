"""Helper functions for fetching asset data"""

import numpy as np
import pandas as pd
from typing import Tuple, List
from openbb_core.app.model.obbject import OBBject
from openbb_optimization.models.optimizer_query_params import OptimizerQueryParams

async def _fetch_equity_price_df(
    symbol: str,
    params: OptimizerQueryParams
) -> Tuple[pd.DataFrame, List[str]]:
    """
    Fetch equity price data.

    Parameters
    ----------
    symbol : str
        Ticker symbol
    params : OptimizerQueryParams
        Query parameters including dates
        
    Returns
    -------
    Tuple[pd.DataFrame, List[str]]
        DataFrame with processed price data and list of any warnings
    """
    from openbb import obb # pylint: disable=import-outside-toplevel
    data: OBBject = obb.equity.price.historical(
        symbol=symbol,
        start_date=params.start_date,
        end_date=params.end_date
    )
    
    warnings = []
    
    # Check for any warnings from the provider
    if data.warnings:
        warnings.extend(data.warnings)
        
    # Check if we got any data
    if not data.results:
        warnings.append(f"No data returned for {symbol} (equity)")    
        return pd.DataFrame(), warnings
    
    df = data.to_dataframe()
    
    # Check provider metadata
    if data.provider:
        warnings.append(f"Data for {symbol} (equity) sourced from {data.provider}")
        
    # Access any extra metadata
    if data.extra and "metadata" in data.extra:
        metadata = data.extra["metadata"]
        if "data_quality" in metadata:
            warnings.append(f"Data quality for {symbol} (equity): {metadata['data_quality']}")
            
    return _process_price_df(data.to_dataframe(), symbol), warnings

async def _fetch_fixed_income_data():
    pass

async def _fetch_currency_data():
    pass

def _process_price_df(df: pd.DataFrame, symbol: str) -> pd.DataFrame:
    """
    Process raw price data into format needed for optimization.
    
    Parameters
    ----------
    df : pd.DataFrame
        Raw price data
    symbol : str
        Ticker symbol for column naming
        
    Returns
    -------
    pd.DataFrame
        Processed price data with single column named by symbol
    """
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(inplace=True)
    df = df.astype(float)
    df.rename(columns={"close": symbol}, inplace=True)
    return df[[symbol]]

def _combine_price_dfs(frames: List[pd.DataFrame]) -> pd.DataFrame:
    """
    Combine multiple price series into single dataframe.
    
    Parameters
    ----------
    frames : List[pd.DataFrame]
        List of single-column dataframes to combine
        
    Returns
    -------
    pd.DataFrame
        Combined price data with aligned dates
    """
    if not frames:
        raise ValueError("No valid price data frames provided")
    
    combined_df = pd.concat(frames, axis=1, join="outer")
    combined_df.replace([np.inf, -np.inf], np.nan, inplace=True)
    combined_df.dropna(how="any", inplace=True)
    
    if combined_df.empty:
        raise ValueError("No valid overlapping data after combining price series")
        
    return combined_df