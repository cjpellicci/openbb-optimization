"""Router for openbb_optimization module."""

from typing import List

from openbb_core.app.router import Router
from openbb_optimization.aggregator import _get_multi_asset_data
from openbb_optimization.features.mean_variance import _mpt_optimize
from openbb_optimization.models.optimizer_query_params import OptimizerQueryParams
from openbb_optimization.models.optimizer_result import OptimizerResult

router = Router(prefix="")

@router.command(
    methods=['POST']
)
async def mean_variance(
    tickers: List[str],
    start_date: str = None,
    end_date: str = None,
    risk_free_rate: float = 0.0,
    max_weight: float = 1.0
) -> OptimizerResult:
    """
    Mean-variance optimization command.
    """
    params = OptimizerQueryParams(
        tickers=tickers,
        start_date=start_date,
        end_date=end_date,
        risk_free_rate=risk_free_rate,
        max_weight=max_weight
    )
    
    # Fetch combined data
    df = await _get_multi_asset_data(params)
    # Run optimization
    result = await _mpt_optimize(df, params)
    
    return result