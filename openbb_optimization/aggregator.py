"""Multi-asset pre-optimization timeseries aggregator"""

import pandas as pd
from openbb import obb

from openbb_optimization.models.optimizer_query_params import OptimizerQueryParams


async def _get_multi_asset_data(params: OptimizerQueryParams) -> pd.DataFrame:
    """
    Fetch & combine price data for tickers in params (equities, crypto, etc.).
    Extend as needed to detect asset classes.
    """
    frames = []
    for ticker in params.ticker:
        data = obb.equity.price.historical(
            symbol=ticker, start_date=params.start_date, end_date=params.end_date
        )
        df = data.to_dataframe()
        df.rename(columns={"close": ticker}, inplace=True)
        frames.append(df[[ticker]])
    combined_df = pd.concat(frames, axis=1, join="outer")
    combined_df.dropna(how="all", inplace=True)

    return combined_df
