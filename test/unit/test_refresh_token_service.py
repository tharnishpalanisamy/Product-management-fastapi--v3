
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


@pytest.mark.asyncio
async def test_issue_refresh_token_persists_hash_and_returns_raw_token(
    service, db, repository, monkeypatch
):
    raw_token = "test-raw-refresh-token"

    monkeypatch.setattr(
        RefreshTokenService,
        "generate_token",
        staticmethod(lambda: raw_token),
    )

    result = await service.issue_refresh_token(user_id=123)

    assert result == raw_token

    repository.create.assert_awaited_once()
    db.commit.assert_awaited_once()
    db.rollback.assert_not_awaited()

    stored_record = repository.create.await_args.args[0]

    assert isinstance(stored_record, RefreshToken)
    assert stored_record.user_id == 123
    assert stored_record.token_hash == service.hash_token(raw_token)
    assert stored_record.token_hash != raw_token
    assert stored_record.expires_at.tzinfo is not None


@pytest.mark.asyncio
async def test_issue_refresh_token_rolls_back_on_database_error(
    service, db, repository, monkeypatch
):
    monkeypatch.setattr(
        RefreshTokenService,
        "generate_token",
        staticmethod(lambda: "test-token"),
    )

    repository.create.side_effect = RuntimeError("Database error")

    with pytest.raises(RuntimeError, match="Database error"):
        await service.issue_refresh_token(user_id=123)

    db.rollback.assert_awaited_once()
    db.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_rotate_refresh_token_replaces_old_token(
    service, db, repository, monkeypatch
):
    old_token = "old-raw-token"
    new_token = "new-raw-token"
    now = datetime.now(timezone.utc)

    old_record = SimpleNamespace(
        id=10,
        user_id=123,
        expires_at=now + timedelta(days=3),
        revoked_at=None,
        replaced_by_id=None,
    )

    new_record = SimpleNamespace(
        id=20,
        user_id=123,
        token_hash=service.hash_token(new_token),
        expires_at=now + timedelta(days=7),
        revoked_at=None,
    )

    repository.get_by_hash_for_update.return_value = old_record

    monkeypatch.setattr(
        service,
        "_build_refresh_token_record",
        lambda user_id: (new_token, new_record),
    )

    user_id, returned_token = await service.rotate_refresh_token(
        old_token
    )

    assert user_id == 123
    assert returned_token == new_token

    repository.get_by_hash_for_update.assert_awaited_once_with(
        service.hash_token(old_token)
    )

    assert old_record.revoked_at is not None
    assert old_record.replaced_by_id == new_record.id

    db.add.assert_called_once_with(new_record)
    assert db.flush.await_count == 2
    db.commit.assert_awaited_once()
    db.rollback.assert_not_awaited()


@pytest.mark.asyncio
async def test_rotate_refresh_token_rejects_unknown_token(
    service, db, repository
):
    repository.get_by_hash_for_update.return_value = None

    with pytest.raises(InvalidRefreshTokenException):
        await service.rotate_refresh_token("unknown-token")

    db.commit.assert_not_awaited()
    db.rollback.assert_not_awaited()
