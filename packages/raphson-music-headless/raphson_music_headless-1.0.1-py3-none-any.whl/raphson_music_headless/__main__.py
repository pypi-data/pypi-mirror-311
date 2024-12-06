import logging
from pathlib import Path

from .config import Config
from .server import App


def main():
    logging.basicConfig(level=logging.INFO)
    config = Config.load(Path('config.json'))
    app = App(config)
    app.start(config)


if __name__ == '__main__':
    main()
