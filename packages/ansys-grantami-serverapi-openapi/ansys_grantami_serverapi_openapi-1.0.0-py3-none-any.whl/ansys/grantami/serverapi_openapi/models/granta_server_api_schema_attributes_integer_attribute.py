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

from ansys.grantami.serverapi_openapi.models.granta_server_api_schema_attributes_attribute import GrantaServerApiSchemaAttributesAttribute  # noqa: F401,E501

class GrantaServerApiSchemaAttributesIntegerAttribute(GrantaServerApiSchemaAttributesAttribute):
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
        'type': 'str',
        'is_unique': 'bool'
    }
    if hasattr(GrantaServerApiSchemaAttributesAttribute, "swagger_types"):
        swagger_types.update(GrantaServerApiSchemaAttributesAttribute.swagger_types)

    attribute_map = {
        'type': 'type',
        'is_unique': 'isUnique'
    }
    if hasattr(GrantaServerApiSchemaAttributesAttribute, "attribute_map"):
        attribute_map.update(GrantaServerApiSchemaAttributesAttribute.attribute_map)

    subtype_mapping = {
    }


    def __init__(self, type='integer', is_unique=None, *args, **kwargs):  # noqa: E501
        """GrantaServerApiSchemaAttributesIntegerAttribute - a model defined in Swagger"""  # noqa: E501
        GrantaServerApiSchemaAttributesAttribute.__init__(self, *args, **kwargs)
        self._type = None
        self._is_unique = None
        self.discriminator = None
        self.type = type
        if is_unique is not None:
            self.is_unique = is_unique

    @property
    def type(self):
        """Gets the type of this GrantaServerApiSchemaAttributesIntegerAttribute.  # noqa: E501

        :return: The type of this GrantaServerApiSchemaAttributesIntegerAttribute.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this GrantaServerApiSchemaAttributesIntegerAttribute.

        :param type: The type of this GrantaServerApiSchemaAttributesIntegerAttribute.  # noqa: E501
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501
        self._type = type

    @property
    def is_unique(self):
        """Gets the is_unique of this GrantaServerApiSchemaAttributesIntegerAttribute.  # noqa: E501

        :return: The is_unique of this GrantaServerApiSchemaAttributesIntegerAttribute.  # noqa: E501
        :rtype: bool
        """
        return self._is_unique

    @is_unique.setter
    def is_unique(self, is_unique):
        """Sets the is_unique of this GrantaServerApiSchemaAttributesIntegerAttribute.

        :param is_unique: The is_unique of this GrantaServerApiSchemaAttributesIntegerAttribute.  # noqa: E501
        :type: bool
        """
        self._is_unique = is_unique

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
        if issubclass(GrantaServerApiSchemaAttributesIntegerAttribute, dict):
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
        if not isinstance(other, GrantaServerApiSchemaAttributesIntegerAttribute):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
