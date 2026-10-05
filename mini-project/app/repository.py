import csv
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

    def get_by_id(self, transaction_id: str) -> Transaction | None:
        """지정한 ID의 거래를 반환한다."""
        for transaction in self.get_all():
            if transaction.id == transaction_id:
                return transaction

        return None

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

    def update(self, transaction: Transaction) -> bool:
        """지정한 거래를 수정하고 성공 여부를 반환한다."""
        temp_path = self.file_path.with_suffix(".tmp")
        updated = False

        with temp_path.open("w", encoding="utf-8") as temp_file:
            for saved_transaction in self.get_all():
                if saved_transaction.id == transaction.id:
                    saved_transaction = transaction
                    updated = True

                data = {
                    "id": saved_transaction.id,
                    "type": saved_transaction.type,
                    "date": saved_transaction.date,
                    "amount": saved_transaction.amount,
                    "category": saved_transaction.category,
                    "memo": saved_transaction.memo,
                    "tags": saved_transaction.tags,
                }

                temp_file.write(
                    json.dumps(data, ensure_ascii=False) + "\n"
                )

        if updated:
            temp_path.replace(self.file_path)
        else:
            temp_path.unlink()

        return updated

    def delete(self, transaction_id: str) -> bool:
        """지정한 ID의 거래를 삭제하고 성공 여부를 반환한다."""
        temp_path = self.file_path.with_suffix(".tmp")
        deleted = False

        with temp_path.open("w", encoding="utf-8") as temp_file:
            for transaction in self.get_all():
                if transaction.id == transaction_id:
                    deleted = True
                    continue

                data = {
                    "id": transaction.id,
                    "type": transaction.type,
                    "date": transaction.date,
                    "amount": transaction.amount,
                    "category": transaction.category,
                    "memo": transaction.memo,
                    "tags": transaction.tags,
                }

                temp_file.write(
                    json.dumps(data, ensure_ascii=False) + "\n"
                )

        if deleted:
            temp_path.replace(self.file_path)
        else:
            temp_path.unlink()

        return deleted

    def import_csv(self, csv_path: Path) -> Iterator[dict]:
        """CSV 파일의 거래 데이터를 한 건씩 반환한다."""
        required_fields = {
            "date",
            "type",
            "category",
            "amount",
        }

        with csv_path.open("r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)

            fieldnames = set(reader.fieldnames or [])
            missing_fields = required_fields - fieldnames

            if missing_fields:
                missing = ", ".join(sorted(missing_fields))
                raise ValueError(
                    f"CSV 필수 컬럼이 없습니다: {missing}"
                )

            for row in reader:
                yield row

    def export_csv(
        self,
        csv_path: Path,
        transactions: Iterator[Transaction],
    ) -> int:
        """거래 내역을 CSV 파일로 저장하고 처리 건수를 반환한다."""
        fieldnames = [
            "date",
            "type",
            "category",
            "amount",
            "memo",
            "tags",
        ]

        count = 0

        with csv_path.open("w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames,
            )
            writer.writeheader()

            for transaction in transactions:
                writer.writerow(
                    {
                        "date": transaction.date,
                        "type": transaction.type,
                        "category": transaction.category,
                        "amount": transaction.amount,
                        "memo": transaction.memo,
                        "tags": ",".join(transaction.tags),
                    }
                )
                count += 1

        return count


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

    def remove(self, name: str) -> None:
        """지정한 카테고리를 삭제한다."""
        categories = [
            category
            for category in self.get_all()
            if category != name
        ]

        with self.file_path.open("w", encoding="utf-8") as file:
            for category in categories:
                data = {"name": category}
                file.write(
                    json.dumps(data, ensure_ascii=False) + "\n"
                )


class BudgetRepository:
    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path

    def get_all(self) -> Iterator[dict]:
        """예산을 한 건씩 읽어 반환한다."""
        with self.file_path.open("r", encoding="utf-8") as file:
            for line in file:
                if line.strip():
                    yield json.loads(line)

    def get_by_month(self, month: str) -> dict | None:
        """지정한 월의 예산을 반환한다."""
        for budget in self.get_all():
            if budget["month"] == month:
                return budget

        return None

    def set(self, month: str, amount: int) -> None:
        """월별 예산을 새로 저장하거나 기존 예산을 변경한다."""
        budgets = list(self.get_all())

        updated = False

        for budget in budgets:
            if budget["month"] == month:
                budget["amount"] = amount
                updated = True
                break

        if not updated:
            budgets.append(
                {
                    "month": month,
                    "amount": amount,
                }
            )

        with self.file_path.open("w", encoding="utf-8") as file:
            for budget in budgets:
                file.write(
                    json.dumps(budget, ensure_ascii=False) + "\n"
                )