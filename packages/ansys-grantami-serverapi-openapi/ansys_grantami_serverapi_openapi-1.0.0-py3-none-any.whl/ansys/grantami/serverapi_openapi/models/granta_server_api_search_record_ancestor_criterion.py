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

from ansys.grantami.serverapi_openapi.models.granta_server_api_search_criterion import GrantaServerApiSearchCriterion  # noqa: F401,E501

class GrantaServerApiSearchRecordAncestorCriterion(GrantaServerApiSearchCriterion):
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
        'ancestor_identity': 'int',
        'direct_parent_only': 'bool',
        'type': 'str'
    }
    if hasattr(GrantaServerApiSearchCriterion, "swagger_types"):
        swagger_types.update(GrantaServerApiSearchCriterion.swagger_types)

    attribute_map = {
        'ancestor_identity': 'ancestorIdentity',
        'direct_parent_only': 'directParentOnly',
        'type': 'type'
    }
    if hasattr(GrantaServerApiSearchCriterion, "attribute_map"):
        attribute_map.update(GrantaServerApiSearchCriterion.attribute_map)

    subtype_mapping = {
    }


    def __init__(self, ancestor_identity=None, direct_parent_only=None, type='recordAncestor', *args, **kwargs):  # noqa: E501
        """GrantaServerApiSearchRecordAncestorCriterion - a model defined in Swagger"""  # noqa: E501
        GrantaServerApiSearchCriterion.__init__(self, *args, **kwargs)
        self._ancestor_identity = None
        self._direct_parent_only = None
        self._type = None
        self.discriminator = None
        if ancestor_identity is not None:
            self.ancestor_identity = ancestor_identity
        if direct_parent_only is not None:
            self.direct_parent_only = direct_parent_only
        self.type = type

    @property
    def ancestor_identity(self):
        """Gets the ancestor_identity of this GrantaServerApiSearchRecordAncestorCriterion.  # noqa: E501

        :return: The ancestor_identity of this GrantaServerApiSearchRecordAncestorCriterion.  # noqa: E501
        :rtype: int
        """
        return self._ancestor_identity

    @ancestor_identity.setter
    def ancestor_identity(self, ancestor_identity):
        """Sets the ancestor_identity of this GrantaServerApiSearchRecordAncestorCriterion.

        :param ancestor_identity: The ancestor_identity of this GrantaServerApiSearchRecordAncestorCriterion.  # noqa: E501
        :type: int
        """
        self._ancestor_identity = ancestor_identity

    @property
    def direct_parent_only(self):
        """Gets the direct_parent_only of this GrantaServerApiSearchRecordAncestorCriterion.  # noqa: E501

        :return: The direct_parent_only of this GrantaServerApiSearchRecordAncestorCriterion.  # noqa: E501
        :rtype: bool
        """
        return self._direct_parent_only

    @direct_parent_only.setter
    def direct_parent_only(self, direct_parent_only):
        """Sets the direct_parent_only of this GrantaServerApiSearchRecordAncestorCriterion.

        :param direct_parent_only: The direct_parent_only of this GrantaServerApiSearchRecordAncestorCriterion.  # noqa: E501
        :type: bool
        """
        self._direct_parent_only = direct_parent_only

    @property
    def type(self):
        """Gets the type of this GrantaServerApiSearchRecordAncestorCriterion.  # noqa: E501

        :return: The type of this GrantaServerApiSearchRecordAncestorCriterion.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this GrantaServerApiSearchRecordAncestorCriterion.

        :param type: The type of this GrantaServerApiSearchRecordAncestorCriterion.  # noqa: E501
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501
        self._type = type

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
        if issubclass(GrantaServerApiSearchRecordAncestorCriterion, dict):
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
        if not isinstance(other, GrantaServerApiSearchRecordAncestorCriterion):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
