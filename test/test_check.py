from pathlib import Path

from database import Session
from monitoring import Monitor

if __name__ == '__main__':
    path = Path("/home/ctree/Documents/Tencent Files")
    # print(path.is_dir())
    monitor = Monitor(path, Session, 0, None)
    monitor._Monitor__check()
