from typing import Union, Dict, List
from .base import BaseService
from ..model.callback import Callback
from ..model.param import TextParam


def _params_convert(task_params: Union[str, Dict, TextParam]):
    # 单个
    if isinstance(task_params, TextParam):
        return task_params.dict()
    elif isinstance(task_params, str):
        return {'text': task_params}

    return task_params


class NamedEntityExtractService(BaseService):
    """品牌、型号、通用名"""

    def extract_sku(self, task_params: Union[str, Dict, TextParam] = None, callback: Callback = None, **kwargs):
        return self.get_client().apply(task_name='named_entity.sku', task_params=_params_convert(task_params), callback=callback, **kwargs)
