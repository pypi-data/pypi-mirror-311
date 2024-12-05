"""High level interface for git functionality."""
from ._version import version

__version__ = version

from ._git import (
    Git,
    RsbGitError,
    RsbGitInternalError,
    Semver,
    Ver,
    check,
    clean,
    deepen,
    describe,
    diff_changed_files,
    format_changelog,
    head_info,
    id,
    is_clean,
    is_shallow,
    latest_tag,
    remote_get_url,
    submodule_update_with_config,
    toplevel_dir,
)

__all__ = [
    "Git",
    "RsbGitError",
    "RsbGitInternalError",
    "Semver",
    "Ver",
    "check",
    "clean",
    "describe",
    "diff_changed_files",
    "format_changelog",
    "head_info",
    "id",
    "is_clean",
    "latest_tag",
    "remote_get_url",
    "submodule_update_with_config",
    "toplevel_dir",
    "is_shallow",
    "deepen",
]
