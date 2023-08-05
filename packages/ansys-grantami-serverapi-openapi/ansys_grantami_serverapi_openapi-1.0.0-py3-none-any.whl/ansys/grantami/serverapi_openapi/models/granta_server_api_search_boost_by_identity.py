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


class GrantaServerApiSearchBoostByIdentity(ModelBase):
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
        'attribute_identity': 'int',
        'boost_factor': 'float'
    }

    attribute_map = {
        'attribute_identity': 'attributeIdentity',
        'boost_factor': 'boostFactor'
    }

    subtype_mapping = {
    }


    def __init__(self, attribute_identity=None, boost_factor=None):  # noqa: E501
        """GrantaServerApiSearchBoostByIdentity - a model defined in Swagger"""  # noqa: E501
        self._attribute_identity = None
        self._boost_factor = None
        self.discriminator = None
        if attribute_identity is not None:
            self.attribute_identity = attribute_identity
        if boost_factor is not None:
            self.boost_factor = boost_factor

    @property
    def attribute_identity(self):
        """Gets the attribute_identity of this GrantaServerApiSearchBoostByIdentity.  # noqa: E501

        :return: The attribute_identity of this GrantaServerApiSearchBoostByIdentity.  # noqa: E501
        :rtype: int
        """
        return self._attribute_identity

    @attribute_identity.setter
    def attribute_identity(self, attribute_identity):
        """Sets the attribute_identity of this GrantaServerApiSearchBoostByIdentity.

        :param attribute_identity: The attribute_identity of this GrantaServerApiSearchBoostByIdentity.  # noqa: E501
        :type: int
        """
        self._attribute_identity = attribute_identity

    @property
    def boost_factor(self):
        """Gets the boost_factor of this GrantaServerApiSearchBoostByIdentity.  # noqa: E501

        :return: The boost_factor of this GrantaServerApiSearchBoostByIdentity.  # noqa: E501
        :rtype: float
        """
        return self._boost_factor

    @boost_factor.setter
    def boost_factor(self, boost_factor):
        """Sets the boost_factor of this GrantaServerApiSearchBoostByIdentity.

        :param boost_factor: The boost_factor of this GrantaServerApiSearchBoostByIdentity.  # noqa: E501
        :type: float
        """
        self._boost_factor = boost_factor

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
        if issubclass(GrantaServerApiSearchBoostByIdentity, dict):
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
        if not isinstance(other, GrantaServerApiSearchBoostByIdentity):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
