from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from client.api_client import ApiClient


class ApplicationApiKeyApi(object):
 
    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def application_apikey_generate_post(self, **kwargs):  # noqa: E501
        """16_999  # noqa: E501

        ### Error Codes  | Code | Name | Message |  | :--- | :--- | :--- |  | 16_999_101 | ApplicationNotFound | Application not found. |  | 16_999_102 | UnknownExceptionWhenCheckApplicationExistence | Unknown exception when checking if application exists. |  | 16_999_103 | UnknownExceptionWhenGenerateApplicationApiKey | Unknown exception when generating application API key. |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.application_apikey_generate_post(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ApplicationapikeyGenerateBody body:
        :return: CreateApplicationApiKeyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.application_apikey_generate_post_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.application_apikey_generate_post_with_http_info(**kwargs)  # noqa: E501
            return data

    def application_apikey_generate_post_with_http_info(self, **kwargs):  # noqa: E501
        """16_999  # noqa: E501

        ### Error Codes  | Code | Name | Message |  | :--- | :--- | :--- |  | 16_999_101 | ApplicationNotFound | Application not found. |  | 16_999_102 | UnknownExceptionWhenCheckApplicationExistence | Unknown exception when checking if application exists. |  | 16_999_103 | UnknownExceptionWhenGenerateApplicationApiKey | Unknown exception when generating application API key. |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.application_apikey_generate_post_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ApplicationapikeyGenerateBody body:
        :return: CreateApplicationApiKeyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method application_apikey_generate_post" % key
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
            '/application-apikey/generate', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='CreateApplicationApiKeyResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def application_apikey_get_by_application_id_get(self, **kwargs):  # noqa: E501
        """16_995  # noqa: E501

        ### Error Codes  | Code | Name | Message |  | :--- | :--- | :--- |  | 16_995_101 | ApplicationApiKeyNotFound | Application API key not found. |  | 16_995_102 | UnknownExceptionWhenTryingFetchApplications | Unknown exception when trying to fetch applications. |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.application_apikey_get_by_application_id_get(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str application_id:
        :return: ApplicationApiKeyByApplicationIdResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.application_apikey_get_by_application_id_get_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.application_apikey_get_by_application_id_get_with_http_info(**kwargs)  # noqa: E501
            return data

    def application_apikey_get_by_application_id_get_with_http_info(self, **kwargs):  # noqa: E501
        """16_995  # noqa: E501

        ### Error Codes  | Code | Name | Message |  | :--- | :--- | :--- |  | 16_995_101 | ApplicationApiKeyNotFound | Application API key not found. |  | 16_995_102 | UnknownExceptionWhenTryingFetchApplications | Unknown exception when trying to fetch applications. |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.application_apikey_get_by_application_id_get_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str application_id:
        :return: ApplicationApiKeyByApplicationIdResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['application_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method application_apikey_get_by_application_id_get" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'application_id' in params:
            query_params.append(('ApplicationId', params['application_id']))  # noqa: E501

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
            '/application-apikey/get-by-application-id', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ApplicationApiKeyByApplicationIdResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def application_apikey_revoke_delete(self, **kwargs):  # noqa: E501
        """16_998  # noqa: E501

        ### Error Codes  | Code | Name | Message |  | :--- | :--- | :--- |  | 16_998_101 | ApplicationApiKeyNotFound | Application API key not found. |  | 16_998_102 | UnknownExceptionWhenCheckApplicationExistence | Unknown exception when checking if application exists. |  | 16_998_103 | UnknownExceptionWhenGenerateApplicationApiKey | Unknown exception when generating application API key. |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.application_apikey_revoke_delete(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id:
        :return: RevokeApplicationApiKeyResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.application_apikey_revoke_delete_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.application_apikey_revoke_delete_with_http_info(**kwargs)  # noqa: E501
            return data

    def application_apikey_revoke_delete_with_http_info(self, **kwargs):  # noqa: E501
        """16_998  # noqa: E501

        ### Error Codes  | Code | Name | Message |  | :--- | :--- | :--- |  | 16_998_101 | ApplicationApiKeyNotFound | Application API key not found. |  | 16_998_102 | UnknownExceptionWhenCheckApplicationExistence | Unknown exception when checking if application exists. |  | 16_998_103 | UnknownExceptionWhenGenerateApplicationApiKey | Unknown exception when generating application API key. |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.application_apikey_revoke_delete_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id:
        :return: RevokeApplicationApiKeyResponse
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
                    " to method application_apikey_revoke_delete" % key
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
            '/application-apikey/revoke', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='RevokeApplicationApiKeyResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
