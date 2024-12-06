from __future__ import annotations

import importlib
import os
from enum import Enum
from typing import Literal

from arraylake.log_util import get_logger
from arraylake.types import BucketResponse, LegacyBucketResponse
from arraylake.types import Repo as RepoModel
from arraylake.types import S3Credentials

logger = get_logger(__name__)

###
# TODO:
# Store the prefix in the metastore alongside the ID
###

ICECHUNK_REQUIRED_ENV_VARS = ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]


class CredentialType(Enum):
    ANONYMOUS = "anonymous"
    ENV = "env"
    PROVIDED = "provided"


def _raise_if_no_icechunk():
    """Check if icechunk is available in the environment and raise an error if it is not.

    Icechunk is required to interact with a V2 repo.
    """
    if not importlib.util.find_spec("icechunk"):
        raise ImportError("Icechunk not found in the environment! Icechunk repos are not supported.")


def _get_credential_type(credentials: S3Credentials | None) -> CredentialType:
    """Determines the credential type based on the given credentials.

    Args:
        credentials: Optional S3Credentials for data access

    Returns:
        CredentialType enum
    """
    if credentials is not None:
        return CredentialType.PROVIDED
    elif all(var in os.environ for var in ICECHUNK_REQUIRED_ENV_VARS):
        return CredentialType.ENV
    else:
        return CredentialType.ANONYMOUS


def _get_icechunk_storage_config(
    repo_id: str,
    bucket_config: BucketResponse,
    prefix: str | None = None,
    credential_type: CredentialType = CredentialType.ANONYMOUS,
    credentials: S3Credentials | None = None,
):  # Removed output type so icechunk import is not required
    """
    If S3 credentials are given, gets the Icechunk storage config from these
    creds. Otherwise, gets the storage config by looking in the environment
    for credentials.

    Args:
        repo_id: Repo ID to use as the storage config prefix
        bucket_config: BucketResponse object containing the bucket nickname
        prefix:
            Optional prefix to use in the Icechunk storage config.
            If not provided, the repo ID will be used.
        credential_type: The type of credentials to use for the storage config
        credentials: Optional S3Credentials for data access

    Returns:
        Icechunk StorageConfig object
    """
    # Check if icechunk is in the environment before proceeding
    _raise_if_no_icechunk()
    import icechunk

    prefix = prefix or str(repo_id)
    logger.debug(f"Using bucket {bucket_config.name} and prefix {prefix} for Icechunk storage config")
    # Check if bucket is an S3 or S3-compatible bucket
    if bucket_config.platform in ("s3", "s3c", "minio"):
        # Extract the endpoint URL from the bucket config, if it exists
        endpoint_url = bucket_config.extra_config.get("endpoint_url")
        if endpoint_url is not None:
            endpoint_url = str(endpoint_url)  # mypy thinks the endpoint_url could be a bool
        region = bucket_config.extra_config.get("region_name")
        if region is not None:
            region = str(region)  # mypy thinks the region could be a bool
        # Extract the use_ssl flag from the bucket config, if it exists
        use_ssl = bucket_config.extra_config.get("use_ssl", True)  # TODO: what should be the default?
        if credential_type is CredentialType.PROVIDED:
            if credentials is None:
                raise ValueError("Credentials must be provided when using the 'provided' credential type.")
            # If S3 credentials are given, use s3_from_config()
            logger.info("Using provided S3 credentials for Icechunk storage config")
            s3_credentials_obj = icechunk.S3Credentials(
                access_key_id=credentials.aws_access_key_id,
                secret_access_key=credentials.aws_secret_access_key,
                session_token=credentials.aws_session_token,
            )
            return icechunk.StorageConfig.s3_from_config(
                bucket=bucket_config.name,
                prefix=prefix,
                credentials=s3_credentials_obj,
                endpoint_url=endpoint_url,
                allow_http=not use_ssl,
                region=region,
            )
        elif credential_type is CredentialType.ENV:
            if not all(var in os.environ for var in ICECHUNK_REQUIRED_ENV_VARS):
                raise ValueError(f"Missing required environment variables for Icechunk storage config: {ICECHUNK_REQUIRED_ENV_VARS}")
            logger.info(f"Enviornment variables {ICECHUNK_REQUIRED_ENV_VARS} found. Using them for Icechunk storage config.")
            return icechunk.StorageConfig.s3_from_env(
                bucket=bucket_config.name,
                prefix=prefix,
                allow_http=not use_ssl,
                endpoint_url=endpoint_url,
                region=region,
            )
        elif credential_type is CredentialType.ANONYMOUS:
            # If all else fails, use anonymous credentials
            logger.info("Using anonymous S3 credentials for Icechunk storage config")
            return icechunk.StorageConfig.s3_anonymous(
                bucket=bucket_config.name,
                prefix=prefix,
                endpoint_url=endpoint_url,
                allow_http=not use_ssl,
                region=region,
            )
        else:
            raise ValueError(f"Unsupported credential type: {credential_type}")
    else:
        raise ValueError(f"Unsupported bucket platform: {bucket_config.platform}")


async def icechunk_store_from_repo_model(
    repo_model: RepoModel,
    prefix: str | None,
    credential_type: CredentialType | None = None,
    credentials: S3Credentials | None = None,
    mode: Literal["r", "r+", "a", "w", "w-"] = "r",
):  # Removed output type so icechunk import is not required
    """Creates an IcechunkStore object from the RepoModel.

    To do this, we build the Icechunk StorageConfig to get the Icechunk store.

    Args:
        repo_model: Repo catalog object containing the repo name, ID, and bucket config
        prefix: Optional prefix for the storage config. If not provided, use repo UUID.
        credential_type: The type of credentials to use for the storage config
        credentials: Optional S3Credentials to use for data access
        mode: The mode to open the icechunk store in.

    Returns:
        IcechunkStore object
    """
    # Check if icechunk is in the environment before proceeding
    _raise_if_no_icechunk()
    from icechunk import IcechunkStore

    # Ensure the bucket isn't None
    # TODO: remove when bucket becomes required
    if repo_model.bucket is None:
        raise ValueError("The bucket on the catalog object cannot be None for Icechunk V2 repos!")

    # mypy seems to think that the bucket could be a legacy bucket response
    if isinstance(repo_model.bucket, LegacyBucketResponse):
        raise ValueError("The bucket on the catalog object cannot be a LegacyBucketResponse for Icechunk V2 repos!")

    # Build the icechunk storage config
    credential_type = credential_type or _get_credential_type(credentials)
    storage_config = _get_icechunk_storage_config(
        repo_id=str(repo_model.id), bucket_config=repo_model.bucket, prefix=prefix, credential_type=credential_type, credentials=credentials
    )

    # Calling open with mode=r+ will attempt to open the store, and if it fails, it will create it
    return IcechunkStore.open_or_create(storage=storage_config, mode=mode)
