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

from ansys.grantami.serverapi_openapi.models.granta_server_api_search_datum_criterion import GrantaServerApiSearchDatumCriterion  # noqa: F401,E501

class GrantaServerApiSearchDiscreteFunctionalRangeDatumCriterion(GrantaServerApiSearchDatumCriterion):
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
        'gte': 'int',
        'lte': 'int',
        'constraints': 'list[GrantaServerApiSearchParameterConstraint]'
    }
    if hasattr(GrantaServerApiSearchDatumCriterion, "swagger_types"):
        swagger_types.update(GrantaServerApiSearchDatumCriterion.swagger_types)

    attribute_map = {
        'type': 'type',
        'gte': 'gte',
        'lte': 'lte',
        'constraints': 'constraints'
    }
    if hasattr(GrantaServerApiSearchDatumCriterion, "attribute_map"):
        attribute_map.update(GrantaServerApiSearchDatumCriterion.attribute_map)

    subtype_mapping = {
        'constraints': 'GrantaServerApiSearchParameterConstraint'
    }


    def __init__(self, type='discreteFunctionalRange', gte=None, lte=None, constraints=None, *args, **kwargs):  # noqa: E501
        """GrantaServerApiSearchDiscreteFunctionalRangeDatumCriterion - a model defined in Swagger"""  # noqa: E501
        GrantaServerApiSearchDatumCriterion.__init__(self, *args, **kwargs)
        self._type = None
        self._gte = None
        self._lte = None
        self._constraints = None
        self.discriminator = None
        self.type = type
        if gte is not None:
            self.gte = gte
        if lte is not None:
            self.lte = lte
        if constraints is not None:
            self.constraints = constraints

    @property
    def type(self):
        """Gets the type of this GrantaServerApiSearchDiscreteFunctionalRangeDatumCriterion.  # noqa: E501

        :return: The type of this GrantaServerApiSearchDiscreteFunctionalRangeDatumCriterion.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this GrantaServerApiSearchDiscreteFunctionalRangeDatumCriterion.

        :param type: The type of this GrantaServerApiSearchDiscreteFunctionalRangeDatumCriterion.  # noqa: E501
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501
        self._type = type

    @property
    def gte(self):
        """Gets the gte of this GrantaServerApiSearchDiscreteFunctionalRangeDatumCriterion.  # noqa: E501
        Greater than or equal to  # noqa: E501

        :return: The gte of this GrantaServerApiSearchDiscreteFunctionalRangeDatumCriterion.  # noqa: E501
        :rtype: int
        """
        return self._gte

    @gte.setter
    def gte(self, gte):
        """Sets the gte of this GrantaServerApiSearchDiscreteFunctionalRangeDatumCriterion.
        Greater than or equal to  # noqa: E501

        :param gte: The gte of this GrantaServerApiSearchDiscreteFunctionalRangeDatumCriterion.  # noqa: E501
        :type: int
        """
        self._gte = gte

    @property
    def lte(self):
        """Gets the lte of this GrantaServerApiSearchDiscreteFunctionalRangeDatumCriterion.  # noqa: E501
        Less than or equal to  # noqa: E501

        :return: The lte of this GrantaServerApiSearchDiscreteFunctionalRangeDatumCriterion.  # noqa: E501
        :rtype: int
        """
        return self._lte

    @lte.setter
    def lte(self, lte):
        """Sets the lte of this GrantaServerApiSearchDiscreteFunctionalRangeDatumCriterion.
        Less than or equal to  # noqa: E501

        :param lte: The lte of this GrantaServerApiSearchDiscreteFunctionalRangeDatumCriterion.  # noqa: E501
        :type: int
        """
        self._lte = lte

    @property
    def constraints(self):
        """Gets the constraints of this GrantaServerApiSearchDiscreteFunctionalRangeDatumCriterion.  # noqa: E501
        Optional unit string. If not included, the gte and lte values are assumed to be in database units.  # noqa: E501

        :return: The constraints of this GrantaServerApiSearchDiscreteFunctionalRangeDatumCriterion.  # noqa: E501
        :rtype: list[GrantaServerApiSearchParameterConstraint]
        """
        return self._constraints

    @constraints.setter
    def constraints(self, constraints):
        """Sets the constraints of this GrantaServerApiSearchDiscreteFunctionalRangeDatumCriterion.
        Optional unit string. If not included, the gte and lte values are assumed to be in database units.  # noqa: E501

        :param constraints: The constraints of this GrantaServerApiSearchDiscreteFunctionalRangeDatumCriterion.  # noqa: E501
        :type: list[GrantaServerApiSearchParameterConstraint]
        """
        self._constraints = constraints

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
        if issubclass(GrantaServerApiSearchDiscreteFunctionalRangeDatumCriterion, dict):
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
        if not isinstance(other, GrantaServerApiSearchDiscreteFunctionalRangeDatumCriterion):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
