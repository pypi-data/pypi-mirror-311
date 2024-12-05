import sys
from pathlib import Path
import atexit

from time import sleep

from watchdog.observers import Observer
from watchdog.observers.api import BaseObserver
from watchdog.events import FileSystemEventHandler, FileSystemEvent

import logging

from repwatcher.db import Game
from repwatcher.gui import edit_game
from repwatcher.replay import process_replay

from .config import get_config
from .webclient import upload_replay_repmastered


class ReplayHandler(FileSystemEventHandler):
    def on_created(self, event: FileSystemEvent):
        if not event.is_directory and event.src_path.endswith(".rep"):
            if not Path(event.src_path).exists():
                return
            parsed_replay, path = process_replay(
                event.src_path, bias_players=get_config().bw_aliases
            )
            if path is None:
                return
            game = Game.from_parsed_replay(parsed_replay, path)
            if game.url:
                return
            game.url = upload_replay_repmastered(Path(path))  # type: ignore
            game.save()

            if get_config().advanced:
                edit_game(game)


def watch() -> None:
    logging.info("Starting RepMastered Watcher")
    config = get_config()

    if not Path(config.replay_directory).exists():
        logging.error(
            f"Replay directory {config.replay_directory} does not exist. Please update the config file."
        )
        sys.exit(1)

    logging.info(f"Watching {config.replay_directory} for new replays")

    observer = Observer()
    observer.schedule(ReplayHandler(), path=config.replay_directory, recursive=True)
    observer.start()

    atexit.register(cleanup, observer)

    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        sys.exit(0)


def cleanup(observer: BaseObserver) -> None:
    logging.info("Shutting down")
    observer.stop()
    observer.join()
