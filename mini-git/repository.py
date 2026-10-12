from datetime import datetime

from algorithms import ancestors, merge_sort, parent_first, shortest_path
from models import Commit


class MiniGitError(Exception):
    """명령어 또는 저장소 작업에서 발생하는 예상 가능한 오류를 나타낸다."""


class Repository:
    """파일 저장이나 네트워크 통신 없이 Mini Git 세션 상태를 관리한다."""

    def __init__(self) -> None:
        self.initialized = False
        self.author = ""
        self.head = "main"
        self.branches: dict[str, str | None] = {}
        self.commits: dict[str, Commit] = {}
        self.keyword_index: dict[str, set[str]] = {}
        self.author_index: dict[str, set[str]] = {}
        self.counter = 0

    def init(self, author: str) -> str:
        """저장소 상태를 초기화하고 비어 있는 main 브랜치를 생성한다."""
        self.__init__()
        self.initialized = True
        self.author = author
        self.branches["main"] = None
        return f"Initialized repository.\nCurrent branch: main\nCurrent user: {author}"

    def require_init(self) -> None:
        """저장소 초기화 전에 작업을 수행하지 못하도록 한다."""
        if not self.initialized:
            raise MiniGitError("Repository not initialized")

    def branch(self, name: str) -> str:
        """현재 브랜치의 최신 커밋을 가리키는 새 브랜치를 생성한다."""
        self.require_init()
        if name in self.branches:
            raise MiniGitError(f"Branch already exists: {name}")
        self.branches[name] = self.branches[self.head]
        return f"Created branch: {name}"

    def switch(self, name: str) -> str:
        """현재 활성화된 브랜치를 변경한다."""
        self.require_init()
        if name not in self.branches:
            raise MiniGitError(f"Unknown branch: {name}")
        self.head = name
        return f"Switched to branch: {name}"

    def commit(self, message: str) -> str:
        """HEAD에 새 커밋을 추가하고 두 종류의 역색인을 갱신한다."""
        self.require_init()
        self.counter += 1
        hash_ = f"{self.counter:06x}"
        parent = self.branches[self.head]
        commit = Commit(
            hash=hash_,
            message=message,
            author=self.author,
            timestamp=datetime.now(),
            parents=(parent,) if parent is not None else (),
        )
        self.commits[hash_] = commit
        self.branches[self.head] = hash_
        self.author_index.setdefault(self.author.lower(), set()).add(hash_)
        for keyword in message.lower().split():
            self.keyword_index.setdefault(keyword, set()).add(hash_)
        return f"[{self.head} {hash_}] {message}"

    def log(self, sort_by: str | None = None) -> list[Commit]:
        """부모 우선 로그 또는 지정된 기준으로 정렬된 커밋 목록을 반환한다."""
        self.require_init()
        items = parent_first(self.commits)
        if sort_by == "date":
            return merge_sort(items, key=lambda commit: commit.timestamp)
        if sort_by == "author":
            return merge_sort(items, key=lambda commit: commit.author.lower())
        return items

    def path(self, start: str, end: str) -> list[str]:
        """존재하는 두 커밋 사이의 무방향 최단 경로를 탐색한다."""
        self.require_init()
        self._require_commit(start)
        self._require_commit(end)
        return shortest_path(start, end, self.commits)

    def ancestor_hashes(self, hash_: str) -> list[str]:
        """지정한 커밋의 모든 조상 커밋 해시를 반환한다."""
        self.require_init()
        self._require_commit(hash_)
        return ancestors(hash_, self.commits)

    def search_keyword(self, keyword: str) -> list[Commit]:
        """정규화된 메시지 토큰과 일치하는 커밋을 검색한다."""
        self.require_init()
        tokens = keyword.lower().split()
        if not tokens:
            return []
        candidates = self.keyword_index.get(tokens[0], set()).copy()
        for token in tokens[1:]:
            candidates.intersection_update(self.keyword_index.get(token, set()))
        matches = (
            self.commits[hash_] for hash_ in candidates
            if keyword.lower() in self.commits[hash_].message.lower()
        )
        return merge_sort(list(matches), key=lambda commit: commit.hash)

    def search_author(self, author: str) -> list[Commit]:
        """대소문자를 구분하지 않고 작성자가 정확히 일치하는 커밋을 검색한다."""
        self.require_init()
        hashes = self.author_index.get(author.lower(), set())
        matches = [self.commits[hash_] for hash_ in hashes]
        return merge_sort(matches, key=lambda commit: commit.hash)

    def _require_commit(self, hash_: str) -> None:
        """존재하지 않는 커밋 해시에 대해 표준화된 오류를 발생시킨다."""
        if hash_ not in self.commits:
            raise MiniGitError(f"Unknown commit: {hash_}")
