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

from ansys.grantami.serverapi_openapi.models.granta_server_api_schema_parameters_update_parameter import GrantaServerApiSchemaParametersUpdateParameter  # noqa: F401,E501

class GrantaServerApiSchemaParametersUpdateNumericParameter(GrantaServerApiSchemaParametersUpdateParameter):
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
        'type': 'str',
        'unit': 'GrantaServerApiSchemaSlimEntitiesSlimUnit',
        'interpolation_type': 'GrantaServerApiSchemaParametersParameterInterpolationType',
        'scale_type': 'GrantaServerApiSchemaParametersParameterScaleType'
    }
    if hasattr(GrantaServerApiSchemaParametersUpdateParameter, "swagger_types"):
        swagger_types.update(GrantaServerApiSchemaParametersUpdateParameter.swagger_types)

    attribute_map = {
        'type': 'type',
        'unit': 'unit',
        'interpolation_type': 'interpolationType',
        'scale_type': 'scaleType'
    }
    if hasattr(GrantaServerApiSchemaParametersUpdateParameter, "attribute_map"):
        attribute_map.update(GrantaServerApiSchemaParametersUpdateParameter.attribute_map)

    subtype_mapping = {
        'unit': 'GrantaServerApiSchemaSlimEntitiesSlimUnit',
        'interpolationType': 'GrantaServerApiSchemaParametersParameterInterpolationType',
        'scaleType': 'GrantaServerApiSchemaParametersParameterScaleType'
    }


    def __init__(self, type='numeric', unit=None, interpolation_type=None, scale_type=None, *args, **kwargs):  # noqa: E501
        """GrantaServerApiSchemaParametersUpdateNumericParameter - a model defined in Swagger"""  # noqa: E501
        GrantaServerApiSchemaParametersUpdateParameter.__init__(self, *args, **kwargs)
        self._type = None
        self._unit = None
        self._interpolation_type = None
        self._scale_type = None
        self.discriminator = None
        self.type = type
        if unit is not None:
            self.unit = unit
        if interpolation_type is not None:
            self.interpolation_type = interpolation_type
        if scale_type is not None:
            self.scale_type = scale_type

    @property
    def type(self):
        """Gets the type of this GrantaServerApiSchemaParametersUpdateNumericParameter.  # noqa: E501

        :return: The type of this GrantaServerApiSchemaParametersUpdateNumericParameter.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this GrantaServerApiSchemaParametersUpdateNumericParameter.

        :param type: The type of this GrantaServerApiSchemaParametersUpdateNumericParameter.  # noqa: E501
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501
        self._type = type

    @property
    def unit(self):
        """Gets the unit of this GrantaServerApiSchemaParametersUpdateNumericParameter.  # noqa: E501

        :return: The unit of this GrantaServerApiSchemaParametersUpdateNumericParameter.  # noqa: E501
        :rtype: GrantaServerApiSchemaSlimEntitiesSlimUnit
        """
        return self._unit

    @unit.setter
    def unit(self, unit):
        """Sets the unit of this GrantaServerApiSchemaParametersUpdateNumericParameter.

        :param unit: The unit of this GrantaServerApiSchemaParametersUpdateNumericParameter.  # noqa: E501
        :type: GrantaServerApiSchemaSlimEntitiesSlimUnit
        """
        self._unit = unit

    @property
    def interpolation_type(self):
        """Gets the interpolation_type of this GrantaServerApiSchemaParametersUpdateNumericParameter.  # noqa: E501

        :return: The interpolation_type of this GrantaServerApiSchemaParametersUpdateNumericParameter.  # noqa: E501
        :rtype: GrantaServerApiSchemaParametersParameterInterpolationType
        """
        return self._interpolation_type

    @interpolation_type.setter
    def interpolation_type(self, interpolation_type):
        """Sets the interpolation_type of this GrantaServerApiSchemaParametersUpdateNumericParameter.

        :param interpolation_type: The interpolation_type of this GrantaServerApiSchemaParametersUpdateNumericParameter.  # noqa: E501
        :type: GrantaServerApiSchemaParametersParameterInterpolationType
        """
        self._interpolation_type = interpolation_type

    @property
    def scale_type(self):
        """Gets the scale_type of this GrantaServerApiSchemaParametersUpdateNumericParameter.  # noqa: E501

        :return: The scale_type of this GrantaServerApiSchemaParametersUpdateNumericParameter.  # noqa: E501
        :rtype: GrantaServerApiSchemaParametersParameterScaleType
        """
        return self._scale_type

    @scale_type.setter
    def scale_type(self, scale_type):
        """Sets the scale_type of this GrantaServerApiSchemaParametersUpdateNumericParameter.

        :param scale_type: The scale_type of this GrantaServerApiSchemaParametersUpdateNumericParameter.  # noqa: E501
        :type: GrantaServerApiSchemaParametersParameterScaleType
        """
        self._scale_type = scale_type

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
        if issubclass(GrantaServerApiSchemaParametersUpdateNumericParameter, dict):
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
        if not isinstance(other, GrantaServerApiSchemaParametersUpdateNumericParameter):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
