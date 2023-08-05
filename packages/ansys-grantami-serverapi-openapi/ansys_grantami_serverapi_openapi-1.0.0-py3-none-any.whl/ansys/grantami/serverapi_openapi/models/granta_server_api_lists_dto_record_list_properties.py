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


class GrantaServerApiListsDtoRecordListProperties(ModelBase):
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
        'description': 'str',
        'notes': 'str',
        'published': 'bool',
        'awaiting_approval': 'bool',
        'internal_use': 'bool'
    }

    attribute_map = {
        'name': 'name',
        'description': 'description',
        'notes': 'notes',
        'published': 'published',
        'awaiting_approval': 'awaitingApproval',
        'internal_use': 'internalUse'
    }

    subtype_mapping = {
    }


    def __init__(self, name=None, description=None, notes=None, published=None, awaiting_approval=None, internal_use=None):  # noqa: E501
        """GrantaServerApiListsDtoRecordListProperties - a model defined in Swagger"""  # noqa: E501
        self._name = None
        self._description = None
        self._notes = None
        self._published = None
        self._awaiting_approval = None
        self._internal_use = None
        self.discriminator = None
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if notes is not None:
            self.notes = notes
        if published is not None:
            self.published = published
        if awaiting_approval is not None:
            self.awaiting_approval = awaiting_approval
        if internal_use is not None:
            self.internal_use = internal_use

    @property
    def name(self):
        """Gets the name of this GrantaServerApiListsDtoRecordListProperties.  # noqa: E501

        :return: The name of this GrantaServerApiListsDtoRecordListProperties.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this GrantaServerApiListsDtoRecordListProperties.

        :param name: The name of this GrantaServerApiListsDtoRecordListProperties.  # noqa: E501
        :type: str
        """
        self._name = name

    @property
    def description(self):
        """Gets the description of this GrantaServerApiListsDtoRecordListProperties.  # noqa: E501

        :return: The description of this GrantaServerApiListsDtoRecordListProperties.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this GrantaServerApiListsDtoRecordListProperties.

        :param description: The description of this GrantaServerApiListsDtoRecordListProperties.  # noqa: E501
        :type: str
        """
        self._description = description

    @property
    def notes(self):
        """Gets the notes of this GrantaServerApiListsDtoRecordListProperties.  # noqa: E501

        :return: The notes of this GrantaServerApiListsDtoRecordListProperties.  # noqa: E501
        :rtype: str
        """
        return self._notes

    @notes.setter
    def notes(self, notes):
        """Sets the notes of this GrantaServerApiListsDtoRecordListProperties.

        :param notes: The notes of this GrantaServerApiListsDtoRecordListProperties.  # noqa: E501
        :type: str
        """
        self._notes = notes

    @property
    def published(self):
        """Gets the published of this GrantaServerApiListsDtoRecordListProperties.  # noqa: E501

        :return: The published of this GrantaServerApiListsDtoRecordListProperties.  # noqa: E501
        :rtype: bool
        """
        return self._published

    @published.setter
    def published(self, published):
        """Sets the published of this GrantaServerApiListsDtoRecordListProperties.

        :param published: The published of this GrantaServerApiListsDtoRecordListProperties.  # noqa: E501
        :type: bool
        """
        self._published = published

    @property
    def awaiting_approval(self):
        """Gets the awaiting_approval of this GrantaServerApiListsDtoRecordListProperties.  # noqa: E501

        :return: The awaiting_approval of this GrantaServerApiListsDtoRecordListProperties.  # noqa: E501
        :rtype: bool
        """
        return self._awaiting_approval

    @awaiting_approval.setter
    def awaiting_approval(self, awaiting_approval):
        """Sets the awaiting_approval of this GrantaServerApiListsDtoRecordListProperties.

        :param awaiting_approval: The awaiting_approval of this GrantaServerApiListsDtoRecordListProperties.  # noqa: E501
        :type: bool
        """
        self._awaiting_approval = awaiting_approval

    @property
    def internal_use(self):
        """Gets the internal_use of this GrantaServerApiListsDtoRecordListProperties.  # noqa: E501

        :return: The internal_use of this GrantaServerApiListsDtoRecordListProperties.  # noqa: E501
        :rtype: bool
        """
        return self._internal_use

    @internal_use.setter
    def internal_use(self, internal_use):
        """Sets the internal_use of this GrantaServerApiListsDtoRecordListProperties.

        :param internal_use: The internal_use of this GrantaServerApiListsDtoRecordListProperties.  # noqa: E501
        :type: bool
        """
        self._internal_use = internal_use

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
        if issubclass(GrantaServerApiListsDtoRecordListProperties, dict):
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
        if not isinstance(other, GrantaServerApiListsDtoRecordListProperties):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
