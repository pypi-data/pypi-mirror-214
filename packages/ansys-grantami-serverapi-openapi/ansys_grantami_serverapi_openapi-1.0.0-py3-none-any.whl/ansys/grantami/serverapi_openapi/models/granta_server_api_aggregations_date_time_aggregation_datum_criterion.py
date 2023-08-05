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

from ansys.grantami.serverapi_openapi.models.granta_server_api_aggregations_aggregation_datum_criterion import GrantaServerApiAggregationsAggregationDatumCriterion  # noqa: F401,E501

class GrantaServerApiAggregationsDateTimeAggregationDatumCriterion(GrantaServerApiAggregationsAggregationDatumCriterion):
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
        'type': 'str'
    }
    if hasattr(GrantaServerApiAggregationsAggregationDatumCriterion, "swagger_types"):
        swagger_types.update(GrantaServerApiAggregationsAggregationDatumCriterion.swagger_types)

    attribute_map = {
        'type': 'type'
    }
    if hasattr(GrantaServerApiAggregationsAggregationDatumCriterion, "attribute_map"):
        attribute_map.update(GrantaServerApiAggregationsAggregationDatumCriterion.attribute_map)

    subtype_mapping = {
    }


    def __init__(self, type='dateTime', *args, **kwargs):  # noqa: E501
        """GrantaServerApiAggregationsDateTimeAggregationDatumCriterion - a model defined in Swagger"""  # noqa: E501
        GrantaServerApiAggregationsAggregationDatumCriterion.__init__(self, *args, **kwargs)
        self._type = None
        self.discriminator = None
        self.type = type

    @property
    def type(self):
        """Gets the type of this GrantaServerApiAggregationsDateTimeAggregationDatumCriterion.  # noqa: E501

        :return: The type of this GrantaServerApiAggregationsDateTimeAggregationDatumCriterion.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this GrantaServerApiAggregationsDateTimeAggregationDatumCriterion.

        :param type: The type of this GrantaServerApiAggregationsDateTimeAggregationDatumCriterion.  # noqa: E501
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501
        self._type = type

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
        if issubclass(GrantaServerApiAggregationsDateTimeAggregationDatumCriterion, dict):
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
        if not isinstance(other, GrantaServerApiAggregationsDateTimeAggregationDatumCriterion):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
