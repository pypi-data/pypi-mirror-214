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


class GrantaServerApiSchemaAttributesMathsContent(ModelBase):
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
        'curve_label': 'str',
        'transpose_axes': 'bool',
        'use_logarithmic_scale': 'bool',
        'expression': 'GrantaServerApiSchemaSlimEntitiesSlimExpression',
        'free_parameter': 'GrantaServerApiSchemaSlimEntitiesSlimNamedEntity',
        'parameter_contents': 'list[GrantaServerApiSchemaParametersParameterContent]'
    }

    attribute_map = {
        'curve_label': 'curveLabel',
        'transpose_axes': 'transposeAxes',
        'use_logarithmic_scale': 'useLogarithmicScale',
        'expression': 'expression',
        'free_parameter': 'freeParameter',
        'parameter_contents': 'parameterContents'
    }

    subtype_mapping = {
        'expression': 'GrantaServerApiSchemaSlimEntitiesSlimExpression',
        'freeParameter': 'GrantaServerApiSchemaSlimEntitiesSlimNamedEntity',
        'parameterContents': 'GrantaServerApiSchemaParametersParameterContent'
    }


    def __init__(self, curve_label=None, transpose_axes=None, use_logarithmic_scale=None, expression=None, free_parameter=None, parameter_contents=None):  # noqa: E501
        """GrantaServerApiSchemaAttributesMathsContent - a model defined in Swagger"""  # noqa: E501
        self._curve_label = None
        self._transpose_axes = None
        self._use_logarithmic_scale = None
        self._expression = None
        self._free_parameter = None
        self._parameter_contents = None
        self.discriminator = None
        if curve_label is not None:
            self.curve_label = curve_label
        if transpose_axes is not None:
            self.transpose_axes = transpose_axes
        if use_logarithmic_scale is not None:
            self.use_logarithmic_scale = use_logarithmic_scale
        if expression is not None:
            self.expression = expression
        if free_parameter is not None:
            self.free_parameter = free_parameter
        if parameter_contents is not None:
            self.parameter_contents = parameter_contents

    @property
    def curve_label(self):
        """Gets the curve_label of this GrantaServerApiSchemaAttributesMathsContent.  # noqa: E501

        :return: The curve_label of this GrantaServerApiSchemaAttributesMathsContent.  # noqa: E501
        :rtype: str
        """
        return self._curve_label

    @curve_label.setter
    def curve_label(self, curve_label):
        """Sets the curve_label of this GrantaServerApiSchemaAttributesMathsContent.

        :param curve_label: The curve_label of this GrantaServerApiSchemaAttributesMathsContent.  # noqa: E501
        :type: str
        """
        self._curve_label = curve_label

    @property
    def transpose_axes(self):
        """Gets the transpose_axes of this GrantaServerApiSchemaAttributesMathsContent.  # noqa: E501

        :return: The transpose_axes of this GrantaServerApiSchemaAttributesMathsContent.  # noqa: E501
        :rtype: bool
        """
        return self._transpose_axes

    @transpose_axes.setter
    def transpose_axes(self, transpose_axes):
        """Sets the transpose_axes of this GrantaServerApiSchemaAttributesMathsContent.

        :param transpose_axes: The transpose_axes of this GrantaServerApiSchemaAttributesMathsContent.  # noqa: E501
        :type: bool
        """
        self._transpose_axes = transpose_axes

    @property
    def use_logarithmic_scale(self):
        """Gets the use_logarithmic_scale of this GrantaServerApiSchemaAttributesMathsContent.  # noqa: E501

        :return: The use_logarithmic_scale of this GrantaServerApiSchemaAttributesMathsContent.  # noqa: E501
        :rtype: bool
        """
        return self._use_logarithmic_scale

    @use_logarithmic_scale.setter
    def use_logarithmic_scale(self, use_logarithmic_scale):
        """Sets the use_logarithmic_scale of this GrantaServerApiSchemaAttributesMathsContent.

        :param use_logarithmic_scale: The use_logarithmic_scale of this GrantaServerApiSchemaAttributesMathsContent.  # noqa: E501
        :type: bool
        """
        self._use_logarithmic_scale = use_logarithmic_scale

    @property
    def expression(self):
        """Gets the expression of this GrantaServerApiSchemaAttributesMathsContent.  # noqa: E501

        :return: The expression of this GrantaServerApiSchemaAttributesMathsContent.  # noqa: E501
        :rtype: GrantaServerApiSchemaSlimEntitiesSlimExpression
        """
        return self._expression

    @expression.setter
    def expression(self, expression):
        """Sets the expression of this GrantaServerApiSchemaAttributesMathsContent.

        :param expression: The expression of this GrantaServerApiSchemaAttributesMathsContent.  # noqa: E501
        :type: GrantaServerApiSchemaSlimEntitiesSlimExpression
        """
        self._expression = expression

    @property
    def free_parameter(self):
        """Gets the free_parameter of this GrantaServerApiSchemaAttributesMathsContent.  # noqa: E501

        :return: The free_parameter of this GrantaServerApiSchemaAttributesMathsContent.  # noqa: E501
        :rtype: GrantaServerApiSchemaSlimEntitiesSlimNamedEntity
        """
        return self._free_parameter

    @free_parameter.setter
    def free_parameter(self, free_parameter):
        """Sets the free_parameter of this GrantaServerApiSchemaAttributesMathsContent.

        :param free_parameter: The free_parameter of this GrantaServerApiSchemaAttributesMathsContent.  # noqa: E501
        :type: GrantaServerApiSchemaSlimEntitiesSlimNamedEntity
        """
        self._free_parameter = free_parameter

    @property
    def parameter_contents(self):
        """Gets the parameter_contents of this GrantaServerApiSchemaAttributesMathsContent.  # noqa: E501

        :return: The parameter_contents of this GrantaServerApiSchemaAttributesMathsContent.  # noqa: E501
        :rtype: list[GrantaServerApiSchemaParametersParameterContent]
        """
        return self._parameter_contents

    @parameter_contents.setter
    def parameter_contents(self, parameter_contents):
        """Sets the parameter_contents of this GrantaServerApiSchemaAttributesMathsContent.

        :param parameter_contents: The parameter_contents of this GrantaServerApiSchemaAttributesMathsContent.  # noqa: E501
        :type: list[GrantaServerApiSchemaParametersParameterContent]
        """
        self._parameter_contents = parameter_contents

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
        if issubclass(GrantaServerApiSchemaAttributesMathsContent, dict):
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
        if not isinstance(other, GrantaServerApiSchemaAttributesMathsContent):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
