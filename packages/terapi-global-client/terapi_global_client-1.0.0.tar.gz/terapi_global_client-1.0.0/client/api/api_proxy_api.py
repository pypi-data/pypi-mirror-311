from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from client.api_client import ApiClient


class ApiProxyApi(object):
 
    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def api_proxy_endpoint_delete(self, x_tenant_id, integration_name, endpoint, **kwargs):  # noqa: E501
        """21_997  # noqa: E501

        ### Error Codes  | Code | Name | Message |  | :--- | :--- | :--- |  | 21_997_101 | TenantNotFound |  |  | 21_997_102 | IntegrationNotFound |  |  | 21_997_103 | UnknownExceptionWhenCallingThirdPartyApi |  |  | 21_997_104 | UnknownExceptionWhenCallAction |  |  | 21_997_105 | IntegrationIsNotEnabled |  |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_proxy_endpoint_delete(x_tenant_id, integration_name, endpoint, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_tenant_id: (required)
        :param str integration_name: (required)
        :param str endpoint: (required)
        :param ApiproxyEndpointBody6 body:
        :return: CallActionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_proxy_endpoint_delete_with_http_info(x_tenant_id, integration_name, endpoint, **kwargs)  # noqa: E501
        else:
            (data) = self.api_proxy_endpoint_delete_with_http_info(x_tenant_id, integration_name, endpoint, **kwargs)  # noqa: E501
            return data

    def api_proxy_endpoint_delete_with_http_info(self, x_tenant_id, integration_name, endpoint, **kwargs):  # noqa: E501
        """21_997  # noqa: E501

        ### Error Codes  | Code | Name | Message |  | :--- | :--- | :--- |  | 21_997_101 | TenantNotFound |  |  | 21_997_102 | IntegrationNotFound |  |  | 21_997_103 | UnknownExceptionWhenCallingThirdPartyApi |  |  | 21_997_104 | UnknownExceptionWhenCallAction |  |  | 21_997_105 | IntegrationIsNotEnabled |  |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_proxy_endpoint_delete_with_http_info(x_tenant_id, integration_name, endpoint, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_tenant_id: (required)
        :param str integration_name: (required)
        :param str endpoint: (required)
        :param ApiproxyEndpointBody6 body:
        :return: CallActionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['x_tenant_id', 'integration_name', 'endpoint', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method api_proxy_endpoint_delete" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'x_tenant_id' is set
        if ('x_tenant_id' not in params or
                params['x_tenant_id'] is None):
            raise ValueError("Missing the required parameter `x_tenant_id` when calling `api_proxy_endpoint_delete`")  # noqa: E501
        # verify the required parameter 'integration_name' is set
        if ('integration_name' not in params or
                params['integration_name'] is None):
            raise ValueError("Missing the required parameter `integration_name` when calling `api_proxy_endpoint_delete`")  # noqa: E501
        # verify the required parameter 'endpoint' is set
        if ('endpoint' not in params or
                params['endpoint'] is None):
            raise ValueError("Missing the required parameter `endpoint` when calling `api_proxy_endpoint_delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'integration_name' in params:
            path_params['integrationName'] = params['integration_name']  # noqa: E501
        if 'endpoint' in params:
            path_params['endpoint'] = params['endpoint']  # noqa: E501

        query_params = []

        header_params = {}
        if 'x_tenant_id' in params:
            header_params['X-Tenant-Id'] = params['x_tenant_id']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['text/plain', 'application/json', 'text/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'text/json', 'application/*+json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Bearer']  # noqa: E501

        return self.api_client.call_api(
            '/api-proxy/{endpoint}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='CallActionResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def api_proxy_endpoint_get(self, integration_name, endpoint, x_tenant_id, **kwargs):  # noqa: E501
        """21_997  # noqa: E501

        ### Error Codes  | Code | Name | Message |  | :--- | :--- | :--- |  | 21_997_101 | TenantNotFound |  |  | 21_997_102 | IntegrationNotFound |  |  | 21_997_103 | UnknownExceptionWhenCallingThirdPartyApi |  |  | 21_997_104 | UnknownExceptionWhenCallAction |  |  | 21_997_105 | IntegrationIsNotEnabled |  |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_proxy_endpoint_get(integration_name, endpoint, x_tenant_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str integration_name: (required)
        :param str endpoint: (required)
        :param str x_tenant_id: (required)
        :return: CallActionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_proxy_endpoint_get_with_http_info(integration_name, endpoint, x_tenant_id, **kwargs)  # noqa: E501
        else:
            (data) = self.api_proxy_endpoint_get_with_http_info(integration_name, endpoint, x_tenant_id, **kwargs)  # noqa: E501
            return data

    def api_proxy_endpoint_get_with_http_info(self, integration_name, endpoint, x_tenant_id, **kwargs):  # noqa: E501
        """21_997  # noqa: E501

        ### Error Codes  | Code | Name | Message |  | :--- | :--- | :--- |  | 21_997_101 | TenantNotFound |  |  | 21_997_102 | IntegrationNotFound |  |  | 21_997_103 | UnknownExceptionWhenCallingThirdPartyApi |  |  | 21_997_104 | UnknownExceptionWhenCallAction |  |  | 21_997_105 | IntegrationIsNotEnabled |  |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_proxy_endpoint_get_with_http_info(integration_name, endpoint, x_tenant_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str integration_name: (required)
        :param str endpoint: (required)
        :param str x_tenant_id: (required)
        :return: CallActionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['integration_name', 'endpoint', 'x_tenant_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method api_proxy_endpoint_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'integration_name' is set
        if ('integration_name' not in params or
                params['integration_name'] is None):
            raise ValueError("Missing the required parameter `integration_name` when calling `api_proxy_endpoint_get`")  # noqa: E501
        # verify the required parameter 'endpoint' is set
        if ('endpoint' not in params or
                params['endpoint'] is None):
            raise ValueError("Missing the required parameter `endpoint` when calling `api_proxy_endpoint_get`")  # noqa: E501
        # verify the required parameter 'x_tenant_id' is set
        if ('x_tenant_id' not in params or
                params['x_tenant_id'] is None):
            raise ValueError("Missing the required parameter `x_tenant_id` when calling `api_proxy_endpoint_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'integration_name' in params:
            path_params['integrationName'] = params['integration_name']  # noqa: E501
        if 'endpoint' in params:
            path_params['endpoint'] = params['endpoint']  # noqa: E501

        query_params = []

        header_params = {}
        if 'x_tenant_id' in params:
            header_params['X-Tenant-Id'] = params['x_tenant_id']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['text/plain', 'application/json', 'text/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Bearer']  # noqa: E501

        return self.api_client.call_api(
            '/api-proxy/{endpoint}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='CallActionResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def api_proxy_endpoint_patch(self, x_tenant_id, integration_name, endpoint, **kwargs):  # noqa: E501
        """21_997  # noqa: E501

        ### Error Codes  | Code | Name | Message |  | :--- | :--- | :--- |  | 21_997_101 | TenantNotFound |  |  | 21_997_102 | IntegrationNotFound |  |  | 21_997_103 | UnknownExceptionWhenCallingThirdPartyApi |  |  | 21_997_104 | UnknownExceptionWhenCallAction |  |  | 21_997_105 | IntegrationIsNotEnabled |  |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_proxy_endpoint_patch(x_tenant_id, integration_name, endpoint, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_tenant_id: (required)
        :param str integration_name: (required)
        :param str endpoint: (required)
        :param ApiproxyEndpointBody9 body:
        :return: CallActionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_proxy_endpoint_patch_with_http_info(x_tenant_id, integration_name, endpoint, **kwargs)  # noqa: E501
        else:
            (data) = self.api_proxy_endpoint_patch_with_http_info(x_tenant_id, integration_name, endpoint, **kwargs)  # noqa: E501
            return data

    def api_proxy_endpoint_patch_with_http_info(self, x_tenant_id, integration_name, endpoint, **kwargs):  # noqa: E501
        """21_997  # noqa: E501

        ### Error Codes  | Code | Name | Message |  | :--- | :--- | :--- |  | 21_997_101 | TenantNotFound |  |  | 21_997_102 | IntegrationNotFound |  |  | 21_997_103 | UnknownExceptionWhenCallingThirdPartyApi |  |  | 21_997_104 | UnknownExceptionWhenCallAction |  |  | 21_997_105 | IntegrationIsNotEnabled |  |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_proxy_endpoint_patch_with_http_info(x_tenant_id, integration_name, endpoint, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_tenant_id: (required)
        :param str integration_name: (required)
        :param str endpoint: (required)
        :param ApiproxyEndpointBody9 body:
        :return: CallActionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['x_tenant_id', 'integration_name', 'endpoint', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method api_proxy_endpoint_patch" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'x_tenant_id' is set
        if ('x_tenant_id' not in params or
                params['x_tenant_id'] is None):
            raise ValueError("Missing the required parameter `x_tenant_id` when calling `api_proxy_endpoint_patch`")  # noqa: E501
        # verify the required parameter 'integration_name' is set
        if ('integration_name' not in params or
                params['integration_name'] is None):
            raise ValueError("Missing the required parameter `integration_name` when calling `api_proxy_endpoint_patch`")  # noqa: E501
        # verify the required parameter 'endpoint' is set
        if ('endpoint' not in params or
                params['endpoint'] is None):
            raise ValueError("Missing the required parameter `endpoint` when calling `api_proxy_endpoint_patch`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'integration_name' in params:
            path_params['integrationName'] = params['integration_name']  # noqa: E501
        if 'endpoint' in params:
            path_params['endpoint'] = params['endpoint']  # noqa: E501

        query_params = []

        header_params = {}
        if 'x_tenant_id' in params:
            header_params['X-Tenant-Id'] = params['x_tenant_id']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['text/plain', 'application/json', 'text/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'text/json', 'application/*+json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Bearer']  # noqa: E501

        return self.api_client.call_api(
            '/api-proxy/{endpoint}', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='CallActionResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def api_proxy_endpoint_post(self, x_tenant_id, integration_name, endpoint, **kwargs):  # noqa: E501
        """21_997  # noqa: E501

        ### Error Codes  | Code | Name | Message |  | :--- | :--- | :--- |  | 21_997_101 | TenantNotFound |  |  | 21_997_102 | IntegrationNotFound |  |  | 21_997_103 | UnknownExceptionWhenCallingThirdPartyApi |  |  | 21_997_104 | UnknownExceptionWhenCallAction |  |  | 21_997_105 | IntegrationIsNotEnabled |  |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_proxy_endpoint_post(x_tenant_id, integration_name, endpoint, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_tenant_id: (required)
        :param str integration_name: (required)
        :param str endpoint: (required)
        :param ApiproxyEndpointBody3 body:
        :return: CallActionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_proxy_endpoint_post_with_http_info(x_tenant_id, integration_name, endpoint, **kwargs)  # noqa: E501
        else:
            (data) = self.api_proxy_endpoint_post_with_http_info(x_tenant_id, integration_name, endpoint, **kwargs)  # noqa: E501
            return data

    def api_proxy_endpoint_post_with_http_info(self, x_tenant_id, integration_name, endpoint, **kwargs):  # noqa: E501
        """21_997  # noqa: E501

        ### Error Codes  | Code | Name | Message |  | :--- | :--- | :--- |  | 21_997_101 | TenantNotFound |  |  | 21_997_102 | IntegrationNotFound |  |  | 21_997_103 | UnknownExceptionWhenCallingThirdPartyApi |  |  | 21_997_104 | UnknownExceptionWhenCallAction |  |  | 21_997_105 | IntegrationIsNotEnabled |  |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_proxy_endpoint_post_with_http_info(x_tenant_id, integration_name, endpoint, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_tenant_id: (required)
        :param str integration_name: (required)
        :param str endpoint: (required)
        :param ApiproxyEndpointBody3 body:
        :return: CallActionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['x_tenant_id', 'integration_name', 'endpoint', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method api_proxy_endpoint_post" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'x_tenant_id' is set
        if ('x_tenant_id' not in params or
                params['x_tenant_id'] is None):
            raise ValueError("Missing the required parameter `x_tenant_id` when calling `api_proxy_endpoint_post`")  # noqa: E501
        # verify the required parameter 'integration_name' is set
        if ('integration_name' not in params or
                params['integration_name'] is None):
            raise ValueError("Missing the required parameter `integration_name` when calling `api_proxy_endpoint_post`")  # noqa: E501
        # verify the required parameter 'endpoint' is set
        if ('endpoint' not in params or
                params['endpoint'] is None):
            raise ValueError("Missing the required parameter `endpoint` when calling `api_proxy_endpoint_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'integration_name' in params:
            path_params['integrationName'] = params['integration_name']  # noqa: E501
        if 'endpoint' in params:
            path_params['endpoint'] = params['endpoint']  # noqa: E501

        query_params = []

        header_params = {}
        if 'x_tenant_id' in params:
            header_params['X-Tenant-Id'] = params['x_tenant_id']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['text/plain', 'application/json', 'text/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'text/json', 'application/*+json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Bearer']  # noqa: E501

        return self.api_client.call_api(
            '/api-proxy/{endpoint}', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='CallActionResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def api_proxy_endpoint_put(self, x_tenant_id, integration_name, endpoint, **kwargs):  # noqa: E501
        """21_997  # noqa: E501

        ### Error Codes  | Code | Name | Message |  | :--- | :--- | :--- |  | 21_997_101 | TenantNotFound |  |  | 21_997_102 | IntegrationNotFound |  |  | 21_997_103 | UnknownExceptionWhenCallingThirdPartyApi |  |  | 21_997_104 | UnknownExceptionWhenCallAction |  |  | 21_997_105 | IntegrationIsNotEnabled |  |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_proxy_endpoint_put(x_tenant_id, integration_name, endpoint, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_tenant_id: (required)
        :param str integration_name: (required)
        :param str endpoint: (required)
        :param ApiproxyEndpointBody body:
        :return: CallActionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_proxy_endpoint_put_with_http_info(x_tenant_id, integration_name, endpoint, **kwargs)  # noqa: E501
        else:
            (data) = self.api_proxy_endpoint_put_with_http_info(x_tenant_id, integration_name, endpoint, **kwargs)  # noqa: E501
            return data

    def api_proxy_endpoint_put_with_http_info(self, x_tenant_id, integration_name, endpoint, **kwargs):  # noqa: E501
        """21_997  # noqa: E501

        ### Error Codes  | Code | Name | Message |  | :--- | :--- | :--- |  | 21_997_101 | TenantNotFound |  |  | 21_997_102 | IntegrationNotFound |  |  | 21_997_103 | UnknownExceptionWhenCallingThirdPartyApi |  |  | 21_997_104 | UnknownExceptionWhenCallAction |  |  | 21_997_105 | IntegrationIsNotEnabled |  |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_proxy_endpoint_put_with_http_info(x_tenant_id, integration_name, endpoint, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_tenant_id: (required)
        :param str integration_name: (required)
        :param str endpoint: (required)
        :param ApiproxyEndpointBody body:
        :return: CallActionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['x_tenant_id', 'integration_name', 'endpoint', 'body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method api_proxy_endpoint_put" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'x_tenant_id' is set
        if ('x_tenant_id' not in params or
                params['x_tenant_id'] is None):
            raise ValueError("Missing the required parameter `x_tenant_id` when calling `api_proxy_endpoint_put`")  # noqa: E501
        # verify the required parameter 'integration_name' is set
        if ('integration_name' not in params or
                params['integration_name'] is None):
            raise ValueError("Missing the required parameter `integration_name` when calling `api_proxy_endpoint_put`")  # noqa: E501
        # verify the required parameter 'endpoint' is set
        if ('endpoint' not in params or
                params['endpoint'] is None):
            raise ValueError("Missing the required parameter `endpoint` when calling `api_proxy_endpoint_put`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'integration_name' in params:
            path_params['integrationName'] = params['integration_name']  # noqa: E501
        if 'endpoint' in params:
            path_params['endpoint'] = params['endpoint']  # noqa: E501

        query_params = []

        header_params = {}
        if 'x_tenant_id' in params:
            header_params['X-Tenant-Id'] = params['x_tenant_id']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['text/plain', 'application/json', 'text/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'text/json', 'application/*+json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Bearer']  # noqa: E501

        return self.api_client.call_api(
            '/api-proxy/{endpoint}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='CallActionResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def api_proxy_oauth2_challenge_get(self, **kwargs):  # noqa: E501
        """api_proxy_oauth2_challenge_get  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_proxy_oauth2_challenge_get(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str tenant_id:
        :return: OAuth2ChallengeDtoResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_proxy_oauth2_challenge_get_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.api_proxy_oauth2_challenge_get_with_http_info(**kwargs)  # noqa: E501
            return data

    def api_proxy_oauth2_challenge_get_with_http_info(self, **kwargs):  # noqa: E501
        """api_proxy_oauth2_challenge_get  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_proxy_oauth2_challenge_get_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str tenant_id:
        :return: OAuth2ChallengeDtoResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['tenant_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method api_proxy_oauth2_challenge_get" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'tenant_id' in params:
            query_params.append(('tenantId', params['tenant_id']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['text/plain', 'application/json', 'text/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Bearer']  # noqa: E501

        return self.api_client.call_api(
            '/api-proxy/oauth2/challenge', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='OAuth2ChallengeDtoResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def api_proxy_unified_contacts_external_id_get(self, external_id, **kwargs):  # noqa: E501
        """api_proxy_unified_contacts_external_id_get  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_proxy_unified_contacts_external_id_get(external_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str external_id: (required)
        :return: UnifiedContactResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_proxy_unified_contacts_external_id_get_with_http_info(external_id, **kwargs)  # noqa: E501
        else:
            (data) = self.api_proxy_unified_contacts_external_id_get_with_http_info(external_id, **kwargs)  # noqa: E501
            return data

    def api_proxy_unified_contacts_external_id_get_with_http_info(self, external_id, **kwargs):  # noqa: E501
        """api_proxy_unified_contacts_external_id_get  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_proxy_unified_contacts_external_id_get_with_http_info(external_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str external_id: (required)
        :return: UnifiedContactResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['external_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method api_proxy_unified_contacts_external_id_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'external_id' is set
        if ('external_id' not in params or
                params['external_id'] is None):
            raise ValueError("Missing the required parameter `external_id` when calling `api_proxy_unified_contacts_external_id_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'external_id' in params:
            path_params['externalId'] = params['external_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['text/plain', 'application/json', 'text/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Bearer']  # noqa: E501

        return self.api_client.call_api(
            '/api-proxy/unified/contacts/{externalId}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='UnifiedContactResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def api_proxy_unified_contacts_get(self, **kwargs):  # noqa: E501
        """api_proxy_unified_contacts_get  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_proxy_unified_contacts_get(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :return: UnifiedContactsListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.api_proxy_unified_contacts_get_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.api_proxy_unified_contacts_get_with_http_info(**kwargs)  # noqa: E501
            return data

    def api_proxy_unified_contacts_get_with_http_info(self, **kwargs):  # noqa: E501
        """api_proxy_unified_contacts_get  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.api_proxy_unified_contacts_get_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :return: UnifiedContactsListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = []  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method api_proxy_unified_contacts_get" % key
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
            ['text/plain', 'application/json', 'text/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['Bearer']  # noqa: E501

        return self.api_client.call_api(
            '/api-proxy/unified/contacts', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='UnifiedContactsListResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
