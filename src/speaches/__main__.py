from __future__ import annotations

import logging
import socket
import sys

import uvicorn

from speaches.dependencies import get_config
from speaches.main import create_app

logger = logging.getLogger(__name__)


def main() -> None:
    config = get_config()
    app = create_app()

    if config.uds:
        logger.info(f"Server will listen on Unix socket: {config.uds}")
        uvicorn.run(
            app,
            uds=config.uds,
            log_level=config.log_level.lower(),
        )
    else:
        host = config.host or "0.0.0.0"
        port = config.port or 0

        if port == 0:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind((host, 0))
            actual_port = sock.getsockname()[1]
            sock.close()

            logger.info("Port 0 requested - OS will assign a random free port")
            logger.info(f"Server will listen on {host}:{actual_port}")
            print(f"SERVER_PORT={actual_port}", flush=True)

            port = actual_port

        uvicorn.run(
            app,
            host=host,
            port=port,
            log_level=config.log_level.lower(),
        )


if __name__ == "__main__":
    sys.exit(main())
