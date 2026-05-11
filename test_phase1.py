#Automated tests for Phase 1 data structures.

import unittest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from stack_queue import Stack, Queue
from linked_list import LinkedList
from bst         import BST


class TestPhase1(unittest.TestCase):

    # ── Stack tests ──
    def test_stack_push_pop_sequence(self):
        #Push 3 items, pop 2 - final size should be 1 and correct order
        s = Stack()
        s.push("A"); s.push("B"); s.push("C")
        self.assertEqual(s.size(), 3)
        self.assertEqual(s.pop(), "C")
        self.assertEqual(s.pop(), "B")
        self.assertEqual(s.size(), 1)
        self.assertEqual(s.peek(), "A")

    def test_stack_empty_pop(self):
        #Popping from empty stack returns None
        s = Stack()
        self.assertIsNone(s.pop())

    def test_stack_is_empty(self):
        #isEmpty() reflects stack state correctly.
        s = Stack()
        self.assertTrue(s.isEmpty())
        s.push(1)
        self.assertFalse(s.isEmpty())

    # ── Queue tests ──
    def test_queue_enqueue_dequeue(self):
        #Enqueue 4 items, dequeue 3 – FIFO order maintained
        q = Queue()
        for v in [10, 20, 30, 40]: q.enqueue(v)
        self.assertEqual(q.size(), 4)
        self.assertEqual(q.dequeue(), 10)   # FIFO – first in
        self.assertEqual(q.dequeue(), 20)
        self.assertEqual(q.dequeue(), 30)
        self.assertEqual(q.size(), 1)
        self.assertEqual(q.peek(), 40)

    def test_queue_empty_dequeue(self):
        #Dequeuing from empty queue returns None
        q = Queue()
        self.assertIsNone(q.dequeue())

    def test_queue_peek_does_not_remove(self):
        #Peek should not remove the front element
        q = Queue()
        q.enqueue("X"); q.enqueue("Y")
        self.assertEqual(q.peek(), "X")
        self.assertEqual(q.size(), 2)

    # ── Linked List tests ──
    def test_linked_list_insert_at_position(self):
        #Insert node with value 10 at position 2
        ll = LinkedList()
        ll.insert_at_index(1, 0)
        ll.insert_at_index(2, 1)
        ll.insert_at_index(3, 2)
        ll.insert_at_index(10, 2)  
        items = ll.to_list()
        self.assertEqual(items[2], 10)

    def test_linked_list_delete_value(self):
        
        #Delete a value that exists
        ll = LinkedList()
        for v in [5, 10, 15]: ll.insert_at_index(v, ll.size())
        ok = ll.delete_value(10)
        self.assertTrue(ok)
        self.assertNotIn(10, ll.to_list())

    def test_linked_list_search(self):
        #Search returns correct index
        ll = LinkedList()
        for v in [100, 200, 300]: ll.insert_at_index(v, ll.size())
        self.assertEqual(ll.search(200), 1)
        self.assertEqual(ll.search(999), -1)

    def test_linked_list_reverse(self):
        #Reverse changes order correctly
        ll = LinkedList()
        for v in [1, 2, 3, 4]: ll.insert_at_index(v, ll.size())
        ll.reverse()
        self.assertEqual(ll.to_list(), [4, 3, 2, 1])

    # ── BST tests ──
    def test_bst_insert_inorder(self):
        #Insert [50, 30, 70] – inorder traversal should be [30, 50, 70]
        bst = BST()
        for v in [50, 30, 70]: bst.insert(v)
        self.assertEqual(bst.inorder(), [30, 50, 70])

    def test_bst_insert_and_inorder_rubric(self):
        #Rubric test: insert [50, 30, 70] – inorder = 30, 50, 70
        bst = BST()
        bst.insert(50); bst.insert(30); bst.insert(70)
        self.assertEqual(bst.inorder(), [30, 50, 70])

    def test_bst_search_found(self):
        #Search returns node when value exists
        bst = BST()
        for v in [10, 5, 20]: bst.insert(v)
        self.assertIsNotNone(bst.search(5))

    def test_bst_search_not_found(self):
        #Search returns None when value is absent
        bst = BST()
        bst.insert(10)
        self.assertIsNone(bst.search(99))

    def test_bst_delete(self):
        #Delete removes value from tree
        bst = BST()
        for v in [20, 10, 30]: bst.insert(v)
        bst.delete(10)
        self.assertIsNone(bst.search(10))
        self.assertEqual(bst.inorder(), [20, 30])

    def test_bst_preorder(self):
        #Preorder visits root before children
        bst = BST()
        for v in [50, 30, 70]: bst.insert(v)
        self.assertEqual(bst.preorder()[0], 50)

    def test_bst_postorder(self):
        #Postorder visits root last.
        bst = BST()
        for v in [50, 30, 70]: bst.insert(v)
        self.assertEqual(bst.postorder()[-1], 50)


if __name__ == "__main__":
    unittest.main()
