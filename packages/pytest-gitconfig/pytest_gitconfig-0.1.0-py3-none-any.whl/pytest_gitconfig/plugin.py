from __future__ import annotations

import os
import shlex
import subprocess

from configparser import ConfigParser
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator

import pytest

DEFAULT_GIT_USER_NAME = "John Doe"
DEFAULT_GIT_USER_EMAIL = "john.doe@local.dev"
DEFAULT_GIT_BRANCH = "main"


def run(cmd: str, *args, **kwargs) -> subprocess.CompletedProcess[str]:
    real_args = [cmd, *args] if args else shlex.split(cmd)
    return subprocess.run(real_args, **kwargs)


@pytest.fixture(scope="session")
def sessionpatch() -> Iterator[pytest.MonkeyPatch]:
    with pytest.MonkeyPatch.context() as mp:
        yield mp


@pytest.fixture(scope="session")
def git_user_name() -> str:
    return DEFAULT_GIT_USER_NAME


@pytest.fixture(scope="session")
def git_user_email() -> str:
    return DEFAULT_GIT_USER_EMAIL


@pytest.fixture(scope="session")
def git_init_default_branch() -> str:
    return DEFAULT_GIT_BRANCH


@dataclass
class GitConfig:
    path: Path

    def __str__(self):
        return str(self.path)

    def set(self, data: dict | None = None, **kwargs):
        cfg = self._read()
        if data:
            for section, options in data.items():
                for option, value in options.items():
                    if not cfg.has_section(section):
                        cfg.add_section(section)
                    cfg.set(section, option, value)
        else:
            for key, value in kwargs.items():
                section, option = self._parse_key(key)
                if not cfg.has_section(section):
                    cfg.add_section(section)
                cfg.set(section, option, value)
        self._write(cfg)

    def get(self, key) -> str:
        cfg = self._read()
        section, option = self._parse_key(key)
        return cfg[section][option]

    def _parse_key(self, key: str) -> list[str]:
        return key.rsplit(".", 1)

    def _read(self) -> ConfigParser:
        cfg = ConfigParser()
        cfg.read(self.path)
        return cfg

    def _write(self, cfg: ConfigParser):
        with self.path.open("w") as out:
            cfg.write(out)


@pytest.fixture(scope="session")
def gitconfig(
    tmp_path_factory: pytest.TempPathFactory,
    sessionpatch: pytest.MonkeyPatch,
    git_user_name: str,
    git_user_email: str,
    git_init_default_branch: str,
) -> GitConfig:
    path = tmp_path_factory.mktemp("git", False) / "config"
    gitconfig = GitConfig(path)

    for var in os.environ:
        if var.startswith("GIT_"):
            sessionpatch.delenv(var, False)
    sessionpatch.setenv("GIT_CONFIG_GLOBAL", str(gitconfig))

    settings: dict[str, Any] = {
        "user.name": git_user_name,
        "user.email": git_user_email,
        "init.defaultBranch": git_init_default_branch,
    }

    gitconfig.set(**settings)

    return gitconfig
