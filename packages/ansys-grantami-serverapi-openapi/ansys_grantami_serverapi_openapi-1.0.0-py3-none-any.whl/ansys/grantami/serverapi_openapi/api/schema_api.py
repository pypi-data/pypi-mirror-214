# coding: utf-8

"""
    MI Server API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import re  # noqa: F401
from . import ApiBase


class SchemaApi(ApiBase):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def v1alpha_schema_mi_version_get(self, **kwargs):  # noqa: E501
        """Returns the currently running MI version to the caller.  # noqa: E501

        This method makes a synchronous HTTP request.

        :return: GrantaServerApiAdminMiVersion
        """
        kwargs['_return_http_data_only'] = True
        (data) = self.v1alpha_schema_mi_version_get_with_http_info(**kwargs)  # noqa: E501
        return data

    def v1alpha_schema_mi_version_get_with_http_info(self, **kwargs):  # noqa: E501
        """Returns the currently running MI version to the caller.  # noqa: E501

        This method makes a synchronous HTTP request.

        :return: GrantaServerApiAdminMiVersion
        """

        all_params = []  # noqa: E501
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in params['kwargs'].items():
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '{}' to method v1alpha_schema_mi_version_get".format(key)
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501
        
        response_type_map = {
            200: 'GrantaServerApiAdminMiVersion',
        }
        
        return self.api_client.call_api(
            '/v1alpha/schema/mi-version', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats,
            response_type_map=response_type_map)
