import logging
import uvicorn

from src.core.app import create_app


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    app = create_app()
    return app


if __name__ == '__main__':
    uvicorn.run(main(), host="0.0.0.0", port=8080)
