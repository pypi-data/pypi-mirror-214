import calendar
import os
import re
import sys
import time
from copy import deepcopy
from typing import List, Generator, Dict, Any, Optional, Tuple

import requests
from azure.storage.blob import BlobClient, ContainerClient
from opensearchpy import OpenSearch
from opensearchpy.helpers import bulk

from ._internal_utils import TokenHolder, _get_azure_storage_url, _sanitize_url
from .config import _ENVS, _ACCESS_TOKEN_ENV_KEY, _REFRESH_TOKEN_ENV_KEY


class SDKClient:
    f"""
    client class providing methods for accessing SDK services: 
        - organizationmanager (access to organizations/spaces)
        - opensearch
        - storage
    
    Authorization for the SDK services is done using JWT tokens, which are stored in memory.
    For every request, the access token is refreshed if it is about to expire or has already expired.
    If no login information is passed to the main class 'SDKClient' during initialization, the access and refresh tokens are expected to be stored in the 
    environment variables of the execution environment.

    Usage::
        If access/refresh token can be found int the env-variables {_ACCESS_TOKEN_ENV_KEY} / {_REFRESH_TOKEN_ENV_KEY}
        >>> import superbdataklient as sdk
        >>> client = sdk.SDKClient()

        or with explicit login:
        >>> import superbdataklient as sdk
        >>> client = sdk.SDKClient(username='hasslethehoff', password='lookingforfreedom')
        
        this module is pre configured for usage with the default instance of the SDK (found here https://sdk.efs.ai) and comes with settings for various 
        different instances
        
        choosing different environment:
        >>> client = sdk.SDKClient(env='sdk-dev')
        
        overwriting settings:
        >>> client = sdk.SDKClient(domain='mydomain.ai', client_id='my-client-id', api_version='v13.37')
    """

    def __init__(self, **kwargs: str) -> None:
        self._env = deepcopy(_ENVS.get(kwargs.get('env', 'sdk')))

        # overwrite settings from args
        if 'domain' in kwargs:
            self._env.domain = kwargs.get('domain')
        if 'realm' in kwargs:
            self._env.realm = kwargs.get('realm')
        if 'client_id' in kwargs:
            self._env.client_id = kwargs.get('client_id')
        if 'api_version' in kwargs:
            self._env.api_version = kwargs.get('api_version')
        self.org_endpoint = f'https://{self._env.domain}/organizationmanager/api/{self._env.api_version}/organization'
        self.space_endpoint = f'https://{self._env.domain}/organizationmanager/api/{self._env.api_version}/space'

        if 'username' in kwargs and 'password' in kwargs:
            self._token_holder = TokenHolder(domain=self._env.domain, realm=self._env.realm, client_id=self._env.client_id)
            self._token_holder.get_tokens_with_credentials(kwargs['username'], kwargs['password'])
        else:
            try:
                access_token = os.environ[_ACCESS_TOKEN_ENV_KEY]
                refresh_token = os.environ[_REFRESH_TOKEN_ENV_KEY]
                self._token_holder = TokenHolder(domain=self._env.domain,
                                                 realm=self._env.realm,
                                                 client_id=self._env.client_id,
                                                 access_token=access_token,
                                                 refresh_token=refresh_token)
            except KeyError:
                print(f'Cannot read token environment variables {_ACCESS_TOKEN_ENV_KEY}, {_REFRESH_TOKEN_ENV_KEY}', file=sys.stderr)
                print('Assert that variables are set or try login initializing with username and password.', file=sys.stderr)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ organizations ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def organization_get_all(self) -> List[Dict[str, Any]]:
        """
        Fetches all Organizations the user has access to.

        :return:
            organizations
        """
        headers = {
            'Authorization': f'Bearer {self._token_holder.get_token()}'
        }
        response = requests.get(self.org_endpoint, headers=headers)
        response.raise_for_status()
        return response.json()

    def organization_get_by_id(self, org_id: int) -> Dict[str, Any]:
        """
        Fetch organization by id.

        :param org_id:
            id of the organization to be fetched
        :return:
            dictionary of the organization
        """
        url = f'{self.org_endpoint}/{org_id}'
        headers = {
            'Authorization': f'Bearer {self._token_holder.get_token()}'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def organization_get_by_name(self, org_name: str) -> Dict[str, Any]:
        """
        Fetches organization by name.

        :param org_name:
            name of the organization
        :return:
            dictionary of the organization
        """
        url = f'{self.org_endpoint}/name/{org_name}'
        headers = {
            'Authorization': f'Bearer {self._token_holder.get_token()}'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ spaces ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def space_get_all(self, org_id: int) -> List[Dict[str, Any]]:
        """
        Gets all spaces of a given organization if the user has access to.

        :param org_id:
            Organization id.
        :return:
            list of spaces

        """
        url = f'{self.space_endpoint}/{org_id}'
        headers = {
            'Authorization': f'Bearer {self._token_holder.get_token()}'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def space_get_by_id(self, org_id: int, space_id: int) -> Dict[str, Any]:
        """
        Fetch space by id.

        :param org_id:
            id of the organization to which the space belongs
        :param space_id:
            id of the space to be fetched
        :return:
            dictionary of the space
        """
        url = f'{self.space_endpoint}/{org_id}/{space_id}'
        headers = {
            'Authorization': f'Bearer {self._token_holder.get_token()}'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def space_get_by_name(self, org_id: int, space_name: str) -> Dict[str, Any]:
        """
        Fetches space by name.

        :param org_id:
            name of the organization to which the space belongs
        :param space_name:
            name of the space
        :return:
            dictionary of the space
        """
        url = f'{self.space_endpoint}/{org_id}/name/{space_name}'
        headers = {
            'Authorization': f'Bearer {self._token_holder.get_token()}'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def space_create(self, org_id: int, space: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a space within the organization specified by id.

        :param org_id:
            organization id within which the space should be created.
        :param space:
            dictionary defining space properties
        :return:
            response body of the http request

        """
        url = f'{self.space_endpoint}/{org_id}'
        headers = {
            "Content-Type": "application/json",
            "Authorization": f'Bearer {self._token_holder.get_token()}'
        }
        response = requests.post(url, json=space, headers=headers)
        response.raise_for_status()
        return response.json()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ indexing ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def index_get_all(self) -> Dict[str, Any]:
        """
        Fetches all indices accessible

        :return:
            indices

        """
        headers = {"Authorization": f"Bearer {self._token_holder.get_token()}"}
        url = f'https://{self._env.domain}/search/{self._env.api_version}/index'
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        res = response.json()

        return res

    def index_search(self, index: str, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        searches a given index with the given query
        :param index:
        :param query:
        :return:
        """
        headers = {
            "Authorization": f"Bearer {self._token_holder.get_token()}"
        }
        url = f'https://{self._env.domain}/elastic/api/{index}/_search'

        response = requests.get(url, headers=headers, json=query)
        response.raise_for_status()
        res = [hit['_source'] for hit in response.json()['hits']['hits']]

        return res

    def index_get_document(self, index: str, doc_id: str) -> Dict[str, Any]:
        """
        Fetches a document from a given opensearch index and returns it's content

        :param index:
            index name
        :param doc_id:
            document id
        :return:
            document

        """
        headers = {"Authorization": f"Bearer {self._token_holder.get_token()}"}
        url = f'https://{self._env.domain}/elastic/api/{index}/_doc/{doc_id}'
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        doc = response.json()['_source']

        return doc

    @staticmethod
    def _get_scroll_id_and_documents(url: str, headers: Dict[str, str]) -> Tuple[Optional[str], List[Dict[str, Any]]]:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        response_json = response.json()
        scroll_id = response_json.get('_scroll_id', None)
        documents = [hit['_source'] for hit in response_json.get('hits', {}).get('hits', [])]

        return scroll_id, documents

    def _delete_scroll_id(self, scroll_id: str, headers: Dict[str, str]) -> None:
        delete_url = f"https://{self._env.domain}/elastic/api/_search/scroll/{scroll_id}"
        response = requests.delete(delete_url, headers=headers)
        response.raise_for_status()

    def index_get_documents(self, index: str, scroll_duration: str = '10m', batch_size: int = 10000) -> Generator[Dict[str, Any], None, None]:
        """
        Generator that yields all documents in the provided OpenSearch index one by one.

        This method uses a generator to fetch the documents in batches, which can be more memory-efficient than fetching all documents at once.

        :param index: The OpenSearch index to retrieve documents from.
        :param scroll_duration: The duration a scroll id remains valid in OpenSearch. Defaults to '10m'.
        :param batch_size: The number of documents to fetch in each batch from OpenSearch. Defaults to 10000.

        :yield: Each document in the OpenSearch index.

        :raises: requests.RequestException if the GET or DELETE requests fail.
        """
        headers = {"Authorization": f"Bearer {self._token_holder.get_token()}"}
        url = f"https://{self._env.domain}/elastic/api/{index}/_search?scroll={scroll_duration}&size={batch_size}"

        scroll_id, documents = self._get_scroll_id_and_documents(url, headers)
        for document in documents:
            yield document

        while documents:
            url = f"https://{self._env.domain}/elastic/api/_search/scroll?scroll={scroll_duration}&scroll_id={scroll_id}"
            scroll_id, documents = self._get_scroll_id_and_documents(url, headers)
            for document in documents:
                yield document

        self._delete_scroll_id(scroll_id, headers)

    def index_get_all_documents(self, index: str) -> List[Dict[str, Any]]:
        """
        Fetches all documents from the specified OpenSearch index.

        :param index: The name of the OpenSearch index from which to fetch documents.

        :return: A list of all documents in the specified index. Each document is represented as a dictionary. If the index does not exist or is empty, an
        empty list is returned.

        :raises: requests.RequestException if there is an issue with the network request to fetch the documents.
        """
        return [doc for doc in self.index_get_documents(index)]

    def index_documents(self, documents: List[Dict[str, Any]], index_name: str, timeout: int = 60, chunk_size=10000) -> None:
        """
        indexes multiple documents to a given index.
        :param timeout:
            timeout for the bulk operation
        :param chunk_size:
        :param documents:
            list of dictionaries to index
        :param index_name:
            index name to index documents to
        :return:
        """
        url = f'https://{self._env.domain}/elastic/api/'
        es = OpenSearch(url, use_ssl=True, headers={"Authorization": "Bearer " + self._token_holder.get_token()}, timeout=timeout)

        # Create data for bulk api
        actions = [
            {
                "_index": index_name,
                "_id": entry.pop('_id') if '_id' in entry else None,
                "_source": entry
            } for entry in documents
        ]

        # Bulk ingest data
        bulk(es, actions, chunk_size=chunk_size)

        # Close Elasticsearch
        es.close()

    def index_filter_by_space(self, organization_name: str, space_name: str, index_type: str) -> List[str]:
        """
        Filtering index by organization, space and index type
        :organization_name:
            name of the organization
        :space_name:
            name of the space '*' for all spaces in the organization
        :index_type:
            type of the index, analysis or measurement
        """
        headers = {"Authorization": f"Bearer {self._token_holder.get_token()}"}
        url = f'https://{self._env.domain}/search/{self._env.api_version}/index?filter={organization_name}_{space_name}_{index_type.lower()}.*'
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        res = response.json()

        return res

    def application_index_create(self, index_name: str, org: str, space: str, mapping: object, index_type='ANALYSIS') -> str:
        """
        Creates an application index
        :index_name:
            custom name for the index
        :org:
            name of the organization
        :space:
            name of the space
        :mapping:
            the mapping
        :type:
            index type with ANALYSIS as default value
        :return:
            response body of the http request
        """

        application_index = {
            "organizationName": org,
            "spaceName": space,
            "customName": index_name,
            "indexType": index_type,
            "mappings": mapping
        }
        url = f'https://{self._env.domain}/metadata/{self._env.api_version}/application-index'
        headers = {
            "Content-Type": "application/json",
            "Authorization": f'Bearer {self._token_holder.get_token()}'
        }
        response = requests.post(url, json=application_index, headers=headers)
        response.raise_for_status()
        # not response.json(), because the endpoint gives me back a string. With json() i get a JSONDecoderError
        return response.text

    def application_index_delete(self, application_index_name: str) -> None:
        """
        Deletes an application index by name
        :application_index_name:
            name of the application index
        """
        url = f'https://{self._env.domain}/metadata/{self._env.api_version}/application-index/{application_index_name}'
        headers = {"Authorization": f'Bearer {self._token_holder.get_token()}'}
        response = requests.delete(url, headers=headers)
        response.raise_for_status()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ storage ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def storage_list_blobs(self, organization: str, space: str) -> List[str]:
        """
        Lists blobs in storage container
        :param organization:
        :param space:
        :return:
            list of blob names
        """
        storage_url = _get_azure_storage_url(organization, space)
        sas_token = self._get_azure_sas_token(organization, space, 'read')
        blob_client = ContainerClient.from_container_url(f'{storage_url}?{sas_token}')
        blobs = blob_client.list_blobs()
        result = [(b['name']) for b in blobs]
        return result

    def storage_upload_files(self, organization: str, space: str, files: List[str], local_dir: str) -> None:
        """
        This method uploads the specified files from a local directory to a designated storage belonging to a space of a particular organization.

        if metadataGenerate is not set on the given space, a 'meta.json' file has to be included in the list of files

        :param organization: str
            The name of the organization to which the space belongs.
        :param space: str
            The name of the space to which to upload the files to.
        :param files: List[str]
            The list of file to be uploaded.
            These files should be present in the specified local directory.
            Each string in the list is a path relative to the local directory.
        :param local_dir: str
            The local directory path on your file system from where files are to be uploaded.
            This path should be accessible with appropriate read permissions.
        :return: None
            This method does not return a value.
            If any exceptions occur during the operation, they will be thrown and should be handled by the calling function.
        """
        if not organization:
            raise ValueError('missing organization name arg')
        if not space:
            raise ValueError('missing space name arg')
        if not files:
            raise ValueError('missing files arg')
        if not local_dir:
            raise ValueError('missing local_dir arg')

        # TODO: rework with api refactoring - this is quite inefficient
        # check if meta.json is needed and/or provided
        org_object = self.organization_get_by_name(org_name=organization)
        space_object = self.space_get_by_name(org_id=org_object['id'], space_name=space)
        if space_object['metadataGenerate'] is False and 'meta.json' not in files:
            raise ValueError('metadataGenerate on space not set and meta.json is missing - required for upload.')

        json_file = open(f'{local_dir}/meta.json', 'r')
        json_string = json_file.read()
        json_file.close()
        validated = self._validate_json(json_string)
        if not validated:
            raise ValueError('meta.json invalid')

        storage_url = _get_azure_storage_url(organization, 'loadingzone')
        sas_token = self._get_azure_sas_token(organization, space, 'upload')
        timestamp = calendar.timegm(time.gmtime())  # timestamp to create the directory with
        for file in files:
            file_path = os.path.join(local_dir, file)
            if not os.path.exists(file_path):
                raise ValueError(f'File {file} does not exist in the specified directory.')
            blob_url = _sanitize_url(f'{storage_url}/{timestamp}/{file}?{sas_token}')
            self._upload_file_azure(blob_url, file_path)

        # start the ingest workflow
        url = f'{self._env.accessmanager_url}/commit?organization={organization}&space={space}&rootDir={timestamp}'
        url = _sanitize_url(url)

        payload = {}
        headers = {
            'Authorization': f'Bearer {self._token_holder.get_token()}'
        }

        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()

    @staticmethod
    def _upload_file_azure(blob_url: str, file_path: str) -> None:
        """
        Uploads files to azure
        :param blob_url:
        :param file_path:
        """
        with BlobClient.from_blob_url(blob_url) as blob_client:
            if not blob_client.exists():
                with open(file_path, "rb") as data:
                    blob_client.upload_blob(data)
            else:
                print(f"The file already exists in the loadingzone: {file_path}")

    def storage_download_files(self, organization: str, space: str, files: List[str], local_dir: str, storage_dir: str = '') -> None:
        """
        Downloads files from storage directory to local directory.
        :param organization:
        :param space:
        :param files:
        :param local_dir:
        :param storage_dir:
        :return:
        """
        return self._storage_download_files_azure(organization, space, files, local_dir, storage_dir)

    def _storage_download_files_azure(self, organization: str, space: str, files: List[str], local_dir: str, storage_dir: str = '') -> None:
        """
        Downloads files from Azure storage directory to local directory.

        For nested blobs local directories are created inside the temporary directory as well.

        Args:
            organization (str): Azure storage account
            space (str): Azure storage container
            storage_dir (str): root directory inside the space (Azure container) to be used
            files (List[str]): list of files to be downloaded
            local_dir (str): local directory to download the files to
        """
        if not organization:
            raise ValueError('missing organization name arg')
        if not space:
            raise ValueError('missing space name arg')
        if not files:
            raise ValueError('missing files arg')
        if not local_dir:
            raise ValueError('missing local_dir arg')

        storage_url = _get_azure_storage_url(organization, space)
        sas_token = self._get_azure_sas_token(organization, space, 'read')

        # download blobs to local directory
        for file in files:
            blob_url = _sanitize_url(f'{storage_url}/{storage_dir}/{file}?{sas_token}')
            with BlobClient.from_blob_url(blob_url) as blob_client:
                dest_file = os.path.join(local_dir, file)

                # for nested blobs, create local path as well!
                os.makedirs(os.path.dirname(dest_file), exist_ok=True)

                with open(dest_file, "wb") as f:
                    data = blob_client.download_blob()
                    data.readinto(f)

    def storage_download_files_with_regex(self, organization: str, space: str, local_dir: str, regex: str, storage_dir: str = '') -> None:
        """
        Downloads files from storage directory to local directory with regex expression.
        :param organization:
        :param space:
        :param local_dir:
        :param regex:
            The regex expression
        :param storage_dir:
        """
        files = self.storage_list_blobs(organization, space)
        files_to_download = []

        for file in files:
            if storage_dir in file:
                x = re.search(regex, file)
                if x:
                    files_to_download.append(file)
        self.storage_download_files(organization, space, files_to_download, local_dir)

    def _validate_json(self, file: str) -> bool:
        """
        Validates the given json
        :param file:
            The json
        :return:
            Returns a bool, to show if the json is valid or not
        """
        url = f'https://{self._env.domain}/metadata/{self._env.api_version}/validateJson'
        payload = file
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self._token_holder.get_token()}'
        }

        response = requests.post(url, headers=headers, data=payload)
        if 200 <= response.status_code < 300:  # valid meta.json
            return True
        if 400 <= response.status_code < 500:  # invalid meta.json
            return False
        else:
            response.raise_for_status()

    def _get_azure_sas_token(self, organization: str, space: str, reqtype: str = 'read') -> str:
        """
        Generates an upload-token via accessmanager (version > 1)

        Parameters
        ----------
        organization : str
            Organization the token shall be created for.
        space : str
            The space the token shall be created from
        reqtype : str
            Type of request. read|upload|delete

        Returns
        -------
        _type_
            The created SAS token.
        """
        url = f'{self._env.accessmanager_url}/{reqtype}?organization={organization}&space={space}'
        url = _sanitize_url(url)

        payload = {}
        headers = {
            'Authorization': f'Bearer {self._token_holder.get_token()}'
        }

        response = requests.post(url, headers=headers, data=payload)

        response.raise_for_status()

        return response.text

    def _storage_delete_files_azure(self, organization: str, space: str, files: List[str], storage_dir: str) -> None:
        """
        Deletes files from azure
        :param organization:
        :param space:
        :param files:
        :param storage_dir:
        """
        if not organization:
            raise ValueError('missing organization name arg')
        if not space:
            raise ValueError('missing space arg')
        if not files:
            raise ValueError('missing files arg')
        if not storage_dir:
            raise ValueError('missing storage_dir arg')

        storage_url = _get_azure_storage_url(organization, space)
        sas_token = self._get_azure_sas_token(organization, space, 'delete')

        for file in files:
            blob_url = _sanitize_url(f'{storage_url}/{storage_dir}/{file}?{sas_token}')
            with BlobClient.from_blob_url(blob_url) as blob_client:
                if blob_client.exists():
                    blob_client.delete_blob()
