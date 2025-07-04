import uvicorn

from src.core.app import create_app


def main():
    app = create_app()
    return app


if __name__ == '__main__':
    uvicorn.run(main(), host="0.0.0.0", port=8000)
