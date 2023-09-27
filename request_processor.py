from abc import abstractmethod, ABC
from typing import Optional

from data_types import RLRRequest, RLRResult, Coord
from logger import Logger

class RequestProcessorBase(ABC):
    @abstractmethod
    def process_request(self, request: RLRRequest) -> RLRResult:
        pass

class RLRRequestProcessor(RequestProcessorBase):
    def process_request(self, request: RLRRequest) -> Optional[RLRResult]:
        """iterate trajectory from request to find intersection part, calc timestamp within the part"""
        Logger.log(f'processing request for car: {request.car_id}')
        second_coord = request.trajectory.pop(0)
        count = len(request.trajectory)
        for _ in range(count):
            first_coord = second_coord
            second_coord = request.trajectory.pop(0)
            intersection_coord = RLRRequestProcessor.find_intersection(request.stop_line_coordinates[0],
                                                                       request.stop_line_coordinates[1], first_coord,
                                                                       second_coord)

            if intersection_coord is not None:
                crossing_timestamp = RLRRequestProcessor.calc_timestamp(intersection_coord.y, first_coord.y,
                                                                        second_coord.y, first_coord.timestamp,
                                                                        second_coord.timestamp)
                return RLRResult(request.car_id, crossing_timestamp)
        return None

    @staticmethod
    def calc_timestamp(intersect_y, y0, y1, t0, t1) -> int:
        p = (intersect_y - y0) / (y1 - y0)
        t = (t1 - t0) * p + t0
        return t

    @staticmethod
    def find_intersection(line_coord_first: Coord, line_coord_second: Coord, prev_coord: Coord,
                          next_coord: Coord) -> Optional[Coord]:
        xr1 = line_coord_first.x
        yr1 = line_coord_first.y
        xr2 = line_coord_second.x
        yr2 = line_coord_second.y
        x3 = prev_coord.x
        y3 = prev_coord.y
        x4 = next_coord.x
        y4 = next_coord.y
        if y4 < y3:
            # trajectory part not legal
            return None
        mr12 = (yr2 - yr1) / (xr2 - xr1) if xr2 != xr1 else None
        br12 = yr1 - xr1 * mr12

        if x3 == x4:
            # car trajectory is parallel to Y axis
            x_intersection = x4
        else:
            m34 = (y4 - y3) / (x4 - x3) if x4 != x3 else None
            if mr12 is None or m34 is None:
                Logger.log('impossible to calculate intersection when delta x equal zero')
                return None
            if mr12 == m34:
                Logger.log('parallel lines, no intersection point')
                return None
            b34 = y3 - x3 * m34
            x_intersection = (br12 - b34) / (m34 - mr12)
        y_intersection = x_intersection * mr12 + br12
        # verify crossing
        if y_intersection > y4:
            return None
        return Coord(x_intersection, y_intersection)

if __name__ == '__main__':
    prc = RLRRequestProcessor()
    inter1 = prc.find_intersection(Coord(10, 20), Coord(20, 18), Coord(10, 10), Coord(20, 20))
    print(inter1)
    print(prc.calc_timestamp(inter1.x, 10, 20, 100, 200))
    print(prc.calc_timestamp(inter1.x, 10, 20, 0, 100))

    # far from target line
    inter1 = prc.find_intersection(Coord(10, 20), Coord(20, 18), Coord(30, 20), Coord(40, 10))
    print(inter1)

    # too short for crossing
    inter1 = prc.find_intersection(Coord(10, 20), Coord(20, 18), Coord(15, 10), Coord(16, 16))
    print(inter1)

    # cross
    inter1 = prc.find_intersection(Coord(10, 20), Coord(20, 18), Coord(15, 10), Coord(16, 26))
    print(inter1)
