from typing import List, Tuple, Any


class Node:
    """
    Node definition should not be changed in any way
    """
    __slots__ = ['key', 'value']

    def __init__(self, k: Any, v: Any):
        """
        Initializes node
        :param k: key to be stored in the node
        :param v: value to be stored in the node
        """
        self.key = k
        self.value = v

    def __lt__(self, other):
        """
        Less than comparator
        :param other: second node to be compared to
        :return: True if the node is less than other, False if otherwise
        """
        return self.key < other.key or (self.key == other.key and self.value < other.value)

    def __gt__(self, other):
        """
        Greater than comparator
        :param other: second node to be compared to
        :return: True if the node is greater than other, False if otherwise
        """
        return self.key > other.key or (self.key == other.key and self.value > other.value)

    def __eq__(self, other):
        """
        Equality comparator
        :param other: second node to be compared to
        :return: True if the nodes are equal, False if otherwise
        """
        return self.key == other.key and self.value == other.value

    def __str__(self):
        """
        Converts node to a string
        :return: string representation of node
        """
        return '({0}, {1})'.format(self.key, self.value)

    __repr__ = __str__


class PriorityQueue:
    """
    Partially completed data structure. Do not modify completed portions in any way
    """
    __slots__ = ['data']

    def __init__(self):
        """
        Initializes the priority heap
        """
        self.data = []

    def __str__(self) -> str:
        """
        Converts the priority heap to a string
        :return: string representation of the heap
        """
        return ', '.join(str(item) for item in self.data)

    __repr__ = __str__

    def to_tree_format_string(self) -> str:
        """
        Prints heap in Breadth First Ordering Format
        :return: String to print
        """
        string = ""
        # level spacing - init
        nodes_on_level = 0
        level_limit = 1
        spaces = 10 * int(1 + len(self))

        for i in range(len(self)):
            space = spaces // level_limit
            # determine spacing

            # add node to str and add spacing
            string += str(self.data[i]).center(space, ' ')

            # check if moving to next level
            nodes_on_level += 1
            if nodes_on_level == level_limit:
                string += '\n'
                level_limit *= 2
                nodes_on_level = 0
            i += 1

        return string

    #   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #   Modify below this line

    def __len__(self) -> int:
        """
        Finds the length of the Queue.
        :return: The current length of the Queue, int
        """
        return len(self.data)

    def empty(self) -> bool:
        """
        Checks if the Queue is empty.
        :return: True if empty, False otherwise
        """
        return not len(self)

    def top(self) -> Node:
        """
        Reads the root node without removing it.
        :return: The root node, or None if it doesn't exist
        """
        return self.data[0] if not self.empty() else None

    def prepare_index(self, index):
        """
        Helper function that prepares an index for internal use.
        It ensures that valid negative indices are turned into their respective
        position while invalid negative indices are marked as such.
        :param: the index to prepare
        :return: the prepared index, or None if it is invalid
        """
        if index < 0:
            index += len(self)
        if 0 <= index < len(self):
            return index
        else:
            return None

    def get_left_child_index(self, index: int) -> int:
        """
        Calculates the index the left child is stored at, if it exists.
        :param: the index of the parent node
        :return: the left child node's index if it exists, None otherwise
        """
        index = self.prepare_index(index)
        if index is None:
            return None
        result = 2 * index + 1
        return result if result < len(self) else None

    def get_right_child_index(self, index: int) -> int:
        """
        Calculates the index the right child is stored at, if it exists.
        :param: the index of the parent node
        :return: the right child node's index if it exists, None otherwise
        """
        index = self.prepare_index(index)
        if index is None:
            return None
        result = 2 * index + 2
        return result if result < len(self) else None

    def get_parent_index(self, index: int) -> int:
        """
        Calculates the index the parent is stored at, if it exists.
        :param: the index of the child node, either left or right
        :return: the parent node's index, or None if the child node is root
        """
        index = self.prepare_index(index)
        if not index:
            return None
        result = (index-1) // 2  # (x//y)*y <= x
        return result

    def _swap(self, i, j):
        """
        Helper function that swaps two indices in the underlying data.
        :param: the first index to be swapped and the second index to be swapped
        :return: None
        """
        temp = self.data[i]
        self.data[i] = self.data[j]
        self.data[j] = temp
        return

    def push(self, key: Any, val: Any) -> None:
        """
        Inserts a node to the heap
        :param: the key to insert the data at and the value to store for the key
        :return: None
        """
        temp_node = Node(key, val)  # create the new node
        self.data.append(temp_node)
        self.percolate_up(len(self) - 1)
        return

    def pop(self) -> Node:
        """
        Removes the smallest element from the priority queue.
        :return: the root node, or None if it doesn't exist
        """
        if self.empty():
            return None
        # switch around the first and last indices in data
        self._swap(0, -1)
        out = self.data.pop()
        self.percolate_down(0)
        return out

    def get_min_child_index(self, index: int) -> int:
        """
        Given an index of a node, will return the index of the smaller child.
        :param: the index of the node to find the smaller child of
        :return: the smaller child's index, or None if no children exist
        """
        left = self.get_left_child_index(index)
        if left is None:
            return None
        right = self.get_right_child_index(index)
        if right is None:
            return left
        if self.data[right] < self.data[left]:
            return right
        else:
            return left

    def percolate_up(self, index: int) -> None:
        """
        Given the index of a node, will move the node up to its valid spot in the heap.
        :param: the index to start sorting into the heap
        :return: None
        """
        parent_index = self.get_parent_index(index)
        if parent_index is None:
            return
        if not self.data[parent_index] > self.data[index]:
            return
        # swap the parent and child nodes
        self._swap(parent_index, index)
        return self.percolate_up(parent_index)

    def percolate_down(self, index: int) -> None:
        """
        Given the index of a node, will move the node down to its valid spot in the heap.
        :param: the index to start sorting into the heap
        :return: None
        """
        child_index = self.get_min_child_index(index)
        if child_index is None:
            return
        if not (self.data[index] > self.data[child_index]):
            return
        # swap the smaller child node for its parent
        self._swap(index, child_index)
        return self.percolate_down(child_index)


class MaxHeap:
    """
    Partially completed data structure. Do not modify completed portions in any way
    """
    __slots__ = ['data']

    def __init__(self):
        """
        Initializes the priority heap
        """
        self.data = PriorityQueue()

    def __str__(self):
        """
        Converts the priority heap to a string
        :return: string representation of the heap
        """
        return ', '.join(str(item) for item in self.data.data)

    def __len__(self):
        """
        Length override function
        :return: Length of the data inside the heap
        """
        return len(self.data)

    def print_tree_format(self):
        """
        Prints heap in bfs format
        """
        self.data.tree_format()

    #   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #   Modify below this line

    def empty(self) -> bool:
        """
        Checks if the MaxHeap is empty.
        :return: True if empty, False otherwise
        """
        return not len(self)

    def top(self) -> int:
        """
        Looks up the topmost entry of the Heap without removing it.
        :return: The largest entry, or None if it doesn't exist
        """
        if self.empty():
            return None
        return self.data.top().value

    def push(self, key: int) -> None:
        """
        Adds the value to the heap
        :param key: the entry to push onto the Heap
        :return: None
        """
        # sorting the negated value of the key in ascending order
        # is equivalent to sorting the value itself in descending order
        self.data.push(-key, key)
        return

    def pop(self) -> int:
        """
        Removes the largest element from the heap, else None
        :return: the largest entry, or None if it doesn't exist
        """
        if self.empty():
            return None
        return self.data.pop().value


def heap_sort(array):
    """
    Sorts the given list in-place, in ascending order, using a MaxHeap
    :param array: the list to be sorted
    :return: the now sorted list
    """
    heap = MaxHeap()
    # add the values to the heap
    for entry in array:
        heap.push(entry)
    for i in range(1, len(array)+1):
        array[-i] = heap.pop()
    return array


def find_ranking(rank, results: List[Tuple[int, str]]) -> str:
    """
    Sorts a season's team results into a ranking and retrieves the team name
    at the desired rank.
    :param: the rank that the result is desired for and  the results of each team
    :return: the name of the team with the least amount of losses by rank
    """
    queue = PriorityQueue()
    # sorts each result into the queue
    for losses, team in results:
        queue.push(losses, team)
    node = None
    # remove rank nodes from the top,
    # representing the rank best teams
    for i in range(rank):
        node = queue.pop()
    # if the team doesn't exist, the value is None
    return node.value if node is not None else None
