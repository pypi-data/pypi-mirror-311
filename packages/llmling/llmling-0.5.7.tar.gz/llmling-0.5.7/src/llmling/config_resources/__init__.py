"""Package resources for LLMling configuration."""

from __future__ import annotations

import importlib.resources
from typing import Final, overload, TYPE_CHECKING

if TYPE_CHECKING:
    from importlib.abc import Traversable


@overload
def get_resource(filename: str) -> str: ...


@overload
def get_resource(filename: str, *, return_traversable: bool = True) -> Traversable: ...


def get_resource(
    filename: str,
    *,
    return_traversable: bool = False,
) -> str | Traversable:
    """Get a package resource.

    Args:
        filename: Resource filename
        return_traversable: Return Traversable object instead of text content

    Returns:
        Either the text content or a Traversable object

    Raises:
        FileNotFoundError: If resource doesn't exist
    """
    resource = importlib.resources.files("llmling.config_resources") / filename
    if not resource.is_file():
        msg = f"Resource not found or not a file: {filename}"
        raise FileNotFoundError(msg)

    return resource if return_traversable else resource.read_text()


# Get Traversable objects for the config files
_test_cfg: Final[Traversable] = get_resource("test.yml", return_traversable=True)
_web_research_cfg: Final[Traversable] = get_resource(
    "web_research.yml",
    return_traversable=True,
)
_watch_examples_cfg: Final[Traversable] = get_resource(
    "watch_examples.yml",
    return_traversable=True,
)

# Export public paths as strings
TEST_CONFIG: Final[str] = str(_test_cfg)
WEB_RESEARCH_CONFIG: Final[str] = str(_web_research_cfg)
WATCH_EXAMPLES_CONFIG: Final[str] = str(_watch_examples_cfg)

__all__ = [
    "TEST_CONFIG",
    "WATCH_EXAMPLES_CONFIG",
    "WEB_RESEARCH_CONFIG",
    "get_resource",
]
