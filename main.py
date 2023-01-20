from pathlib import Path
from typing import Set

from watchfiles.main import FileChange

import config
from db_helper import DBHelper

from monitoring import Monitor
from database import Session


def handler(changes: Set[FileChange]):
    for change in changes:
        print(f"{change[1]} was {change[0].name}.")


def main():
    helper = DBHelper(Session)
    monitor = Monitor(Path(config.root), helper, 5, handler)
    monitor.start()


if __name__ == '__main__':
    main()
