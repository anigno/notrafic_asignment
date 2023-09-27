import time

from data_types import RLRRequest, Coord, TimedCoord
from invokers import RLRRequestInvoker
from logger import Logger
from rlr import RLR
from testing.mocks import PersistenceMock, ProcessorMock

class IntegrationTest:
    """test full system flow"""

    def __init__(self):
        self.persistence_mock = PersistenceMock()
        processor = ProcessorMock()
        invoker = RLRRequestInvoker(processor=processor, persistence=self.persistence_mock)
        self.rlr = RLR(invoker=invoker)
        self.rlr.start_invoker()

    def test1(self):
        req = RLRRequest(car_id=1000,
                         stop_line_coordinates=[Coord(5, 20), Coord(15, 20)],
                         trajectory=[TimedCoord(6, 5, 10), TimedCoord(7, 15, 15), TimedCoord(8, 30, 22)])
        self.rlr.calc_crossing_timestamp(req)
        self.rlr.calc_crossing_timestamp(req)
        self.rlr.calc_crossing_timestamp(req)
        time.sleep(1)
        Logger.log(self.persistence_mock.data)
        # 3 calls to rlr produces 3 results
        assert len(self.persistence_mock.data) == 3

if __name__ == '__main__':
    tests = IntegrationTest()
    tests.test1()
