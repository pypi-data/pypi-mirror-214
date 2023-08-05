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


class GrantaServerApiSchemaDiscreteTypesInfo(ModelBase):
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
        'discrete_types': 'list[GrantaServerApiSchemaDiscreteType]'
    }

    attribute_map = {
        'discrete_types': 'discreteTypes'
    }

    subtype_mapping = {
        'discreteTypes': 'GrantaServerApiSchemaDiscreteType'
    }


    def __init__(self, discrete_types=None):  # noqa: E501
        """GrantaServerApiSchemaDiscreteTypesInfo - a model defined in Swagger"""  # noqa: E501
        self._discrete_types = None
        self.discriminator = None
        if discrete_types is not None:
            self.discrete_types = discrete_types

    @property
    def discrete_types(self):
        """Gets the discrete_types of this GrantaServerApiSchemaDiscreteTypesInfo.  # noqa: E501

        :return: The discrete_types of this GrantaServerApiSchemaDiscreteTypesInfo.  # noqa: E501
        :rtype: list[GrantaServerApiSchemaDiscreteType]
        """
        return self._discrete_types

    @discrete_types.setter
    def discrete_types(self, discrete_types):
        """Sets the discrete_types of this GrantaServerApiSchemaDiscreteTypesInfo.

        :param discrete_types: The discrete_types of this GrantaServerApiSchemaDiscreteTypesInfo.  # noqa: E501
        :type: list[GrantaServerApiSchemaDiscreteType]
        """
        self._discrete_types = discrete_types

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
        if issubclass(GrantaServerApiSchemaDiscreteTypesInfo, dict):
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
        if not isinstance(other, GrantaServerApiSchemaDiscreteTypesInfo):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
