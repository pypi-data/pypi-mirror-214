from __future__ import annotations

import pytest

USER_NAME = "Overridden user Name"
USER_EMAIL = "hello@nowhere.com"
DEFAULT_BRANCH = "master"


@pytest.fixture(scope="session")
def git_user_name() -> str:
    return USER_NAME


@pytest.fixture(scope="session")
def git_user_email() -> str:
    return USER_EMAIL


@pytest.fixture(scope="session")
def git_init_default_branch() -> str:
    return DEFAULT_BRANCH


def test_gitconfig_fixture_override(gitconfig):
    assert gitconfig.get("user.name") == USER_NAME
    assert gitconfig.get("user.email") == USER_EMAIL
    assert gitconfig.get("init.defaultBranch") == DEFAULT_BRANCH
