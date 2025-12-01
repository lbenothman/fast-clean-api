import pytest
import pytest_asyncio
from pytest_asyncio import is_async_test

from adapters.connection_engines.sql_alchemy.models import Base
from adapters.connection_engines.sql_alchemy.session import get_session_maker
from drivers.config.settings import TestSettings


@pytest_asyncio.fixture(scope="session")
async def settings():
    return TestSettings()


def pytest_collection_modifyitems(items):
    """
    Pytest hook
    Configure all async tests to use session-scoped event loop.

    This prevents "Task attached to a different loop" errors when using
    session-scoped async fixtures with pytest-asyncio.
    """
    pytest_asyncio_tests = (item for item in items if is_async_test(item))
    session_scope_marker = pytest.mark.asyncio(loop_scope="session")
    for async_test in pytest_asyncio_tests:
        # append=False REPLACES the existing marker instead of adding
        async_test.add_marker(session_scope_marker, append=False)


# PROBLEM: This fixture is created with scope="session"
# It runs in EVENT LOOP #1 when the test session starts
# Pytest tests with function scope will create another event loop
# To fix the issue we need to add loop_scope="session" for each test
@pytest_asyncio.fixture(scope="session")
async def db_session_maker_fixture(settings: TestSettings):
    return get_session_maker(settings)


@pytest_asyncio.fixture(scope="session")
async def setup_database_fixture(db_session_maker_fixture):
    engine = db_session_maker_fixture.kw[
        "bind"
    ]  # The engine is stored in the 'bind' keyword argument

    # For Supabase: Create tables without dropping (to avoid timeout issues)
    # Tables will be cleaned up via DELETE statements in individual tests
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)  # type: ignore
    except Exception as e:
        # If tables already exist, that's fine - continue
        print(f"Database setup info: {e}")

    yield

    # Cleanup: Drop all tables after test session
    # Note: For Supabase, you might want to skip this and clean manually
    # to avoid timeout issues on teardown
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)  # type: ignore
    except Exception as e:
        print(f"Database teardown info: {e}")


@pytest_asyncio.fixture(scope="session")
async def db_session_fixture(db_session_maker_fixture, setup_database_fixture):
    # No need to start the session, we don't need to commit for the tests
    async with db_session_maker_fixture() as session:
        yield session
