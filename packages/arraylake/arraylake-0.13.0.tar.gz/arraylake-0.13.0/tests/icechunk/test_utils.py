import datetime
from uuid import uuid4

import icechunk
import pytest

from arraylake.client import AsyncClient
from arraylake.repos.icechunk.utils import (
    ICECHUNK_REQUIRED_ENV_VARS,
    CredentialType,
    _get_icechunk_storage_config,
    icechunk_store_from_repo_model,
)
from arraylake.types import DBID, BucketResponse, LegacyBucketResponse, Platform
from arraylake.types import Repo as RepoModel
from arraylake.types import (
    RepoOperationMode,
    RepoOperationStatusResponse,
    S3Credentials,
)

repo_id = DBID(b"some_repo_id")


@pytest.fixture
def bucket_config() -> BucketResponse:
    return BucketResponse(
        id=uuid4(),
        platform="s3",
        nickname="test-bucket-nickname",
        name="test",
        is_default=False,
        extra_config={
            "use_ssl": True,
            "endpoint_url": "http://foo.com",
            "region_name": "us-west-1",
        },
    )


def test_get_icechunk_storage_config_credentials(
    bucket_config: BucketResponse,
):
    creds = S3Credentials(
        aws_access_key_id="aws_access_key_id",
        aws_secret_access_key="aws_secret_access_key",
        aws_session_token="aws_session_token",
        expiration=None,
    )
    store_config = _get_icechunk_storage_config(
        repo_id=repo_id, bucket_config=bucket_config, prefix=None, credentials=creds, credential_type=CredentialType.PROVIDED
    )
    assert isinstance(store_config, icechunk.StorageConfig)

    # assert store_config.bucket == bucket_config.name
    # assert isinstance(store_config.credentials, icechunk.S3Credentials)
    # assert store_config.credentials.access_key_id == creds.aws_access_key_id
    # assert store_config.credentials.secret_access_key == creds.aws_secret_access_key
    # assert store_config.credentials.session_token == creds.aws_session_token

    # assert store_config.allow_http is False
    # assert store_config.anon is False
    # assert store_config.endpoint_url == "http://foo.com"
    # assert store_config.prefix == str(repo_id)
    # assert store_config.region == "us-west-1"


def test_get_icechunk_storage_config_from_env(bucket_config: BucketResponse, monkeypatch):
    for var in ICECHUNK_REQUIRED_ENV_VARS:
        monkeypatch.setenv(var, "test")

    store_config = _get_icechunk_storage_config(
        repo_id=repo_id, bucket_config=bucket_config, prefix=None, credentials=None, credential_type=CredentialType.ENV
    )
    assert isinstance(store_config, icechunk.StorageConfig)
    # assert store_config.bucket == bucket_config.name
    # # Credentials are None because these get passed to S3 directly from the environment in icechunk
    # assert store_config.credentials is None
    # assert store_config.anon is False

    # Remove environment variables
    for var in ICECHUNK_REQUIRED_ENV_VARS:
        monkeypatch.delenv(var)


def test_get_icechunk_storage_config_anonymous(
    bucket_config: BucketResponse,
):
    bucket_config = bucket_config.model_copy()
    bucket_config.extra_config["use_ssl"] = False
    del bucket_config.extra_config["endpoint_url"]
    del bucket_config.extra_config["region_name"]

    store_config = _get_icechunk_storage_config(
        repo_id=repo_id, bucket_config=bucket_config, prefix="test-prefix", credential_type=CredentialType.ANONYMOUS, credentials=None
    )
    assert isinstance(store_config, icechunk.StorageConfig)

    # assert store_config.bucket == bucket_config.name
    # assert store_config.credentials is None
    # assert store_config.allow_http is True
    # assert store_config.anon is True
    # assert store_config.endpoint_url is None
    # assert store_config.prefix == "test-prefix"
    # assert store_config.region is None


def test_get_icechunk_storage_config_gcs_raises():
    with pytest.raises(ValueError) as excinfo:
        _get_icechunk_storage_config(
            repo_id=repo_id,
            bucket_config=BucketResponse(
                id=uuid4(), nickname="gcs-bucket-test", platform="gs", name="gcs", is_default=False, extra_config={}
            ),
        )
    assert "Unsupported bucket platform" in str(excinfo)


@pytest.mark.asyncio
async def test_get_icechunk_store_from_repo_model_minio_from_env(isolated_org_with_bucket, token, monkeypatch):
    """Tests that the environment variables are used on the backend in icechunk for minio test setup"""
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "minio123")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "minio123")
    monkeypatch.setenv("AWS_REGION", "us-east-1")

    aclient = AsyncClient(token=token)
    org, bucket_nickname = isolated_org_with_bucket
    bucket_config = await aclient.get_bucket_config(org=org, nickname=bucket_nickname)

    repo_model = RepoModel(
        _id=repo_id,
        org="earthmover",
        name="repo-name",
        updated=datetime.datetime.now(),
        status=RepoOperationStatusResponse(mode=RepoOperationMode.ONLINE, initiated_by={}),
        bucket=bucket_config,
    )
    await icechunk_store_from_repo_model(repo_model=repo_model, prefix=None, mode="w")

    # Remove environment variables
    monkeypatch.delenv("AWS_ACCESS_KEY_ID")
    monkeypatch.delenv("AWS_SECRET_ACCESS_KEY")
    monkeypatch.delenv("AWS_REGION")


@pytest.mark.asyncio
async def test_icechunk_store_from_repo_model_no_bucket_raises():
    with pytest.raises(ValueError) as excinfo:
        await icechunk_store_from_repo_model(
            repo_model=RepoModel(
                _id=repo_id,
                org="earthmover",
                name="repo-name",
                updated=datetime.datetime.now(),
                status=RepoOperationStatusResponse(mode=RepoOperationMode.ONLINE, initiated_by={}),
                bucket=None,
            ),
            prefix=None,
        )
    assert "The bucket on the catalog object cannot be None for Icechunk V2 repos!" in str(excinfo.value)


@pytest.mark.asyncio
async def test_icechunk_store_from_repo_model_legacy_bucket_raises():
    with pytest.raises(ValueError) as excinfo:
        await icechunk_store_from_repo_model(
            repo_model=RepoModel(
                _id=repo_id,
                org="earthmover",
                name="repo-name",
                updated=datetime.datetime.now(),
                status=RepoOperationStatusResponse(mode=RepoOperationMode.ONLINE, initiated_by={}),
                bucket=LegacyBucketResponse(
                    id=uuid4(),
                    name="bucket-name",
                    platform="s3",
                    nickname="bucket-nickname",
                    updated=datetime.datetime.now(),
                    extra_config={},
                    auth_method="auth",
                    is_default=False,
                ),
            ),
            prefix=None,
        )
    assert "The bucket on the catalog object cannot be a LegacyBucketResponse for Icechunk V2 repos!" in str(excinfo.value)
