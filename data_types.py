from typing import List

class Coord:
    """two dim coordinate"""

    def __init__(self, x: float, y: float):
        self.x: float = x
        self.y: float = y

    def __str__(self):
        return f'[{self.x} {self.y}]'

class TimedCoord(Coord):
    """coordinate with timestamp"""

    def __init__(self, x: float, y: float, timestamp: int):
        super().__init__(x, y)
        self.timestamp: int = timestamp

    def __str__(self):
        return f'[{self.timestamp} {super().__str__()}]'

class RLRRequest:
    """red line runner request data"""

    def __init__(self, car_id: int, stop_line_coordinates: List[Coord], trajectory: List[TimedCoord]):
        self.car_id = car_id
        self.stop_line_coordinates = stop_line_coordinates
        self.trajectory = trajectory

class RLRResult:
    """red line runner result data"""

    def __init__(self, car_id, crossing_timestamp):
        self.car_id = car_id
        self.crossing_timestamp = crossing_timestamp

    def __str__(self):
        return f'[RLRResult {self.car_id} {self.crossing_timestamp}]'
