from unittest import TestCase

from data_types import Coord, TimedCoord
from request_processor import RLRRequestProcessor

class ProcessingTests(TestCase):
    def setUp(self) -> None:
        self.proc = RLRRequestProcessor()

    def test_request_processor_traj_parallel(self):
        test_coords = [Coord(5, 20), Coord(15, 20), TimedCoord(10, 10, 0), TimedCoord(10, 30, 100)]
        coord = self.proc.find_intersection(*test_coords)
        self.assertEqual(coord.x, 10)
        self.assertEqual(coord.y, 20)

    def test_request_processor_traj_diagonal_1(self):
        test_coords = [Coord(5, 20), Coord(15, 20), TimedCoord(5, 10, 0), TimedCoord(15, 30, 100)]
        coord = self.proc.find_intersection(*test_coords)
        self.assertEqual(coord.x, 10)
        self.assertEqual(coord.y, 20)

    def test_request_processor_traj_diagonal_2(self):
        test_coords = [Coord(5, 20), Coord(15, 20), TimedCoord(15, 10, 0), TimedCoord(5, 30, 100)]
        coord = self.proc.find_intersection(*test_coords)
        self.assertEqual(coord.x, 10)
        self.assertEqual(coord.y, 20)

    def test_request_processor_stop_line_diagonal_1(self):
        test_coords = [Coord(5, 20), Coord(15, 22), TimedCoord(10, 10, 0), TimedCoord(10, 30, 100)]
        coord = self.proc.find_intersection(*test_coords)
        self.assertEqual(coord.x, 10)
        self.assertEqual(coord.y, 21)

    def test_request_processor_no_cross(self):
        test_coords = [Coord(5, 22), Coord(15, 20), TimedCoord(10, 10, 0), TimedCoord(10, 15, 100)]
        coord = self.proc.find_intersection(*test_coords)
        self.assertIsNone(coord)

    def test_request_processor_stop_line_diagonal_2(self):
        test_coords = [Coord(5, 22), Coord(15, 20), TimedCoord(10, 10, 0), TimedCoord(10, 30, 100)]
        coord = self.proc.find_intersection(*test_coords)
        self.assertEqual(coord.x, 10)
        self.assertEqual(coord.y, 21)

    def test_calc_timestamp_1(self):
        timestamp = self.proc.calc_timestamp(5, 0, 10, 0, 100)
        self.assertEqual(timestamp, 50)

    def test_calc_timestamp_2(self):
        timestamp = self.proc.calc_timestamp(47, 20, 60, 30, 40)
        print(timestamp)
        self.assertEqual(timestamp, 36.75)
