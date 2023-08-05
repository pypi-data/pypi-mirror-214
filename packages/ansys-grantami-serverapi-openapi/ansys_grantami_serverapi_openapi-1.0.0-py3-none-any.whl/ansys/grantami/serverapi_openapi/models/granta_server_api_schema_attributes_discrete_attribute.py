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

class GrantaServerApiSchemaAttributesDiscreteAttribute(GrantaServerApiSchemaAttributesAttribute):
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
        'discrete_type': 'GrantaServerApiSchemaSlimEntitiesSlimNamedEntity',
        'is_multi_valued': 'bool'
    }
    if hasattr(GrantaServerApiSchemaAttributesAttribute, "swagger_types"):
        swagger_types.update(GrantaServerApiSchemaAttributesAttribute.swagger_types)

    attribute_map = {
        'type': 'type',
        'discrete_type': 'discreteType',
        'is_multi_valued': 'isMultiValued'
    }
    if hasattr(GrantaServerApiSchemaAttributesAttribute, "attribute_map"):
        attribute_map.update(GrantaServerApiSchemaAttributesAttribute.attribute_map)

    subtype_mapping = {
        'discreteType': 'GrantaServerApiSchemaSlimEntitiesSlimNamedEntity',
    }


    def __init__(self, type='discrete', discrete_type=None, is_multi_valued=None, *args, **kwargs):  # noqa: E501
        """GrantaServerApiSchemaAttributesDiscreteAttribute - a model defined in Swagger"""  # noqa: E501
        GrantaServerApiSchemaAttributesAttribute.__init__(self, *args, **kwargs)
        self._type = None
        self._discrete_type = None
        self._is_multi_valued = None
        self.discriminator = None
        self.type = type
        if discrete_type is not None:
            self.discrete_type = discrete_type
        if is_multi_valued is not None:
            self.is_multi_valued = is_multi_valued

    @property
    def type(self):
        """Gets the type of this GrantaServerApiSchemaAttributesDiscreteAttribute.  # noqa: E501

        :return: The type of this GrantaServerApiSchemaAttributesDiscreteAttribute.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this GrantaServerApiSchemaAttributesDiscreteAttribute.

        :param type: The type of this GrantaServerApiSchemaAttributesDiscreteAttribute.  # noqa: E501
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501
        self._type = type

    @property
    def discrete_type(self):
        """Gets the discrete_type of this GrantaServerApiSchemaAttributesDiscreteAttribute.  # noqa: E501

        :return: The discrete_type of this GrantaServerApiSchemaAttributesDiscreteAttribute.  # noqa: E501
        :rtype: GrantaServerApiSchemaSlimEntitiesSlimNamedEntity
        """
        return self._discrete_type

    @discrete_type.setter
    def discrete_type(self, discrete_type):
        """Sets the discrete_type of this GrantaServerApiSchemaAttributesDiscreteAttribute.

        :param discrete_type: The discrete_type of this GrantaServerApiSchemaAttributesDiscreteAttribute.  # noqa: E501
        :type: GrantaServerApiSchemaSlimEntitiesSlimNamedEntity
        """
        self._discrete_type = discrete_type

    @property
    def is_multi_valued(self):
        """Gets the is_multi_valued of this GrantaServerApiSchemaAttributesDiscreteAttribute.  # noqa: E501

        :return: The is_multi_valued of this GrantaServerApiSchemaAttributesDiscreteAttribute.  # noqa: E501
        :rtype: bool
        """
        return self._is_multi_valued

    @is_multi_valued.setter
    def is_multi_valued(self, is_multi_valued):
        """Sets the is_multi_valued of this GrantaServerApiSchemaAttributesDiscreteAttribute.

        :param is_multi_valued: The is_multi_valued of this GrantaServerApiSchemaAttributesDiscreteAttribute.  # noqa: E501
        :type: bool
        """
        self._is_multi_valued = is_multi_valued

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
        if issubclass(GrantaServerApiSchemaAttributesDiscreteAttribute, dict):
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
        if not isinstance(other, GrantaServerApiSchemaAttributesDiscreteAttribute):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
