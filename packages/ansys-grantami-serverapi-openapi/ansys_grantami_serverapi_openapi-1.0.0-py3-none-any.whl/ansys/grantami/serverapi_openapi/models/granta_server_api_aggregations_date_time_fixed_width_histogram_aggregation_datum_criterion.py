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

class GrantaServerApiAggregationsDateTimeFixedWidthHistogramAggregationDatumCriterion(GrantaServerApiAggregationsAggregationDatumCriterion):
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
        'interval': 'str',
        'offset': 'str',
        'type': 'str'
    }
    if hasattr(GrantaServerApiAggregationsAggregationDatumCriterion, "swagger_types"):
        swagger_types.update(GrantaServerApiAggregationsAggregationDatumCriterion.swagger_types)

    attribute_map = {
        'interval': 'interval',
        'offset': 'offset',
        'type': 'type'
    }
    if hasattr(GrantaServerApiAggregationsAggregationDatumCriterion, "attribute_map"):
        attribute_map.update(GrantaServerApiAggregationsAggregationDatumCriterion.attribute_map)

    subtype_mapping = {
    }


    def __init__(self, interval=None, offset=None, type='dateTimeFixedWidthHistogram', *args, **kwargs):  # noqa: E501
        """GrantaServerApiAggregationsDateTimeFixedWidthHistogramAggregationDatumCriterion - a model defined in Swagger"""  # noqa: E501
        GrantaServerApiAggregationsAggregationDatumCriterion.__init__(self, *args, **kwargs)
        self._interval = None
        self._offset = None
        self._type = None
        self.discriminator = None
        if interval is not None:
            self.interval = interval
        if offset is not None:
            self.offset = offset
        self.type = type

    @property
    def interval(self):
        """Gets the interval of this GrantaServerApiAggregationsDateTimeFixedWidthHistogramAggregationDatumCriterion.  # noqa: E501
        Fixed size of the resulting histogram buckets, in SI time units. Must be an integer followed by one of the following units: ms (milliseconds), s (seconds), m (minutes), h (hours), d (days)  # noqa: E501

        :return: The interval of this GrantaServerApiAggregationsDateTimeFixedWidthHistogramAggregationDatumCriterion.  # noqa: E501
        :rtype: str
        """
        return self._interval

    @interval.setter
    def interval(self, interval):
        """Sets the interval of this GrantaServerApiAggregationsDateTimeFixedWidthHistogramAggregationDatumCriterion.
        Fixed size of the resulting histogram buckets, in SI time units. Must be an integer followed by one of the following units: ms (milliseconds), s (seconds), m (minutes), h (hours), d (days)  # noqa: E501

        :param interval: The interval of this GrantaServerApiAggregationsDateTimeFixedWidthHistogramAggregationDatumCriterion.  # noqa: E501
        :type: str
        """
        self._interval = interval

    @property
    def offset(self):
        """Gets the offset of this GrantaServerApiAggregationsDateTimeFixedWidthHistogramAggregationDatumCriterion.  # noqa: E501
        Optional offset of the lowest bucket boundary, in SI time units. Must be an integer followed by one of the following units: ms (milliseconds), s (seconds), m (minutes), h (hours), d (days). Defaults to 0. Must be less than the interval. Negative offsets (e.g. \"-6h\") are supported  # noqa: E501

        :return: The offset of this GrantaServerApiAggregationsDateTimeFixedWidthHistogramAggregationDatumCriterion.  # noqa: E501
        :rtype: str
        """
        return self._offset

    @offset.setter
    def offset(self, offset):
        """Sets the offset of this GrantaServerApiAggregationsDateTimeFixedWidthHistogramAggregationDatumCriterion.
        Optional offset of the lowest bucket boundary, in SI time units. Must be an integer followed by one of the following units: ms (milliseconds), s (seconds), m (minutes), h (hours), d (days). Defaults to 0. Must be less than the interval. Negative offsets (e.g. \"-6h\") are supported  # noqa: E501

        :param offset: The offset of this GrantaServerApiAggregationsDateTimeFixedWidthHistogramAggregationDatumCriterion.  # noqa: E501
        :type: str
        """
        self._offset = offset

    @property
    def type(self):
        """Gets the type of this GrantaServerApiAggregationsDateTimeFixedWidthHistogramAggregationDatumCriterion.  # noqa: E501

        :return: The type of this GrantaServerApiAggregationsDateTimeFixedWidthHistogramAggregationDatumCriterion.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this GrantaServerApiAggregationsDateTimeFixedWidthHistogramAggregationDatumCriterion.

        :param type: The type of this GrantaServerApiAggregationsDateTimeFixedWidthHistogramAggregationDatumCriterion.  # noqa: E501
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
        if issubclass(GrantaServerApiAggregationsDateTimeFixedWidthHistogramAggregationDatumCriterion, dict):
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
        if not isinstance(other, GrantaServerApiAggregationsDateTimeFixedWidthHistogramAggregationDatumCriterion):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
