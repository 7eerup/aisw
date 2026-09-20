"""Mini Redis의 핵심 데이터 저장 및 관리 로직을 구현하는 모듈."""

import time

from structures.doubly_linked_list import DoublyLinkedList
from structures.hash_map import HashMap
from structures.min_heap import MinHeap


class MiniRedis:
    """문자열 데이터, LRU, TTL, 메모리를 관리하는 Mini Redis 클래스."""

    def __init__(self):
        """Mini Redis에서 사용하는 자료구조와 상태를 초기화한다."""
        self.store = HashMap()
        self.lru_nodes = HashMap()
        self.lru_list = DoublyLinkedList()

        self.expirations = HashMap()
        self.expiry_heap = MinHeap()

        self.maxmemory = 0
        self.used_memory = 0
        self.evicted_keys = 0

    def _calculate_entry_size(self, key, value):
        """키와 값이 차지하는 UTF-8 기준 바이트 크기를 계산한다."""
        key_size = len(key.encode("utf-8"))
        value_size = len(value.encode("utf-8"))

        return key_size + value_size

    def _is_expired(self, key):
        """키가 만료되었는지 확인한다."""
        expire_at = self.expirations.get(key)

        if expire_at is None:
            return False

        return time.time() >= expire_at

    def _delete_key(self, key):
        """키와 관련된 데이터, TTL, LRU 정보를 함께 삭제한다."""
        value = self.store.get(key)

        if value is None:
            return False

        entry_size = self._calculate_entry_size(key, value)

        self.store.remove(key)

        if self.expirations.contains(key):
            self.expirations.remove(key)

        lru_node = self.lru_nodes.get(key)

        if lru_node is not None:
            self.lru_list.remove_node(lru_node)
            self.lru_nodes.remove(key)

        self.used_memory -= entry_size

        return True

    def _cleanup_expired(self):
        """현재 시각을 기준으로 만료된 키들을 정리한다."""
        current_time = time.time()

        while self.expiry_heap.size() > 0:
            expire_at, key = self.expiry_heap.peek()

            if expire_at > current_time:
                break

            self.expiry_heap.pop()

            current_expire_at = self.expirations.get(key)

            if current_expire_at is None:
                continue

            if current_expire_at != expire_at:
                continue

            self._delete_key(key)

    def set(self, key, value):
        """키와 값을 저장하고 메모리 제한 및 LRU 상태를 관리한다."""
        self._cleanup_expired()

        new_size = self._calculate_entry_size(key, value)

        if self.maxmemory > 0 and new_size > self.maxmemory:
            return False

        old_value = self.store.get(key)

        if old_value is not None:
            old_size = self._calculate_entry_size(key, old_value)
            self.used_memory -= old_size

            if self.expirations.contains(key):
                self.expirations.remove(key)

            lru_node = self.lru_nodes.get(key)
            self.lru_list.move_to_front(lru_node)
        else:
            lru_node = self.lru_list.insert_front(key)
            self.lru_nodes.put(key, lru_node)

        self.store.put(key, value)
        self.used_memory += new_size

        while (
            self.maxmemory > 0
            and self.used_memory > self.maxmemory
        ):
            lru_node = self.lru_list.tail

            if lru_node is None:
                break

            lru_key = lru_node.data
            self._delete_key(lru_key)
            self.evicted_keys += 1

        return True

    def get(self, key):
        """키에 해당하는 값을 조회하고 성공 시 LRU 순서를 갱신한다."""
        if self._is_expired(key):
            self._delete_key(key)
            return None

        value = self.store.get(key)

        if value is None:
            return None

        lru_node = self.lru_nodes.get(key)

        if lru_node is not None:
            self.lru_list.move_to_front(lru_node)

        return value

    def delete(self, key):
        """키와 관련된 데이터를 삭제하고 성공 여부를 반환한다."""
        if self._is_expired(key):
            self._delete_key(key)
            return 0

        if not self.store.contains(key):
            return 0

        self._delete_key(key)
        return 1

    def exists(self, key):
        """키가 존재하는지 확인하고 정수 형태의 결과를 반환한다."""
        if self._is_expired(key):
            self._delete_key(key)
            return 0

        if self.store.contains(key):
            return 1

        return 0

    def dbsize(self):
        """현재 저장된 유효한 키의 개수를 반환한다."""
        self._cleanup_expired()
        return self.store.size()

    def keys(self):
        """현재 저장된 유효한 모든 키를 리스트로 반환한다."""
        self._cleanup_expired()
        return self.store.keys()

    def expire(self, key, seconds):
        """키에 만료 시간을 설정하고 성공 여부를 반환한다."""
        if self._is_expired(key):
            self._delete_key(key)
            return 0

        if not self.store.contains(key):
            return 0

        if seconds <= 0:
            self._delete_key(key)
            return 1

        expire_at = time.time() + seconds

        self.expirations.put(key, expire_at)
        self.expiry_heap.push((expire_at, key))

        return 1

    def ttl(self, key):
        """키의 남은 만료 시간을 초 단위 정수로 반환한다."""
        if self._is_expired(key):
            self._delete_key(key)
            return -2

        if not self.store.contains(key):
            return -2

        expire_at = self.expirations.get(key)

        if expire_at is None:
            return -1

        remaining = int(expire_at - time.time())

        if remaining < 0:
            self._delete_key(key)
            return -2

        return remaining

    def set_maxmemory(self, maxmemory):
        """최대 메모리 제한을 설정한다."""
        self._cleanup_expired()

        self.maxmemory = maxmemory

        return True

    def info_memory(self):
        """현재 메모리 사용량과 제한 및 제거된 키 수를 반환한다."""
        self._cleanup_expired()

        return (
            f"used_memory:{self.used_memory}\n"
            f"maxmemory:{self.maxmemory}\n"
            f"evicted_keys:{self.evicted_keys}"
        )