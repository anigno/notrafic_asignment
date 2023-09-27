from typing import Optional

import data_types
from invokers import RLRRequestInvoker
from persistence import PersistenceToFile
from request_processor import RLRRequestProcessor
from rlr import RLR

class Main:
    """application entry point, construct classes dependencies and run application"""

    def __init__(self):
        self.rlr: Optional[RLR] = None

    def construct(self):
        filename = 'crossing_events.txt'
        processor = RLRRequestProcessor()
        persistence = PersistenceToFile(filename, is_clean_file=True)
        invoker = RLRRequestInvoker(processor=processor, persistence=persistence)
        self.rlr = RLR(invoker=invoker)

    def run(self):
        self.rlr.start_invoker()

if __name__ == '__main__':
    main = Main()
    main.construct()
    main.run()

    # simulate 10 requests
    for i in range(10):
        req = data_types.RLRRequest(car_id=i,
                                    stop_line_coordinates=[data_types.Coord(5, 20), data_types.Coord(15, 20)],
                                    trajectory=[data_types.TimedCoord(6, 5, 10), data_types.TimedCoord(7, 15 + i, 15),
                                                data_types.TimedCoord(8, 30, 22)])
        main.rlr.calc_crossing_timestamp(req)
    input('press Enter to exit')
