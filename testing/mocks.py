from data_types import RLRResult, RLRRequest
from persistence import PersistenceBase
from request_processor import RequestProcessorBase

class PersistenceMock(PersistenceBase):
    def __init__(self):
        self.data = []

    def write(self, result: RLRResult):
        self.data.append(result)

class ProcessorMock(RequestProcessorBase):
    def process_request(self, request: RLRRequest) -> RLRResult:
        return RLRResult(request.car_id, 100)
