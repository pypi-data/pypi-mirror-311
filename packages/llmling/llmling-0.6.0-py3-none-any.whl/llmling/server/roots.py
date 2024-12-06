"""Root management for MCP server."""

from __future__ import annotations

import enum
import os
from typing import TYPE_CHECKING

from mcp.types import Root as McpRoot
from pydantic import BaseModel, ConfigDict, FileUrl
from upath import UPath

from llmling.core import exceptions
from llmling.core.log import get_logger


if TYPE_CHECKING:
    import os

logger = get_logger(__name__)


class RootType(enum.StrEnum):
    """Type of root directory."""

    CONFIG = "config"  # Config file's directory
    WORKSPACE = "workspace"  # Current workspace
    VIRTUAL = "virtual"  # Virtual root for non-file resources


class RootOptions(BaseModel):
    """Root configuration options."""

    type: RootType = RootType.CONFIG
    path: str | os.PathLike[str] | None = None
    allow_parent_access: bool = False

    model_config = ConfigDict(frozen=True)


class ServerRoot:
    """Manages root directories for server resources."""

    def __init__(self, options: RootOptions | None = None) -> None:
        """Initialize root manager."""
        self.options = options or RootOptions()
        self._roots: dict[str, UPath] = {}
        self._virtual_roots: dict[str, str] = {}

    def initialize(self, config_path: str | os.PathLike[str] | None = None) -> None:
        """Initialize roots based on configuration."""
        match self.options.type:
            case RootType.CONFIG:
                if not config_path:
                    msg = "Config path required for CONFIG root type"
                    raise exceptions.ConfigError(msg)
                self._add_file_root("config", UPath(config_path).parent)

            case RootType.WORKSPACE:
                self._add_file_root("workspace", UPath.cwd())

            case RootType.VIRTUAL:
                # Only use virtual roots
                self._add_virtual_root("resources", "resource://")
                self._add_virtual_root("virtual", "virtual://")

        logger.info(
            "Initialized roots: file=%d, virtual=%d",
            len(self._roots),
            len(self._virtual_roots),
        )

    def _add_file_root(self, name: str, path: UPath) -> None:
        """Add a file system root."""
        if not path.exists():
            msg = f"Root path does not exist: {path}"
            raise exceptions.ConfigError(msg)

        # Convert to absolute path
        abs_path = path.resolve()

        # Validate parent access
        if not self.options.allow_parent_access:
            try:
                abs_path.relative_to(UPath.cwd())
            except ValueError as exc:
                msg = f"Path {path} is outside current directory"
                raise exceptions.ConfigError(msg) from exc

        self._roots[name] = abs_path
        logger.debug("Added file root %r: %s", name, abs_path)

    def _add_virtual_root(self, name: str, uri_prefix: str) -> None:
        """Add a virtual root."""
        self._virtual_roots[name] = uri_prefix
        logger.debug("Added virtual root %r: %s", name, uri_prefix)

    def resolve_path(self, path: str | os.PathLike[str]) -> UPath:
        """Resolve a path relative to appropriate root."""
        path_obj = UPath(path)

        # Check if it's already absolute or has a scheme
        if path_obj.is_absolute() or path_obj.protocol:
            return path_obj

        # Try to resolve relative to each root
        for root_path in self._roots.values():
            candidate = root_path / path_obj
            if candidate.exists():
                return candidate

        msg = f"Could not resolve path: {path}"
        raise exceptions.ResourceError(msg)

    def get_mcp_roots(self) -> list[McpRoot]:
        """Get roots in MCP format for protocol responses."""
        roots = [
            McpRoot(
                uri=FileUrl(f"file:///{str(path).lstrip('/')}"),
                name=name,
            )
            for name, path in self._roots.items()
        ]

        roots.extend(
            McpRoot(uri=FileUrl(uri_prefix), name=name)
            for name, uri_prefix in self._virtual_roots.items()
        )
        return roots
