#Automated tests for Phase 2 algorithms

import unittest
import sys, os, heapq
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from sorting         import bubble_steps, selection_steps, merge_steps
from graph_traversal import Graph
from heap            import node_positions


# Run a step generator to completion and return final array
def run_steps(gen):
    last = None
    for step in gen:
        last = step
    return last[0] if last else []


class TestPhase2(unittest.TestCase):

    def test_bubble_sort_correctness(self):
        arr = [5, 3, 8, 1, 2]
        result = run_steps(bubble_steps(arr))
        self.assertEqual(result, [1, 2, 3, 5, 8])

    def test_bubble_sort_already_sorted(self):
        arr = [1, 2, 3, 4, 5]
        result = run_steps(bubble_steps(arr))
        self.assertEqual(result, [1, 2, 3, 4, 5])

    def test_bubble_sort_reverse(self):
        arr = [5, 4, 3, 2, 1]
        result = run_steps(bubble_steps(arr))
        self.assertEqual(result, [1, 2, 3, 4, 5])

    def test_selection_sort_correctness(self):
        arr = [5, 3, 8, 1, 2]
        result = run_steps(selection_steps(arr))
        self.assertEqual(result, [1, 2, 3, 5, 8])

    def test_selection_sort_single(self):
        arr = [42]
        result = run_steps(selection_steps(arr))
        self.assertEqual(result, [42])

    def test_merge_sort_correctness(self):
        arr = [5, 3, 8, 1, 2]
        steps = merge_steps(arr)
        result = steps[-1][0]
        self.assertEqual(result, [1, 2, 3, 5, 8])

    def test_merge_sort_duplicates(self):
        arr = [3, 1, 4, 1, 5, 9, 2, 6]
        steps = merge_steps(arr)
        result = steps[-1][0]
        self.assertEqual(result, sorted(arr))

    def test_merge_sort_empty(self):
        arr = []
        steps = merge_steps(arr)
        self.assertEqual(steps[-1][0], [])

    def test_bfs_visits_all_reachable(self):
        g = Graph(directed=False)
        for v in ["A","B","C","D","E","F","G"]: g.addVertex(v)
        for e in [("A","B"),("A","C"),("B","D"),("B","E"),("C","F"),("C","G")]:
            g.addEdge(*e)
        steps   = list(g.bfs_steps("A"))
        visited = steps[-1][2] if steps else set()
        self.assertEqual(len(visited), 7)

    def test_bfs_start_visited_first(self):
        g = Graph(directed=False)
        for v in ["A","B","C"]: g.addVertex(v)
        g.addEdge("A","B"); g.addEdge("B","C")
        steps = list(g.bfs_steps("A"))
        self.assertIn("A", steps[0][2])

    def test_bfs_order_breadth(self):
        g = Graph(directed=False)
        for v in ["A","B","C","D"]: g.addVertex(v)
        g.addEdge("A","B"); g.addEdge("B","C"); g.addEdge("C","D")
        steps = list(g.bfs_steps("A"))
        final_order = steps[-1][3]
        self.assertEqual(final_order, ["A","B","C","D"])

    def test_dfs_visits_all_reachable(self):
        g = Graph(directed=False)
        for v in ["A","B","C","D"]: g.addVertex(v)
        g.addEdge("A","B"); g.addEdge("A","C"); g.addEdge("C","D")
        steps   = list(g.dfs_steps("A"))
        visited = steps[-1][2] if steps else set()
        self.assertEqual(len(visited), 4)

    def test_dfs_start_first(self):
        g = Graph(directed=False)
        for v in ["X","Y"]: g.addVertex(v)
        g.addEdge("X","Y")
        steps = list(g.dfs_steps("X"))
        self.assertEqual(steps[0][0], "X")

    def test_heap_min_property(self):
        """After pushes the root (index 0) should be the minimum."""
        h = []
        for v in [15, 40, 25, 60, 10, 35]: heapq.heappush(h, v)
        self.assertEqual(h[0], 10)

    def test_heap_extract_min(self):
        """Extract-min should always return the smallest value."""
        h = []
        for v in [30, 10, 20]: heapq.heappush(h, v)
        self.assertEqual(heapq.heappop(h), 10)
        self.assertEqual(heapq.heappop(h), 20)

    def test_heap_size_after_operations(self):
        h = []
        for v in [5, 3, 8]: heapq.heappush(h, v)
        heapq.heappop(h)
        self.assertEqual(len(h), 2)

    def test_node_positions_root(self):
        """Root (index 0) should be positioned at the top centre."""
        pos = node_positions(7, 450, 150)
        self.assertIn(0, pos)
        self.assertAlmostEqual(pos[0][0], 450, delta=5)


if __name__ == "__main__":
    unittest.main()
