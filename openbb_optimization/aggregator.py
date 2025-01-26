"""Multi-asset pre-optimization timeseries aggregator"""

import numpy as np
import pandas as pd


from openbb_optimization.models.optimizer_query_params import OptimizerQueryParams


async def _get_multi_asset_data(params: OptimizerQueryParams) -> pd.DataFrame:
    """
    Fetch & combine price data for symbols in params (equities, crypto, etc.).
    Extend as needed to detect asset classes.
    """
    from openbb import obb # pylint: disable=import-outside-toplevel
    frames = []
    for symbol in params.symbols:
        data = obb.equity.price.historical(
            symbol=symbol, start_date=params.start_date, end_date=params.end_date
        )
        df = data.to_dataframe().astype(float)
        df.rename(columns={"close": symbol}, inplace=True)
        
        frames.append(df[[symbol]])
    combined_df = pd.concat(frames, axis=1, join="outer")
    combined_df.replace([np.inf, -np.inf], np.nan, inplace=True)
    combined_df.dropna(how="any", inplace=True)

    return combined_df
