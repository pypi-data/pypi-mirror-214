# coding: utf-8

"""
    MI Server API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401
from . import ModelBase

from ansys.grantami.serverapi_openapi.models.granta_server_api_aggregations_attribute_aggregation_criterion import GrantaServerApiAggregationsAttributeAggregationCriterion  # noqa: F401,E501

class GrantaServerApiAggregationsAttributeAggregationExistsCriterion(GrantaServerApiAggregationsAttributeAggregationCriterion):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'attribute_aggregation_criterion_type': 'str',
        'inner_criterion': 'GrantaServerApiAggregationsAggregationDatumExistsCriterion'
    }
    if hasattr(GrantaServerApiAggregationsAttributeAggregationCriterion, "swagger_types"):
        swagger_types.update(GrantaServerApiAggregationsAttributeAggregationCriterion.swagger_types)

    attribute_map = {
        'attribute_aggregation_criterion_type': 'attributeAggregationCriterionType',
        'inner_criterion': 'innerCriterion'
    }
    if hasattr(GrantaServerApiAggregationsAttributeAggregationCriterion, "attribute_map"):
        attribute_map.update(GrantaServerApiAggregationsAttributeAggregationCriterion.attribute_map)

    subtype_mapping = {
        'innerCriterion': 'GrantaServerApiAggregationsAggregationDatumExistsCriterion'
    }


    def __init__(self, attribute_aggregation_criterion_type='exists', inner_criterion=None, *args, **kwargs):  # noqa: E501
        """GrantaServerApiAggregationsAttributeAggregationExistsCriterion - a model defined in Swagger"""  # noqa: E501
        GrantaServerApiAggregationsAttributeAggregationCriterion.__init__(self, *args, **kwargs)
        self._attribute_aggregation_criterion_type = None
        self._inner_criterion = None
        self.discriminator = None
        self.attribute_aggregation_criterion_type = attribute_aggregation_criterion_type
        if inner_criterion is not None:
            self.inner_criterion = inner_criterion

    @property
    def attribute_aggregation_criterion_type(self):
        """Gets the attribute_aggregation_criterion_type of this GrantaServerApiAggregationsAttributeAggregationExistsCriterion.  # noqa: E501

        :return: The attribute_aggregation_criterion_type of this GrantaServerApiAggregationsAttributeAggregationExistsCriterion.  # noqa: E501
        :rtype: str
        """
        return self._attribute_aggregation_criterion_type

    @attribute_aggregation_criterion_type.setter
    def attribute_aggregation_criterion_type(self, attribute_aggregation_criterion_type):
        """Sets the attribute_aggregation_criterion_type of this GrantaServerApiAggregationsAttributeAggregationExistsCriterion.

        :param attribute_aggregation_criterion_type: The attribute_aggregation_criterion_type of this GrantaServerApiAggregationsAttributeAggregationExistsCriterion.  # noqa: E501
        :type: str
        """
        if attribute_aggregation_criterion_type is None:
            raise ValueError("Invalid value for `attribute_aggregation_criterion_type`, must not be `None`")  # noqa: E501
        self._attribute_aggregation_criterion_type = attribute_aggregation_criterion_type

    @property
    def inner_criterion(self):
        """Gets the inner_criterion of this GrantaServerApiAggregationsAttributeAggregationExistsCriterion.  # noqa: E501

        :return: The inner_criterion of this GrantaServerApiAggregationsAttributeAggregationExistsCriterion.  # noqa: E501
        :rtype: GrantaServerApiAggregationsAggregationDatumExistsCriterion
        """
        return self._inner_criterion

    @inner_criterion.setter
    def inner_criterion(self, inner_criterion):
        """Sets the inner_criterion of this GrantaServerApiAggregationsAttributeAggregationExistsCriterion.

        :param inner_criterion: The inner_criterion of this GrantaServerApiAggregationsAttributeAggregationExistsCriterion.  # noqa: E501
        :type: GrantaServerApiAggregationsAggregationDatumExistsCriterion
        """
        self._inner_criterion = inner_criterion

    def get_real_child_model(self, data):
        """Raises a NotImplementedError for a type without a discriminator defined."""
        raise NotImplementedError()

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr in self.swagger_types.keys():
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(GrantaServerApiAggregationsAttributeAggregationExistsCriterion, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, GrantaServerApiAggregationsAttributeAggregationExistsCriterion):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
