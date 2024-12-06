from __future__ import annotations

import asyncio
import sys

from llmling.server import serve


if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def main() -> None:
    """Run the LLMling server."""
    config_path = (
        sys.argv[1] if len(sys.argv) > 1 else "src/llmling/config_resources/test.yml"
    )

    try:
        await serve(config_path)
    except KeyboardInterrupt:
        print("\nServer stopped by user", file=sys.stderr)
    except Exception as exc:  # noqa: BLE001
        print(f"Fatal server error: {exc}", file=sys.stderr)
        sys.exit(1)


def run() -> None:
    """Entry point for the server."""
    asyncio.run(main())


if __name__ == "__main__":
    run()
