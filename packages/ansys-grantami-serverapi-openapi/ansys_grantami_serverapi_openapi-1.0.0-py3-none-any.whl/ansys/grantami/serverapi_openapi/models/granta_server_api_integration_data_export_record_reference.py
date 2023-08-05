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


class GrantaServerApiIntegrationDataExportRecordReference(ModelBase):
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
        'record_history_identity': 'int',
        'database_key': 'str'
    }

    attribute_map = {
        'record_history_identity': 'recordHistoryIdentity',
        'database_key': 'databaseKey'
    }

    subtype_mapping = {
    }


    def __init__(self, record_history_identity=None, database_key=None):  # noqa: E501
        """GrantaServerApiIntegrationDataExportRecordReference - a model defined in Swagger"""  # noqa: E501
        self._record_history_identity = None
        self._database_key = None
        self.discriminator = None
        if record_history_identity is not None:
            self.record_history_identity = record_history_identity
        if database_key is not None:
            self.database_key = database_key

    @property
    def record_history_identity(self):
        """Gets the record_history_identity of this GrantaServerApiIntegrationDataExportRecordReference.  # noqa: E501

        :return: The record_history_identity of this GrantaServerApiIntegrationDataExportRecordReference.  # noqa: E501
        :rtype: int
        """
        return self._record_history_identity

    @record_history_identity.setter
    def record_history_identity(self, record_history_identity):
        """Sets the record_history_identity of this GrantaServerApiIntegrationDataExportRecordReference.

        :param record_history_identity: The record_history_identity of this GrantaServerApiIntegrationDataExportRecordReference.  # noqa: E501
        :type: int
        """
        self._record_history_identity = record_history_identity

    @property
    def database_key(self):
        """Gets the database_key of this GrantaServerApiIntegrationDataExportRecordReference.  # noqa: E501

        :return: The database_key of this GrantaServerApiIntegrationDataExportRecordReference.  # noqa: E501
        :rtype: str
        """
        return self._database_key

    @database_key.setter
    def database_key(self, database_key):
        """Sets the database_key of this GrantaServerApiIntegrationDataExportRecordReference.

        :param database_key: The database_key of this GrantaServerApiIntegrationDataExportRecordReference.  # noqa: E501
        :type: str
        """
        self._database_key = database_key

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
        if issubclass(GrantaServerApiIntegrationDataExportRecordReference, dict):
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
        if not isinstance(other, GrantaServerApiIntegrationDataExportRecordReference):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
