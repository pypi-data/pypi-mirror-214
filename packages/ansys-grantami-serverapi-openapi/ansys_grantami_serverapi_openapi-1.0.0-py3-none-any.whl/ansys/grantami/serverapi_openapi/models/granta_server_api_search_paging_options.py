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


class GrantaServerApiSearchPagingOptions(ModelBase):
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
        'page_size': 'int',
        'keep_alive_in_minutes': 'int',
        'page_number': 'int'
    }

    attribute_map = {
        'page_size': 'pageSize',
        'keep_alive_in_minutes': 'keepAliveInMinutes',
        'page_number': 'pageNumber'
    }

    subtype_mapping = {
    }


    def __init__(self, page_size=None, keep_alive_in_minutes=None, page_number=None):  # noqa: E501
        """GrantaServerApiSearchPagingOptions - a model defined in Swagger"""  # noqa: E501
        self._page_size = None
        self._keep_alive_in_minutes = None
        self._page_number = None
        self.discriminator = None
        if page_size is not None:
            self.page_size = page_size
        if keep_alive_in_minutes is not None:
            self.keep_alive_in_minutes = keep_alive_in_minutes
        if page_number is not None:
            self.page_number = page_number

    @property
    def page_size(self):
        """Gets the page_size of this GrantaServerApiSearchPagingOptions.  # noqa: E501
        The number of results that should be returned in each page  # noqa: E501

        :return: The page_size of this GrantaServerApiSearchPagingOptions.  # noqa: E501
        :rtype: int
        """
        return self._page_size

    @page_size.setter
    def page_size(self, page_size):
        """Sets the page_size of this GrantaServerApiSearchPagingOptions.
        The number of results that should be returned in each page  # noqa: E501

        :param page_size: The page_size of this GrantaServerApiSearchPagingOptions.  # noqa: E501
        :type: int
        """
        self._page_size = page_size

    @property
    def keep_alive_in_minutes(self):
        """Gets the keep_alive_in_minutes of this GrantaServerApiSearchPagingOptions.  # noqa: E501
        The length of time that the paginated search should be kept in memory  # noqa: E501

        :return: The keep_alive_in_minutes of this GrantaServerApiSearchPagingOptions.  # noqa: E501
        :rtype: int
        """
        return self._keep_alive_in_minutes

    @keep_alive_in_minutes.setter
    def keep_alive_in_minutes(self, keep_alive_in_minutes):
        """Sets the keep_alive_in_minutes of this GrantaServerApiSearchPagingOptions.
        The length of time that the paginated search should be kept in memory  # noqa: E501

        :param keep_alive_in_minutes: The keep_alive_in_minutes of this GrantaServerApiSearchPagingOptions.  # noqa: E501
        :type: int
        """
        self._keep_alive_in_minutes = keep_alive_in_minutes

    @property
    def page_number(self):
        """Gets the page_number of this GrantaServerApiSearchPagingOptions.  # noqa: E501
        (Optional) the (1-indexed) number of the page to return from the search. No pages are returned if not provided  # noqa: E501

        :return: The page_number of this GrantaServerApiSearchPagingOptions.  # noqa: E501
        :rtype: int
        """
        return self._page_number

    @page_number.setter
    def page_number(self, page_number):
        """Sets the page_number of this GrantaServerApiSearchPagingOptions.
        (Optional) the (1-indexed) number of the page to return from the search. No pages are returned if not provided  # noqa: E501

        :param page_number: The page_number of this GrantaServerApiSearchPagingOptions.  # noqa: E501
        :type: int
        """
        self._page_number = page_number

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
        if issubclass(GrantaServerApiSearchPagingOptions, dict):
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
        if not isinstance(other, GrantaServerApiSearchPagingOptions):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
