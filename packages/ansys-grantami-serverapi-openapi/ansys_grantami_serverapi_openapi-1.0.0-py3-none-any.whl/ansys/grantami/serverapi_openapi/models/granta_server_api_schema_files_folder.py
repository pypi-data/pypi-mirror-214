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


class GrantaServerApiSchemaFilesFolder(ModelBase):
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
        'parent_guid': 'str',
        'name': 'str',
        'guid': 'str'
    }

    attribute_map = {
        'parent_guid': 'parentGuid',
        'name': 'name',
        'guid': 'guid'
    }

    subtype_mapping = {
    }


    def __init__(self, parent_guid=None, name=None, guid=None):  # noqa: E501
        """GrantaServerApiSchemaFilesFolder - a model defined in Swagger"""  # noqa: E501
        self._parent_guid = None
        self._name = None
        self._guid = None
        self.discriminator = None
        if parent_guid is not None:
            self.parent_guid = parent_guid
        if name is not None:
            self.name = name
        if guid is not None:
            self.guid = guid

    @property
    def parent_guid(self):
        """Gets the parent_guid of this GrantaServerApiSchemaFilesFolder.  # noqa: E501

        :return: The parent_guid of this GrantaServerApiSchemaFilesFolder.  # noqa: E501
        :rtype: str
        """
        return self._parent_guid

    @parent_guid.setter
    def parent_guid(self, parent_guid):
        """Sets the parent_guid of this GrantaServerApiSchemaFilesFolder.

        :param parent_guid: The parent_guid of this GrantaServerApiSchemaFilesFolder.  # noqa: E501
        :type: str
        """
        self._parent_guid = parent_guid

    @property
    def name(self):
        """Gets the name of this GrantaServerApiSchemaFilesFolder.  # noqa: E501

        :return: The name of this GrantaServerApiSchemaFilesFolder.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this GrantaServerApiSchemaFilesFolder.

        :param name: The name of this GrantaServerApiSchemaFilesFolder.  # noqa: E501
        :type: str
        """
        self._name = name

    @property
    def guid(self):
        """Gets the guid of this GrantaServerApiSchemaFilesFolder.  # noqa: E501

        :return: The guid of this GrantaServerApiSchemaFilesFolder.  # noqa: E501
        :rtype: str
        """
        return self._guid

    @guid.setter
    def guid(self, guid):
        """Sets the guid of this GrantaServerApiSchemaFilesFolder.

        :param guid: The guid of this GrantaServerApiSchemaFilesFolder.  # noqa: E501
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
        if issubclass(GrantaServerApiSchemaFilesFolder, dict):
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
        if not isinstance(other, GrantaServerApiSchemaFilesFolder):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
