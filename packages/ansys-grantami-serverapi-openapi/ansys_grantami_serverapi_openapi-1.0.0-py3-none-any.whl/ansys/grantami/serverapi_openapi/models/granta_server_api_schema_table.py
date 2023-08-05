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


class GrantaServerApiSchemaTable(ModelBase):
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
        'default_subset': 'GrantaServerApiSchemaSlimEntitiesSlimSubset',
        'subsets': 'list[GrantaServerApiSchemaSlimEntitiesSlimSubset]',
        'default_layout': 'GrantaServerApiSchemaSlimEntitiesSlimLayout',
        'layouts': 'list[GrantaServerApiSchemaSlimEntitiesSlimLayout]',
        'is_hidden_from_browse': 'bool',
        'is_hidden_from_search': 'bool',
        'is_versioned': 'bool',
        'display_names': 'dict(str, str)',
        'name': 'str',
        'guid': 'str'
    }

    attribute_map = {
        'default_subset': 'defaultSubset',
        'subsets': 'subsets',
        'default_layout': 'defaultLayout',
        'layouts': 'layouts',
        'is_hidden_from_browse': 'isHiddenFromBrowse',
        'is_hidden_from_search': 'isHiddenFromSearch',
        'is_versioned': 'isVersioned',
        'display_names': 'displayNames',
        'name': 'name',
        'guid': 'guid'
    }

    subtype_mapping = {
        'defaultSubset': 'GrantaServerApiSchemaSlimEntitiesSlimSubset',
        'subsets': 'GrantaServerApiSchemaSlimEntitiesSlimSubset',
        'defaultLayout': 'GrantaServerApiSchemaSlimEntitiesSlimLayout',
        'layouts': 'GrantaServerApiSchemaSlimEntitiesSlimLayout',
    }


    def __init__(self, default_subset=None, subsets=None, default_layout=None, layouts=None, is_hidden_from_browse=None, is_hidden_from_search=None, is_versioned=None, display_names=None, name=None, guid=None):  # noqa: E501
        """GrantaServerApiSchemaTable - a model defined in Swagger"""  # noqa: E501
        self._default_subset = None
        self._subsets = None
        self._default_layout = None
        self._layouts = None
        self._is_hidden_from_browse = None
        self._is_hidden_from_search = None
        self._is_versioned = None
        self._display_names = None
        self._name = None
        self._guid = None
        self.discriminator = None
        if default_subset is not None:
            self.default_subset = default_subset
        if subsets is not None:
            self.subsets = subsets
        if default_layout is not None:
            self.default_layout = default_layout
        if layouts is not None:
            self.layouts = layouts
        if is_hidden_from_browse is not None:
            self.is_hidden_from_browse = is_hidden_from_browse
        if is_hidden_from_search is not None:
            self.is_hidden_from_search = is_hidden_from_search
        if is_versioned is not None:
            self.is_versioned = is_versioned
        if display_names is not None:
            self.display_names = display_names
        if name is not None:
            self.name = name
        if guid is not None:
            self.guid = guid

    @property
    def default_subset(self):
        """Gets the default_subset of this GrantaServerApiSchemaTable.  # noqa: E501

        :return: The default_subset of this GrantaServerApiSchemaTable.  # noqa: E501
        :rtype: GrantaServerApiSchemaSlimEntitiesSlimSubset
        """
        return self._default_subset

    @default_subset.setter
    def default_subset(self, default_subset):
        """Sets the default_subset of this GrantaServerApiSchemaTable.

        :param default_subset: The default_subset of this GrantaServerApiSchemaTable.  # noqa: E501
        :type: GrantaServerApiSchemaSlimEntitiesSlimSubset
        """
        self._default_subset = default_subset

    @property
    def subsets(self):
        """Gets the subsets of this GrantaServerApiSchemaTable.  # noqa: E501

        :return: The subsets of this GrantaServerApiSchemaTable.  # noqa: E501
        :rtype: list[GrantaServerApiSchemaSlimEntitiesSlimSubset]
        """
        return self._subsets

    @subsets.setter
    def subsets(self, subsets):
        """Sets the subsets of this GrantaServerApiSchemaTable.

        :param subsets: The subsets of this GrantaServerApiSchemaTable.  # noqa: E501
        :type: list[GrantaServerApiSchemaSlimEntitiesSlimSubset]
        """
        self._subsets = subsets

    @property
    def default_layout(self):
        """Gets the default_layout of this GrantaServerApiSchemaTable.  # noqa: E501

        :return: The default_layout of this GrantaServerApiSchemaTable.  # noqa: E501
        :rtype: GrantaServerApiSchemaSlimEntitiesSlimLayout
        """
        return self._default_layout

    @default_layout.setter
    def default_layout(self, default_layout):
        """Sets the default_layout of this GrantaServerApiSchemaTable.

        :param default_layout: The default_layout of this GrantaServerApiSchemaTable.  # noqa: E501
        :type: GrantaServerApiSchemaSlimEntitiesSlimLayout
        """
        self._default_layout = default_layout

    @property
    def layouts(self):
        """Gets the layouts of this GrantaServerApiSchemaTable.  # noqa: E501

        :return: The layouts of this GrantaServerApiSchemaTable.  # noqa: E501
        :rtype: list[GrantaServerApiSchemaSlimEntitiesSlimLayout]
        """
        return self._layouts

    @layouts.setter
    def layouts(self, layouts):
        """Sets the layouts of this GrantaServerApiSchemaTable.

        :param layouts: The layouts of this GrantaServerApiSchemaTable.  # noqa: E501
        :type: list[GrantaServerApiSchemaSlimEntitiesSlimLayout]
        """
        self._layouts = layouts

    @property
    def is_hidden_from_browse(self):
        """Gets the is_hidden_from_browse of this GrantaServerApiSchemaTable.  # noqa: E501

        :return: The is_hidden_from_browse of this GrantaServerApiSchemaTable.  # noqa: E501
        :rtype: bool
        """
        return self._is_hidden_from_browse

    @is_hidden_from_browse.setter
    def is_hidden_from_browse(self, is_hidden_from_browse):
        """Sets the is_hidden_from_browse of this GrantaServerApiSchemaTable.

        :param is_hidden_from_browse: The is_hidden_from_browse of this GrantaServerApiSchemaTable.  # noqa: E501
        :type: bool
        """
        self._is_hidden_from_browse = is_hidden_from_browse

    @property
    def is_hidden_from_search(self):
        """Gets the is_hidden_from_search of this GrantaServerApiSchemaTable.  # noqa: E501

        :return: The is_hidden_from_search of this GrantaServerApiSchemaTable.  # noqa: E501
        :rtype: bool
        """
        return self._is_hidden_from_search

    @is_hidden_from_search.setter
    def is_hidden_from_search(self, is_hidden_from_search):
        """Sets the is_hidden_from_search of this GrantaServerApiSchemaTable.

        :param is_hidden_from_search: The is_hidden_from_search of this GrantaServerApiSchemaTable.  # noqa: E501
        :type: bool
        """
        self._is_hidden_from_search = is_hidden_from_search

    @property
    def is_versioned(self):
        """Gets the is_versioned of this GrantaServerApiSchemaTable.  # noqa: E501

        :return: The is_versioned of this GrantaServerApiSchemaTable.  # noqa: E501
        :rtype: bool
        """
        return self._is_versioned

    @is_versioned.setter
    def is_versioned(self, is_versioned):
        """Sets the is_versioned of this GrantaServerApiSchemaTable.

        :param is_versioned: The is_versioned of this GrantaServerApiSchemaTable.  # noqa: E501
        :type: bool
        """
        self._is_versioned = is_versioned

    @property
    def display_names(self):
        """Gets the display_names of this GrantaServerApiSchemaTable.  # noqa: E501

        :return: The display_names of this GrantaServerApiSchemaTable.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._display_names

    @display_names.setter
    def display_names(self, display_names):
        """Sets the display_names of this GrantaServerApiSchemaTable.

        :param display_names: The display_names of this GrantaServerApiSchemaTable.  # noqa: E501
        :type: dict(str, str)
        """
        self._display_names = display_names

    @property
    def name(self):
        """Gets the name of this GrantaServerApiSchemaTable.  # noqa: E501

        :return: The name of this GrantaServerApiSchemaTable.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this GrantaServerApiSchemaTable.

        :param name: The name of this GrantaServerApiSchemaTable.  # noqa: E501
        :type: str
        """
        self._name = name

    @property
    def guid(self):
        """Gets the guid of this GrantaServerApiSchemaTable.  # noqa: E501

        :return: The guid of this GrantaServerApiSchemaTable.  # noqa: E501
        :rtype: str
        """
        return self._guid

    @guid.setter
    def guid(self, guid):
        """Sets the guid of this GrantaServerApiSchemaTable.

        :param guid: The guid of this GrantaServerApiSchemaTable.  # noqa: E501
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
        if issubclass(GrantaServerApiSchemaTable, dict):
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
        if not isinstance(other, GrantaServerApiSchemaTable):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
