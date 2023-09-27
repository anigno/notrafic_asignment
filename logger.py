from datetime import datetime
from threading import RLock

class Logger:
    """implementation of simple locked console logging"""
    locker = RLock()

    @staticmethod
    def log(message: str):
        with Logger.locker:
            print(f'{datetime.now().strftime("%H:%M:%S.%f")[:-3]}->{message}')

if __name__ == '__main__':
    Logger.log('hello')
