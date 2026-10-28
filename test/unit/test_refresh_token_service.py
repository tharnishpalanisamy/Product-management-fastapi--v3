
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock
import pytest
from app.exceptions import InvalidRefreshTokenException
from app.models import RefreshToken
from app.services.refresh_token_service import RefreshTokenService


@pytest.fixture
def db():
    session = MagicMock()
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    session.flush = AsyncMock()
    return session


@pytest.fixture
def repository():
    repo = MagicMock()
    repo.create = AsyncMock()
    repo.get_by_hash_for_update = AsyncMock()
    repo.revoke_all_active_for_user = AsyncMock()
    return repo


@pytest.fixture
def service(db, repository):
    return RefreshTokenService(db, repository)


def test_generate_token_returns_random_opaque_strings():
    token1 = RefreshTokenService.generate_token()
    token2 = RefreshTokenService.generate_token()

    assert isinstance(token1, str)
    assert token1
    assert token1 != token2
    assert "." not in token1


def test_hash_token_is_deterministic_and_not_raw_token():
    raw_token = "example-refresh-token"

    hash1 = RefreshTokenService.hash_token(raw_token)
    hash2 = RefreshTokenService.hash_token(raw_token)

    assert hash1 == hash2
    assert hash1 != raw_token
    assert len(hash1) == 64


def test_build_refresh_token_record(service):
    raw_token, record = service._build_refresh_token_record(
        user_id=123
    )

    assert isinstance(record, RefreshToken)
    assert record.user_id == 123
    assert record.token_hash == service.hash_token(raw_token)
    assert record.token_hash != raw_token
    assert record.expires_at.tzinfo is not None

    expected_expiry = (
        datetime.now(timezone.utc)
        + timedelta(days=service.REFRESH_TOKEN_EXPIRE_DAYS)
    )

    assert abs((record.expires_at - expected_expiry).total_seconds()) < 2

