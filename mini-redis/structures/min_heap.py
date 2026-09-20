"""TTL 만료 시간을 관리하기 위한 최소 힙 구현 모듈."""


class MinHeap:
    """가장 빠른 만료 시간을 루트에 유지하는 최소 힙 클래스."""

    def __init__(self):
        """힙 데이터를 저장할 리스트를 초기화한다."""
        self.heap = []

    def push(self, item):
        """새로운 항목을 힙에 추가하고 최소 힙 구조를 유지한다."""
        self.heap.append(item)
        self._heapify_up(len(self.heap) - 1)

    def _heapify_up(self, index):
        """지정한 인덱스의 항목을 위로 이동시켜 최소 힙을 유지한다."""
        while index > 0:
            parent_index = (index - 1) // 2

            if self.heap[parent_index][0] <= self.heap[index][0]:
                break

            self.heap[parent_index], self.heap[index] = (
                self.heap[index],
                self.heap[parent_index],
            )

            index = parent_index

    def peek(self):
        """힙의 최솟값을 제거하지 않고 반환한다."""
        if not self.heap:
            return None

        return self.heap[0]

    def pop(self):
        """힙의 최솟값을 제거하고 반환한다."""
        if not self.heap:
            return None

        if len(self.heap) == 1:
            return self.heap.pop()

        min_item = self.heap[0]
        self.heap[0] = self.heap.pop()

        self._heapify_down(0)

        return min_item

    def _heapify_down(self, index):
        """지정한 인덱스의 항목을 아래로 이동시켜 최소 힙을 유지한다."""
        length = len(self.heap)

        while True:
            left_index = index * 2 + 1
            right_index = index * 2 + 2
            smallest_index = index

            if (
                left_index < length
                and self.heap[left_index][0]
                < self.heap[smallest_index][0]
            ):
                smallest_index = left_index

            if (
                right_index < length
                and self.heap[right_index][0]
                < self.heap[smallest_index][0]
            ):
                smallest_index = right_index

            if smallest_index == index:
                break

            self.heap[index], self.heap[smallest_index] = (
                self.heap[smallest_index],
                self.heap[index],
            )

            index = smallest_index

    def size(self):
        """힙에 저장된 항목의 개수를 반환한다."""
        return len(self.heap)