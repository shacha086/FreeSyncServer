from pathlib import Path
from typing import List, Tuple, Union

from sqlalchemy.orm import sessionmaker, Session

from model.Files import Files


class DBHelper(object):
    _session: sessionmaker

    def __init__(self, session: sessionmaker):
        self._session = session

    def session(self) -> Session:
        return self._session()

    def is_exist(self, path: Union[str, Path], session: Session = None) -> bool:
        def _(sess: Session):
            return sess.query(Files).get(str(path)) is not None

        if session is None:
            with self.session() as session:
                return _(session)

        else:
            return _(session)

    def get(self, path: Union[str, Path], session: Session = None):
        path = str(path)

        def _(sess: Session):
            return file.hash if (file := sess.query(Files).get(path)) else None

        if session is None:
            with self.session() as session:
                return _(session)
        else:
            return _(session)

    def set(self, 
            path: Union[str, Path], 
            hash_: str, 
            session: Session = None, 
            commit: bool = False, 
            force_exist: bool = None):
        path = str(path)

        def _(sess: Session):
            exist = force_exist
            if exist is None:
                exist = self.is_exist(path)

            if exist is True:
                sess.query(Files).filter(Files.path == path).update({"hash": hash_})
            else:
                sess.add(Files(path=path, hash=hash_))

        if session is None:
            with self.session() as session:
                try:
                    return _(session)
                finally:
                    session.commit()

        else:
            try:
                return _(session)
            finally:
                if commit:
                    session.commit()

    def delete(self, path: Union[str, Path], session: Session = None, commit: bool = False):
        path = str(path)

        def _(sess: Session):
            return sess.query(Files).filter(Files.path == path).delete()

        if session is None:
            with self.session() as session:
                try:
                    return _(session)
                finally:
                    session.commit()
        else:
            try:
                return _(session)
            finally:
                if commit:
                    session.commit()

    def get_slice(self, slice_: Tuple[int, int], session: Session = None) -> List[Files]:
        def _(sess: Session):
            return sess.query(Files).slice(start=slice_[0], stop=slice_[1]).all()

        if session is None:
            with self.session() as session:
                return _(session)
        else:
            return _(session)

    def get_all(self, limit: Union[int] = None, session: Session = None) -> List[Files]:
        def _(sess: Session):
            return sess.query(Files).limit(limit).all()

        if session is None:
            with self.session() as session:
                return _(session)
        else:
            return _(session)

    @classmethod
    def commit(cls, session: Session):
        session.commit()
        