from collections import deque
from typing import Callable, TypeVar

from models import Commit

T = TypeVar("T")


def merge_sort(items: list[T], key: Callable[[T], object]) -> list[T]:
    """표준 정렬 API를 사용하지 않고 안정적인 오름차순 병합 정렬을 수행한다."""
    if len(items) < 2:
        return items[:]

    middle = len(items) // 2
    left = merge_sort(items[:middle], key)
    right = merge_sort(items[middle:], key)
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


def parent_first(commits: dict[str, Commit]) -> list[Commit]:
    """모든 커밋을 부모가 자식보다 먼저 나오도록 위상 정렬하여 반환한다."""
    degrees = {hash_: len(commit.parents) for hash_, commit in commits.items()}
    children = {hash_: [] for hash_ in commits}
    for hash_, commit in commits.items():
        for parent in commit.parents:
            children[parent].append(hash_)

    queue = deque(hash_ for hash_, degree in degrees.items() if degree == 0)
    result = []
    while queue:
        current = queue.popleft()
        result.append(commits[current])
        for child in children[current]:
            degrees[child] -= 1
            if degrees[child] == 0:
                queue.append(child)
    return result


def ancestors(start: str, commits: dict[str, Commit]) -> list[str]:
    """지정한 커밋의 모든 조상 해시를 중복 없이 탐색 순서대로 반환한다."""
    visited = {start}
    stack = list(reversed(commits[start].parents))
    result = []
    while stack:
        current = stack.pop()
        if current in visited:
            continue
        visited.add(current)
        result.append(current)
        stack.extend(reversed(commits[current].parents))
    return result


def shortest_path(start: str, end: str, commits: dict[str, Commit]) -> list[str]:
    """두 커밋 사이에서 사전순으로 가장 작은 최단 무방향 경로를 반환한다."""
    neighbors = {hash_: set(commit.parents) for hash_, commit in commits.items()}
    for hash_, commit in commits.items():
        for parent in commit.parents:
            neighbors[parent].add(hash_)

    distances = {end: 0}
    queue = deque([end])
    while queue:
        current = queue.popleft()
        for neighbor in neighbors[current]:
            if neighbor not in distances:
                distances[neighbor] = distances[current] + 1
                queue.append(neighbor)

    if start not in distances:
        return []

    path = [start]
    while path[-1] != end:
        current = path[-1]
        candidates = (
            neighbor for neighbor in neighbors[current]
            if distances.get(neighbor) == distances[current] - 1
        )

        path.append(min(candidates))

    return path
