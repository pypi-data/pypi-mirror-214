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

from ansys.grantami.serverapi_openapi.models.granta_server_api_data_export_datums_discrete_functional_datum import GrantaServerApiDataExportDatumsDiscreteFunctionalDatum  # noqa: F401,E501

class GrantaServerApiDataExportDatumsDiscreteFunctionalGridDatum(GrantaServerApiDataExportDatumsDiscreteFunctionalDatum):
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
        'graph_type': 'str',
        'values': 'list[GrantaServerApiDataExportDatumsDiscreteGridPoint]'
    }
    if hasattr(GrantaServerApiDataExportDatumsDiscreteFunctionalDatum, "swagger_types"):
        swagger_types.update(GrantaServerApiDataExportDatumsDiscreteFunctionalDatum.swagger_types)

    attribute_map = {
        'graph_type': 'graphType',
        'values': 'values'
    }
    if hasattr(GrantaServerApiDataExportDatumsDiscreteFunctionalDatum, "attribute_map"):
        attribute_map.update(GrantaServerApiDataExportDatumsDiscreteFunctionalDatum.attribute_map)

    subtype_mapping = {
        'values': 'GrantaServerApiDataExportDatumsDiscreteGridPoint'
    }


    def __init__(self, graph_type='grid', values=None, *args, **kwargs):  # noqa: E501
        """GrantaServerApiDataExportDatumsDiscreteFunctionalGridDatum - a model defined in Swagger"""  # noqa: E501
        GrantaServerApiDataExportDatumsDiscreteFunctionalDatum.__init__(self, *args, **kwargs)
        self._graph_type = None
        self._values = None
        self.discriminator = None
        self.graph_type = graph_type
        if values is not None:
            self.values = values

    @property
    def graph_type(self):
        """Gets the graph_type of this GrantaServerApiDataExportDatumsDiscreteFunctionalGridDatum.  # noqa: E501

        :return: The graph_type of this GrantaServerApiDataExportDatumsDiscreteFunctionalGridDatum.  # noqa: E501
        :rtype: str
        """
        return self._graph_type

    @graph_type.setter
    def graph_type(self, graph_type):
        """Sets the graph_type of this GrantaServerApiDataExportDatumsDiscreteFunctionalGridDatum.

        :param graph_type: The graph_type of this GrantaServerApiDataExportDatumsDiscreteFunctionalGridDatum.  # noqa: E501
        :type: str
        """
        if graph_type is None:
            raise ValueError("Invalid value for `graph_type`, must not be `None`")  # noqa: E501
        self._graph_type = graph_type

    @property
    def values(self):
        """Gets the values of this GrantaServerApiDataExportDatumsDiscreteFunctionalGridDatum.  # noqa: E501

        :return: The values of this GrantaServerApiDataExportDatumsDiscreteFunctionalGridDatum.  # noqa: E501
        :rtype: list[GrantaServerApiDataExportDatumsDiscreteGridPoint]
        """
        return self._values

    @values.setter
    def values(self, values):
        """Sets the values of this GrantaServerApiDataExportDatumsDiscreteFunctionalGridDatum.

        :param values: The values of this GrantaServerApiDataExportDatumsDiscreteFunctionalGridDatum.  # noqa: E501
        :type: list[GrantaServerApiDataExportDatumsDiscreteGridPoint]
        """
        self._values = values

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
        if issubclass(GrantaServerApiDataExportDatumsDiscreteFunctionalGridDatum, dict):
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
        if not isinstance(other, GrantaServerApiDataExportDatumsDiscreteFunctionalGridDatum):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
