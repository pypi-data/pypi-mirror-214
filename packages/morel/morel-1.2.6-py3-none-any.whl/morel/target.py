import importlib
import json
from multiprocessing import Lock
import sys

from pathlib import Path
from typing import Iterable
from morel.singleton import SingletonMeta


class _restrictedDict(dict):
    def __init__(self):
        return super().__init__()

    def __init__(self, initialD):
        return super().__init__(initialD)

    def __getitem__(self, key):
        val = dict.__getitem__(self, key)
        # print("GET", key, val)
        if (
            not isinstance(val, Iterable)
            or isinstance(val, str)
            or isinstance(val, bytes)
            # any other iterable that souldn't be iterated?
        ):
            return [
                val,
            ]
        return val

    def __setitem__(self, key, val):
        # print("SET", key, val)
        dict.__setitem__(self, key, val)

    def append(self, dict2) -> None:  # inplace
        dict2 = _restrictedDict(dict2)
        for k, v in dict2.items():
            if k not in self:
                self[k] = v
                continue

            if isinstance(self[k], dict) and not isinstance(self[k], _restrictedDict):
                self[k] = _restrictedDict(self[k])

            if isinstance(self[k], list):
                self[k] = set(self[k])

            if not isinstance(self[k], Iterable):
                self[k] = {
                    self[k],
                }

            if isinstance(self[k], _restrictedDict):
                self[k].append(dict2[k])

            elif isinstance(self[k], set):
                self[k] |= {
                    v,
                }

            # print(self)


class Targets(_restrictedDict, metaclass=SingletonMeta):
    def __init__(self):
        self._lock = Lock()
        # self.update()

    def __getitem__(self, key):
        super().__getitem__(self, key)

    def setBaseDir(self, dir):
        self.p = Path(dir)

    def add_targets(self, targets):
        self.append(targets)

    def update(self):
        if not hasattr(self, "p"):
            print(
                "Error! Targets not updated - you need to set base directory with Targets().setBaseDir(targets_directory)"
            )
            return
        with self._lock:
            files = list(self.p.glob("**/[!_]*.py"))
            targets_functions = []

            for targ in files:
                name = targ.stem

                try:
                    spec = importlib.util.spec_from_file_location(name, targ.resolve())
                    module = importlib.util.module_from_spec(spec)  # type: ignore
                    sys.modules[name] = module
                    spec.loader.exec_module(module)  # type: ignore
                    targetfun = getattr(sys.modules[name], "main")
                    targets_functions.append(targetfun)
                except Exception as e:
                    print(f"Exception on module {name}:\n{e}")

            # print(targets_functions)
            for function in targets_functions:
                self.add_targets(function())


if __name__ == "__main__":
    json.dump(Targets, sys.stdout, indent=2)
