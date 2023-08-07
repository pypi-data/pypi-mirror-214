from .metrics import MetricsCalculation
from .mos_config import SimulationSettings, Strategy
from .utils.enums import CalculationTypeEnum
from .validations import TypeValidation


BDAY_METRICS = [("LEVEL", "EXRT"),
                ("LEVEL", "ABSOLUTE"),
                ("LEVEL", "ABSOLUTE_BMK"),
                ("PERFORMANCE", "ABSOLUTE"),
                ("PERFORMANCE", "ABSOLUTE_BMK"),
                ("PERFORMANCE", "RELATIVE"),
                ("SIMPLE", "NUM_CONS"),
                ("SIMPLE", "NUM_CONS_BMK"),
                ("TURNOVER", "STANDARD")
                ]

REBAL_METRICS = [("OPTIMIZER_RESULT", "TAX_BY_GROUP_FULL_PORTFOLIO"),
                 ("OPTIMIZER_RESULT", "PORTFOLIO_SUMMARY"),
                 ("OPTIMIZER_RESULT", "OPTIMIZATION_STATUS"),
                 ("OPTIMIZER_RESULT", "TRADE_LIST"),
                 ("OPTIMIZER_RESULT", "ASSET_DETAILS"),
                 ("OPTIMIZER_RESULT", "PROFILE_DIAGNOSTICS"),
                 ("OPTIMIZER_RESULT", "INPUT_DATA_ERRORS")
                 ]


class Profile:
    """
    A profile request definition (also referred to as profile) contains all information required to construct a portfolio using the defined strategy on a specific date or to run a backtest over a period of time.

    Args:
        strategy (Strategy): Strategy definition containing universe, optimization settings, etc.
        simulation_settings (SimulationSettings): Settings containing type of calculation and date range.
        metrics_calculation (MetricsCalculation): (optional) Metrics as per calculation type. 
        
        Default for REBALANCE:
            ``[("OPTIMIZER_RESULT", "TAX_BY_GROUP_FULL_PORTFOLIO"),
            ("OPTIMIZER_RESULT", "PORTFOLIO_SUMMARY"),
            ("OPTIMIZER_RESULT", "OPTIMIZATION_STATUS"),
            ("OPTIMIZER_RESULT", "TRADE_LIST"),
            ("OPTIMIZER_RESULT", "ASSET_DETAILS"),
            ("OPTIMIZER_RESULT", "PROFILE_DIAGNOSTICS"),
            ("OPTIMIZER_RESULT", "INPUT_DATA_ERRORS")]``
        
        Default for BACKCALCULATION :
            ``[("OPTIMIZER_RESULT", "TAX_BY_GROUP_FULL_PORTFOLIO"),
            ("OPTIMIZER_RESULT", "PORTFOLIO_SUMMARY"),
            ("OPTIMIZER_RESULT", "OPTIMIZATION_STATUS"),
            ("OPTIMIZER_RESULT", "TRADE_LIST"),
            ("OPTIMIZER_RESULT", "ASSET_DETAILS"),
            ("OPTIMIZER_RESULT", "PROFILE_DIAGNOSTICS"),
            ("OPTIMIZER_RESULT", "INPUT_DATA_ERRORS"),
            ("LEVEL", "EXRT"),
            ("LEVEL", "ABSOLUTE"),
            ("LEVEL", "ABSOLUTE_BMK"),
            ("PERFORMANCE", "ABSOLUTE"),
            ("PERFORMANCE", "ABSOLUTE_BMK"),
            ("PERFORMANCE", "RELATIVE"),
            ("SIMPLE", "NUM_CONS"),
            ("SIMPLE", "NUM_CONS_BMK"),
            ("TURNOVER", "STANDARD")]``
        
        Default for Other calc types :
            ``[("LEVEL", "EXRT"),
            ("LEVEL", "ABSOLUTE"),
            ("LEVEL", "ABSOLUTE_BMK"),
            ("PERFORMANCE", "ABSOLUTE"),
            ("PERFORMANCE", "ABSOLUTE_BMK"),
            ("PERFORMANCE", "RELATIVE"),
            ("SIMPLE", "NUM_CONS"),
            ("SIMPLE", "NUM_CONS_BMK"),
            ("TURNOVER", "STANDARD")]``

    Returns:
            body (dict): Dictionary representation of Profile.
    """

    strategy = TypeValidation('strategy', Strategy, mandatory=True)
    simulation_settings = TypeValidation('simulation_settings', SimulationSettings, mandatory=True)
    metrics_calculation = TypeValidation('metrics_calculation', MetricsCalculation)

    def __init__(
            self,
            strategy,
            simulation_settings,
            metrics_calculation = None,
            profile_id=None,
            profile_name=None
    ):
        self.strategy = strategy
        self.simulation_settings = simulation_settings
        self.profile_id = profile_id
        self.profile_name = profile_name

        if metrics_calculation is None:
            metrics_calculation = MetricsCalculation()

        self.metrics_calculation = metrics_calculation

        # change metric list based on calc type
        if metrics_calculation is not None and isinstance(metrics_calculation, MetricsCalculation):
            if simulation_settings is not None and isinstance(simulation_settings, SimulationSettings):
                if metrics_calculation.metric_list is None:
                    if simulation_settings.calculation_type == CalculationTypeEnum.REBALANCE:
                        metrics_calculation.metric_list = REBAL_METRICS
                    elif simulation_settings.calculation_type in (CalculationTypeEnum.BACKCALCULATION, CalculationTypeEnum.SIMULATION):
                        metrics_calculation.metric_list = REBAL_METRICS + BDAY_METRICS
                    else:
                        metrics_calculation.metric_list = BDAY_METRICS

    @property
    def body(self):
        """
         Method to generate request body as dictionary based on the parameters configured.

        Returns:
            dict: Dictionary representation of the profile.
        """
        strategy_input = {
            "strategyDefinition": {
                "values": [self.strategy.body],
                "objType": "StrategyDefinitions",
            }
        }

        profile = {
            # "id": self.profile_id,
            "rebasingEnabled": None,
            "debugOptions": None,
            "requestInfo": None,
            "calculationContext": None,
            "strategyInput": strategy_input,
            "simulationSettings": self.simulation_settings.body,
            "solutionSettings": None,
            "metricsCalculation": self.metrics_calculation.body if self.metrics_calculation is not None else None,
        }

        if self.profile_name:
            profile["requestInfo"] = {"name": self.profile_name}

        return profile

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.__dict__}>"
