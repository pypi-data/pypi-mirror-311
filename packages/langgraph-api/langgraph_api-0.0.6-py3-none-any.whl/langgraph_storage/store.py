import os
from collections import defaultdict
from typing import Any

from langgraph.checkpoint.memory import PersistentDict
from langgraph.store.memory import InMemoryStore

from langgraph_api.graph import resolve_embeddings

_STORE_CONFIG = None


class DiskBackedInMemStore(InMemoryStore):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._data = PersistentDict(dict, filename=_STORE_FILE)
        self._vectors = PersistentDict(lambda: defaultdict(dict), filename=_VECTOR_FILE)
        self._load_data(self._data, which="data")
        self._load_data(self._vectors, which="vectors")

    def _load_data(self, container: PersistentDict, which: str) -> None:
        if not container.filename:
            return
        try:
            container.load()
        except FileNotFoundError:
            # It's okay if the file doesn't exist yet
            pass

        except (EOFError, ValueError) as e:
            raise RuntimeError(
                f"Failed to load store {which} from {container.filename}. "
                "This may be due to changes in the stored data structure. "
                "Consider clearing the local store by running: rm -rf .langgraph_api"
            ) from e
        except Exception as e:
            raise RuntimeError(
                f"Unexpected error loading store {which} from {container.filename}: {str(e)}"
            ) from e

    def close(self) -> None:
        self._data.close()
        self._vectors.close()


_STORE_FILE = os.path.join(".langgraph_api", "store.pckl")
_VECTOR_FILE = os.path.join(".langgraph_api", "store.vectors.pckl")
os.makedirs(".langgraph_api", exist_ok=True)
STORE = DiskBackedInMemStore()


def set_store_config(config) -> None:
    global _STORE_CONFIG, STORE
    _STORE_CONFIG = config.copy()
    _STORE_CONFIG["index"]["embed"] = resolve_embeddings(_STORE_CONFIG.get("index", {}))
    # Re-create the store
    STORE.close()
    STORE = DiskBackedInMemStore(index=_STORE_CONFIG.get("index", {}))


def Store(*args: Any, **kwargs: Any) -> DiskBackedInMemStore:
    return STORE
