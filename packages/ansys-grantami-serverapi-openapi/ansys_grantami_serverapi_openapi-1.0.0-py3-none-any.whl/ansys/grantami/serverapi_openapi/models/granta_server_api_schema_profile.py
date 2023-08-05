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


class GrantaServerApiSchemaProfile(ModelBase):
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
        'description': 'str',
        'homepage_url': 'str',
        'profile_tables': 'list[GrantaServerApiSchemaSlimEntitiesSlimProfileTable]',
        'key': 'str',
        'guid': 'str',
        'group_name': 'str',
        'is_implicit': 'bool',
        'name': 'str'
    }

    attribute_map = {
        'description': 'description',
        'homepage_url': 'homepageUrl',
        'profile_tables': 'profileTables',
        'key': 'key',
        'guid': 'guid',
        'group_name': 'groupName',
        'is_implicit': 'isImplicit',
        'name': 'name'
    }

    subtype_mapping = {
        'profileTables': 'GrantaServerApiSchemaSlimEntitiesSlimProfileTable',
    }


    def __init__(self, description=None, homepage_url=None, profile_tables=None, key=None, guid=None, group_name=None, is_implicit=None, name=None):  # noqa: E501
        """GrantaServerApiSchemaProfile - a model defined in Swagger"""  # noqa: E501
        self._description = None
        self._homepage_url = None
        self._profile_tables = None
        self._key = None
        self._guid = None
        self._group_name = None
        self._is_implicit = None
        self._name = None
        self.discriminator = None
        if description is not None:
            self.description = description
        if homepage_url is not None:
            self.homepage_url = homepage_url
        if profile_tables is not None:
            self.profile_tables = profile_tables
        if key is not None:
            self.key = key
        if guid is not None:
            self.guid = guid
        if group_name is not None:
            self.group_name = group_name
        if is_implicit is not None:
            self.is_implicit = is_implicit
        if name is not None:
            self.name = name

    @property
    def description(self):
        """Gets the description of this GrantaServerApiSchemaProfile.  # noqa: E501

        :return: The description of this GrantaServerApiSchemaProfile.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this GrantaServerApiSchemaProfile.

        :param description: The description of this GrantaServerApiSchemaProfile.  # noqa: E501
        :type: str
        """
        self._description = description

    @property
    def homepage_url(self):
        """Gets the homepage_url of this GrantaServerApiSchemaProfile.  # noqa: E501

        :return: The homepage_url of this GrantaServerApiSchemaProfile.  # noqa: E501
        :rtype: str
        """
        return self._homepage_url

    @homepage_url.setter
    def homepage_url(self, homepage_url):
        """Sets the homepage_url of this GrantaServerApiSchemaProfile.

        :param homepage_url: The homepage_url of this GrantaServerApiSchemaProfile.  # noqa: E501
        :type: str
        """
        self._homepage_url = homepage_url

    @property
    def profile_tables(self):
        """Gets the profile_tables of this GrantaServerApiSchemaProfile.  # noqa: E501

        :return: The profile_tables of this GrantaServerApiSchemaProfile.  # noqa: E501
        :rtype: list[GrantaServerApiSchemaSlimEntitiesSlimProfileTable]
        """
        return self._profile_tables

    @profile_tables.setter
    def profile_tables(self, profile_tables):
        """Sets the profile_tables of this GrantaServerApiSchemaProfile.

        :param profile_tables: The profile_tables of this GrantaServerApiSchemaProfile.  # noqa: E501
        :type: list[GrantaServerApiSchemaSlimEntitiesSlimProfileTable]
        """
        self._profile_tables = profile_tables

    @property
    def key(self):
        """Gets the key of this GrantaServerApiSchemaProfile.  # noqa: E501
        Key is a unique identifier of a profile. Separate from guid.  # noqa: E501

        :return: The key of this GrantaServerApiSchemaProfile.  # noqa: E501
        :rtype: str
        """
        return self._key

    @key.setter
    def key(self, key):
        """Sets the key of this GrantaServerApiSchemaProfile.
        Key is a unique identifier of a profile. Separate from guid.  # noqa: E501

        :param key: The key of this GrantaServerApiSchemaProfile.  # noqa: E501
        :type: str
        """
        self._key = key

    @property
    def guid(self):
        """Gets the guid of this GrantaServerApiSchemaProfile.  # noqa: E501
        Guid is a unique identifier of a profile. Separate from key.  # noqa: E501

        :return: The guid of this GrantaServerApiSchemaProfile.  # noqa: E501
        :rtype: str
        """
        return self._guid

    @guid.setter
    def guid(self, guid):
        """Sets the guid of this GrantaServerApiSchemaProfile.
        Guid is a unique identifier of a profile. Separate from key.  # noqa: E501

        :param guid: The guid of this GrantaServerApiSchemaProfile.  # noqa: E501
        :type: str
        """
        self._guid = guid

    @property
    def group_name(self):
        """Gets the group_name of this GrantaServerApiSchemaProfile.  # noqa: E501

        :return: The group_name of this GrantaServerApiSchemaProfile.  # noqa: E501
        :rtype: str
        """
        return self._group_name

    @group_name.setter
    def group_name(self, group_name):
        """Sets the group_name of this GrantaServerApiSchemaProfile.

        :param group_name: The group_name of this GrantaServerApiSchemaProfile.  # noqa: E501
        :type: str
        """
        self._group_name = group_name

    @property
    def is_implicit(self):
        """Gets the is_implicit of this GrantaServerApiSchemaProfile.  # noqa: E501

        :return: The is_implicit of this GrantaServerApiSchemaProfile.  # noqa: E501
        :rtype: bool
        """
        return self._is_implicit

    @is_implicit.setter
    def is_implicit(self, is_implicit):
        """Sets the is_implicit of this GrantaServerApiSchemaProfile.

        :param is_implicit: The is_implicit of this GrantaServerApiSchemaProfile.  # noqa: E501
        :type: bool
        """
        self._is_implicit = is_implicit

    @property
    def name(self):
        """Gets the name of this GrantaServerApiSchemaProfile.  # noqa: E501

        :return: The name of this GrantaServerApiSchemaProfile.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this GrantaServerApiSchemaProfile.

        :param name: The name of this GrantaServerApiSchemaProfile.  # noqa: E501
        :type: str
        """
        self._name = name

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
        if issubclass(GrantaServerApiSchemaProfile, dict):
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
        if not isinstance(other, GrantaServerApiSchemaProfile):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
