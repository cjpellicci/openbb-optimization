"""Router for openbb_optimization module."""

from typing import List

from openbb_core.app.router import Router
from openbb_core.app.model.obbject import OBBject
from openbb_optimization.aggregator import _aggregate_asset_data
from openbb_optimization.features.mean_variance import _mpt_optimize
from openbb_optimization.models.optimizer_query_params import OptimizerQueryParams
from openbb_optimization.models.optimizer_result import OptimizerResult

router = Router(prefix="", description="Portfolio optimization tools.")


@router.command()
async def mean_variance(
    symbols: List[str],
    start_date: str = None,
    end_date: str = None,
    risk_free_rate: float = 0.0,
    max_weight: float = 1.0,
) -> OBBject[OptimizerResult]:
    """
    Mean-variance optimization command.
    """
    params = OptimizerQueryParams(
        symbols=symbols,
        start_date=start_date,
        end_date=end_date,
        risk_free_rate=risk_free_rate,
        max_weight=max_weight,
    )

    # Fetch combined data
    df = await _aggregate_asset_data(params)
    # Run optimization
    result = await _mpt_optimize(df, params)

    return OBBject(results=result)
