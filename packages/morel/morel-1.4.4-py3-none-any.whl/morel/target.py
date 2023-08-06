import importlib
import _collections_abc
import json
from multiprocessing import Lock
import sys
from collections import UserDict
from pathlib import Path
import time
from typing import Iterable

from morel.singleton import SingletonMeta
from morel.logger import logger


class _restrictedDict(UserDict):
    def __init__(self):
        return super().__init__()

    # def __init__(self, initialD):
    #    return super().__init__(initialD)

    # def __getitem__(self, key):
    #    return UserDict.__getitem__(self, key)

    # def __setitem__(self, key, val):
    #    UserDict.__setitem__(self, key, val)

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


class _Targets(_restrictedDict):
    def __init__(self):
        super().__init__()
        self._lock = Lock()
        self.target_functions = []
        self.log = logger
        self.last_update = time.time()

    # def __getitem__(self, key):
    #    return dict.__getitem__(self, key)

    def setBaseDir(self, dir):
        self.p = Path(dir)

    def setLogger(self, logger):
        self.log = logger

    def add_targets(self, targets):
        self.append(targets)

    def update_targets(self):
        if not hasattr(self, "p"):
            self.log.info(
                "Error! Targets not updated - you need to set base directory with Targets.setBaseDir(targets_directory)"
            )
            return
        else:
            self.log.info(f"basedir is {self.p}")
        with self._lock:
            files = list(self.p.glob("[!_]*.py"))
            self.log.info(f"Target files: {files}")
            target_funcs = []
            for targ in files:
                name = targ.stem

                try:
                    spec = importlib.util.spec_from_file_location(name, targ.resolve())
                    module = importlib.util.module_from_spec(spec)  # type: ignore
                    sys.modules[name] = module
                    spec.loader.exec_module(module)  # type: ignore
                    targetfun = getattr(sys.modules[name], "main")
                    target_funcs.append(targetfun)
                except Exception as e:
                    self.log.error(f"Exception on module {name}:\n{e}")
            self.target_functions = target_funcs
            self.log.info(f"Target functions: {self.target_functions}")

    def update(self):
        with self._lock:
            if time.time() - self.last_update > 2:
                for function in self.targets_functions:
                    self.add_targets(function())
                self.last_update = time.time()


Targets = _Targets()
if __name__ == "__main__":
    json.dump(Targets, sys.stdout, indent=2)
