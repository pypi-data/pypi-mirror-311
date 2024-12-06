from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from client.api_client import ApiClient


class ApplicationApi(object):
 
    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def application_create_post(self, **kwargs):  # noqa: E501
        """15_999  # noqa: E501

        ### Error Codes  | Code | Name | Message |  | :--- | :--- | :--- |  | 15_999_101 | ApplicationNameAlreadyExist | Application name already exists. |  | 15_999_102 | UnknownExceptionWhenValidateApplicationNameUniqueness | Unknown exception when validating application name uniqueness. |  | 15_999_103 | UnknownExceptionWhenInsertApplication | Unknown exception when inserting application. |  | 15_999_104 | UserNotFound | User not found. |  | 15_999_105 | UnknownExceptionWhenCreateOrganization |  |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.application_create_post(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ApplicationCreateBody body:
        :return: CreateApplicationResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.application_create_post_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.application_create_post_with_http_info(**kwargs)  # noqa: E501
            return data

    def application_create_post_with_http_info(self, **kwargs):  # noqa: E501
        """15_999  # noqa: E501

        ### Error Codes  | Code | Name | Message |  | :--- | :--- | :--- |  | 15_999_101 | ApplicationNameAlreadyExist | Application name already exists. |  | 15_999_102 | UnknownExceptionWhenValidateApplicationNameUniqueness | Unknown exception when validating application name uniqueness. |  | 15_999_103 | UnknownExceptionWhenInsertApplication | Unknown exception when inserting application. |  | 15_999_104 | UserNotFound | User not found. |  | 15_999_105 | UnknownExceptionWhenCreateOrganization |  |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.application_create_post_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ApplicationCreateBody body:
        :return: CreateApplicationResponse
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
                    " to method application_create_post" % key
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
            '/application/create', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='CreateApplicationResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def application_delete_delete(self, **kwargs):  # noqa: E501
        """15_997  # noqa: E501

        ### Error Codes  | Code | Name | Message |  | :--- | :--- | :--- |  | 15_997_101 | ApplicationNotFound | Application not found. |  | 15_997_102 | UnknownExceptionWhenFetchApplicationExistence | Unknown exception when fetching application existence. |  | 15_997_103 | UnknownExceptionWhenDeleteApplication | Unknown exception when deleting application. |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.application_delete_delete(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id:
        :return: DeleteApplicationResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.application_delete_delete_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.application_delete_delete_with_http_info(**kwargs)  # noqa: E501
            return data

    def application_delete_delete_with_http_info(self, **kwargs):  # noqa: E501
        """15_997  # noqa: E501

        ### Error Codes  | Code | Name | Message |  | :--- | :--- | :--- |  | 15_997_101 | ApplicationNotFound | Application not found. |  | 15_997_102 | UnknownExceptionWhenFetchApplicationExistence | Unknown exception when fetching application existence. |  | 15_997_103 | UnknownExceptionWhenDeleteApplication | Unknown exception when deleting application. |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.application_delete_delete_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str id:
        :return: DeleteApplicationResponse
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
                    " to method application_delete_delete" % key
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
            '/application/delete', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='DeleteApplicationResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def application_list_get(self, **kwargs):  # noqa: E501
        """15_996  # noqa: E501

        ### Error Codes  | Code | Name | Message |  | :--- | :--- | :--- |  | 15_996_101 | UnknownExceptionWhenTryingFetchApplications | Unknown exception when trying to fetch applications. |  | 15_996_102 | UserNotFound | User not found. |  | 15_996_103 | UnknownExceptionWhenInsertApplication | Unknown exception when inserting application. |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.application_list_get(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int page:
        :param int per_page:
        :return: UserApplicationListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.application_list_get_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.application_list_get_with_http_info(**kwargs)  # noqa: E501
            return data

    def application_list_get_with_http_info(self, **kwargs):  # noqa: E501
        """15_996  # noqa: E501

        ### Error Codes  | Code | Name | Message |  | :--- | :--- | :--- |  | 15_996_101 | UnknownExceptionWhenTryingFetchApplications | Unknown exception when trying to fetch applications. |  | 15_996_102 | UserNotFound | User not found. |  | 15_996_103 | UnknownExceptionWhenInsertApplication | Unknown exception when inserting application. |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.application_list_get_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int page:
        :param int per_page:
        :return: UserApplicationListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['page', 'per_page']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method application_list_get" % key
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
            '/application/list', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='UserApplicationListResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def application_update_put(self, **kwargs):  # noqa: E501
        """15_998  # noqa: E501

        ### Error Codes  | Code | Name | Message |  | :--- | :--- | :--- |  | 15_998_101 | ApplicationNotFound | Application not found. |  | 15_998_102 | UnknownExceptionWhenFetchApplication | Unknown exception when fetching application. |  | 15_998_103 | UnknownExceptionWhenInsertApplication | Unknown exception when inserting application. |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.application_update_put(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ApplicationUpdateBody body:
        :return: UpdateApplicationResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.application_update_put_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.application_update_put_with_http_info(**kwargs)  # noqa: E501
            return data

    def application_update_put_with_http_info(self, **kwargs):  # noqa: E501
        """15_998  # noqa: E501

        ### Error Codes  | Code | Name | Message |  | :--- | :--- | :--- |  | 15_998_101 | ApplicationNotFound | Application not found. |  | 15_998_102 | UnknownExceptionWhenFetchApplication | Unknown exception when fetching application. |  | 15_998_103 | UnknownExceptionWhenInsertApplication | Unknown exception when inserting application. |  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.application_update_put_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ApplicationUpdateBody body:
        :return: UpdateApplicationResponse
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
                    " to method application_update_put" % key
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
            '/application/update', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='UpdateApplicationResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
