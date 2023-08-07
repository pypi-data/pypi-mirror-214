import copy
import pandas as pd
from .utils.enums import CalculationTypeEnum, TriggerCalendarEnum
from .validations import TypeValidation, StringDateFormat
from .client_portfolio import CashPortfolio, ClientPortfolio


class SimulationSettings:
    """
    Service to define the job type and date range for running the optimization.

    Args:
        analysis_date (str): The date in YYYY-MM-DD format for which the account is being rebalanced; do not set with from_date.
        from_date (str): The starting date in YYYY-MM-DD format for a simulation; do not set with analysis_date.
        to_date (str): The ending date in YYYY-MM-DD format for a simulation; do not set with analysis_date.
        calculation_type (CalculationTypeEnum): (optional) Use to specify behavior of the calculation. The following options are available:

                    •REBALANCE - (default) rebalance a portfolio for one day only. Use the latest available portfolio given the date of calculation.
                    •SIMULATION - compute a time series of portfolio using the latest available portfolio given the first day of calculation. Skip last rebalancing.
                    •EOD/BACKCALCULATION - compute a time series of portfolio using the portfolio at the day of the calculation. Fail if not present. Perform last rebalancing.

    Returns:
            None

    """
    analysis_date = StringDateFormat('analysis_date')
    calculation_type = TypeValidation('calculation_type', CalculationTypeEnum)
    from_date = StringDateFormat('from_date')
    to_date = StringDateFormat('to_date')

    def __init__(self, analysis_date=None, calculation_type=CalculationTypeEnum.REBALANCE, from_date=None,
                 to_date=None):

        self._validate_calc_dates(analysis_date, calculation_type, from_date, to_date)

        self.calculation_type = calculation_type
        self.analysis_date = analysis_date
        self.from_date = from_date
        self.to_date = to_date

        self.calculation_currency = "USD"
        self.calendar_name = None

    def _validate_calc_dates(self, analysis_date, calculation_type, from_date, to_date):
        if from_date and analysis_date:
            raise ValueError('Both analysis_date and from_date specified, please pass one or the other')
        if calculation_type == CalculationTypeEnum.REBALANCE:
            if analysis_date is None:
                raise ValueError("analysis_date should be provided in calculationType REBALANCE")
        if calculation_type in (
                CalculationTypeEnum.EOD, CalculationTypeEnum.BACKCALCULATION, CalculationTypeEnum.SIMULATION):
            if from_date is None or to_date is None:
                raise ValueError(
                    "From date and To date should be provided in calculationType EOD/BACKCALCULATION/SIMULATION")

    @property
    def body(self):
        """
        Dictionary representation of Simulation settings.

        Returns:
            dict: Dictionary representation of the node.
        """
        if self.calculation_type == CalculationTypeEnum.REBALANCE:
            date_settings = {
                "objType": "AnalysisDate",
                "value": self.analysis_date,
            }
        else:
            date_settings = {
                "fromDate": self.from_date,
                "toDate": self.to_date,
                "objType": "DateRange",
            }

        return {
            "calculationCurrency": self.calculation_currency,
            "dateSettings": date_settings,
            "asAtDate": None,
            "calendarName": self.calendar_name,
            "region": None,
            "maxGap": None,
            "calculationType": self.calculation_type.value,
        }


class ReferenceUniverse:
    """
    ReferenceUniverse holds the universe, benchmark and portfolio for a strategy.

    Args:
        universe (List[Portfolio,pd.Dataframe]) : (optional) Universe portfolio, which is the list of all assets eligible for consideration for inclusion in a portfolio. You can use an existing saved portfolio or benchmark to define the universe. Default value is ['UNX000000034908161'].
        benchmark (List[pd.Dataframe]) : (optional) Benchmark for the optimization. Default value is ['UNX000000034908161'].
        portfolio (Portfolio): (optional) Client portfolio object or cash portfolio. Default value is CashPortfolio.

    Returns:
            None
    """

    universe = TypeValidation('universe', list)
    benchmark = TypeValidation('benchmark', list)

    def __init__(
            self,
            universe: list = None,
            benchmark: list = None,
            portfolio=CashPortfolio()
    ):
        """"""
        # universe can take a list of universes, and be constructed from a benchmark or
        # user portfolio

        self.universe = universe
        self.benchmark = benchmark

        if universe and not isinstance(universe, list):
            raise TypeError("Universe must be list of Dataframes or client portfolios.")

        if benchmark and not isinstance(benchmark, list):
            raise TypeError("Benchmark  must be list of Dataframes or client portfolios.")

        self.universe = self.__get_univ(universe) if universe else ['UNX000000034908161']

        self.benchmark = self.__get_univ(benchmark) if benchmark else ['UNX000000034908161']

        self.portfolio = portfolio
        self.ref_univ_id = "BaseRefUniverse"
        self.benchmark_ref_name = "BaseBenchmark"
        self.universe_ref_name = "BaseUniverse"

    @property
    def body(self):
        """
        Dictionary representation of Reference Universe settings.

        Returns:
            dict: Dictionary representation of the node.
        """

        universe = self.__get_universe_body()

        current_portfolio = self.portfolio.body

        reference_benchmark = self.__get_benchmark_univ_body()

        reference_universe = {
            "referenceUniverseId": self.ref_univ_id,
            "universe": universe,
            "currentPortfolio": current_portfolio,
            "referenceBenchmark": reference_benchmark,
        }
        return reference_universe

    def __get_universe_body(self):
        """
        Form universe body depending on if universe is a client portfolio or MDSUID dataframe.
        """

        univ_body = []
        for univ in self.universe:
            if self.is_client_port_univ(univ):
                univ_dict = {
                    "objType": "UniverseFromPortfolio",
                    "portfolioSearchInput": {}
                }
                univ_body.append(self.__update_univ_as_client_port(ref_dict=univ_dict, univ=univ))

            else:
                univ_dict = {
                    "objType": "UniverseFromPortfolio",
                    "portfolioSearchInput": {
                        "objType": "PortfolioSearchInput",
                        "identification": {
                            "objType": "SimpleIdentification",
                            "source": "PAT",
                        },
                    },
                }

                univ_body.append(self.__update_univ_dict(ref_dict=univ_dict, univ=univ))

        return univ_body

    def is_client_port_univ(self, field):
        """
        Check if the universe is a list of client portfolios. If yes set univ_as_client_port = True.
        """
        univ_as_client_port = False
        if isinstance(field, ClientPortfolio):
            univ_as_client_port = True
        return univ_as_client_port

    def is_df_univ(self, field):
        """
        Check if the universe is a list of dataframes. If yes set is_df_univ = True.
        """
        is_univ_df = False
        if isinstance(field, pd.DataFrame):
            is_univ_df = True
        return is_univ_df

    def __get_univ(self, universe):
        """
        Get a list of MDSUID from dataframe.
        """
        univ_list = []
        for univ in universe:
            if self.is_df_univ(univ):
                univ_list.extend(univ['mdsId'].to_list())
            elif self.is_client_port_univ(univ):
                univ_list.append(univ)
            else:
                raise TypeError("Benchmark/Universe must be list of Dataframes or client portfolios.")

        return univ_list

    def __update_univ_dict(self, ref_dict, univ):
        """
        Update universe body if universe is MDSUID.
        """

        __dict_copy = copy.deepcopy(ref_dict)
        __dict_copy.get("portfolioSearchInput").get("identification").update(
            {"portfolioId": univ, "name": univ})
        return __dict_copy

    def __update_univ_as_client_port(self, ref_dict, univ):
        """
        Update universe body if universe is client portfolio.
        """
        __dict_copy = copy.deepcopy(ref_dict)
        __dict_copy.get("portfolioSearchInput").update(univ.body)
        return __dict_copy

    def __get_benchmark_univ_body(self):
        """
        Form benchmark body.
        """
        bench_body = []
        benchmark_name = f"{self.benchmark_ref_name}"

        for index, bench in enumerate(self.benchmark, start=1):

            if len(self.benchmark) > 1:
                benchmark_name = f"{self.benchmark_ref_name}_{index}"

            if self.is_client_port_univ(bench):
                benchmark_dict = {
                    "benchmarkRefName": benchmark_name,
                    "portfolioSearchInput": {}
                }
                bench_body.append(self.__update_univ_as_client_port(ref_dict=benchmark_dict, univ=bench))

            else:
                benchmark_dict = {
                    "benchmarkRefName": benchmark_name,
                    "portfolioSearchInput": {
                        "objType": "PortfolioSearchInput",
                        "identification": {
                            "objType": "SimpleIdentification",
                            "source": "PAT",
                        },
                    },
                }

                bench_body.append(self.__update_univ_dict(ref_dict=benchmark_dict, univ=bench))
        return bench_body


    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.__dict__}>"


class Strategy:
    """
    Service to create a strategy definition where you can further add the optimization settings, reference universe, optimization methodology and so on.

    Args:
        ref_universe (ReferenceUniverse): Defines the universe and set of benchmarks for the strategy to work with.
        node_list (List): List of nodes to add.
        trigger_calendar (TriggerCalendarEnum): (optional) TriggerCalendar to trigger rebalances based on a regular calendar. Default value is FIRST_DAY_OF_MONTH.

    Returns:
            None

    """

    ref_universe = TypeValidation('ref_universe', ReferenceUniverse, mandatory=True)
    node_list = TypeValidation('node_list', list, mandatory=True)
    trigger_calendar = TypeValidation('trigger_calendar', TriggerCalendarEnum)

    def __init__(self, ref_universe, node_list, trigger_calendar=TriggerCalendarEnum.FIRST_DAY_OF_MONTH):
        self.ref_universe = ref_universe
        self.trigger_calendar = trigger_calendar
        self.node_list = node_list

    @property
    def body(self):
        """
        Dictionary representation of Strategy settings.

        Returns:
            dict: Dictionary representation of the node.
        """
        problem_formulation = [n.body for n in self.node_list]
        strategy = {
            "trigger": {"objType": "TriggerCalendar", "calendar": self.trigger_calendar.value},
            "problemFormulation": problem_formulation,
            "referenceUniverse": [
                {"referenceUniverseDefinition": self.ref_universe.body}
            ],
        }
        return strategy
