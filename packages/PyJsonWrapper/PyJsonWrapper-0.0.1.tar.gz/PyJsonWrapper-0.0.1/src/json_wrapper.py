import json
import sys
from typing import Any, List, Union
from collections.abc import Iterable, Mapping

JsonType = Union[str, int, bool, dict, list, None]

Path = Union[str, int, List[Union[int, str]]]


class JsonWrapper(Mapping):
    def __init__(self, value: JsonType):
        self._value = value

    def __getitem__(self, key: Path):
        if isinstance(key, (int, str)):
            t_value = self._value[key]
        else:
            t_value = self._value
            for k in key:
                t_value = t_value[k]
        return JsonWrapper(t_value)

    def __iter__(self):
        for item in self._value:
            if isinstance(item, (dict, list)):
                yield JsonWrapper(item)
            else:
                yield item
            
    def __len__(self):
        return len(self._value)

    def __str__(self) -> str:
        return str(self._value)

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: "JsonWrapper") -> bool:
        return self._value == other.value

    @property
    def value(self):
        return self._value

    @classmethod
    def loads(cls, s, **kw) -> "JsonWrapper":
        value = json.loads(s, **kw)
        return JsonWrapper(value)

    def get(self, key: Path, default: Any = None):
        try:
            return self.__getitem__(key)
        except (KeyError, IndexError, TypeError):
            return default

    def get_value(self, key: Path, default: Any = None):
        try:
            res = self.__getitem__(key)
            return res._value
        except (KeyError, IndexError, TypeError):
            return default

    def find_by_key(self, key: str, count: int = -1):
        if count <= 0:
            count = sys.maxsize
        res = []
        temp_nodes = [self]
        while temp_nodes:
            node = temp_nodes.pop(0)
            if isinstance(node.value, dict):
                for k, v in node.items():
                    if k == key:
                        res.append(v)
                        if len(res) == count:
                            return res
                    if isinstance(v, (dict, list)):
                        temp_nodes.append(v)
            elif isinstance(node.value, list):
                for v in node:
                    if isinstance(v, (dict, list)):
                        temp_nodes.append(v)
        return res

    def find_one_by_key(self, key: str):
        res = self.find_by_key(key, 1)
        if res:
            return res[0]
        return None

    def is_none(self):
        return self._value is None
