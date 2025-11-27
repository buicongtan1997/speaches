from __future__ import annotations

import sys

import uvicorn

from speaches.dependencies import get_config
from speaches.main import create_app


def main() -> None:
    config = get_config()
    app = create_app()

    host = config.host or "0.0.0.0"
    port = config.port or 8000

    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level=config.log_level.lower(),
    )


if __name__ == "__main__":
    sys.exit(main())
