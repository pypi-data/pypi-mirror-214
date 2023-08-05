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


class GrantaServerApiListsDtoUserPermissionDto(ModelBase):
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
        'user_or_group_name': 'str',
        'user_or_group_identifier': 'str',
        'flags': 'GrantaServerApiListsDtoRecordListPermissionFlagsDto'
    }

    attribute_map = {
        'user_or_group_name': 'userOrGroupName',
        'user_or_group_identifier': 'userOrGroupIdentifier',
        'flags': 'flags'
    }

    subtype_mapping = {
        'flags': 'GrantaServerApiListsDtoRecordListPermissionFlagsDto'
    }


    def __init__(self, user_or_group_name=None, user_or_group_identifier=None, flags=None):  # noqa: E501
        """GrantaServerApiListsDtoUserPermissionDto - a model defined in Swagger"""  # noqa: E501
        self._user_or_group_name = None
        self._user_or_group_identifier = None
        self._flags = None
        self.discriminator = None
        if user_or_group_name is not None:
            self.user_or_group_name = user_or_group_name
        if user_or_group_identifier is not None:
            self.user_or_group_identifier = user_or_group_identifier
        if flags is not None:
            self.flags = flags

    @property
    def user_or_group_name(self):
        """Gets the user_or_group_name of this GrantaServerApiListsDtoUserPermissionDto.  # noqa: E501
        The user or group name.  # noqa: E501

        :return: The user_or_group_name of this GrantaServerApiListsDtoUserPermissionDto.  # noqa: E501
        :rtype: str
        """
        return self._user_or_group_name

    @user_or_group_name.setter
    def user_or_group_name(self, user_or_group_name):
        """Sets the user_or_group_name of this GrantaServerApiListsDtoUserPermissionDto.
        The user or group name.  # noqa: E501

        :param user_or_group_name: The user_or_group_name of this GrantaServerApiListsDtoUserPermissionDto.  # noqa: E501
        :type: str
        """
        self._user_or_group_name = user_or_group_name

    @property
    def user_or_group_identifier(self):
        """Gets the user_or_group_identifier of this GrantaServerApiListsDtoUserPermissionDto.  # noqa: E501
        The user or group identifier  # noqa: E501

        :return: The user_or_group_identifier of this GrantaServerApiListsDtoUserPermissionDto.  # noqa: E501
        :rtype: str
        """
        return self._user_or_group_identifier

    @user_or_group_identifier.setter
    def user_or_group_identifier(self, user_or_group_identifier):
        """Sets the user_or_group_identifier of this GrantaServerApiListsDtoUserPermissionDto.
        The user or group identifier  # noqa: E501

        :param user_or_group_identifier: The user_or_group_identifier of this GrantaServerApiListsDtoUserPermissionDto.  # noqa: E501
        :type: str
        """
        self._user_or_group_identifier = user_or_group_identifier

    @property
    def flags(self):
        """Gets the flags of this GrantaServerApiListsDtoUserPermissionDto.  # noqa: E501

        :return: The flags of this GrantaServerApiListsDtoUserPermissionDto.  # noqa: E501
        :rtype: GrantaServerApiListsDtoRecordListPermissionFlagsDto
        """
        return self._flags

    @flags.setter
    def flags(self, flags):
        """Sets the flags of this GrantaServerApiListsDtoUserPermissionDto.

        :param flags: The flags of this GrantaServerApiListsDtoUserPermissionDto.  # noqa: E501
        :type: GrantaServerApiListsDtoRecordListPermissionFlagsDto
        """
        self._flags = flags

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
        if issubclass(GrantaServerApiListsDtoUserPermissionDto, dict):
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
        if not isinstance(other, GrantaServerApiListsDtoUserPermissionDto):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
