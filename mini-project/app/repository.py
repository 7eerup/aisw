import json
from pathlib import Path
from typing import Iterator

from .models import Transaction


class TransactionRepository:
    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path

    def get_all(self) -> Iterator[Transaction]:
        """거래 내역을 한 건씩 읽어 반환한다."""
        with self.file_path.open("r", encoding="utf-8") as file:
            for line in file:
                if line.strip():
                    data = json.loads(line)
                    yield Transaction(**data)

    def get_all_latest(self) -> Iterator[Transaction]:
        """거래 내역을 파일 끝에서부터 읽어 최신순으로 반환한다."""
        with self.file_path.open("rb") as file:
            file.seek(0, 2)
            position = file.tell()
            buffer = b""

            while position > 0:
                position -= 1
                file.seek(position)
                byte = file.read(1)

                if byte == b"\n":
                    if buffer:
                        line = buffer[::-1].decode("utf-8")
                        data = json.loads(line)
                        yield Transaction(**data)
                        buffer = b""
                else:
                    buffer += byte

            if buffer:
                line = buffer[::-1].decode("utf-8")
                data = json.loads(line)
                yield Transaction(**data)

    def add(self, transaction: Transaction) -> None:
        """거래 내역 한 건을 JSONL 파일에 추가한다."""
        data = {
            "id": transaction.id,
            "type": transaction.type,
            "date": transaction.date,
            "amount": transaction.amount,
            "category": transaction.category,
            "memo": transaction.memo,
            "tags": transaction.tags,
        }

        with self.file_path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(data, ensure_ascii=False) + "\n")


class CategoryRepository:
    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path

    def get_all(self) -> Iterator[str]:
        """카테고리를 한 건씩 읽어 반환한다."""
        with self.file_path.open("r", encoding="utf-8") as file:
            for line in file:
                if line.strip():
                    data = json.loads(line)
                    yield data["name"]

    def add(self, name: str) -> None:
        """카테고리 한 건을 JSONL 파일에 추가한다."""
        data = {"name": name}

        with self.file_path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(data, ensure_ascii=False) + "\n")


class BudgetRepository:
    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path

    def get_all(self) -> Iterator[dict]:
        """예산을 한 건씩 읽어 반환한다."""
        with self.file_path.open("r", encoding="utf-8") as file:
            for line in file:
                if line.strip():
                    yield json.loads(line)

    def add(self, month: str, amount: int) -> None:
        """월별 예산 한 건을 JSONL 파일에 추가한다."""
        data = {
            "month": month,
            "amount": amount,
        }

        with self.file_path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(data, ensure_ascii=False) + "\n")