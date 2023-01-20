from pathlib import Path
from threading import Timer
from typing import Callable, Set, Union

from sqlalchemy.orm import Session
from watchfiles.main import FileChange, Change

from db_helper import DBHelper
from exception.ArgumentError import ArgumentError
from exception.IllegalStateError import IllegalStateError
from util import checksum


class Monitor(object):
    root: Path
    interval: int
    helper: DBHelper
    tl: Union[Timer, None] = None
    listener: Callable[[Set[FileChange]], None]

    def __init__(self,
                 path: Path,
                 helper: DBHelper,
                 interval: int,
                 listener: Callable[[Set[FileChange]], None]
                 ):

        if not path.is_dir():
            raise ArgumentError("The given path is not a directory.")

        self.root = path
        self.interval = interval
        self.helper = helper
        self.listener = listener
        ...

    def __check(self):
        changes: Set[FileChange] = set()
        with self.helper.session() as session:
            session: Session
            all_file = [str(it.absolute()) for it in self.root.rglob("*") if it.is_file()]
            # use get_slice() later if the db size is bigger than excepted
            for saved_file in self.helper.get_all(session=session):
                str_saved_file_path = str(saved_file.path)
                if str_saved_file_path not in all_file:
                    changes.add((Change.deleted, str_saved_file_path))
                    self.helper.delete(path=str_saved_file_path, session=session)
                    continue

                all_file.remove(str_saved_file_path)
                try:
                    md5 = checksum(str_saved_file_path)
                except FileNotFoundError:
                    continue

                if md5 != saved_file.hash:
                    changes.add((Change.modified, str_saved_file_path))
                    self.helper.set(path=str_saved_file_path, hash_=md5, session=session)

            if all_file:
                for added_file in all_file:
                    changes.add((Change.added, added_file))
                    self.helper.set(path=added_file, hash_=checksum(added_file), session=session)

            session.commit()
            self.listener(changes)

    def start(self):
        if isinstance(self.tl, Timer):
            self.tl.cancel()

        def __loop():
            self.__check()
            self.start()

        self.tl = Timer(function=__loop, interval=self.interval)
        self.tl.start()

    def stop(self):
        if not isinstance(self.tl, Timer):
            raise IllegalStateError("Trying to stop a monitor which had never been started.")

        self.tl.cancel()
        self.tl = None
