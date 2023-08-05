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


class GrantaMISearchRecordPropertyFakeAttributeNumbers(ModelBase):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    allowed enum values
    """
    BREADCRUMBS_IDENTITY_10_GUID_00000007_0000_0000_0000_000000000000_ = "{\"name\":\"Breadcrumbs\",\"identity\":-10,\"guid\":\"00000007-0000-0000-0000-000000000000\"}"
    TREENAME_IDENTITY_9_GUID_00000006_0000_0000_0000_000000000000_ = "{\"name\":\"TreeName\",\"identity\":-9,\"guid\":\"00000006-0000-0000-0000-000000000000\"}"
    TABLEIDENTITY_IDENTITY_8_GUID_00000005_0000_0000_0000_000000000000_ = "{\"name\":\"TableIdentity\",\"identity\":-8,\"guid\":\"00000005-0000-0000-0000-000000000000\"}"
    TABLENAME_IDENTITY_7_GUID_00000004_0000_0000_0000_000000000000_ = "{\"name\":\"TableName\",\"identity\":-7,\"guid\":\"00000004-0000-0000-0000-000000000000\"}"
    RECORDCOLOR_IDENTITY_6_GUID_00000003_0000_0000_0000_000000000000_ = "{\"name\":\"RecordColor\",\"identity\":-6,\"guid\":\"00000003-0000-0000-0000-000000000000\"}"
    DATABASEKEY_IDENTITY_5_GUID_00000002_0000_0000_0000_000000000000_ = "{\"name\":\"DatabaseKey\",\"identity\":-5,\"guid\":\"00000002-0000-0000-0000-000000000000\"}"
    RECORDNAME_IDENTITY_4_GUID_00000001_0000_0000_0000_000000000000_ = "{\"name\":\"RecordName\",\"identity\":-4,\"guid\":\"00000001-0000-0000-0000-000000000000\"}"
    RECORDMODIFIEDBY_IDENTITY_3_GUID_00000009_0000_0000_0000_000000000000_ = "{\"name\":\"RecordModifiedBy\",\"identity\":-3,\"guid\":\"00000009-0000-0000-0000-000000000000\"}"
    RECORDCREATEDBY_IDENTITY_2_GUID_00000008_0000_0000_0000_000000000000_ = "{\"name\":\"RecordCreatedBy\",\"identity\":-2,\"guid\":\"00000008-0000-0000-0000-000000000000\"}"
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
    }

    attribute_map = {
    }

    subtype_mapping = {
    }


    def __init__(self):  # noqa: E501
        """GrantaMISearchRecordPropertyFakeAttributeNumbers - a model defined in Swagger"""  # noqa: E501
        self.discriminator = None

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
        if issubclass(GrantaMISearchRecordPropertyFakeAttributeNumbers, dict):
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
        if not isinstance(other, GrantaMISearchRecordPropertyFakeAttributeNumbers):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
