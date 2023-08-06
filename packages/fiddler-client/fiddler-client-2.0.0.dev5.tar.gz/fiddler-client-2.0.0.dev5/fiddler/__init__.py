"""
Fiddler Client Module
=====================

A Python client for Fiddler service.

TODO: Add Licence.
"""
import configparser
import functools
import warnings
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from fiddler import utils
from fiddler._version import __version__
from fiddler.client import Fiddler, PredictionEventBundle
from fiddler.core_objects import (
    ArtifactStatus,
    BaselineType,
    BatchPublishType,
    Column,
    CustomFeature,
    DatasetInfo,
    DataType,
    DeploymentType,
    ExplanationMethod,
    FiddlerPublishSchema,
    FiddlerTimestamp,
    ModelInfo,
    ModelInputType,
    ModelTask,
    WeightingParams,
    WindowSize,
)
from fiddler.exceptions import NotSupported
from fiddler.fiddler_api import FiddlerApi as FiddlerApiV1
from fiddler.packtools import gem
from fiddler.utils import ColorLogger
from fiddler.v2.api.api import FiddlerClient
from fiddler.v2.api.explainability_mixin import (
    DatasetDataSource,
    RowDataSource,
    SqlSliceQueryDataSource,
)
from fiddler.v2.constants import CSV_EXTENSION, FileType
from fiddler.v2.schema.alert import (
    AlertCondition,
    AlertType,
    BinSize,
    ComparePeriod,
    CompareTo,
    Metric,
    Priority,
)
from fiddler.v2.schema.job import JobStatus
from fiddler.v2.schema.model_deployment import DeploymentParams, ModelDeployment
from fiddler.v2.utils.helpers import match_semvar, raise_not_supported
from fiddler.validator import PackageValidator, ValidationChainSettings, \
    ValidationModule

logger = utils.logging.getLogger(__name__)

SUPPORTED_API_VERSIONS = ['v2']


class FiddlerApi:
    """Client of all connections to the Fiddler API.
    :param url:         The base URL of the API to connect to. Usually either
        https://<yourorg>.fiddler.ai (cloud) or http://localhost:4100 (onebox)
    :param org_id:      The name of your organization in the Fiddler platform
    :param auth_token:  Token used to authenticate. Your token can be
        created, found, and changed at <FIDDLER URL>/settings/credentials.
    :param proxies:     Optionally, a dict of proxy URLs. e.g.,
                    proxies = {'http' : 'http://proxy.example.com:1234',
                               'https': 'https://proxy.example.com:5678'}
    :param verbose:     if True, api calls will be logged verbosely,
                    *warning: all information required for debugging will be
                    logged including the auth_token.
    :param timeout:     How long to wait for the server to respond before giving up
    :param version:     Version of the client you want to instantiate. Options [v1,v2]
    :param verify: if False, certificate verification will be disabled when
                establishing an SSL connection.
    """

    def __new__(
        cls,
        url: Optional[str] = None,
        org_id: Optional[str] = None,
        auth_token: Optional[str] = None,
        proxies: Optional[dict] = None,
        verbose: Optional[bool] = False,
        timeout: int = 1200,  # sec
        version: str = 'v2',
        verify: bool = True,
    ):
        url, org_id, auth_token = cls._get_connection_parameters(
            url, org_id, auth_token, version
        )

        # Validation of version, org_id is handled by FiddlerApiV1.
        client_v1 = FiddlerApiV1(
            url=url,
            org_id=org_id,
            auth_token=auth_token,
            proxies=proxies,
            verbose=verbose,
            timeout=timeout,
            verify=verify,
        )
        # @todo: Handle proxies in v2
        client_v2 = FiddlerClient(
            url=url,
            organization_name=org_id,
            auth_token=auth_token,
            timeout=timeout,
            verify=verify,
        )

        if match_semvar(
            client_v2.server_info.server_version,
            '<22.12.0',
        ):
            raise_not_supported(
                compatible_client_version='1.7',
                client_version=__version__,
                server_version=client_v2.server_info.server_version,
            )

        obj = lambda: None  # instantiate an empty object # noqa

        if match_semvar(
            client_v2.server_info.server_version,
            '>=23.2.0',
        ):
            obj.get_mutual_information = functools.partial(
                _get_mutual_information, client_v2
            )
            obj.get_mutual_information.__doc__ = (
                client_v1.get_mutual_information.__doc__
            )
        else:
            obj.get_mutual_information = client_v1.get_mutual_information

        # explicitly binding non-conflicting v1 methods to the v2 obj
        # conflicting methods will use v2 method by default for this condition
        # obj.project = client_v1.project

        # Alerts
        obj.get_alert_rules = client_v2.get_alert_rules
        obj.get_triggered_alerts = client_v2.get_triggered_alerts
        obj.add_alert_rule = client_v2.add_alert_rule
        obj.delete_alert_rule = client_v2.delete_alert_rule
        obj.build_notifications_config = client_v2.build_notifications_config

        # Baseline handling
        obj.add_baseline = client_v2.add_baseline
        obj.get_baseline = client_v2.get_baseline
        obj.list_baselines = client_v2.list_baselines
        obj.delete_baseline = client_v2.delete_baseline

        # Infer DatasetInfo using infer-data-type API
        obj.infer_dataset_info = client_v2.infer_dataset_info

        obj.v1 = client_v1
        obj.v2 = client_v2
        return obj

    @staticmethod
    def _get_connection_parameters(
        url: str, org_id: str, auth_token: str, version: int
    ) -> Tuple:
        if Path('fiddler.ini').is_file():
            config = configparser.ConfigParser()
            config.read('fiddler.ini')
            info = config['FIDDLER']
            if not url:
                url = info.get('url', None)
            if not org_id:
                org_id = info.get('org_id', None)
            if not auth_token:
                auth_token = info.get('auth_token', None)

        if not url:
            raise ValueError('Could not find url. Please enter a valid url')
        if not org_id:
            raise ValueError('Could not find org_id. Please enter a valid org_id')
        if not auth_token:
            raise ValueError(
                'Could not find auth_token. Please enter a valid auth_token'
            )
        if version not in SUPPORTED_API_VERSIONS:
            raise ValueError(
                f'version={version} not supported. Please enter a valid version. '
                f'Supported versions={SUPPORTED_API_VERSIONS}'
            )

        return url, org_id, auth_token


def _get_mutual_information(
    client_v2: FiddlerClient,
    project_id: str,
    dataset_id: str,
    features: List[str],
    normalized: Optional[bool] = False,
    slice_query: Optional[str] = None,
    sample_size: Optional[int] = 10000,
    seed: Optional[float] = None,
) -> Dict[str, Dict[str, float]]:
    """
    The Mutual information measures the dependency between two random variables.
    It's a non-negative value. If two random variables are independent MI is
    equal to zero. Higher MI values means higher dependency.

    :param project_id: The unique identifier of the model's project on the
        Fiddler engine.
    :param dataset_id: The unique identifier of the dataset in the
        Fiddler engine.
    :param features: list of features to compute mutual information with respect to
           all the variables in the dataset.
    :param normalized: If set to True, it will compute Normalized Mutual Information
    :param slice_query: Optional slice query
    :param sample_size: Optional sample size for the selected dataset
    :param seed: Optional seed for sampling
    :return: a dictionary of mutual information w.r.t the given features.
    """
    if seed:
        message = 'Argument seed is now deprecated, ignoring it.'
        warnings.warn(message, DeprecationWarning)

    if not slice_query:
        slice_query = f'SELECT * FROM {dataset_id}'

    if isinstance(features, list):
        message = (
            'Argument features will soon support a single column to compute '
            'mutual information on.'
        )
        warnings.warn(message, DeprecationWarning)

    if isinstance(features, str):
        features = [features]

    if not isinstance(features, list):
        raise ValueError(f'Invalid type: {type(features)} for the argument features.')

    # Compatibility layer
    response = {}
    for column_name in features:
        response[column_name] = client_v2.get_mutual_information(
            project_name=project_id,
            dataset_name=dataset_id,
            query=slice_query,
            column_name=column_name,
            normalized=normalized,
            num_samples=sample_size,
        )

    return response


__all__ = [
    '__version__',
    'BatchPublishType',
    'Column',
    'CustomFeature',
    'ColorLogger',
    'DatasetInfo',
    'DataType',
    'Fiddler',
    'FiddlerApi',
    'FiddlerClient',
    'FiddlerTimestamp',
    'FiddlerPublishSchema',
    'gem',
    'ModelInfo',
    'ModelInputType',
    'ModelTask',
    'WeightingParams',
    'ExplanationMethod',
    'PredictionEventBundle',
    'PackageValidator',
    'ValidationChainSettings',
    'ValidationModule',
    'utils',
    # Exposing constants
    'CSV_EXTENSION',
]
