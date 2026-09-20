"""체이닝 방식의 해시맵 구현 모듈."""


class HashNode:
    """해시맵 버킷에 저장되는 하나의 노드를 표현하는 클래스."""

    def __init__(self, key, value):
        """키, 값, 다음 노드 참조를 초기화한다."""
        self.key = key
        self.value = value
        self.next = None


class HashMap:
    """체이닝 방식으로 키-값 데이터를 관리하는 해시맵 클래스."""

    def __init__(self, initial_capacity=8):
        """버킷 배열과 해시맵의 기본 상태를 초기화한다."""
        self.capacity = initial_capacity
        self.buckets = [None] * self.capacity
        self.count = 0

    def _hash(self, key):
        """문자열 키를 버킷 인덱스로 변환한다."""
        hash_value = 0

        for char in key:
            hash_value = (
                hash_value * 31 + ord(char)
            ) % self.capacity

        return hash_value

    def put(self, key, value):
        """키와 값을 해시맵에 저장하고 기존 키가 있으면 값을 갱신한다."""
        index = self._hash(key)
        current = self.buckets[index]

        while current is not None:
            if current.key == key:
                current.value = value
                return

            current = current.next

        self._insert_without_resize(key, value)

        if self.count / self.capacity > 0.75:
            self._resize()

    def _insert_without_resize(self, key, value):
        """크기 확장 검사 없이 키와 값을 현재 버킷에 저장한다."""
        index = self._hash(key)

        new_node = HashNode(key, value)
        new_node.next = self.buckets[index]
        self.buckets[index] = new_node

        self.count += 1

    def _resize(self):
        """버킷 크기를 2배로 확장하고 기존 데이터를 다시 배치한다."""
        old_buckets = self.buckets

        self.capacity *= 2
        self.buckets = [None] * self.capacity
        self.count = 0

        for bucket in old_buckets:
            current = bucket

            while current is not None:
                self._insert_without_resize(
                    current.key,
                    current.value,
                )
                current = current.next

    def get(self, key):
        """키에 해당하는 값을 찾아 반환한다."""
        index = self._hash(key)
        current = self.buckets[index]

        while current is not None:
            if current.key == key:
                return current.value

            current = current.next

        return None

    def remove(self, key):
        """키에 해당하는 노드를 제거하고 값을 반환한다."""
        index = self._hash(key)
        current = self.buckets[index]
        previous = None

        while current is not None:
            if current.key == key:
                if previous is None:
                    self.buckets[index] = current.next
                else:
                    previous.next = current.next

                self.count -= 1
                return current.value

            previous = current
            current = current.next

        return None

    def contains(self, key):
        """키가 해시맵에 존재하는지 확인한다."""
        index = self._hash(key)
        current = self.buckets[index]

        while current is not None:
            if current.key == key:
                return True

            current = current.next

        return False

    def keys(self):
        """해시맵에 저장된 모든 키를 리스트로 반환한다."""
        result = []

        for bucket in self.buckets:
            current = bucket

            while current is not None:
                result.append(current.key)
                current = current.next

        return result

    def size(self):
        """해시맵에 저장된 키-값의 개수를 반환한다."""
        return self.count