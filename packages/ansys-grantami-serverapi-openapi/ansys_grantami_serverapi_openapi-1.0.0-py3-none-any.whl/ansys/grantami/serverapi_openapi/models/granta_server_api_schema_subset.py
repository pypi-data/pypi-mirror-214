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


class GrantaServerApiSchemaSubset(ModelBase):
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
        'associated_layout': 'GrantaServerApiSchemaSlimEntitiesSlimLayout',
        'display_names': 'dict(str, str)',
        'name': 'str',
        'guid': 'str'
    }

    attribute_map = {
        'associated_layout': 'associatedLayout',
        'display_names': 'displayNames',
        'name': 'name',
        'guid': 'guid'
    }

    subtype_mapping = {
        'associatedLayout': 'GrantaServerApiSchemaSlimEntitiesSlimLayout',
    }


    def __init__(self, associated_layout=None, display_names=None, name=None, guid=None):  # noqa: E501
        """GrantaServerApiSchemaSubset - a model defined in Swagger"""  # noqa: E501
        self._associated_layout = None
        self._display_names = None
        self._name = None
        self._guid = None
        self.discriminator = None
        if associated_layout is not None:
            self.associated_layout = associated_layout
        if display_names is not None:
            self.display_names = display_names
        if name is not None:
            self.name = name
        if guid is not None:
            self.guid = guid

    @property
    def associated_layout(self):
        """Gets the associated_layout of this GrantaServerApiSchemaSubset.  # noqa: E501

        :return: The associated_layout of this GrantaServerApiSchemaSubset.  # noqa: E501
        :rtype: GrantaServerApiSchemaSlimEntitiesSlimLayout
        """
        return self._associated_layout

    @associated_layout.setter
    def associated_layout(self, associated_layout):
        """Sets the associated_layout of this GrantaServerApiSchemaSubset.

        :param associated_layout: The associated_layout of this GrantaServerApiSchemaSubset.  # noqa: E501
        :type: GrantaServerApiSchemaSlimEntitiesSlimLayout
        """
        self._associated_layout = associated_layout

    @property
    def display_names(self):
        """Gets the display_names of this GrantaServerApiSchemaSubset.  # noqa: E501

        :return: The display_names of this GrantaServerApiSchemaSubset.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._display_names

    @display_names.setter
    def display_names(self, display_names):
        """Sets the display_names of this GrantaServerApiSchemaSubset.

        :param display_names: The display_names of this GrantaServerApiSchemaSubset.  # noqa: E501
        :type: dict(str, str)
        """
        self._display_names = display_names

    @property
    def name(self):
        """Gets the name of this GrantaServerApiSchemaSubset.  # noqa: E501

        :return: The name of this GrantaServerApiSchemaSubset.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this GrantaServerApiSchemaSubset.

        :param name: The name of this GrantaServerApiSchemaSubset.  # noqa: E501
        :type: str
        """
        self._name = name

    @property
    def guid(self):
        """Gets the guid of this GrantaServerApiSchemaSubset.  # noqa: E501

        :return: The guid of this GrantaServerApiSchemaSubset.  # noqa: E501
        :rtype: str
        """
        return self._guid

    @guid.setter
    def guid(self, guid):
        """Sets the guid of this GrantaServerApiSchemaSubset.

        :param guid: The guid of this GrantaServerApiSchemaSubset.  # noqa: E501
        :type: str
        """
        self._guid = guid

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
        if issubclass(GrantaServerApiSchemaSubset, dict):
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
        if not isinstance(other, GrantaServerApiSchemaSubset):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
