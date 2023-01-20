from pathlib import Path
from typing import Callable, Set

from watchfiles.main import FileChange

from db_helper import DBHelper


class Watcher(object):
    root: Path
    helper: DBHelper
    listener: Callable[[Set[FileChange]], None]

