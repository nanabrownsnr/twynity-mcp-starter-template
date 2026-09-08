"""Provide safe environment defaults and shared fixtures for starter tests.

Add reusable fixtures here; never replace these placeholders with live secrets.
"""

import os

import pytest

# The production settings remain required by the application. Tests use local
# placeholders so contributors do not need private infrastructure or a .env.
os.environ.setdefault("USAGE_REPORT_ENDPOINT", "http://usage.invalid/report")
os.environ.setdefault("ACCOUNT_SERVICE_URL", "http://account.invalid")
os.environ.setdefault("ACCOUNT_SERVICE_JWKS_ENDPOINT", "/.well-known/jwks.json")
os.environ.setdefault("ACCOUNT_SERVICE_JWKS_CACHE_TTL", "300")
os.environ.setdefault("LICENSE_KEY", "test-license")
os.environ.setdefault("LICENSE_SERVER_BASE_URL", "http://license.invalid")
os.environ.setdefault("LICENSE_SERVER_JWKS_ENDPOINT", "/.well-known/jwks.json")
os.environ.setdefault("LICENSE_SERVER_ACTIVATION_ENDPOINT", "/activate")


@pytest.fixture
def greeting_name():
    """Reusable example input for the starter tool."""
    return "Ada"
