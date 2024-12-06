from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from client.api_client import ApiClient


class IntegrationApi(object):
 
    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def integration_get_get(self, **kwargs):  # noqa: E501
        """17_997  # noqa: E501

        ### Error Codes  | Code | Name | Message |  | :--- | :--- | :--- |  | 17_997_101 | UnknownExceptionWhenTryingFetchOneIntegration |  |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.integration_get_get(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id:
        :return: GetOneIntegrationResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.integration_get_get_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.integration_get_get_with_http_info(**kwargs)  # noqa: E501
            return data

    def integration_get_get_with_http_info(self, **kwargs):  # noqa: E501
        """17_997  # noqa: E501

        ### Error Codes  | Code | Name | Message |  | :--- | :--- | :--- |  | 17_997_101 | UnknownExceptionWhenTryingFetchOneIntegration |  |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.integration_get_get_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id:
        :return: GetOneIntegrationResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method integration_get_get" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'id' in params:
            query_params.append(('Id', params['id']))  # noqa: E501

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
            '/integration/get', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GetOneIntegrationResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def integration_list_get(self, **kwargs):  # noqa: E501
        """17_999  # noqa: E501

        ### Error Codes  | Code | Name | Message |  | :--- | :--- | :--- |  | 17_999_101 | UnknownExceptionWhenTryingFetchIntegrations | Unknown exception when trying to fetch integrations. |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.integration_list_get(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int page:
        :param int per_page:
        :param str search_keyword:
        :param str category_id:
        :return: IntegrationListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.integration_list_get_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.integration_list_get_with_http_info(**kwargs)  # noqa: E501
            return data

    def integration_list_get_with_http_info(self, **kwargs):  # noqa: E501
        """17_999  # noqa: E501

        ### Error Codes  | Code | Name | Message |  | :--- | :--- | :--- |  | 17_999_101 | UnknownExceptionWhenTryingFetchIntegrations | Unknown exception when trying to fetch integrations. |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.integration_list_get_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int page:
        :param int per_page:
        :param str search_keyword:
        :param str category_id:
        :return: IntegrationListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['page', 'per_page', 'search_keyword', 'category_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method integration_list_get" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'page' in params:
            query_params.append(('Page', params['page']))  # noqa: E501
        if 'per_page' in params:
            query_params.append(('PerPage', params['per_page']))  # noqa: E501
        if 'search_keyword' in params:
            query_params.append(('SearchKeyword', params['search_keyword']))  # noqa: E501
        if 'category_id' in params:
            query_params.append(('CategoryId', params['category_id']))  # noqa: E501

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
            '/integration/list', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='IntegrationListResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
