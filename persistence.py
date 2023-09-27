import os
from abc import ABC, abstractmethod

from data_types import RLRResult
from logger import Logger

class PersistenceBase(ABC):
    """results persistence base class"""

    @abstractmethod
    def write(self, result: RLRResult):
        pass

class PersistenceToFile(PersistenceBase):
    """implementation for writing results to a file"""

    def __init__(self, filename: str, is_clean_file=False):
        self._filename = filename
        if is_clean_file:
            try:
                if os.path.exists(filename):
                    os.remove(filename)
            except Exception as ex:
                Logger.log(str(ex))
                raise ex

    def write(self, result: RLRResult):
        with open(self._filename, 'a+') as file_handle:
            file_handle.write(f'{result.car_id} {result.crossing_timestamp}\n')
        Logger.log(f'{result}')

if __name__ == '__main__':
    ptf = PersistenceToFile('test.txt', True)
    ptf.write(RLRResult(1234, 10.54))
    ptf.write(RLRResult(3421, 17.54))
    ptf.write(RLRResult(1234, 10.54))
