from __future__ import annotations

import asyncio
from typing import Any

from fsspec.spec import AbstractFileSystem

from llmling.config.models import TextResource
from llmling.core.log import get_logger
from llmling.resources.registry import ResourceRegistry


logger = get_logger(__name__)


class ResourceFileSystem(AbstractFileSystem):
    """FileSystem interface to LLMling resources using fsspec.

    Features:
    - Basic file-like operations (read/write) through fsspec
    - Resource listing and metadata
    - Path validation and normalization
    - Caching support
    - Globbing and filtering
    - Optional write support for resources that allow it
    """

    # Core configs
    protocol = ("llmfs", "resource")  # Register both protocols
    _CACHING_EXPIRY = 60  # Cache expiry in seconds

    def __init__(
        self,
        registry: ResourceRegistry,
        write_enabled: bool = False,
        enable_cache: bool = True,
        cache_expiry: int | None = None,
        **storage_options: Any,
    ) -> None:
        """Initialize filesystem.

        Args:
            registry: LLMling resource registry
            write_enabled: Whether to allow write operations
            enable_cache: Whether to enable content caching
            cache_expiry: Cache expiry time in seconds
            **storage_options: Additional fsspec options
        """
        super().__init__(**storage_options)
        self.registry = registry
        self._write_enabled = write_enabled
        self._enable_cache = enable_cache
        self._cache_expiry = cache_expiry or self._CACHING_EXPIRY
        self._resource_cache: dict[str, dict[str, Any]] = {}

        # Cache invalidation timer
        self._last_cache_cleanup = time.time()

    def _invalidate_cache(self) -> None:
        """Clear expired cache entries."""
        now = time.time()
        if now - self._last_cache_cleanup > self._cache_expiry:
            self._resource_cache.clear()
            self._last_cache_cleanup = now

    def ls(
        self,
        path: str | None = None,
        detail: bool = True,
        **kwargs: Any,
    ) -> list[dict[str, Any]] | list[str]:
        """List available resources with metadata."""
        resources = []
        for name in self.registry.list_items():
            if path and not name.startswith(path):
                continue

            try:
                resource = self.registry[name]
                info = {
                    "name": name,
                    "size": None,  # Determined on load
                    "type": resource.resource_type,
                    "uri": self.registry.get_uri(name),
                    "mtime": None,  # Could track modification time
                    "created": None,  # Could track creation time
                    "metadata": getattr(resource, "metadata", {}),
                }
                resources.append(info)
            except Exception:
                logger.exception("Failed to get info for resource: %s", name)

        return resources if detail else [r["name"] for r in resources]

    async def _rm(self, path: str) -> None:
        """Remove a resource if write enabled."""
        if not self._write_enabled:
            msg = "Filesystem is read-only"
            raise PermissionError(msg)
        try:
            del self.registry[path]
        except KeyError as exc:
            msg = f"Resource not found: {path}"
            raise FileNotFoundError(msg) from exc

    def rm_file(self, path: str) -> None:
        """Remove a single file."""
        asyncio.run(self._rm(path))

    def rm(self, path: str, recursive: bool = False, maxdepth: int | None = None) -> None:
        """Remove resource(s)."""
        if recursive:
            # Remove all resources under path
            for name in self.registry.list_items():
                if name.startswith(path):
                    asyncio.run(self._rm(name))
        else:
            self.rm_file(path)

    async def _cat_file(self, path: str) -> bytes:
        """Get raw bytes of resource content."""
        try:
            loaded = await self.registry.load(path)
            return loaded.content.encode()
        except Exception as exc:
            msg = f"Failed to read resource {path}"
            raise FileNotFoundError(msg) from exc

    def cat_file(self, path: str) -> bytes:
        """Get bytes of resource."""
        return asyncio.run(self._cat_file(path))

    def cat(self, path: str) -> bytes:
        """Get resource content."""
        return self.cat_file(path)

    def pipe_file(self, path: str, value: bytes | str) -> None:
        """Write data to resource if enabled."""
        if not self._write_enabled:
            msg = "Filesystem is read-only"
            raise PermissionError(msg)

        # Convert to TextResource
        content = value.decode() if isinstance(value, bytes) else value
        self.registry.register(
            path,
            TextResource(content=content),
            replace=True,
        )

    def pipe(self, path: str, value: bytes | str) -> None:
        """Write data to resource."""
        self.pipe_file(path, value)

    def find(self, path: str, maxdepth: int | None = None, **kwargs: Any) -> list[str]:
        """Find resources matching pattern."""
        import fnmatch

        pattern = path.rstrip("/") + "/*"
        matches = []

        for name in self.registry.list_items():
            if fnmatch.fnmatch(name, pattern):
                matches.append(name)

        return matches

    def isdir(self, path: str) -> bool:
        """Check if path is a directory."""
        # Check if any resources start with this path
        return any(name.startswith(path) for name in self.registry.list_items())

    def isfile(self, path: str) -> bool:
        """Check if path is a file."""
        try:
            return path in self.registry
        except KeyError:
            return False

    def modified(self, path: str) -> float:
        """Get modified time of resource."""
        if path in self._resource_cache:
            return self._resource_cache[path].get("mtime", 0.0)
        return 0.0

    def ukey(self, path: str) -> str:
        """Get unique key for resource."""
        info = self.info(path)
        return f"{path}_{info.get('mtime', '')}_{info.get('size', '')}"

    def size(self, path: str) -> int:
        """Get resource size."""
        info = self.info(path)
        return info.get("size", 0)

    def created(self, path: str) -> float:
        """Get creation time."""
        info = self.info(path)
        return info.get("created", 0.0)


if __name__ == "__main__":
    import logging

    from llmling.config.loading import load_config
    from llmling.config_resources import TEST_CONFIG
    from llmling.processors.registry import ProcessorRegistry
    from llmling.resources import ResourceLoaderRegistry

    # Enable debug logging
    logging.basicConfig(level=logging.DEBUG)

    async def test_resource_fs():
        # Load test configuration
        config = load_config(TEST_CONFIG)

        # Create registries
        loader_registry = ResourceLoaderRegistry()
        processor_registry = ProcessorRegistry()
        resource_registry = ResourceRegistry(
            loader_registry=loader_registry,
            processor_registry=processor_registry,
        )

        # Register resources from config
        for name, resource in config.resources.items():
            resource_registry.register(name, resource)

        # Create filesystem
        fs = ResourceFileSystem(resource_registry)

        # List resources
        print("\nAvailable resources:")
        for resource in fs.ls(detail=True):
            print(f"- {resource['name']} ({resource['type']})")

        # Try to read each resource
        for resource in fs.ls(detail=True):
            name = resource["name"]
            print(f"\nReading {name}:")
            try:
                async with await fs.open(name, "r") as f:
                    content = f.read()
                    preview = content[:100] + "..." if len(content) > 100 else content
                    print(f"Content preview: {preview}")
            except Exception as e:
                print(f"Error: {e}")

    # Run test
    asyncio.run(test_resource_fs())
