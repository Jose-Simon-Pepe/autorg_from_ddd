from datetime import datetime
import os
import csv
from autorg.domain.protocols.repository import Repository
from autorg.domain.entities.input import Input


class CsvRepository(Repository):
    def __init__(self,path:str ="data.csv"):
        """En caso de no especificarse un path, se usara el repo general"""
        self._repo_path = path
        self.rows = []

    def _file_exists(self):
        return os.path.exists(self._repo_path)

    def store(self, inp: Input) -> None:
        row = [str(inp.id()), inp.value().get("creation_date"), inp.value().get("content")]

        mode = "a" if os.path.exists(self._repo_path) else "w"
        with open(self._repo_path, mode, newline="") as file:
            writer = csv.writer(file)
            writer.writerow(row)

    def getAll(self) -> list[Input]:
        if len(self.rows) != 0:
            return self.rows

        elif self._file_exists():
            self._read_file()
        return self.rows

    def _read_file(self):
        with open(self._repo_path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                inp = Input(
                    id=int(row[0]),
                    creation_date=datetime.fromisoformat(row[1]),
                    content=row[2],
                )
                self.rows.append(inp)
