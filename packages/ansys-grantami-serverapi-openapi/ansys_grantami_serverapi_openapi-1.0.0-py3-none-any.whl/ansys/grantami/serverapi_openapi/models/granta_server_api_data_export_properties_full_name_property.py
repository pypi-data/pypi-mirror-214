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

from ansys.grantami.serverapi_openapi.models.granta_server_api_data_export_properties_property import GrantaServerApiDataExportPropertiesProperty  # noqa: F401,E501

class GrantaServerApiDataExportPropertiesFullNameProperty(GrantaServerApiDataExportPropertiesProperty):
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
        'property_name': 'str',
        'full_name': 'str'
    }
    if hasattr(GrantaServerApiDataExportPropertiesProperty, "swagger_types"):
        swagger_types.update(GrantaServerApiDataExportPropertiesProperty.swagger_types)

    attribute_map = {
        'property_name': 'propertyName',
        'full_name': 'fullName'
    }
    if hasattr(GrantaServerApiDataExportPropertiesProperty, "attribute_map"):
        attribute_map.update(GrantaServerApiDataExportPropertiesProperty.attribute_map)

    subtype_mapping = {
    }


    def __init__(self, property_name='fullName', full_name=None, *args, **kwargs):  # noqa: E501
        """GrantaServerApiDataExportPropertiesFullNameProperty - a model defined in Swagger"""  # noqa: E501
        GrantaServerApiDataExportPropertiesProperty.__init__(self, *args, **kwargs)
        self._property_name = None
        self._full_name = None
        self.discriminator = None
        self.property_name = property_name
        if full_name is not None:
            self.full_name = full_name

    @property
    def property_name(self):
        """Gets the property_name of this GrantaServerApiDataExportPropertiesFullNameProperty.  # noqa: E501

        :return: The property_name of this GrantaServerApiDataExportPropertiesFullNameProperty.  # noqa: E501
        :rtype: str
        """
        return self._property_name

    @property_name.setter
    def property_name(self, property_name):
        """Sets the property_name of this GrantaServerApiDataExportPropertiesFullNameProperty.

        :param property_name: The property_name of this GrantaServerApiDataExportPropertiesFullNameProperty.  # noqa: E501
        :type: str
        """
        if property_name is None:
            raise ValueError("Invalid value for `property_name`, must not be `None`")  # noqa: E501
        self._property_name = property_name

    @property
    def full_name(self):
        """Gets the full_name of this GrantaServerApiDataExportPropertiesFullNameProperty.  # noqa: E501

        :return: The full_name of this GrantaServerApiDataExportPropertiesFullNameProperty.  # noqa: E501
        :rtype: str
        """
        return self._full_name

    @full_name.setter
    def full_name(self, full_name):
        """Sets the full_name of this GrantaServerApiDataExportPropertiesFullNameProperty.

        :param full_name: The full_name of this GrantaServerApiDataExportPropertiesFullNameProperty.  # noqa: E501
        :type: str
        """
        self._full_name = full_name

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
        if issubclass(GrantaServerApiDataExportPropertiesFullNameProperty, dict):
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
        if not isinstance(other, GrantaServerApiDataExportPropertiesFullNameProperty):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
