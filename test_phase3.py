#Automated tests for Phase 3 puzzle logic.

import unittest
import sys, os, heapq
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pathfinding import dijkstra_grid
from dp_grid     import count_paths, reconstruct_path


class TestPhase3(unittest.TestCase):

    def test_dijkstra_finds_path(self):
        #Simple 3x3 open grid should have a path from (0,0) to (2,2)
        grid = [[0,0,0],[0,0,0],[0,0,0]]
        vorder, path = dijkstra_grid(grid, (0,0), (2,2))
        self.assertTrue(len(path) > 0)
        self.assertEqual(path[0],  (0,0))
        self.assertEqual(path[-1], (2,2))

    def test_dijkstra_path_length(self):
        #Shortest path in open 3x3 grid is 5 steps (right right down down = 4 moves, 5 cells)
        grid = [[0,0,0],[0,0,0],[0,0,0]]
        _, path = dijkstra_grid(grid, (0,0), (2,2))
        self.assertEqual(len(path), 5)

    def test_dijkstra_blocked_path(self):
        #Wall blocking all routes should return empty 
        grid = [[0,1,0],[1,1,0],[0,0,0]]
        _, path = dijkstra_grid(grid, (0,0), (2,2))
        self.assertEqual(path, [])

    def test_dijkstra_start_equals_end(self):
        #Start same as end should return a single-cell path
        grid = [[0,0],[0,0]]
        _, path = dijkstra_grid(grid, (0,0), (0,0))
        self.assertEqual(path, [(0,0)])

    def test_dijkstra_visited_order(self):
        #Visited order should start with the start cell
        grid = [[0,0,0],[0,0,0],[0,0,0]]
        vorder, _ = dijkstra_grid(grid, (0,0), (2,2))
        self.assertEqual(vorder[0], (0,0))

    def test_dijkstra_avoids_walls(self):
        #Path should not include wall cells.
        grid = [[0,0,0],[0,1,0],[0,0,0]]
        _, path = dijkstra_grid(grid, (0,0), (2,2))
        self.assertNotIn((1,1), path)

    # ── Event Queue ──
    def test_event_queue_min_priority_first(self):
        #Lowest priority number processed first (min-heap)  
        h = []
        heapq.heappush(h, (3, "SendEmail"))
        heapq.heappush(h, (1, "CriticalFix"))
        heapq.heappush(h, (5, "Backup"))
        heapq.heappush(h, (2, "AlertUser"))
        first = heapq.heappop(h)
        self.assertEqual(first, (1, "CriticalFix"))

    def test_event_queue_order(self):
        #Events popped in priority order
        h = []
        for p, n in [(3,"C"),(1,"A"),(2,"B")]: heapq.heappush(h,(p,n))
        order = [heapq.heappop(h)[1] for _ in range(3)]
        self.assertEqual(order, ["A","B","C"])

    def test_event_queue_size(self):
        h = []
        for p, n in [(1,"X"),(2,"Y"),(3,"Z")]: heapq.heappush(h,(p,n))
        self.assertEqual(len(h), 3)
        heapq.heappop(h)
        self.assertEqual(len(h), 2)

    def test_event_queue_empty_pop(self):
        #Popping empty list raises IndexError (standard Python behaviour)
        h = []
        with self.assertRaises(IndexError):
            heapq.heappop(h)

    # ── DP Grid path counting ──
    def test_dp_open_grid_paths(self):
        #2x2 open grid has exactly 2 paths
        grid = [[0,0],[0,0]]
        dp   = count_paths(grid)
        self.assertEqual(dp[1][1], 2)

    def test_dp_3x3_open(self):
        #3x3 open grid has 6 unique paths
        grid = [[0]*3 for _ in range(3)]
        dp   = count_paths(grid)
        self.assertEqual(dp[2][2], 6)

    def test_dp_wall_blocks_path(self):
        #Wall at (0,1) and (1,0) should block all paths in 2x2
        grid = [[0,1],[1,0]]
        dp   = count_paths(grid)
        self.assertEqual(dp[1][1], 0)

    def test_dp_single_row(self):
        #Single row with no walls – exactly 1 path
        grid = [[0,0,0,0]]
        dp   = count_paths(grid)
        self.assertEqual(dp[0][3], 1)

    def test_dp_single_col(self):
        #Single column with no walls – exactly 1 path
        grid = [[0],[0],[0]]
        dp   = count_paths(grid)
        self.assertEqual(dp[2][0], 1)

    def test_dp_reconstruct_path_start_end(self):
        #Reconstructed path starts at (0,0) and ends at bottom-right
        grid = [[0]*3 for _ in range(3)]
        dp   = count_paths(grid)
        path = reconstruct_path(dp, grid)
        self.assertEqual(path[0],  (0, 0))
        self.assertEqual(path[-1], (2, 2))

    def test_dp_reconstruct_no_path(self):
        #No path returns empty list
        grid = [[0,1],[1,0]]
        dp   = count_paths(grid)
        path = reconstruct_path(dp, grid)
        self.assertEqual(path, [])


if __name__ == "__main__":
    unittest.main()
