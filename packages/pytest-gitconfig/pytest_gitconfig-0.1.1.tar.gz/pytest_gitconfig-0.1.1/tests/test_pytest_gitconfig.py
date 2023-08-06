from __future__ import annotations

import os
import subprocess

from pathlib import Path


def assert_config(key, expected):
    __tracebackhide__ = True
    assert (
        subprocess.check_output(f"git config {key}", shell=True).strip().decode("utf-8") == expected
    )


def test_gitconfig(gitconfig):
    assert gitconfig.path != Path("~/.gitconfig")
    assert str(gitconfig) == str(gitconfig.path)
    assert os.environ["GIT_CONFIG_GLOBAL"] == str(gitconfig.path)


def test_gitconfig_set_kwargs(gitconfig):
    expected = "new name"
    gitconfig.set(**{"user.name": expected})

    assert_config("user.name", expected)


def test_gitconfig_set_dict(gitconfig):
    expected = "new name"
    gitconfig.set({"user": {"name": expected}})

    assert_config("user.name", expected)
