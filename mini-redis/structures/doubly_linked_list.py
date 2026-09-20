"""LRU 관리를 위한 이중 연결 리스트 구현 모듈."""


class Node:
    """이중 연결 리스트의 하나의 노드를 표현하는 클래스."""

    def __init__(self, data):
        """노드의 데이터와 이전/다음 노드 참조를 초기화한다."""
        self.prev = None
        self.next = None
        self.data = data


class DoublyLinkedList:
    """이중 연결 리스트를 관리하는 클래스."""

    def __init__(self):
        """리스트의 head, tail, 길이를 초기화한다."""
        self.head = None
        self.tail = None
        self.length = 0

    def insert_front(self, data):
        """리스트의 맨 앞에 새로운 노드를 추가한다."""
        new_node = Node(data)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

        self.length += 1

        return new_node

    def insert_back(self, data):
        """리스트의 맨 뒤에 새로운 노드를 추가한다."""
        new_node = Node(data)

        if self.tail is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

        self.length += 1

        return new_node

    def remove_front(self):
        """리스트의 맨 앞 노드를 제거하고 반환한다."""
        if self.head is None:
            return None

        removed_node = self.head

        if self.head is self.tail:
            self.head = None
            self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = None
            removed_node.next = None

        self.length -= 1

        return removed_node

    def remove_back(self):
        """리스트의 맨 뒤 노드를 제거하고 반환한다."""
        if self.tail is None:
            return None

        removed_node = self.tail

        if self.head is self.tail:
            self.head = None
            self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None
            removed_node.prev = None

        self.length -= 1

        return removed_node

    def remove_node(self, node):
        """지정한 노드를 리스트에서 제거하고 반환한다."""
        if node is None:
            return None

        if node is self.head:
            return self.remove_front()

        if node is self.tail:
            return self.remove_back()

        node.prev.next = node.next
        node.next.prev = node.prev

        node.prev = None
        node.next = None

        self.length -= 1

        return node

    def move_to_front(self, node):
        """지정한 노드를 리스트의 맨 앞으로 이동한다."""
        if node is None or node is self.head:
            return node

        if node is self.tail:
            self.tail = node.prev
            self.tail.next = None
        else:
            node.prev.next = node.next
            node.next.prev = node.prev

        node.prev = None
        node.next = self.head
        self.head.prev = node
        self.head = node

        return node