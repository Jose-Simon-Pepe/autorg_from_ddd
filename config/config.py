import tomllib
from metaclasses.single import Single

class Config(metaclass=Single):


    def __init__(self,path:str="config.toml") -> None:
        self._path = path
        self._read_file()
        self.project: dict = {}


    def _read_file(self):
        try:
            with open(self._path, "rb") as f:
                data = tomllib.load(f)

                self.config = data
            
        except FileNotFoundError as err:
            print(f"Error: file not found {err}")

    def storage(self, key) -> dict[str, str]:
        return self.config.get("storage")[key]

    def load_project_metadata(self):
        self.project["name"] = self.config.get("project")["name"]
        self.project["version"] = self.config.get("project")["version"]


class DuplicatedConfigError(BaseException):
    pass

