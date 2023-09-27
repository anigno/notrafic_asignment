from abc import ABC, abstractmethod
from queue import Queue
from threading import Thread

from data_types import RLRRequest
from logger import Logger
from persistence import PersistenceBase
from request_processor import RequestProcessorBase

class RequestInvokerBase(ABC):
    """handles requests collecting and processing"""

    def __init__(self, processor: RequestProcessorBase, persistence: PersistenceBase):
        self.processor = processor
        self.persistence = persistence

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def add_request(self, request: RLRRequest):
        pass

class RLRRequestInvoker(RequestInvokerBase):
    """implement request enqueuing and threaded processing"""

    def __init__(self, processor: RequestProcessorBase, persistence: PersistenceBase):
        super().__init__(processor, persistence)
        self.rlr_requests_queue: Queue[RLRRequest] = Queue()
        self.invoker_thread = Thread(target=self._invoker_thread_start, daemon=True)

    def start(self):
        self.invoker_thread.start()

    def _invoker_thread_start(self):
        while True:
            request = self.rlr_requests_queue.get(block=True)
            Logger.log(f'handling request for car: {request.car_id}')
            result = self.processor.process_request(request)
            self.persistence.write(result)

    def add_request(self, request: RLRRequest):
        Logger.log(f'added request for car: {request.car_id}')
        self.rlr_requests_queue.put(request)
