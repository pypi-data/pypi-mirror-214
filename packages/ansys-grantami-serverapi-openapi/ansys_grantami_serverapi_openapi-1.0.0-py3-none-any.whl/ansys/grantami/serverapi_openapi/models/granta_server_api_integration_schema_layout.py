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


class GrantaServerApiIntegrationSchemaLayout(ModelBase):
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
        'name': 'str',
        'attribute_identities': 'list[int]'
    }

    attribute_map = {
        'name': 'name',
        'attribute_identities': 'attributeIdentities'
    }

    subtype_mapping = {
    }


    def __init__(self, name=None, attribute_identities=None):  # noqa: E501
        """GrantaServerApiIntegrationSchemaLayout - a model defined in Swagger"""  # noqa: E501
        self._name = None
        self._attribute_identities = None
        self.discriminator = None
        if name is not None:
            self.name = name
        if attribute_identities is not None:
            self.attribute_identities = attribute_identities

    @property
    def name(self):
        """Gets the name of this GrantaServerApiIntegrationSchemaLayout.  # noqa: E501

        :return: The name of this GrantaServerApiIntegrationSchemaLayout.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this GrantaServerApiIntegrationSchemaLayout.

        :param name: The name of this GrantaServerApiIntegrationSchemaLayout.  # noqa: E501
        :type: str
        """
        self._name = name

    @property
    def attribute_identities(self):
        """Gets the attribute_identities of this GrantaServerApiIntegrationSchemaLayout.  # noqa: E501

        :return: The attribute_identities of this GrantaServerApiIntegrationSchemaLayout.  # noqa: E501
        :rtype: list[int]
        """
        return self._attribute_identities

    @attribute_identities.setter
    def attribute_identities(self, attribute_identities):
        """Sets the attribute_identities of this GrantaServerApiIntegrationSchemaLayout.

        :param attribute_identities: The attribute_identities of this GrantaServerApiIntegrationSchemaLayout.  # noqa: E501
        :type: list[int]
        """
        self._attribute_identities = attribute_identities

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
        if issubclass(GrantaServerApiIntegrationSchemaLayout, dict):
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
        if not isinstance(other, GrantaServerApiIntegrationSchemaLayout):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
