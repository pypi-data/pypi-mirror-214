from dataclasses import dataclass, field
from typing import Optional, Union
from .utils.enums import TaxArbitrageGainEnum
from .dataclass_validations import BaseDataClassValidator


@dataclass
class CashFlowOptSetting:
    """
    Optimizer setting for cashflows.

    Args:
        amount (int): (optional) Amount of cashflow. Default value is None.
        cash_type (str): (optional) Cashflow type; accepted values are PERCENT or AMOUNT. Default value is PERCENT.

    Returns:
            body (dict): Dictionary representation of CashFlowOptSetting.
    """

    amount: Optional[int] = None
    cash_type: Optional[str] = "PERCENT"

    @property
    def body(self):
        """
        Dictionary representation of CashFlowOptSetting.

        Returns:
            dict: Dictionary representation of the node.
        """
        cash_opt_body = {
            "amount": self.amount,
            "type": self.cash_type
        }
        return cash_opt_body


@dataclass
class TaxOptimizationSetting(BaseDataClassValidator):
    """
    Settings for tax aware optimization.

    Args:
        tax_unit (str): (optional) Unit of tax-related parameters. Allowed values are 'dollar'(for absolute amounts) and 'decimal' (for amounts relative to the base). Default value is 'dollar'
        enable_two_rate (bool): (optional) When set to “true”, taxable tax lots are classified into either long-term or short-term and are taxed accordingly at the same two rates. Default value is True.
        short_term_period (int): (optional) Number of days for a period to be termed short term. Default value is 365.
        long_term_tax_rate (int, float): (optional) Long term tax rate applied to assets.
        short_term_tax_rate (int, float): (optional) Short term tax rate applied to assets.
        wash_sale_rule (str):  (optional) Actions to take for washlots. Allowed values are:
        
                            • ignored – no action taken even if a wash sale occurred
                            • disallowed - (default) wash sales are prevented from happening
                            • tradeoff - wash sales can take place as long as it helps maximize the objective function
                            
        washSalePeriod (int): (optional) Number of days of wash sale period. Default value is 30.
        sellingOrderRule (str): (optional) The order in which to sell from tax lots. Default value is auto. Allowed values are:
        
                            • auto - order in which tax lots are traded for each asset is automatically determined based on the marginal contribution of each tax lot to the objective
                            • hifo - tax lots with fewer gains or more losses are traded before those with more gains and fewer losses
                            • lifo - tax lots bought later are traded before those bought earlier
                            • fifo -tax lots bought earlier are traded before those bought later
                            

    Returns:
            body (dict): Dictionary representation of TaxOptimizationSetting.

    """

    tax_unit: str = "dollar"
    enable_two_rate: bool = True
    short_term_period: int = 365
    long_term_tax_rate: Optional[Union[float, int]] = None
    short_term_tax_rate: Optional[Union[float, int]] = None
    wash_sale_rule: str = "disallowed"
    wash_sale_period: int = 30
    selling_order_rule: str = "auto"

    @property
    def body(self):
        """
        Method to generate request body as dictionary based on the parameters configured.
        Returns:
            dict: Dictionary representation of the node.
        """
        tax_opt_setting_body = {
            "taxUnit": self.tax_unit,
            "enableTwoRate": self.enable_two_rate,
            "shortTermPeriod": self.short_term_period,
            "longTermTaxRate": self.long_term_tax_rate,
            "shortTermTaxRate": self.short_term_tax_rate,
            "washSaleRule": self.wash_sale_rule,
            "washSalePeriod": self.wash_sale_period,
            "sellingOrderRule": self.selling_order_rule
        }
        return tax_opt_setting_body


@dataclass
class OptimizationSettings(BaseDataClassValidator):
    """
    General settings for optimization.

    Args:
        risk_model (str): (optional) Risk model to be used for optimization. Default value is GEMLTL.
        solver (int): (optional) Default value is None
        tax_approach (int): Tax approach
        paring_approach (int): (optional) Asset/trade paring information of the optimal portfolio. Default value is None.
        transaction_type (str): (optional) Transaction type. Default value is None.
        cash_in_portfolio_lower_bound (int, float): (optional) Lower bound to set up cashflow in relation to the portfolio base value.
        cash_in_portfolio_upper_bound (int, float): (optional) Upper bound to set up cashflow in relation to the portfolio base value.
        cash_flow_settings (CashFlowOptSetting): (optional) Settings for the cashflow.
        tax_optimization_setting (TaxOptimizationSetting): (optional) Settings for tax aware optimization – this is optional but required if tax aware optimization.

    Returns:
            body (dict): Dictionary representation of OptimizationSettings.
    """

    risk_model: str = "GEMLTL"
    solver: Optional[int] = None
    tax_approach: Optional[int] = None
    paring_approach: Optional[int] = None
    transaction_type: Optional[str] = None
    cash_in_portfolio_lower_bound: Optional[Union[int, float]] = None
    cash_in_portfolio_upper_bound: Optional[Union[int, float]] = None
    cash_flow_settings: Optional[CashFlowOptSetting] = None
    tax_optimization_setting: Optional[TaxOptimizationSetting] = None

    @property
    def body(self):
        """
        Method to generate request body as dictionary based on the parameters configured.

        Returns:
            dict: Dictionary representation of the node.
        """
        opt_setting_body = {
            "riskModel": self.risk_model,
            "solver": self.solver,
            "taxApproach": self.tax_approach,
            "paringApproach": self.paring_approach,
            "transactionType": self.transaction_type,
            "cashInPortfolioLowerBound": self.cash_in_portfolio_lower_bound,
            "cashInPortfolioUpperBound": self.cash_in_portfolio_upper_bound
        }
        if self.cash_flow_settings is not None:
            opt_setting_body.update({"cashFlowSettings": self.cash_flow_settings.body})
        if self.tax_optimization_setting is not None:
            opt_setting_body.update({"taxOptimizationSettings": self.tax_optimization_setting.body})

        return opt_setting_body


@dataclass
class GenericObjectiveFunction(BaseDataClassValidator):
    """
    Generic objective function for the optimization.

    Args:
        tax_term (int, float):(optional) Multiplier for tax based optimization. Default value is None.
        lossBenefitTerm (int, float):(optional) Default value is None.
        sp_risk_aversion (int, float):(optional) Risk aversion for specific risk. Default value is 0.0075.
        cf_risk_aversion (int, float):(optional) Risk aversion for common factor risk. Default value is 0.0075.
        alpha_attribute (str): (optional) Default value is None.
        alpha_term (int, float): (optional) Default value is None.
        transaction_cost_term (str):(optional) Default value is None.
        minimize_active_risk (bool):(optional) Flag to minimize active risk . Default value is True.
        t_cost_attribute (str): (optional) Datapoint name that contains the transaction cost amount.Default value is None.

    Returns:
            body (dict): Dictionary representation of GenericObjectiveFunction.
    """
    tax_term: Optional[Union[float, int]] = None
    loss_benefit_term: Optional[Union[float, int]] = None
    sp_risk_aversion: Optional[Union[float, int]] = 0.0075
    cf_risk_aversion: Optional[Union[float, int]] = 0.0075
    alpha_attribute: Optional[str] = None
    alpha_term: Optional[Union[int, float]] = None
    transaction_cost_term: Optional[str] = None
    minimize_active_risk: Optional[bool] = None
    t_cost_attribute: Optional[str] = None

    @property
    def body(self):
        """
        Method to generate request body as dictionary based on the parameters configured.

        Returns:
            dict: Dictionary representation of the node.
        """
        gen_obj_body = {
            "objType": "Generic",
            "info": "Generic",
            "taxTerm": self.tax_term,
            "lossBenefitTerm": self.loss_benefit_term,
            "riskAversion": {"specific": self.sp_risk_aversion, "commonFactor": self.cf_risk_aversion},
            "alphaAttribute": self.alpha_attribute,
            "alphaTerm": self.alpha_term,
            "transactionCostTerm": self.transaction_cost_term,
            "minimizeActiveRisk": self.minimize_active_risk,
            "tCostAttribute": self.t_cost_attribute
        }
        return gen_obj_body


@dataclass
class TaxArbitrage(BaseDataClassValidator):
    """
    Place bounds on the net realized capital gain or loss at the portfolio level.

    Args:
        tax_category (str): (optional) Allowed values are longTerm, shortTerm, taxFree. Default value is None.
        gain_type (str): (optional) Allowed values are capitalGain, capitalLoss, capitalNet. Default value 'capitalNet'
        upper_bound (float): (optional) Maximum allowed value for the selected gain/loss. Default value is None.
        lower_bound (float): (optional) Minimum allowed value for the selected gain/loss. Default value is None.

    Returns:
            body (dict): Dictionary representation of TaxArbitrage.
    """

    tax_category: Optional[str] = None
    gain_type: TaxArbitrageGainEnum = TaxArbitrageGainEnum.CAPITAL_NET
    upper_bound: Optional[Union[float, int]] = None
    lower_bound: Optional[Union[float, int]] = None

    @property
    def body(self):
        """
        Method to generate request body as dictionary based on the parameters configured.

        Returns:
            dict: Dictionary representation of the node.
        """
        __body = {
            "taxCategory": self.tax_category,
            "gainType": self.gain_type.value,
            "upperBound": self.upper_bound,
            "lowerBound": self.lower_bound
        }
        return __body


@dataclass
class FullSpecOptimizationNode(BaseDataClassValidator):
    """
    Used for tax optimization and other optimization problems where you are not composing the optimization problem by layers, but rather defining all at once.

    Args:
        opt_settings (OptimizationSettings): (optional) Optimizer setting parameter of type OptimizationSettings.
        objective_function (GenericObjectiveFunction): (optional) Optimizer objectives.
        constraints (list): (optional) List of constraints. Default value is None.
        tax_arbitrages (list): (optional) List of tax arbitrage of type TaxArbitrage. Default value is None.

    Returns:
            body (dict): Dictionary representation of FullSpecOptimizationNode.
    """

    opt_settings: Optional[OptimizationSettings] = field(default_factory=OptimizationSettings)
    objective_function: Optional[GenericObjectiveFunction] = field(default_factory=GenericObjectiveFunction)
    constraints: Optional[list] = None
    tax_arbitrages: Optional[list] = None

    @property
    def body(self):
        """The dictionary structure for MOS Full Optimization node.

        Returns:
            dict: Dictionary representation of the node.
        """

        _body = {
            "node": {
                "active": None,
                "doNotHoldCriteria": None,
                "doNotTradeCriteria": None,
                "hocDate": None,
                "noBuy": None,
                "noSell": None,
                "objType": "Optimization",
                "objectiveFunction": self.objective_function.body,
                "optSettings": self.opt_settings.body,
                "overrideTrigger": None
            },
            "nodeInfo": "Optimization",
        }

        if self.constraints is not None and len(self.constraints) > 0:
            _body.get("node").update({"constraint": [c.body for c in self.constraints]})

        if self.tax_arbitrages is not None and len(self.tax_arbitrages) > 0:
            _body.get("node").update({"taxArbitrage": [a.body for a in self.tax_arbitrages]})

        return _body
