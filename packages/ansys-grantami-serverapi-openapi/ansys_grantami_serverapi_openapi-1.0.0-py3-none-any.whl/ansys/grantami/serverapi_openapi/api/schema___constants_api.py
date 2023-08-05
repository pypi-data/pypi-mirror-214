# coding: utf-8

"""
    MI Server API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import re  # noqa: F401
from . import ApiBase


class SchemaConstantsApi(ApiBase):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def v1alpha_databases_database_key_constants_constant_guid_delete(self, database_key, constant_guid, **kwargs):  # noqa: E501
        """Delete a constant  # noqa: E501

        This method makes a synchronous HTTP request.

        :param str database_key: Database in which constant will be search for (required)
        :param str constant_guid: Guid of constant to delete (required)
        :return: None
        """
        kwargs['_return_http_data_only'] = True
        (data) = self.v1alpha_databases_database_key_constants_constant_guid_delete_with_http_info(database_key, constant_guid, **kwargs)  # noqa: E501
        return data

    def v1alpha_databases_database_key_constants_constant_guid_delete_with_http_info(self, database_key, constant_guid, **kwargs):  # noqa: E501
        """Delete a constant  # noqa: E501

        This method makes a synchronous HTTP request.

        :param str database_key: Database in which constant will be search for (required)
        :param str constant_guid: Guid of constant to delete (required)
        :return: None
        """

        all_params = ['database_key', 'constant_guid']  # noqa: E501
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in params['kwargs'].items():
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '{}' to method v1alpha_databases_database_key_constants_constant_guid_delete".format(key)
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'database_key' is set
        if ('database_key' not in params or
                params['database_key'] is None):
            raise ValueError("Missing the required parameter `database_key` when calling `v1alpha_databases_database_key_constants_constant_guid_delete`")  # noqa: E501
        # verify the required parameter 'constant_guid' is set
        if ('constant_guid' not in params or
                params['constant_guid'] is None):
            raise ValueError("Missing the required parameter `constant_guid` when calling `v1alpha_databases_database_key_constants_constant_guid_delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'database_key' in params:
            path_params['database-key'] = params['database_key']  # noqa: E501
        if 'constant_guid' in params:
            path_params['constant-guid'] = params['constant_guid']  # noqa: E501

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
            400: 'GrantaServerApiExceptionsConstantDeletionException',
            200: None,
            403: None,
            404: None,
        }
        
        return self.api_client.call_api(
            '/v1alpha/databases/{database-key}/constants/{constant-guid}', 'DELETE',
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

    def v1alpha_databases_database_key_constants_constant_guid_get(self, database_key, constant_guid, **kwargs):  # noqa: E501
        """Get individual constant  # noqa: E501

        This method makes a synchronous HTTP request.

        :param str database_key: Database in which constant will be search for (required)
        :param str constant_guid: Guid of requested constant (required)
        :return: GrantaServerApiSchemaConstantsConstant
        """
        kwargs['_return_http_data_only'] = True
        (data) = self.v1alpha_databases_database_key_constants_constant_guid_get_with_http_info(database_key, constant_guid, **kwargs)  # noqa: E501
        return data

    def v1alpha_databases_database_key_constants_constant_guid_get_with_http_info(self, database_key, constant_guid, **kwargs):  # noqa: E501
        """Get individual constant  # noqa: E501

        This method makes a synchronous HTTP request.

        :param str database_key: Database in which constant will be search for (required)
        :param str constant_guid: Guid of requested constant (required)
        :return: GrantaServerApiSchemaConstantsConstant
        """

        all_params = ['database_key', 'constant_guid']  # noqa: E501
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in params['kwargs'].items():
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '{}' to method v1alpha_databases_database_key_constants_constant_guid_get".format(key)
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'database_key' is set
        if ('database_key' not in params or
                params['database_key'] is None):
            raise ValueError("Missing the required parameter `database_key` when calling `v1alpha_databases_database_key_constants_constant_guid_get`")  # noqa: E501
        # verify the required parameter 'constant_guid' is set
        if ('constant_guid' not in params or
                params['constant_guid'] is None):
            raise ValueError("Missing the required parameter `constant_guid` when calling `v1alpha_databases_database_key_constants_constant_guid_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'database_key' in params:
            path_params['database-key'] = params['database_key']  # noqa: E501
        if 'constant_guid' in params:
            path_params['constant-guid'] = params['constant_guid']  # noqa: E501

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
            200: 'GrantaServerApiSchemaConstantsConstant',
            404: None,
        }
        
        return self.api_client.call_api(
            '/v1alpha/databases/{database-key}/constants/{constant-guid}', 'GET',
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

    def v1alpha_databases_database_key_constants_constant_guid_patch(self, database_key, constant_guid, **kwargs):  # noqa: E501
        """Update constant.  # noqa: E501

        This method makes a synchronous HTTP request.

        :param str database_key: Database in which constant will be search for (required)
        :param str constant_guid: Guid of constant to update (required)
        :param GrantaServerApiSchemaConstantsUpdateConstant body: Constant data to be updated
        :return: GrantaServerApiSchemaConstantsConstant
        """
        kwargs['_return_http_data_only'] = True
        (data) = self.v1alpha_databases_database_key_constants_constant_guid_patch_with_http_info(database_key, constant_guid, **kwargs)  # noqa: E501
        return data

    def v1alpha_databases_database_key_constants_constant_guid_patch_with_http_info(self, database_key, constant_guid, **kwargs):  # noqa: E501
        """Update constant.  # noqa: E501

        This method makes a synchronous HTTP request.

        :param str database_key: Database in which constant will be search for (required)
        :param str constant_guid: Guid of constant to update (required)
        :param GrantaServerApiSchemaConstantsUpdateConstant body: Constant data to be updated
        :return: GrantaServerApiSchemaConstantsConstant
        """

        all_params = ['database_key', 'constant_guid', 'body']  # noqa: E501
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in params['kwargs'].items():
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '{}' to method v1alpha_databases_database_key_constants_constant_guid_patch".format(key)
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'database_key' is set
        if ('database_key' not in params or
                params['database_key'] is None):
            raise ValueError("Missing the required parameter `database_key` when calling `v1alpha_databases_database_key_constants_constant_guid_patch`")  # noqa: E501
        # verify the required parameter 'constant_guid' is set
        if ('constant_guid' not in params or
                params['constant_guid'] is None):
            raise ValueError("Missing the required parameter `constant_guid` when calling `v1alpha_databases_database_key_constants_constant_guid_patch`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'database_key' in params:
            path_params['database-key'] = params['database_key']  # noqa: E501
        if 'constant_guid' in params:
            path_params['constant-guid'] = params['constant_guid']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json-patch+json', 'application/json', 'text/json', 'application/*+json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501
        
        response_type_map = {
            200: 'GrantaServerApiSchemaConstantsConstant',
            400: None,
            403: None,
            404: None,
        }
        
        return self.api_client.call_api(
            '/v1alpha/databases/{database-key}/constants/{constant-guid}', 'PATCH',
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

    def v1alpha_databases_database_key_constants_get(self, database_key, **kwargs):  # noqa: E501
        """Get all constants  # noqa: E501

        This method makes a synchronous HTTP request.

        :param str database_key: (required)
        :return: GrantaServerApiSchemaConstantsConstantsInfo
        """
        kwargs['_return_http_data_only'] = True
        (data) = self.v1alpha_databases_database_key_constants_get_with_http_info(database_key, **kwargs)  # noqa: E501
        return data

    def v1alpha_databases_database_key_constants_get_with_http_info(self, database_key, **kwargs):  # noqa: E501
        """Get all constants  # noqa: E501

        This method makes a synchronous HTTP request.

        :param str database_key: (required)
        :return: GrantaServerApiSchemaConstantsConstantsInfo
        """

        all_params = ['database_key']  # noqa: E501
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in params['kwargs'].items():
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '{}' to method v1alpha_databases_database_key_constants_get".format(key)
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'database_key' is set
        if ('database_key' not in params or
                params['database_key'] is None):
            raise ValueError("Missing the required parameter `database_key` when calling `v1alpha_databases_database_key_constants_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'database_key' in params:
            path_params['database-key'] = params['database_key']  # noqa: E501

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
            200: 'GrantaServerApiSchemaConstantsConstantsInfo',
            404: None,
        }
        
        return self.api_client.call_api(
            '/v1alpha/databases/{database-key}/constants', 'GET',
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

    def v1alpha_databases_database_key_constants_post(self, database_key, **kwargs):  # noqa: E501
        """Create a new constant.  # noqa: E501

        This method makes a synchronous HTTP request.

        :param str database_key: Database in which constant will be created (required)
        :param GrantaServerApiSchemaConstantsCreateConstant body: Constant to add to database
        :return: GrantaServerApiSchemaConstantsConstant
        """
        kwargs['_return_http_data_only'] = True
        (data) = self.v1alpha_databases_database_key_constants_post_with_http_info(database_key, **kwargs)  # noqa: E501
        return data

    def v1alpha_databases_database_key_constants_post_with_http_info(self, database_key, **kwargs):  # noqa: E501
        """Create a new constant.  # noqa: E501

        This method makes a synchronous HTTP request.

        :param str database_key: Database in which constant will be created (required)
        :param GrantaServerApiSchemaConstantsCreateConstant body: Constant to add to database
        :return: GrantaServerApiSchemaConstantsConstant
        """

        all_params = ['database_key', 'body']  # noqa: E501
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in params['kwargs'].items():
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '{}' to method v1alpha_databases_database_key_constants_post".format(key)
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'database_key' is set
        if ('database_key' not in params or
                params['database_key'] is None):
            raise ValueError("Missing the required parameter `database_key` when calling `v1alpha_databases_database_key_constants_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'database_key' in params:
            path_params['database-key'] = params['database_key']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json-patch+json', 'application/json', 'text/json', 'application/*+json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501
        
        response_type_map = {
            200: 'GrantaServerApiSchemaConstantsConstant',
            201: None,
            400: None,
            403: None,
            404: None,
        }
        
        return self.api_client.call_api(
            '/v1alpha/databases/{database-key}/constants', 'POST',
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
