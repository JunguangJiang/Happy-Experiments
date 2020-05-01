import time
import fcntl
import jsonpickle


class ExclusivePersistentObject:
    def __init__(self, disk_filename):
        self.disk_filename = disk_filename
        self.file = None

    def create(self, object):
        with open(self.disk_filename, "w")as f:
            f.write(jsonpickle.encode(object))

    def load(self):
        self.file = open(self.disk_filename, "r+")
        fcntl.flock(self.file, fcntl.LOCK_EX)
        data = self.file.read()
        object = jsonpickle.decode(data)
        return object

    def dump(self, object):
        assert self.file is not None
        self.file.seek(0)
        self.file.truncate()
        self.file.write(jsonpickle.encode(object))
        self.file.close()
        self.file = None


def get_current_time():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())