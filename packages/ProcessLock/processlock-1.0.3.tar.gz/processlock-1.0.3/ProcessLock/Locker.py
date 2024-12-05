import os
import sys
import uuid
import queue
import threading
import portalocker

def get_home_dir():
    '''
    获得家目录
    :return:
    '''
    if sys.platform == 'win32':
        homedir = os.environ['USERPROFILE']
    elif sys.platform == 'linux' or sys.platform == 'darwin':
        homedir = os.environ['HOME']
    else:
        raise NotImplemented(f'Error! Not this system. {sys.platform}')
    return homedir

class ProcessLock():
    """ 进程锁 """
    def __init__(self, id=None, wait=True):
        """
        初始化进程锁
            id : (str)
                锁id,相同id的锁为同一把锁
            wait : (bool)
                如果其他对象已经获取了锁,是否等待锁释放
                    True : 等待锁释放
                    False : 如果锁被占用抛出AlreadyLocked异常
        """
        tmp_path = os.path.join(get_home_dir(), ".ProcessLockTmp")
        if not os.path.exists(tmp_path):
            os.mkdir(tmp_path)

        if id:
            self.id = os.path.join(tmp_path, id)
        else:
            self.id = os.path.join(tmp_path, str(uuid.uuid1()))

        self._check_interval = 0.25

        if wait:
            # 不是真等待,是把超时设置为5年左右
            self._timeout = 150000000
            self._fail_when_locked = False
        else:
            # 如果锁锁定直接抛出异常
            self._timeout = 0
            self._fail_when_locked = True

    def acquire(self):
        run_acquire_info_queue = queue.Queue()
        def sub():
            try:
                with portalocker.Lock(self.id, 'w', check_interval=self._check_interval, timeout=self._timeout, fail_when_locked=self._fail_when_locked) as fh:
                    self._lock_queue = queue.Queue()
                    run_acquire_info_queue.put("OK")
                    try:
                        self._lock_queue.get()
                        del self._lock_queue
                    finally:
                        # flush and sync to filesystem
                        fh.flush()
                        os.fsync(fh.fileno())
            except Exception as err:
                # only portalocker.AlreadyLocked
                run_acquire_info_queue.put(err)

        acquire_th = threading.Thread(target=sub)
        acquire_th.daemon = True
        acquire_th.start()

        run_acquire_info = run_acquire_info_queue.get()
        if run_acquire_info != "OK":
            raise portalocker.AlreadyLocked(run_acquire_info)

    def release(self):
        try:
            self._lock_queue.put(True)
        except AttributeError:
            raise RuntimeError("release unlocked lock")

    def locked(self) -> bool:
        try:
            with portalocker.Lock(self.id, 'w', timeout=0, fail_when_locked=True) as fh:
                # flush and sync to filesystem
                fh.flush()
                os.fsync(fh.fileno())
        except portalocker.LockException:
            return True
        else:
            return False
