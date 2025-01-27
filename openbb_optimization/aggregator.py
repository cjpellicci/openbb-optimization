"""Multi-asset pre-optimization timeseries aggregator."""

import pandas as pd
from openbb_optimization.models.optimizer_query_params import OptimizerQueryParams
from openbb_optimization.utils.helpers import _fetch_equity_price_df, _combine_price_dfs


from openbb_optimization.models.optimizer_query_params import OptimizerQueryParams


async def _aggregate_asset_data(params: OptimizerQueryParams) -> pd.DataFrame:
    """
    Fetch and combine price data for multiple assets.
    
    Parameters
    ----------
    params : OptimizerQueryParams
        Query parameters including symbols and dates
        
    Returns
    -------
    pd.DataFrame
        Combined price data for all assets
    """
    frames = []
    warnings = []
    
    for symbol in params.symbols:
        df, symbol_warnings = await _fetch_equity_price_df(symbol, params)
        if not df.empty:
            frames.append(df)
        warnings.extend(symbol_warnings)
        
    if not frames:
        raise ValueError("No valid data retrieved for any symbols")
    
    return _combine_price_dfs(frames)