import shlex

from models import Commit
from repository import MiniGitError, Repository


def format_commit(commit: Commit) -> str:
    """커밋의 필수 메타데이터를 지정된 형식으로 출력한다."""
    timestamp = commit.timestamp.strftime("%Y-%m-%d %H:%M:%S")
    return (
        f"commit {commit.hash} ({commit.author}, {timestamp}) "
        f"[{commit.branch}]\n"
        f"{commit.message}"
    )


def format_search(commits: list[Commit]) -> str:
    """역색인 검색 결과를 커밋 해시와 메시지 형식으로 출력한다."""
    lines = [f"Found {len(commits)} commit(s):"]
    lines.extend(f"- {commit.hash}: {commit.message}" for commit in commits)
    return "\n".join(lines)


def execute(line: str, repo: Repository) -> str | None:
    """명령어를 파싱하고 실행하며, 종료 요청 시 None을 반환한다."""
    try:
        args = shlex.split(line)
    except ValueError as exc:
        raise MiniGitError("Invalid args") from exc

    if not args:
        return ""
    command = args[0].upper()
    params = args[1:]

    if command in ("EXIT", "QUIT") and not params:
        return None
    if command == "INIT" and len(params) == 1 and params[0].strip():
        return repo.init(params[0])
    if command == "BRANCH" and len(params) == 1 and params[0].strip():
        return repo.branch(params[0])
    if command == "SWITCH" and len(params) == 1 and params[0].strip():
        return repo.switch(params[0])
    if command == "COMMIT" and len(params) == 1 and params[0].strip():
        return repo.commit(params[0])
    if command == "LOG":
        if not params:
            return "\n".join(format_commit(item) for item in repo.log())
        if len(params) == 1 and params[0] in ("--sort-by=date", "--sort-by=author"):
            sort_by = params[0].split("=", 1)[1]
            return "\n".join(format_commit(item) for item in repo.log(sort_by))
    if command == "PATH" and len(params) == 2:
        path = repo.path(*params)
        return "Path: " + " -> ".join(path) if path else "No path"
    if command == "ANCESTORS" and len(params) == 1:
        hashes = repo.ancestor_hashes(params[0])
        return "\n".join(hashes) if hashes else "No ancestors"
    if command == "SEARCH" and len(params) == 1:
        arg = params[0]
        if arg.startswith("--author=") and arg[len("--author="):].strip():
            return format_search(repo.search_author(arg[len("--author="):]))
        if arg and not arg.startswith("--"):
            return format_search(repo.search_keyword(arg))

    raise MiniGitError("Invalid args")


def repl() -> None:
    """exit, quit 또는 입력 종료 시까지 명령어를 반복 입력받아 실행한다."""
    repo = Repository()
    while True:
        try:
            line = input("mini-git> ")
            result = execute(line, repo)
            if result is None:
                break
            if result:
                print(result)
        except MiniGitError as exc:
            print(exc)
        except (EOFError, KeyboardInterrupt):
            print()
            break
