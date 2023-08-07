from dataclasses import dataclass
from typing import List, Optional, Union
from .utils.enums import ConstraintScopeEnum
from .full_optimizer_node import TaxArbitrage
from .dataclass_validations import BaseDataClassValidator


@dataclass()
class CategoryOrder(BaseDataClassValidator):
    """
    Allows users to specify a relaxation order for constraint categories to help build constraint hierarchy.

    Args:
        category (str) : Category of the constraint.
        order (str) : Relaxation order; the lower the priority, the earlier the constraint category is relaxed.

    Returns:
            body (dict): Dictionary representation of CategoryOrder constraint.
    """

    category: str
    order: str

    @property
    def body(self):
        """
        Dictionary representation of CategoryOrder constraint.

        Returns:
            dict: Dictionary representation of the constraint.
        """
        body = {
            "category": self.category,
            "order": self.order
        }
        return body


@dataclass()
class GroupBound(BaseDataClassValidator):
    """
    GroupBound constraint

    Args:
        group_field (list) : Category/group of the constraint.
        scope (str) : Scope of the constraint.
        lower_bound (str) : (optional) Lower bound of the constraint. Default value is None.
        upper_bound (str) : (optional) Upper bound of the constraint. Default value is None.
        is_soft (bool) : Specify if the constraint is mandatory or soft. Default value is False.

    Returns:
            body (dict): Dictionary representation of GroupBound constraint.
    """

    group_field: List[str]
    scope: str
    lower_bound: Optional[str] = None
    upper_bound: Optional[str] = None
    is_soft: Optional[bool] = False

    @property
    def body(self):
        """
        Dictionary representation of GroupBound constraint.

        Returns:
            dict: Dictionary representation of the constraint.
        """
        body = {'scope': self.scope,
                'groupField': [a for a in self.group_field],
                'upperBound': self.upper_bound,
                'lowerBound': self.lower_bound,
                'isSoft': self.is_soft
                }
        return body


@dataclass()
class SpecificBound(BaseDataClassValidator):
    """
    SpecificBound constraint

    Args:
        conditional (str) : Indicates if the constraint is conditional.
        scope (str) : Scope of the constraint.
        lower_bound (str) : (optional) Lower bound of the constraint. Default value is None.
        upper_bound (str) : (optional) Upper bound of the constraint. Default value is None.
        is_soft (bool) : Specify if the constraint is mandatory or soft. Default value is False.

    Returns:
            body (dict): Dictionary representation of SpecificBound constraint.
    """

    conditional: str
    scope: str
    lower_bound: Optional[str] = None
    upper_bound: Optional[str] = None
    is_soft: Optional[bool] = False

    @property
    def body(self):
        """
        Dictionary representation of SpecificBound constraint.

        Returns:
            dict: Dictionary representation of the constraint.
        """
        body = {'scope': self.scope,
                'conditional': self.conditional,
                'upperBound': self.upper_bound,
                'lowerBound': self.lower_bound,
                'isSoft': self.is_soft}

        return body


@dataclass()
class OverallBound(BaseDataClassValidator):
    """
    OverallBound constraint

    Args:
        scope (ConstraintScopeEnum) : Scope of the constraint.
        lower_bound (str) : (optional) Lower bound of the constraint. Default value is None.
        upper_bound (str) : (optional) Upper bound of the constraint. Default value is None.
        is_soft (bool) : Specify if the constraint is mandatory or soft. Default value is False.

    Returns:
            body (dict): Dictionary representation of OverallBound constraint.
    """

    scope: ConstraintScopeEnum
    lower_bound: Optional[str] = None
    upper_bound: Optional[str] = None
    is_soft: Optional[bool] = False

    @property
    def body(self):
        """
        Dictionary representation of OverallBound constraint.

        Returns:
            dict: Dictionary representation of the constraint.
        """
        body = {'scope': self.scope.value,
                'lowerBound': self.lower_bound,
                'upperBound': self.upper_bound,
                'isSoft': self.is_soft}

        return body


@dataclass()
class Bounds(BaseDataClassValidator):
    """
    Bounds constraint

    Args:
       overall (List[OverallBound]) : (optional) List of overall bounds. Default value is None.
       groups (List[GroupBound]) : (optional) List of group bounds. Default value is None.
       specific (List[SpecificBound]) : (optional) List of specific bounds. Default value is None.

    Returns:
        body (dict): Dictionary representation of Bounds constraint.
   """

    overall: Optional[List[OverallBound]] = None
    groups: Optional[List[GroupBound]] = None
    specific: Optional[List[SpecificBound]] = None

    @property
    def body(self):
        """
        Dictionary representation of Bounds constraint.

        Returns:
            dict: Dictionary representation of the constraint.
        """
        body = {}
        if self.overall:
            body['overall'] = [a.body for a in self.overall]
        if self.specific:
            body['specific'] = [a.body for a in self.specific]
        if self.groups:
            body['groups'] = [a.body for a in self.groups]

        return body


@dataclass()
class Aggregation(BaseDataClassValidator):
    """
    Aggregation constraint

    Args:
       agg_method (str) : Aggregation method
       weight (str) : Weight

    Returns:
        body (dict): Dictionary representation of Aggregation constraint.
    """

    agg_method: str
    weight: str

    @property
    def body(self):
        """
        Dictionary representation of Aggregation constraint.

        Returns:
            dict: Dictionary representation of the constraint.
        """

        body = {'aggMethod': self.agg_method,
                'weight': self.weight
                }

        return body


@dataclass()
class AssetWeight(BaseDataClassValidator):
    """
    Asset weight for AssetBoundConstraint.

    Args:
       id (str) : Id of Asset.
       weight (int, float) : Weight of Asset.

    Returns:
        body (dict): Dictionary representation of AssetWeight.
    """

    id: str
    weight: Union[int, float]

    @property
    def body(self):
        """
        Dictionary representation of AssetWeight.

        Returns:
            dict: Dictionary representation of AssetWeight.
        """

        body = {
            'id': self.id,
            'weight': self.weight
        }

        return body


@dataclass()
class ConditionalAssetWeight(BaseDataClassValidator):
    """
    Conditional asset weight for AssetBoundConstraint.

    Args:
       condition (str) : Condition for Asset.
       weight (int, float) : Weight of Asset.

    Returns:
        body (dict): Dictionary representation of ConditionalAssetWeight.
    """

    condition: str
    weight: Union[int, float]

    @property
    def body(self):
        """
        Dictionary representation of ConditionalAssetWeight.

        Returns:
            dict: Dictionary representation of ConditionalAssetWeight.
        """

        body = {
            "objType": 'ConditionalAssetsWeight',
            'condition': self.condition,
            'weight': self.weight
        }

        return body


@dataclass()
class AssetTradeSize(BaseDataClassValidator):
    """
    Asset trade size for AssetTradeSizeConstraint.

    Args:
        id (str) : Id of asset.
        trade_value (int, float) : trade size.

    Returns:
        body (dict): Dictionary representation of AssetTradeSize.
    """

    id: str
    trade_value: Union[int, float]

    @property
    def body(self):
        """
        Dictionary representation of AssetTradeSize.

        Returns:
            dict: Dictionary representation of AssetTradeSize.
        """

        body = {
            'assetId': self.id,
            'tradeValue': self.trade_value
        }

        return body


@dataclass
class NetTaxImpact(BaseDataClassValidator):
    """
    Net tax impact settings for TaxConstraint. Specify a lower bound and/or an upper bound on the net tax impact of the portfolio.

    Args:
        id (str) : Id.
        upper_bound (int, float) : If omitted then does not affect the bounds in the net tax impact of optimization.
        lower_bound (int, float) : If omitted then does not affect the bounds in the net tax impact of optimization.

    Returns:
        body (dict): Dictionary representation of NetTaxImpact.
    """

    id: str
    upper_bound: Union[int, float]
    lower_bound: Union[int, float]

    @property
    def body(self):
        """
        Dictionary representation of NetTaxImpact.

        Returns:
            dict: Dictionary representation of NetTaxImpact.
        """

        body = {
            'id': self.id,
            'upperBound': self.upper_bound,
            'lowerBound': self.lower_bound
        }

        return body


class ConstraintFactory:
    """
    Class to represent all constraint nodes.
    """

    @dataclass()
    class RoundLotConstraint(BaseDataClassValidator):
        """
        Allows you to specify a round lot constraint.

        Args:
            lot_size (str): User can provide either 1 for unit lot size for all assets or userdata point for asset level lot size. Default is 1 if userdata is not provided for an asset.
            enforce_closeout (bool): If set to true, lots smaller than the lot size are closed out. Default value is False.
            allow_closeout (bool): If set to true, optimizer may close out a position even if the lot size is below the lot_size. Default value is False.
            is_soft (bool): (optional) Specify if the constraint is mandatory or soft. Default value is False.

        Returns:
            RoundLotConstraint dictionary
        """

        lot_size: Optional[str] = None
        enforce_closeout: Optional[bool] = False
        allow_closeout: Optional[bool] = False
        is_soft: Optional[bool] = False

        @property
        def body(self):
            """
            Dictionary representation of RoundLotConstraint constraint.

            Returns:
                dict: Dictionary representation of the constraint.
            """
            body = {
                "objType": "RoundLotConstraint",
                "lotSize": self.lot_size,
                "enforceOddLotCloseOut": self.enforce_closeout,
                "allowOddLotCloseOut": self.allow_closeout,
                "isSoft": self.is_soft
            }
            return body

    @dataclass()
    class NonCashAssetBound(BaseDataClassValidator):
        """
        Allows you to specify the upper and lower weight bounds for all non-cash assets.

        Args:
            upper_bound (str): Maximum weight that any non-cash asset must have in the optimal portfolio.
            lower_bound (str):  Minimum weight that any non-cash asset must have in the optimal portfolio. If you set a minimum, the optimizer must include these assets and weights, or it will not produce an optimal portfolio.

        Returns:
            NonCashAssetBound dictionary
        """

        upper_bound: str
        lower_bound: str

        @property
        def body(self):
            """
            Dictionary representation of NonCashAssetBound constraint.

            Returns:
                dict: Dictionary representation of the constraint.
            """
            body = {
                "objType": 'NonCashAssetBound',
                "upperBound": self.upper_bound,
                "lowerBound": self.lower_bound
            }
            return body

    @dataclass()
    class GeneralRatioConstraint(BaseDataClassValidator):
        """
        Add a ratio constraint with arbitrary coefficients.

        Args:
            upper_bound (str): Upper bound of the constraint.
            lower_bound (str): Lower bound of the constraint.
            numerator_field (str): Numerator field.
            denominator_field (str): (optional) Denominator field. Default value is None.
        Returns:
            GeneralRatioConstraint dictionary
        """

        upper_bound: str
        lower_bound: str
        numerator_field: str
        denominator_field: Optional[str] = None

        @property
        def body(self):
            """
            Dictionary representation of GeneralRatioConstraint.

            Returns:
                dict: Dictionary representation of the constraint.
            """
            body = {
                "objType": 'GeneralRatioConstraint',
                "upperBound": self.upper_bound,
                "lowerBound": self.lower_bound,
                "numeratorField": self.numerator_field,
                "denominatorField": self.denominator_field,
            }
            return body

    @dataclass()
    class GroupRatio(BaseDataClassValidator):
        """
        Create group level ratio constraint.

        Args:
            field (str): Field
            group_field  (List[str]): List of group fields.
            group_key (str): Group key.

        Returns:
            GroupRatio dictionary
        """

        field: str
        group_field: List[str]
        group_key: str

        @property
        def body(self):
            """
            Dictionary representation of GroupRatio constraint.

            Returns:
                dict: Dictionary representation of the constraint.
            """
            body = {
                "field": self.field,
                "groupField": self.group_field,
                "groupKey": self.group_key,
            }
            return body

    @dataclass()
    class GroupRatioConstraint(BaseDataClassValidator):
        """
        Add a ratio constraint with arbitrary coefficients for group of assets. Both the numerator and the denominator coefficients come from group attributes.

        Args:
            upper_bound (str): Upper bound of the constraint.
            lower_bound (str): Lower bound of the constraint.
            numerator_field (str): Numerator field.
            numerator_group_field (List[str]): Numerator group field.
            numerator_group_key (str): Numerator group key.
            denominator_field (str): (optional) Denominator field. Default value is None.
            denominator_group_field (List[str]): (optional) Denominator group field. Default value is None.
            denominator_group_key (str): (optional) Denominator group key. Default value is None.

        Returns:
            GroupRatioConstraint dictionary

        """

        upper_bound: str
        lower_bound: str
        numerator_field: str
        numerator_group_field: List[str]
        numerator_group_key: str
        denominator_field: Optional[str] = None
        denominator_group_field: Optional[List[str]] = None
        denominator_group_key: Optional[str] = None

        @property
        def body(self):
            """
            Dictionary representation of GroupRatioConstraint constraint.

            Returns:
                dict: Dictionary representation of the constraint.
            """

            numerator_group = ConstraintFactory.GroupRatio(field=self.numerator_field,
                                                           group_field=self.numerator_group_field,
                                                           group_key=self.numerator_group_key).body

            if self.denominator_field is None:
                denominator_group = None
            else:
                denominator_group = ConstraintFactory.GroupRatio(field=self.denominator_field,
                                                                 group_field=self.denominator_group_field,
                                                                 group_key=self.denominator_group_key).body

            body = {
                "objType": 'GroupRatioConstraint',
                "upperBound": self.upper_bound,
                "lowerBound": self.lower_bound,
                "numeratorGroup": numerator_group,
                "denominatorGroup": denominator_group
            }
            return body

    @dataclass()
    class ThresholdConstraint(BaseDataClassValidator):
        """
        Allows you to specify a minimum holding (long) asset weight threshold for all assets in the optimized portfolio.

        Args:
            minimum_holding_level (int, float): Minimum holding level for an asset if it takes on a long position.
            allow_closeout (bool): If set to true, optimizer may close out a position even if the transaction size is below the minimum threshold. Default value is  False.
            enable_grand_father_rule (bool): If set to true, then the grandfather rule is enabled for minimum holding level threshold constraint. Default value is False.
            is_soft (bool): (optional) Specify if the constraint is mandatory or soft. Default value is False.

        Returns:
            ThresholdConstraint dictionary

        """

        minimum_holding_level: Union[int, float]
        allow_closeout: Optional[bool] = False
        enable_grand_father_rule: Optional[bool] = False
        is_soft: Optional[bool] = False

        @property
        def body(self):
            """
            Dictionary representation of ThresholdConstraint.

            Returns:
                dict: Dictionary representation of the constraint.
            """
            body = {
                "objType": 'ThresholdConstraint',
                "allowCloseout": self.allow_closeout,
                "enableGrandfatherRule": self.enable_grand_father_rule,
                "longSide": {'isSoft': self.is_soft, 'minimum': self.minimum_holding_level}
            }
            return body

    @dataclass()
    class AssetTradeSizeConstraint(BaseDataClassValidator):
        """
        Allows you to set upper trade size bound on the specific security.

        Args:
            trade_size_list (List(AssetTradeSize)) : List of assets and the trade size bound.
            is_soft (bool) : (optional) Specify if the constraint is mandatory or soft. Default value is False.

        Returns:
            AssetTradeSizeConstraint dictionary
        """

        trade_size_list: List[AssetTradeSize]
        is_soft: Optional[bool] = False

        @property
        def body(self):
            """
            Dictionary representation of AssetTradeSizeConstraint.

            Returns:
                dict: Dictionary representation of the constraint.
            """
            body = {
                "objType": "AssetTradeSizeConstraint",
                "tradeSize": [a.body for a in self.trade_size_list]
            }
            return body

    @dataclass()
    class NumberOfAssets(BaseDataClassValidator):
        """
        Allows you to specify the minimum and maximum number of assets that the optimized portfolio can have.

        Args:
            min (int): (optional) Minimum number of assets to be held in the portfolio. Default value is None.
            max (int): (optional) Maximum number of assets that can be held in the portfolio. Default value is None.
            is_soft (bool): (optional) Specify if the constraint is mandatory or soft. Default value is False.

        Returns:
            NumberOfAssets dictionary

        """

        min: Optional[int] = None
        max: Optional[int] = None
        is_soft: Optional[bool] = False

        @property
        def body(self):
            """
            Dictionary representation of NumberOfAssets constraint.

            Returns:
                dict: Dictionary representation of the constraint.
            """
            body = {
                "objType": 'NumberOfAssets',
                "min": self.min,
                "max": self.max,
                "isSoft": self.is_soft
            }
            return body

    @dataclass()
    class ConstraintPriority(BaseDataClassValidator):
        """
        Allows you to build a constraint hierarchy. If the problem becomes infeasible, the optimization algorithm will relax the constraints in the specified order until a solution can be found, or infeasibility will be reported.

        Args:
            category_orders (List[CategoryOrder]) : Relaxation order for the categories. If the problem becomes infeasible, the optimization algorithm will relax the constraints in the specified order until a solution is found, or infeasibility will be reported.

        Returns:
            ConstraintPriority dictionary

        """
        category_orders: List[CategoryOrder]

        @property
        def body(self):
            """
            Dictionary representation of ConstraintPriority constraint.

            Returns:
                dict: Dictionary representation of the constraint.
            """
            body = {
                "objType": 'ConstraintPriority',
                "categoryOrders": [a.body for a in self.category_orders],

            }
            return body

    @dataclass()
    class RiskConstraint(BaseDataClassValidator):
        """
        Allows you to specify a target portfolio or active risk for the optimized portfolio.

        Args:
            upper_bound (int, float) : An upper bound on the level of total or active risk for the optimal portfolio.
            use_relative_risk (bool) : If set to true, the upper bound limits the contribution of a particular risk source to the portfolio’s total risk. Should be set as false for tax aware optimization cases. Default value is False.
            risk_source_type (str): Limit total risk, factor risk, or specific risk. Default value is None.
            reference_portfolio (str): If this parameter is set, the risk constraint limits active risk of the optimal portfolio. Default value is None.
            is_soft (bool) : (optional) Specify if the constraint is mandatory or soft. Default value is True.


        Returns:
            RiskConstraint dictionary
        """

        upper_bound: Union[int, float]
        use_relative_risk: bool = False
        risk_source_type: Optional[str] = None
        reference_portfolio: Optional[str] = None
        is_soft: Optional[bool] = True

        @property
        def body(self):
            """
            Dictionary representation of RiskConstraint.

            Returns:
                dict: Dictionary representation of the constraint.
            """
            body = {
                "objType": 'RiskConstraint',
                "upperBound": self.upper_bound,
                "useRelativeRisk": self.use_relative_risk,
                "riskSourceType": self.risk_source_type,
                "referencePortfolio": self.reference_portfolio,
                "isSoft": self.is_soft
            }
            return body

    @dataclass()
    class TransactionCostConstraint(BaseDataClassValidator):
        """
        Allows you to specify an upper bound on the transaction costs(% of portfolio AUM) to be undertaken to arrive at the optimized portfolio.

        Args:
            upper_bound (int, float): Specify the maximum transaction cost the optimizer can incur in constructing an optimal portfolio.
            t_cost_attribute (str): Datapoint name that contains the transaction cost amount.
            is_soft (bool): (optional) Specify if the constraint is mandatory or soft. Default value is False.


        Returns:
            TransactionCostConstraint dictionary
        """

        upper_bound: Union[int, float]
        t_cost_attribute: str
        is_soft: Optional[bool] = False

        @property
        def body(self):
            """
            Dictionary representation of TransactionCostConstraint.

            Returns:
                dict: Dictionary representation of the constraint.
            """
            body = {
                "objType": 'TransactionCostConstraint',
                "upperBound": self.upper_bound,
                "tCostAttribute": self.t_cost_attribute,
                "isSoft": self.is_soft
            }
            return body

    @dataclass()
    class TradabilityConstraint(BaseDataClassValidator):
        """
        Allows you to specify upper and lower bound weight limits relative to the current weight of the asset in the initial portfolio based on the tradability score of the asset in MarketAxess.

        Args:
            required_score (int): Tradability score of the asset in MarketAxess.
            condition (str): (optional) Condition. Default value is None.

        Returns:
            TradabilityConstraint dictionary
        """

        required_score: int
        condition: Optional[str] = None

        @property
        def body(self):
            """
            Dictionary representation of TradabilityConstraint.

            Returns:
                dict: Dictionary representation of the constraint.
            """
            body = {
                "objType": 'TradabilityConstraint',
                "requiredScore": self.required_score,
                "condition": self.condition,
            }
            return body

    @dataclass()
    class TurnoverConstraint(BaseDataClassValidator):
        """
        Allows you to specify an upper bound on the turnover (% of portfolio AUM) to be undertaken to arrive at the optimized portfolio.

        Args:
            upper_bound (int, float): Specify the maximum turnover the optimizer must observe in producing an optimal portfolio.
            is_soft (bool): (optional) Specify if the constraint is mandatory or soft. Default value is False.

        Returns:
            TurnoverConstraint dictionary
        """

        upper_bound: Union[int, float]
        is_soft: Optional[bool] = False

        @property
        def body(self):
            """
            Dictionary representation of TurnoverConstraint.

            Returns:
                dict: Dictionary representation of the constraint.
            """
            body = {
                "objType": 'TurnoverConstraint',
                "upperBound": self.upper_bound,
                "isSoft": self.is_soft
            }
            return body

    @dataclass()
    class AssetBoundConstraint(BaseDataClassValidator):
        """
        Allows you to set asset-level bound for specific assets in the optimal portfolio.

        Args:
            asset_bound_type (ConditionalAssetWeight, List(AssetWeight)) : Asset bound constraint type.

        Returns:
            AssetBoundConstraint dictionary
        """

        asset_bound_type: Union[List[AssetWeight], ConditionalAssetWeight]

        @property
        def body(self):
            """
            Dictionary representation of AssetBoundConstraint.

            Returns:
                dict: Dictionary representation of the constraint.
            """
            body = {
                "objType": 'AssetBoundConstraint',
                "assetBoundConstraintType": {}
            }

            if isinstance(self.asset_bound_type, ConditionalAssetWeight):
                body["assetBoundConstraintType"] = self.asset_bound_type.body
            elif isinstance(self.asset_bound_type, List) and all(
                    isinstance(x, AssetWeight) for x in self.asset_bound_type):
                body["assetBoundConstraintType"]["objType"] = "AssetsWeight"
                body["assetBoundConstraintType"]["assets"] = [n.body for n in self.asset_bound_type]
            return body

    @dataclass()
    class LinearConstraint(BaseDataClassValidator):
        """
        Allows you to specify asset bounds, custom constraint and group constraint on the holdings of the optimized portfolio.

        Args:
            constraint_field  (str): Name of the constraint.
            bounds (Bounds): Minimum and maximum value for the constraint; 3 levels are available: overall, groups, specific.
            aggregation (Aggregation): (optional) Aggregation. Default value is None.

        Returns:
            LinearConstraint dictionary
        """

        constraint_field: str
        bounds: Bounds

        @property
        def body(self):
            """
            Dictionary representation of LinearConstraint.

            Returns:
                dict: Dictionary representation of the constraint.
            """
            body = {
                "objType": 'LinearConstraint',
                "constraintField": self.constraint_field,
                "bounds": self.bounds.body
            }
            return body

    @dataclass()
    class TaxConstraint(BaseDataClassValidator):
        """
        Allows you to specify tax limit and tax settings.

        Args:
            tax_limit  (int, float): (optional) Tax limit.
            min_holding_period (int): (optional) Minimum holding period.
            net_tax_impact (NetTaxImpact): (optional) Specify a lower bound and/or an upper bound on the net tax impact of the portfolio.
            tax_arbitrages (List(TaxArbitrage)): (optional) Net Realized Gain Cap that defines net realize capital gain constraint.

        Returns:
            TaxConstraint dictionary
        """

        tax_limit: Optional[Union[int, float]] = None
        min_holding_period: Optional[int] = None
        net_tax_impact: Optional[NetTaxImpact] = None
        tax_arbitrages: Optional[List[TaxArbitrage]] = None

        @property
        def body(self):
            """
            Dictionary representation of TaxConstraint.

            Returns:
                dict: Dictionary representation of the constraint.
            """
            body = {
                "objType": 'TaxConstraint',
                "taxLimit": self.tax_limit,
                "minHoldingPeriod": self.min_holding_period,
                "netTaxImpact": self.net_tax_impact.body,
                "taxArbitrage": [a.body for a in self.tax_arbitrages]
            }
            return body
