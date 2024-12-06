from __future__ import annotations

import posixpath
from typing import TYPE_CHECKING, Any

from fsspec.asyn import AsyncFileSystem

from llmling.core.log import get_logger


if TYPE_CHECKING:
    from llmling.testing.testclient import MCPInProcSession


logger = get_logger(__name__)


class ClientAdapter:
    """Adapter to make MCPInProcSession work with MCPFileSystem."""

    def __init__(self, client: MCPInProcSession) -> None:
        """Initialize adapter with client.

        Args:
            client: Initialized MCPInProcSession
        """
        self.client = client

    async def list_resources(self) -> dict[str, Any]:
        """Get resources list."""
        try:
            return await self.client.send_request("resources/list")
        except Exception:
            logger.exception("Failed to list resources")
            return {"resources": []}

    async def list_prompts(self) -> dict[str, Any]:
        """Get prompts list."""
        try:
            return await self.client.send_request("prompts/list")
        except Exception:
            logger.exception("Failed to list prompts")
            return {"prompts": []}

    async def list_tools(self) -> dict[str, Any]:
        """Get tools list."""
        try:
            return await self.client.send_request("tools/list")
        except Exception:
            logger.exception("Failed to list tools")
            return {"tools": []}

    async def read_resource(self, uri: str) -> dict[str, Any]:
        """Read resource content."""
        try:
            # Convert file:// URIs to resource:// for our test server
            if uri.startswith("file://"):
                uri = f"resource://{uri.split('/', 3)[-1]}"
            return await self.client.send_request(
                "resources/read",
                {"uri": uri},
            )
        except Exception as e:
            logger.exception("Failed to read resource")
            return {"text": f"Error: {e}"}


class MCPFileSystem(AsyncFileSystem):
    """Async filesystem interface to MCP server resources.

    Provides a virtual filesystem structure for MCP resources:
    /resources/ - MCP resources from resources/list
    /prompts/   - Prompt templates from prompts/list
    /tools/     - Available tools from tools/list
    """

    protocol = "mcp"
    root_marker = "/"

    def __init__(
        self,
        client: ClientAdapter,
        *,
        async_impl: bool = True,
        **storage_options: Any,
    ) -> None:
        """Initialize filesystem with MCP client adapter."""
        super().__init__(async_impl=async_impl, **storage_options)
        self.client = client
        # Cache directories
        self._resource_cache: dict[str, Any] = {}
        self._prompt_cache: dict[str, Any] = {}
        self._tool_cache: dict[str, Any] = {}

    async def _ls(
        self,
        path: str,
        detail: bool = True,
        **kwargs: Any,
    ) -> list[dict[str, Any]] | list[str]:
        """List directory contents."""
        path = self._strip_protocol(path or "")
        path = path.strip("/")

        entries: list[dict[str, Any]] = []

        # Root directory - show virtual folders
        if not path:
            entries.extend([
                self._dir_entry("resources"),
                self._dir_entry("prompts"),
                self._dir_entry("tools"),
            ])

        # List contents of virtual directories
        elif path == "resources":
            response = await self.client.list_resources()
            for resource in response.get("resources", []):
                self._resource_cache[resource["name"]] = resource
                entries.append(
                    self._file_entry(
                        name=resource["name"],
                        content_type=resource.get("mimeType"),
                    )
                )

        elif path == "prompts":
            response = await self.client.list_prompts()
            for prompt in response.get("prompts", []):
                self._prompt_cache[prompt["name"]] = prompt
                entries.append(
                    self._file_entry(
                        name=prompt["name"],
                        content_type="text/plain",
                    )
                )

        elif path == "tools":
            response = await self.client.list_tools()
            for tool in response.get("tools", []):
                self._tool_cache[tool["name"]] = tool
                entries.append(
                    self._file_entry(
                        name=tool["name"],
                        content_type="application/json",
                    )
                )
        else:
            msg = f"Directory not found: {path}"
            raise FileNotFoundError(msg)

        if not detail:
            return [entry["name"] for entry in entries]
        return entries

    def _dir_entry(self, name: str) -> dict[str, Any]:
        """Create directory entry info."""
        return {
            "name": name,
            "size": 0,
            "type": "directory",
        }

    def _file_entry(
        self,
        name: str,
        size: int | None = None,
        content_type: str | None = None,
    ) -> dict[str, Any]:
        """Create file entry info."""
        return {
            "name": name,
            "size": size or 0,
            "type": "file",
            "contentType": content_type,
        }

    async def _info(self, path: str, **kwargs: Any) -> dict[str, Any]:
        """Get info about path."""
        path = self._strip_protocol(path).strip("/")

        # Virtual directories
        if not path or path in ("resources", "prompts", "tools"):
            return self._dir_entry(path or "/")

        # Split into directory and name
        dirname, basename = posixpath.split(path)

        # Look up in appropriate cache based on directory
        if dirname == "resources":
            if resource := self._resource_cache.get(basename):
                return self._file_entry(
                    name=resource["name"],
                    content_type=resource.get("mimeType"),
                )
        elif dirname == "prompts":
            if prompt := self._prompt_cache.get(basename):
                return self._file_entry(
                    name=prompt["name"],
                    content_type="text/plain",
                )
        elif dirname == "tools" and (tool := self._tool_cache.get(basename)):
            return self._file_entry(
                name=tool["name"],
                content_type="application/json",
            )

        msg = f"Path not found: {path}"
        raise FileNotFoundError(msg)

    async def _cat_file(self, path: str) -> bytes:
        """Get file contents as bytes."""
        path = self._strip_protocol(path).strip("/")
        dirname, basename = posixpath.split(path)

        try:
            if dirname == "resources":
                # Get resource content
                if resource := self._resource_cache.get(basename):
                    response = await self.client.read_resource(resource["uri"])
                    return response["text"].encode()

            elif dirname == "prompts":
                # Get prompt template
                if prompt := self._prompt_cache.get(basename):
                    import json

                    return json.dumps(prompt, indent=2).encode()

            # Get tool info
            elif dirname == "tools":
                if tool := self._tool_cache.get(basename):
                    import json

                    return json.dumps(tool, indent=2).encode()

            msg = f"File not found: {path}"
            raise FileNotFoundError(msg)

        except Exception as exc:
            msg = f"Failed to read {path}"
            raise FileNotFoundError(msg) from exc

    async def _get_file(self, rpath: str, lpath: str, **kwargs: Any) -> None:
        """Download remote file to local."""
        data = await self._cat_file(rpath)
        async with await self._open(lpath, "wb") as f:
            await f.write(data)

    async def _open(
        self,
        path: str,
        mode: str = "rb",
        block_size: int | None = None,
        **kwargs: Any,
    ) -> AsyncFileStream:
        """Open a file."""
        if mode != "rb":
            msg = "Write operations not supported"
            raise NotImplementedError(msg)

        data = await self._cat_file(path)
        return AsyncFileStream(data)


class AsyncFileStream:
    """Simple async file-like object."""

    def __init__(self, data: bytes) -> None:
        self.data = data
        self.pos = 0

    async def read(self, length: int = -1) -> bytes:
        """Read specified number of bytes."""
        if length < 0:
            length = len(self.data) - self.pos
        end = min(self.pos + length, len(self.data))
        chunk = self.data[self.pos : end]
        self.pos = end
        return chunk

    async def write(self, data: bytes) -> int:
        """Write bytes to stream."""
        msg = "Stream is read-only"
        raise NotImplementedError(msg)

    async def seek(self, pos: int, whence: int = 0) -> int:
        """Seek to position."""
        if whence == 0:
            self.pos = pos
        elif whence == 1:
            self.pos += pos
        elif whence == 2:
            self.pos = len(self.data) + pos
        return self.pos

    async def tell(self) -> int:
        """Get current position."""
        return self.pos

    async def close(self) -> None:
        """Close the stream."""
        self.pos = 0

    async def __aenter__(self) -> AsyncFileStream:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()


if __name__ == "__main__":
    import asyncio
    import logging
    import sys

    # from typing import Any
    from llmling.testing.testclient import MCPInProcSession

    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    async def run_demo() -> None:
        # Create client that connects to server subprocess
        client = MCPInProcSession(
            [sys.executable, "-m", "llmling.server"],
            config_path="src/llmling/config_resources/test.yml",
        )

        try:
            # Start client (spawns server subprocess)
            await client.start()
            logger.info("Client started")

            # Perform handshake
            await client.do_handshake()
            logger.info("Handshake completed")

            # Create adapter and filesystem
            adapter = ClientAdapter(client)
            fs = MCPFileSystem(adapter)

            # Demo operations using async methods
            logger.info("\nListing root directory:")
            entries = await fs._ls("/")
            for entry in entries:
                logger.info("  %s", entry["name"])

            logger.info("\nListing resources:")
            resources = await fs._ls("/resources")
            for resource in resources:
                logger.info("  %s", resource["name"])
                # Try to read content
                try:
                    content = await fs._cat_file(f"/resources/{resource['name']}")
                    logger.info("    Content: %s", content.decode())
                except Exception as e:
                    logger.error("    Failed to read content: %s", e)

            logger.info("\nListing prompts:")
            prompts = await fs._ls("/prompts")
            for prompt in prompts:
                logger.info("  %s", prompt["name"])

            logger.info("\nListing tools:")
            tools = await fs._ls("/tools")
            for tool in tools:
                logger.info("  %s", tool["name"])

        except Exception as e:
            logger.error("Demo failed: %s", e)
            raise
        finally:
            try:
                await client.close()
            except Exception as e:
                logger.warning("Cleanup error: %s", e)

    # Run demo
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    try:
        asyncio.run(run_demo())
    except KeyboardInterrupt:
        logger.info("Demo interrupted by user")
    except Exception as e:
        logger.error("Fatal error: %s", e)
        sys.exit(1)
