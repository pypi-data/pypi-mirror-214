##
#   Copyright 2021 Alibaba, Inc. and its affiliates. All Rights Reserved.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
##

# -*- coding: utf-8 -*-

import json
from typing import Type, Any, Dict, Union, Optional
from centaur.common.types import CentaurProtocol, CentaurResponse, CollectionMeta
from centaur.common.error import CentaurCode, CentaurException
from centaur.core.models.create_collection_request import CreateCollectionRequest
from centaur.core.models.describe_collection_request import DescribeCollectionRequest
from centaur.core.models.drop_collection_request import DropCollectionRequest
from centaur.core.collection import Collection

__all__ = ["Client"]


class Client(object):

    """
    A Client for interacting with Centaur Server
    """
    def __init__(self, *,
                 api_key: str,
                 endpoint: str = "47.97.181.111:80",
                 timeout: float = 10.0,
                 protocol: CentaurProtocol = CentaurProtocol.GRPC):

        """
        Create a new Centaur Client and Connect to Centaur Server.

        Args:
            api_key (str): access key provided by centaur server.
            endpoint (str): centaur server endpoint. [optional]
                            default is "centaur-hangzhou.aliyuncs.com".
            timeout (str): centaur server remote procedure call timeout in second. [optional]
                           default is 10.0 seconds, 0.0 means infinite timeout.
            protocol (CentaurProtocol): centaur server remote procedure call protocol. [optional]
                                        default is CentaurProtocol.GRPC, CentaurProtocol.HTTP is also supported.

        Return:
            Client, includes a series of Collection related operations

        Example:
            client = Client(api_key="test")
            if not client:
                raise RuntimeError(f"Client initialize Failed, error:{client.code}, message:{client.message}")
        """

        """
        api_key: str
        """
        self._api_key = api_key
        """
        endpoint: str
        """
        self._endpoint = endpoint
        """
        timeout: float = 10.0,
        """
        self._timeout = timeout
        """
        protocol: CentaurProtocol = CentaurProtocol.GRPC
        """
        self._protocol = protocol
        """
        _version: str
        """
        self._version = None
        """
        _handler: RPCHandler
        """
        self._handler = None
        """
        _code: str
        _message: str
        _request_id: str
        """
        self._code = CentaurCode.Unknown
        self._message = ""
        self._request_id = ""
        """
        _cache: dict
        """
        self._cache = {}

        if self._protocol == CentaurProtocol.GRPC:
            from centaur.core.handler.grpc_handler import GRPCHandler
            self._handler = GRPCHandler(endpoint=self._endpoint,
                                        api_key=self._api_key,
                                        timeout=self._timeout)
        elif self._protocol == CentaurProtocol.HTTP:
            from centaur.core.handler.http_handler import HTTPHandler
            self._handler = HTTPHandler(endpoint=self._endpoint,
                                        api_key=self._api_key,
                                        timeout=self._timeout)
        else:
            self._code = CentaurCode.InvalidArgument
            self._message = f"CentaurSDK Client Protocol({protocol}) is Invalid, only support CentaurProtocol.GRPC or CentaurProtocol.HTTP"
            return

        check_version_rsp = self._check_version()
        self._code = check_version_rsp.code
        self._message = check_version_rsp.message
        self._request_id = check_version_rsp.request_id
        if check_version_rsp.code == CentaurCode.Success:
            self._version = check_version_rsp.output

    def create(self,
               name: str,
               dimension: int,
               *,
               dtype: Union[Type[int], Type[float]] = float,
               fields_schema: Optional[Dict[str, Union[Type[str], Type[int], Type[float], Type[bool]]]] = None,
               metric: str = 'euclidean',
               extra_params: Optional[Dict[str, Any]] = None) -> CentaurResponse:

        """
        Create a Collection.

        Args:
            name (str): collection name
            dimension (int): vector dimension in collection
            dtype (Union[Type[int], Type[float], Type[bool]]): vector data type in collection
            fields_schema (Optional[Optional[Dict[str, Union[Type[str], Type[int], Type[float], Type[bool]]]]): attribute fields in vector
            metric (str): vector metric in collection, support 'euclidean' and 'dotproduct', default is 'euclidean'
            extra_params (Optional[Dict[str, Any]]): extra params for collection

        Return:
            CentaurResponse, include code / message / request_id,
                             code == CentaurCode.Success means create collection success, otherwise means failure.
        """

        if self._code != CentaurCode.Success:
            return CentaurResponse(None,
                                   exception=CentaurException(code=CentaurCode.RuntimeError,
                                                              reason="CentaurSDK Client initialize Failed",
                                                              request_id=self._request_id))

        try:
            create_request = CreateCollectionRequest(name=name,
                                                     dimension=dimension,
                                                     dtype=dtype,
                                                     fields_schema=fields_schema,
                                                     metric=metric,
                                                     extra_params=extra_params)
        except CentaurException as e:
            return CentaurResponse(None, exception=e)

        return CentaurResponse(self._handler.create_collection(create_request))

    def delete(self, name: str) -> CentaurResponse:

        """
        Delete a Collection.

        Args:
            name (str): collection name

        Return:
            CentaurResponse, include code / message / request_id,
                             code == CentaurCode.Success means Delete Collection success, otherwise means failure.
        """

        if self._code != CentaurCode.Success:
            return CentaurResponse(None,
                                   exception=CentaurException(code=CentaurCode.RuntimeError,
                                                              reason="CentaurSDK Client initialize Failed",
                                                              request_id=self._request_id))

        try:
            drop_request = DropCollectionRequest(name=name)
        except CentaurException as e:
            return CentaurResponse(None, exception=e)

        drop_response = CentaurResponse(self._handler.drop_collection(drop_request))
        if drop_response.code == CentaurCode.Success:
            if name in self._cache:
                self._cache.pop(name)
        return drop_response

    def describe(self, name: str) -> CentaurResponse:

        """
        Describe a Collection.

        Args:
            name (str): collection name

        Return:
            CentaurResponse, include code / message / request_id / output,
                             code == CentaurCode.Success means describe collection success and output include a collection meta, otherwise means failure.

        Example:
            rsp = self.client.describe("collection_name")
            if not rsp:
                raise RuntimeError(f"DescribeCollection Failed, error:{rsp.code}, message:{rsp.message}")
            collection_meta = rsp.output
            print("collection_meta:", collection_meta)
        """

        if self._code != CentaurCode.Success:
            return CentaurResponse(None,
                                   exception=CentaurException(code=CentaurCode.RuntimeError,
                                                              reason="CentaurSDK Client initialize Failed",
                                                              request_id=self._request_id))

        try:
            describe_request = DescribeCollectionRequest(name=name)
        except CentaurException as e:
            return CentaurResponse(None, exception=e)

        describe_response = CentaurResponse(self._handler.describe_collection(describe_request))
        if describe_response.code != CentaurCode.Success:
            return describe_response

        try:
            describe_response.output = CollectionMeta(meta=describe_response.output)
            return describe_response
        except CentaurException as e:
            return CentaurResponse(None, exception=e)

    def get(self, name: str) -> Collection:

        """
        Get a Collection Instance with a series of Doc related operations.

        Args:
            name (str): collection name

        Return:
            Collection or CentaurResponse, include code / message / request_id.
            if code == CentaurCode.Success means a collection instance is obtained and include a series of doc related operations.
            otherwise means failure and a centaurResponse instance is obtained.

        Example:
            collection = self.client.get("collection_name")
            if not collection:
                raise RuntimeError(f"GetCollection Failed, error:{collection.code}, message:{collection.message}")
            print("collection:", collection)
        """

        if self._code != CentaurCode.Success:
            return Collection(exception=CentaurException(code=CentaurCode.RuntimeError,
                                                         reason="CentaurSDK Client initialize Failed",
                                                         request_id=self._request_id))

        if name in self._cache:
            return self._cache[name]

        try:
            describe_request = DescribeCollectionRequest(name=name)
        except CentaurException as e:
            return Collection(exception=e)

        describe_response = CentaurResponse(self._handler.describe_collection(describe_request))
        if describe_response.code != CentaurCode.Success:
            return Collection(response=describe_response.response)

        try:
            collection_meta = CollectionMeta(meta=describe_response.output)
            self._cache[name] = Collection(response=describe_response.response,
                                           collection_meta=collection_meta,
                                           handler=self._handler)
            return self._cache[name]
        except CentaurException as e:
            return Collection(exception=e)

    def list(self) -> CentaurResponse:

        """
        Get a Collection Name List from Centaur Server.

        Return:
            CentaurResponse, include code / message / request_id / output,
                             code == CentaurCode.Success means output is a collection name List

        Example:
            rsp = self.client.list()
            if not rsp:
                raise RuntimeError(f"ListCollection Failed, error:{rsp.code}, message:{rsp.message}")
            collection_list = rsp.output
            print("collection_list:", collection_list)
        """

        if self._code != CentaurCode.Success:
            return CentaurResponse(None,
                                   exception=CentaurException(code=CentaurCode.RuntimeError,
                                                              reason="CentaurSDK Client initialize Failed",
                                                              request_id=self._request_id))

        list_response = CentaurResponse(self._handler.list_collections())
        if list_response.code != CentaurCode.Success:
            return list_response

        collection_list = []
        if not isinstance(list_response.output, list):
            list_response.output = collection_list
            return list_response

        for collection in list_response.output:
            if 'collection_name' in collection['schema']:
                collection_list.append(collection['schema']['collection_name'])

        list_response.output = collection_list
        return list_response

    def close(self) -> None:

        """
        Close a Centaur Client

        Return: None
        """

        if self._code != CentaurCode.Success:
            return None

        self._code = CentaurCode.Closed
        self._cache = {}

        try:
            self._handler.close()
        except Exception as e:
            return None

    def _check_version(self) -> CentaurResponse:
        version_response = CentaurResponse(self._handler.get_version())
        if version_response.code != CentaurCode.Success:
            return version_response
        return version_response

    @property
    def code(self):
        return self._code

    @property
    def request_id(self):
        return self._request_id

    @property
    def message(self):
        return self._message

    @property
    def version(self):
        if self._version is None:
            return ""
        return self._version

    def __dict__(self):
        return {
            'code': self.code,
            'message': self.message,
            'request_id': self.request_id,
            'version': self.version
        }

    def __str__(self):
        return json.dumps(self.__dict__())

    def __repr__(self):
        return self.__str__()

    def __bool__(self):
        return self._code == CentaurCode.Success

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
