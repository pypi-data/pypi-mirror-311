# Author: kk.Fang(fkfkbill@gmail.com)

__all__ = [
    "EnsuredDict",
    "EnsuredDictValue",
    "EDV"
]

import copy
import json
from typing import Dict, Optional, Union, Any, Tuple


class EnsuredDictValue:
    """缺省值，不填则默认使用None"""

    def __init__(self,
                 default_value=None,
                 extra: Optional[Union[dict, list, tuple, Any]] = None,
                 **kwargs):
        """
        :param default_value: 缺省值，如果是一个callable，则在实例化的时候执行并回填其返回值
        :param extra: 额外信息，不会作用于具体的dict
        :param kwargs:
        """
        self.default_value = default_value
        self.extra = extra


EDV = EnsuredDictValue


class EnsuredDictMeta(type):

    def __init__(cls, name, bases, attrs: Dict):
        super().__init__(name, bases, attrs)
        ENSURED_DICT = {}
        TEMPLATE = {}
        for b in bases:
            if getattr(b, "ENSURED_DICT", {}):
                ENSURED_DICT.update(b.ENSURED_DICT)
        for k, v in attrs.items():
            if isinstance(v, EnsuredDictValue):
                TEMPLATE[k] = v
                if not callable(v.default_value):
                    v = v.default_value
                    if v is not None and not isinstance(v, (str, int, float, tuple)):
                        # be careful of those changeable objects
                        v = copy.deepcopy(v)
                ENSURED_DICT[k] = v
        if not getattr(cls, "TEMPLATE", None):
            cls.TEMPLATE = TEMPLATE
        else:
            cls.TEMPLATE.update(TEMPLATE)
        cls.ENSURED_DICT = ENSURED_DICT


class EnsuredDict(dict, metaclass=EnsuredDictMeta):
    """一个保证字段的字典"""

    # 可变对象是否需要深拷贝
    CHANGEABLE_VALUE_NEED_DEEPCOPY: bool = True

    @classmethod
    def ensured_keys(cls) -> Tuple[str, ...]:
        return tuple(list(cls().keys()))

    def __init__(self, *args, **kwargs):
        super(EnsuredDict, self).__init__(*args, **kwargs)
        for k, v in self.ENSURED_DICT.items():
            if isinstance(v, EnsuredDictValue):
                v = v.default_value
            if callable(v):
                # ony accept callable with no input arguments
                v = v()
            if v is not None and not isinstance(v, (str, int, float, tuple)):
                if self.CHANGEABLE_VALUE_NEED_DEEPCOPY:
                    v = copy.deepcopy(v)
            self[k] = self.get(k, v)

    def to_json(self, *args, **kwargs):
        return json.dumps(self, *args, **kwargs)
