# Copyright (C) 2022 CVAT.ai Corporation
#
# SPDX-License-Identifier: MIT

# CVAT REST API
#
# REST API for Computer Vision Annotation Tool (CVAT)  # noqa: E501
#
# The version of the OpenAPI document: 2.4.6
# Contact: support@cvat.ai
# Generated by: https://openapi-generator.tech


from __future__ import annotations

import typing
import urllib3

import re  # noqa: F401

from cvat_sdk.api_client.api_client import ApiClient, Endpoint as _Endpoint
from cvat_sdk.api_client.model_utils import (  # noqa: F401
    date,
    datetime,
    file_type,
    none_type,
)
from cvat_sdk.api_client.model.comment_read import CommentRead
from cvat_sdk.api_client.model.comment_write_request import CommentWriteRequest
from cvat_sdk.api_client.model.paginated_comment_read_list import PaginatedCommentReadList
from cvat_sdk.api_client.model.patched_comment_write_request import PatchedCommentWriteRequest

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    # Enable introspection. Can't work normally due to cyclic imports
    from cvat_sdk.api_client.apis import *
    from cvat_sdk.api_client.models import *


class CommentsApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client
        self.create_endpoint = _Endpoint(
            settings={
                'response_schema': (CommentRead,),
                'auth': [
                    'basicAuth',
                    'csrfAuth',
                    'sessionAuth',
                    'signatureAuth',
                    'tokenAuth'
                ],
                'endpoint_path': '/api/comments',
                'operation_id': 'create',
                'http_method': 'POST',
                'servers': None,
            },
            params_map={
                'all': [
                    'comment_write_request',
                    'x_organization',
                    'org',
                    'org_id',
                ],
                'required': [
                    'comment_write_request',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'comment_write_request':
                        (CommentWriteRequest,),
                    'x_organization':
                        (str,),
                    'org':
                        (str,),
                    'org_id':
                        (int,),
                },
                'attribute_map': {
                    'x_organization': 'X-Organization',
                    'org': 'org',
                    'org_id': 'org_id',
                },
                'location_map': {
                    'comment_write_request': 'body',
                    'x_organization': 'header',
                    'org': 'query',
                    'org_id': 'query',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/vnd.cvat+json'
                ],
                'content_type': [
                    'application/json'
                ]
            },
            api_client=api_client
        )
        self.destroy_endpoint = _Endpoint(
            settings={
                'response_schema': None,
                'auth': [
                    'basicAuth',
                    'csrfAuth',
                    'sessionAuth',
                    'signatureAuth',
                    'tokenAuth'
                ],
                'endpoint_path': '/api/comments/{id}',
                'operation_id': 'destroy',
                'http_method': 'DELETE',
                'servers': None,
            },
            params_map={
                'all': [
                    'id',
                ],
                'required': [
                    'id',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'id':
                        (int,),
                },
                'attribute_map': {
                    'id': 'id',
                },
                'location_map': {
                    'id': 'path',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [],
                'content_type': [],
            },
            api_client=api_client
        )
        self.list_endpoint = _Endpoint(
            settings={
                'response_schema': (PaginatedCommentReadList,),
                'auth': [
                    'basicAuth',
                    'csrfAuth',
                    'sessionAuth',
                    'signatureAuth',
                    'tokenAuth'
                ],
                'endpoint_path': '/api/comments',
                'operation_id': 'list',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'x_organization',
                    'filter',
                    'frame_id',
                    'issue_id',
                    'job_id',
                    'org',
                    'org_id',
                    'owner',
                    'page',
                    'page_size',
                    'search',
                    'sort',
                ],
                'required': [],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'x_organization':
                        (str,),
                    'filter':
                        (str,),
                    'frame_id':
                        (int,),
                    'issue_id':
                        (int,),
                    'job_id':
                        (int,),
                    'org':
                        (str,),
                    'org_id':
                        (int,),
                    'owner':
                        (str,),
                    'page':
                        (int,),
                    'page_size':
                        (int,),
                    'search':
                        (str,),
                    'sort':
                        (str,),
                },
                'attribute_map': {
                    'x_organization': 'X-Organization',
                    'filter': 'filter',
                    'frame_id': 'frame_id',
                    'issue_id': 'issue_id',
                    'job_id': 'job_id',
                    'org': 'org',
                    'org_id': 'org_id',
                    'owner': 'owner',
                    'page': 'page',
                    'page_size': 'page_size',
                    'search': 'search',
                    'sort': 'sort',
                },
                'location_map': {
                    'x_organization': 'header',
                    'filter': 'query',
                    'frame_id': 'query',
                    'issue_id': 'query',
                    'job_id': 'query',
                    'org': 'query',
                    'org_id': 'query',
                    'owner': 'query',
                    'page': 'query',
                    'page_size': 'query',
                    'search': 'query',
                    'sort': 'query',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/vnd.cvat+json'
                ],
                'content_type': [],
            },
            api_client=api_client
        )
        self.partial_update_endpoint = _Endpoint(
            settings={
                'response_schema': (CommentRead,),
                'auth': [
                    'basicAuth',
                    'csrfAuth',
                    'sessionAuth',
                    'signatureAuth',
                    'tokenAuth'
                ],
                'endpoint_path': '/api/comments/{id}',
                'operation_id': 'partial_update',
                'http_method': 'PATCH',
                'servers': None,
            },
            params_map={
                'all': [
                    'id',
                    'patched_comment_write_request',
                ],
                'required': [
                    'id',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'id':
                        (int,),
                    'patched_comment_write_request':
                        (PatchedCommentWriteRequest,),
                },
                'attribute_map': {
                    'id': 'id',
                },
                'location_map': {
                    'id': 'path',
                    'patched_comment_write_request': 'body',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/vnd.cvat+json'
                ],
                'content_type': [
                    'application/json'
                ]
            },
            api_client=api_client
        )
        self.retrieve_endpoint = _Endpoint(
            settings={
                'response_schema': (CommentRead,),
                'auth': [
                    'basicAuth',
                    'csrfAuth',
                    'sessionAuth',
                    'signatureAuth',
                    'tokenAuth'
                ],
                'endpoint_path': '/api/comments/{id}',
                'operation_id': 'retrieve',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'id',
                ],
                'required': [
                    'id',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'id':
                        (int,),
                },
                'attribute_map': {
                    'id': 'id',
                },
                'location_map': {
                    'id': 'path',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/vnd.cvat+json'
                ],
                'content_type': [],
            },
            api_client=api_client
        )

    def create(
        self,
        comment_write_request: CommentWriteRequest,
        *,
        _parse_response: bool = True,
        _request_timeout: typing.Union[int, float, tuple] = None,
        _validate_inputs: bool = True,
        _validate_outputs: bool = True,
        _check_status: bool = True,
        _spec_property_naming: bool = False,
        _content_type: typing.Optional[str] = None,
        _host_index: typing.Optional[int] = None,
        _request_auths: typing.Optional[typing.List] = None,
        _async_call: bool = False,
        **kwargs,
    ) -> typing.Tuple[typing.Optional[CommentRead], urllib3.HTTPResponse]:
        """Method creates a comment  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass _async_call=True

        >>> thread = api.create(comment_write_request, _async_call=True)
        >>> result = thread.get()

        Args:
            comment_write_request (CommentWriteRequest):

        Keyword Args:
            x_organization (str): Organization unique slug. [optional]
            org (str): Organization unique slug. [optional]
            org_id (int): Organization identifier. [optional]
            _parse_response (bool): if False, the response data will not be parsed,
                None is returned for data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _validate_inputs (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _validate_outputs (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _check_status (bool): whether to check response status
                for being positive or not.
                Default is True
            _spec_property_naming (bool): True if the variable names in the input data
                are serialized names, as specified in the OpenAPI document.
                False if the variable names in the input data
                are pythonic names, e.g. snake case (default)
            _content_type (str/None): force body content-type.
                Default is None and content-type will be predicted by allowed
                content-types and body.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            _request_auths (list): set to override the auth_settings for an a single
                request; this effectively ignores the authentication
                in the spec for a single request.
                Default is None
            _async_call (bool): execute request asynchronously

        Returns:
            (CommentRead, HTTPResponse)
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs['_async_call'] = _async_call
        kwargs['_parse_response'] = _parse_response
        kwargs['_request_timeout'] = _request_timeout
        kwargs['_validate_inputs'] = _validate_inputs
        kwargs['_validate_outputs'] = _validate_outputs
        kwargs['_check_status'] = _check_status
        kwargs['_spec_property_naming'] = _spec_property_naming
        kwargs['_content_type'] = _content_type
        kwargs['_host_index'] = _host_index
        kwargs['_request_auths'] = _request_auths
        kwargs['comment_write_request'] = comment_write_request
        return self.create_endpoint.call_with_http_info(**kwargs)

    def destroy(
        self,
        id: int,
        *,
        _parse_response: bool = True,
        _request_timeout: typing.Union[int, float, tuple] = None,
        _validate_inputs: bool = True,
        _validate_outputs: bool = True,
        _check_status: bool = True,
        _spec_property_naming: bool = False,
        _content_type: typing.Optional[str] = None,
        _host_index: typing.Optional[int] = None,
        _request_auths: typing.Optional[typing.List] = None,
        _async_call: bool = False,
        **kwargs,
    ) -> typing.Tuple[typing.Optional[None], urllib3.HTTPResponse]:
        """Method deletes a comment  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass _async_call=True

        >>> thread = api.destroy(id, _async_call=True)
        >>> result = thread.get()

        Args:
            id (int): A unique integer value identifying this comment.

        Keyword Args:
            _parse_response (bool): if False, the response data will not be parsed,
                None is returned for data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _validate_inputs (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _validate_outputs (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _check_status (bool): whether to check response status
                for being positive or not.
                Default is True
            _spec_property_naming (bool): True if the variable names in the input data
                are serialized names, as specified in the OpenAPI document.
                False if the variable names in the input data
                are pythonic names, e.g. snake case (default)
            _content_type (str/None): force body content-type.
                Default is None and content-type will be predicted by allowed
                content-types and body.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            _request_auths (list): set to override the auth_settings for an a single
                request; this effectively ignores the authentication
                in the spec for a single request.
                Default is None
            _async_call (bool): execute request asynchronously

        Returns:
            (None, HTTPResponse)
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs['_async_call'] = _async_call
        kwargs['_parse_response'] = _parse_response
        kwargs['_request_timeout'] = _request_timeout
        kwargs['_validate_inputs'] = _validate_inputs
        kwargs['_validate_outputs'] = _validate_outputs
        kwargs['_check_status'] = _check_status
        kwargs['_spec_property_naming'] = _spec_property_naming
        kwargs['_content_type'] = _content_type
        kwargs['_host_index'] = _host_index
        kwargs['_request_auths'] = _request_auths
        kwargs['id'] = id
        return self.destroy_endpoint.call_with_http_info(**kwargs)

    def list(
        self,
        *,
        _parse_response: bool = True,
        _request_timeout: typing.Union[int, float, tuple] = None,
        _validate_inputs: bool = True,
        _validate_outputs: bool = True,
        _check_status: bool = True,
        _spec_property_naming: bool = False,
        _content_type: typing.Optional[str] = None,
        _host_index: typing.Optional[int] = None,
        _request_auths: typing.Optional[typing.List] = None,
        _async_call: bool = False,
        **kwargs,
    ) -> typing.Tuple[typing.Optional[PaginatedCommentReadList], urllib3.HTTPResponse]:
        """Method returns a paginated list of comments  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass _async_call=True

        >>> thread = api.list(_async_call=True)
        >>> result = thread.get()


        Keyword Args:
            x_organization (str): Organization unique slug. [optional]
            filter (str): A filter term. Available filter_fields: ['owner', 'id', 'issue_id', 'frame_id', 'job_id']. [optional]
            frame_id (int): A simple equality filter for the frame_id field. [optional]
            issue_id (int): A simple equality filter for the issue_id field. [optional]
            job_id (int): A simple equality filter for the job_id field. [optional]
            org (str): Organization unique slug. [optional]
            org_id (int): Organization identifier. [optional]
            owner (str): A simple equality filter for the owner field. [optional]
            page (int): A page number within the paginated result set.. [optional]
            page_size (int): Number of results to return per page.. [optional]
            search (str): A search term. Available search_fields: ('owner',). [optional]
            sort (str): Which field to use when ordering the results. Available ordering_fields: ['owner', 'id', 'issue_id', 'frame_id', 'job_id']. [optional]
            _parse_response (bool): if False, the response data will not be parsed,
                None is returned for data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _validate_inputs (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _validate_outputs (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _check_status (bool): whether to check response status
                for being positive or not.
                Default is True
            _spec_property_naming (bool): True if the variable names in the input data
                are serialized names, as specified in the OpenAPI document.
                False if the variable names in the input data
                are pythonic names, e.g. snake case (default)
            _content_type (str/None): force body content-type.
                Default is None and content-type will be predicted by allowed
                content-types and body.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            _request_auths (list): set to override the auth_settings for an a single
                request; this effectively ignores the authentication
                in the spec for a single request.
                Default is None
            _async_call (bool): execute request asynchronously

        Returns:
            (PaginatedCommentReadList, HTTPResponse)
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs['_async_call'] = _async_call
        kwargs['_parse_response'] = _parse_response
        kwargs['_request_timeout'] = _request_timeout
        kwargs['_validate_inputs'] = _validate_inputs
        kwargs['_validate_outputs'] = _validate_outputs
        kwargs['_check_status'] = _check_status
        kwargs['_spec_property_naming'] = _spec_property_naming
        kwargs['_content_type'] = _content_type
        kwargs['_host_index'] = _host_index
        kwargs['_request_auths'] = _request_auths
        return self.list_endpoint.call_with_http_info(**kwargs)

    def partial_update(
        self,
        id: int,
        *,
        _parse_response: bool = True,
        _request_timeout: typing.Union[int, float, tuple] = None,
        _validate_inputs: bool = True,
        _validate_outputs: bool = True,
        _check_status: bool = True,
        _spec_property_naming: bool = False,
        _content_type: typing.Optional[str] = None,
        _host_index: typing.Optional[int] = None,
        _request_auths: typing.Optional[typing.List] = None,
        _async_call: bool = False,
        **kwargs,
    ) -> typing.Tuple[typing.Optional[CommentRead], urllib3.HTTPResponse]:
        """Methods does a partial update of chosen fields in a comment  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass _async_call=True

        >>> thread = api.partial_update(id, _async_call=True)
        >>> result = thread.get()

        Args:
            id (int): A unique integer value identifying this comment.

        Keyword Args:
            patched_comment_write_request (PatchedCommentWriteRequest): [optional]
            _parse_response (bool): if False, the response data will not be parsed,
                None is returned for data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _validate_inputs (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _validate_outputs (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _check_status (bool): whether to check response status
                for being positive or not.
                Default is True
            _spec_property_naming (bool): True if the variable names in the input data
                are serialized names, as specified in the OpenAPI document.
                False if the variable names in the input data
                are pythonic names, e.g. snake case (default)
            _content_type (str/None): force body content-type.
                Default is None and content-type will be predicted by allowed
                content-types and body.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            _request_auths (list): set to override the auth_settings for an a single
                request; this effectively ignores the authentication
                in the spec for a single request.
                Default is None
            _async_call (bool): execute request asynchronously

        Returns:
            (CommentRead, HTTPResponse)
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs['_async_call'] = _async_call
        kwargs['_parse_response'] = _parse_response
        kwargs['_request_timeout'] = _request_timeout
        kwargs['_validate_inputs'] = _validate_inputs
        kwargs['_validate_outputs'] = _validate_outputs
        kwargs['_check_status'] = _check_status
        kwargs['_spec_property_naming'] = _spec_property_naming
        kwargs['_content_type'] = _content_type
        kwargs['_host_index'] = _host_index
        kwargs['_request_auths'] = _request_auths
        kwargs['id'] = id
        return self.partial_update_endpoint.call_with_http_info(**kwargs)

    def retrieve(
        self,
        id: int,
        *,
        _parse_response: bool = True,
        _request_timeout: typing.Union[int, float, tuple] = None,
        _validate_inputs: bool = True,
        _validate_outputs: bool = True,
        _check_status: bool = True,
        _spec_property_naming: bool = False,
        _content_type: typing.Optional[str] = None,
        _host_index: typing.Optional[int] = None,
        _request_auths: typing.Optional[typing.List] = None,
        _async_call: bool = False,
        **kwargs,
    ) -> typing.Tuple[typing.Optional[CommentRead], urllib3.HTTPResponse]:
        """Method returns details of a comment  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass _async_call=True

        >>> thread = api.retrieve(id, _async_call=True)
        >>> result = thread.get()

        Args:
            id (int): A unique integer value identifying this comment.

        Keyword Args:
            _parse_response (bool): if False, the response data will not be parsed,
                None is returned for data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _validate_inputs (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _validate_outputs (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _check_status (bool): whether to check response status
                for being positive or not.
                Default is True
            _spec_property_naming (bool): True if the variable names in the input data
                are serialized names, as specified in the OpenAPI document.
                False if the variable names in the input data
                are pythonic names, e.g. snake case (default)
            _content_type (str/None): force body content-type.
                Default is None and content-type will be predicted by allowed
                content-types and body.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            _request_auths (list): set to override the auth_settings for an a single
                request; this effectively ignores the authentication
                in the spec for a single request.
                Default is None
            _async_call (bool): execute request asynchronously

        Returns:
            (CommentRead, HTTPResponse)
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs['_async_call'] = _async_call
        kwargs['_parse_response'] = _parse_response
        kwargs['_request_timeout'] = _request_timeout
        kwargs['_validate_inputs'] = _validate_inputs
        kwargs['_validate_outputs'] = _validate_outputs
        kwargs['_check_status'] = _check_status
        kwargs['_spec_property_naming'] = _spec_property_naming
        kwargs['_content_type'] = _content_type
        kwargs['_host_index'] = _host_index
        kwargs['_request_auths'] = _request_auths
        kwargs['id'] = id
        return self.retrieve_endpoint.call_with_http_info(**kwargs)

