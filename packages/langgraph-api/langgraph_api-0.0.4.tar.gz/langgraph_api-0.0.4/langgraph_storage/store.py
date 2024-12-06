import os
from typing import Any

from langgraph.checkpoint.memory import PersistentDict
from langgraph.store.memory import InMemoryStore


class DiskBackedInMemStore(InMemoryStore):
    def __init__(self, *args: Any, filename: str | None = None, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.filename = filename
        self._data = PersistentDict(dict, filename=self.filename)
        self._load_data()

    def _load_data(self) -> None:
        if not self.filename:
            return
        try:
            self._data.load()
        except FileNotFoundError:
            # It's okay if the file doesn't exist yet
            pass
        except (EOFError, ValueError) as e:
            raise RuntimeError(
                f"Failed to load store from {self.filename}. "
                "This may be due to changes in the stored data structure. "
                "Consider clearing the local store by running: rm -rf .langgraph_api"
            ) from e
        except Exception as e:
            raise RuntimeError(
                f"Unexpected error loading store from {self.filename}: {str(e)}"
            ) from e

    def close(self) -> None:
        self._data.close()


_STORE_FILE = os.path.join(".langgraph_api", "store.pckl")
os.makedirs(".langgraph_api", exist_ok=True)
STORE = DiskBackedInMemStore(filename=_STORE_FILE)


def Store(*args: Any, **kwargs: Any) -> DiskBackedInMemStore:
    return STORE
