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

from ansys.grantami.serverapi_openapi.models.granta_server_api_data_export_datums_link_datum import GrantaServerApiDataExportDatumsLinkDatum  # noqa: F401,E501

class GrantaServerApiDataExportDatumsLinkedRecordsDatum(GrantaServerApiDataExportDatumsLinkDatum):
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
        'link_group_name': 'str',
        'link_attribute_type': 'GrantaServerApiLinkAttributeType',
        'export_in_reversed_direction': 'bool',
        'target_database_guid': 'str',
        'linked_records': 'list[GrantaServerApiDataExportRecordWithData]',
        'link_group_names_by_database_key': 'dict(str, str)',
        'link_group_identities_by_database_key': 'dict(str, int)',
        'link_datum_type': 'str'
    }
    if hasattr(GrantaServerApiDataExportDatumsLinkDatum, "swagger_types"):
        swagger_types.update(GrantaServerApiDataExportDatumsLinkDatum.swagger_types)

    attribute_map = {
        'link_group_name': 'linkGroupName',
        'link_attribute_type': 'linkAttributeType',
        'export_in_reversed_direction': 'exportInReversedDirection',
        'target_database_guid': 'targetDatabaseGuid',
        'linked_records': 'linkedRecords',
        'link_group_names_by_database_key': 'linkGroupNamesByDatabaseKey',
        'link_group_identities_by_database_key': 'linkGroupIdentitiesByDatabaseKey',
        'link_datum_type': 'linkDatumType'
    }
    if hasattr(GrantaServerApiDataExportDatumsLinkDatum, "attribute_map"):
        attribute_map.update(GrantaServerApiDataExportDatumsLinkDatum.attribute_map)

    subtype_mapping = {
        'linkAttributeType': 'GrantaServerApiLinkAttributeType',
        'linkedRecords': 'GrantaServerApiDataExportRecordWithData',
    }


    def __init__(self, link_group_name=None, link_attribute_type=None, export_in_reversed_direction=None, target_database_guid=None, linked_records=None, link_group_names_by_database_key=None, link_group_identities_by_database_key=None, link_datum_type='linkGroup', *args, **kwargs):  # noqa: E501
        """GrantaServerApiDataExportDatumsLinkedRecordsDatum - a model defined in Swagger"""  # noqa: E501
        GrantaServerApiDataExportDatumsLinkDatum.__init__(self, *args, **kwargs)
        self._link_group_name = None
        self._link_attribute_type = None
        self._export_in_reversed_direction = None
        self._target_database_guid = None
        self._linked_records = None
        self._link_group_names_by_database_key = None
        self._link_group_identities_by_database_key = None
        self._link_datum_type = None
        self.discriminator = None
        if link_group_name is not None:
            self.link_group_name = link_group_name
        if link_attribute_type is not None:
            self.link_attribute_type = link_attribute_type
        if export_in_reversed_direction is not None:
            self.export_in_reversed_direction = export_in_reversed_direction
        if target_database_guid is not None:
            self.target_database_guid = target_database_guid
        if linked_records is not None:
            self.linked_records = linked_records
        if link_group_names_by_database_key is not None:
            self.link_group_names_by_database_key = link_group_names_by_database_key
        if link_group_identities_by_database_key is not None:
            self.link_group_identities_by_database_key = link_group_identities_by_database_key
        self.link_datum_type = link_datum_type

    @property
    def link_group_name(self):
        """Gets the link_group_name of this GrantaServerApiDataExportDatumsLinkedRecordsDatum.  # noqa: E501

        :return: The link_group_name of this GrantaServerApiDataExportDatumsLinkedRecordsDatum.  # noqa: E501
        :rtype: str
        """
        return self._link_group_name

    @link_group_name.setter
    def link_group_name(self, link_group_name):
        """Sets the link_group_name of this GrantaServerApiDataExportDatumsLinkedRecordsDatum.

        :param link_group_name: The link_group_name of this GrantaServerApiDataExportDatumsLinkedRecordsDatum.  # noqa: E501
        :type: str
        """
        self._link_group_name = link_group_name

    @property
    def link_attribute_type(self):
        """Gets the link_attribute_type of this GrantaServerApiDataExportDatumsLinkedRecordsDatum.  # noqa: E501

        :return: The link_attribute_type of this GrantaServerApiDataExportDatumsLinkedRecordsDatum.  # noqa: E501
        :rtype: GrantaServerApiLinkAttributeType
        """
        return self._link_attribute_type

    @link_attribute_type.setter
    def link_attribute_type(self, link_attribute_type):
        """Sets the link_attribute_type of this GrantaServerApiDataExportDatumsLinkedRecordsDatum.

        :param link_attribute_type: The link_attribute_type of this GrantaServerApiDataExportDatumsLinkedRecordsDatum.  # noqa: E501
        :type: GrantaServerApiLinkAttributeType
        """
        self._link_attribute_type = link_attribute_type

    @property
    def export_in_reversed_direction(self):
        """Gets the export_in_reversed_direction of this GrantaServerApiDataExportDatumsLinkedRecordsDatum.  # noqa: E501

        :return: The export_in_reversed_direction of this GrantaServerApiDataExportDatumsLinkedRecordsDatum.  # noqa: E501
        :rtype: bool
        """
        return self._export_in_reversed_direction

    @export_in_reversed_direction.setter
    def export_in_reversed_direction(self, export_in_reversed_direction):
        """Sets the export_in_reversed_direction of this GrantaServerApiDataExportDatumsLinkedRecordsDatum.

        :param export_in_reversed_direction: The export_in_reversed_direction of this GrantaServerApiDataExportDatumsLinkedRecordsDatum.  # noqa: E501
        :type: bool
        """
        self._export_in_reversed_direction = export_in_reversed_direction

    @property
    def target_database_guid(self):
        """Gets the target_database_guid of this GrantaServerApiDataExportDatumsLinkedRecordsDatum.  # noqa: E501

        :return: The target_database_guid of this GrantaServerApiDataExportDatumsLinkedRecordsDatum.  # noqa: E501
        :rtype: str
        """
        return self._target_database_guid

    @target_database_guid.setter
    def target_database_guid(self, target_database_guid):
        """Sets the target_database_guid of this GrantaServerApiDataExportDatumsLinkedRecordsDatum.

        :param target_database_guid: The target_database_guid of this GrantaServerApiDataExportDatumsLinkedRecordsDatum.  # noqa: E501
        :type: str
        """
        self._target_database_guid = target_database_guid

    @property
    def linked_records(self):
        """Gets the linked_records of this GrantaServerApiDataExportDatumsLinkedRecordsDatum.  # noqa: E501

        :return: The linked_records of this GrantaServerApiDataExportDatumsLinkedRecordsDatum.  # noqa: E501
        :rtype: list[GrantaServerApiDataExportRecordWithData]
        """
        return self._linked_records

    @linked_records.setter
    def linked_records(self, linked_records):
        """Sets the linked_records of this GrantaServerApiDataExportDatumsLinkedRecordsDatum.

        :param linked_records: The linked_records of this GrantaServerApiDataExportDatumsLinkedRecordsDatum.  # noqa: E501
        :type: list[GrantaServerApiDataExportRecordWithData]
        """
        self._linked_records = linked_records

    @property
    def link_group_names_by_database_key(self):
        """Gets the link_group_names_by_database_key of this GrantaServerApiDataExportDatumsLinkedRecordsDatum.  # noqa: E501

        :return: The link_group_names_by_database_key of this GrantaServerApiDataExportDatumsLinkedRecordsDatum.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._link_group_names_by_database_key

    @link_group_names_by_database_key.setter
    def link_group_names_by_database_key(self, link_group_names_by_database_key):
        """Sets the link_group_names_by_database_key of this GrantaServerApiDataExportDatumsLinkedRecordsDatum.

        :param link_group_names_by_database_key: The link_group_names_by_database_key of this GrantaServerApiDataExportDatumsLinkedRecordsDatum.  # noqa: E501
        :type: dict(str, str)
        """
        self._link_group_names_by_database_key = link_group_names_by_database_key

    @property
    def link_group_identities_by_database_key(self):
        """Gets the link_group_identities_by_database_key of this GrantaServerApiDataExportDatumsLinkedRecordsDatum.  # noqa: E501

        :return: The link_group_identities_by_database_key of this GrantaServerApiDataExportDatumsLinkedRecordsDatum.  # noqa: E501
        :rtype: dict(str, int)
        """
        return self._link_group_identities_by_database_key

    @link_group_identities_by_database_key.setter
    def link_group_identities_by_database_key(self, link_group_identities_by_database_key):
        """Sets the link_group_identities_by_database_key of this GrantaServerApiDataExportDatumsLinkedRecordsDatum.

        :param link_group_identities_by_database_key: The link_group_identities_by_database_key of this GrantaServerApiDataExportDatumsLinkedRecordsDatum.  # noqa: E501
        :type: dict(str, int)
        """
        self._link_group_identities_by_database_key = link_group_identities_by_database_key

    @property
    def link_datum_type(self):
        """Gets the link_datum_type of this GrantaServerApiDataExportDatumsLinkedRecordsDatum.  # noqa: E501

        :return: The link_datum_type of this GrantaServerApiDataExportDatumsLinkedRecordsDatum.  # noqa: E501
        :rtype: str
        """
        return self._link_datum_type

    @link_datum_type.setter
    def link_datum_type(self, link_datum_type):
        """Sets the link_datum_type of this GrantaServerApiDataExportDatumsLinkedRecordsDatum.

        :param link_datum_type: The link_datum_type of this GrantaServerApiDataExportDatumsLinkedRecordsDatum.  # noqa: E501
        :type: str
        """
        if link_datum_type is None:
            raise ValueError("Invalid value for `link_datum_type`, must not be `None`")  # noqa: E501
        self._link_datum_type = link_datum_type

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
        if issubclass(GrantaServerApiDataExportDatumsLinkedRecordsDatum, dict):
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
        if not isinstance(other, GrantaServerApiDataExportDatumsLinkedRecordsDatum):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
