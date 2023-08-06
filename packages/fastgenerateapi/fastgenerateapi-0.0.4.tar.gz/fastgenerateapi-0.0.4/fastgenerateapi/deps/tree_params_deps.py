from typing import Type, Any, Optional

from fastapi import Depends
from pydantic.fields import FieldInfo

from fastgenerateapi.settings.register_settings import settings

from fastgenerateapi.pydantic_utils.base_model import QueryConfig
from pydantic import BaseModel, create_model


def tree_params_deps():
    """
        生成 tree 开始筛选字段的依赖
    """
    filter_tree_params_model: Type[BaseModel] = create_model(
        __model_name="TreeFilterParams", **{
            settings.app_settings.DEFAULT_TREE_FILTER_FIELD: (Optional[str], FieldInfo(default=None, description="起始节点ID"))
        },  __config__=QueryConfig)

    def filter_query(filter_params: filter_tree_params_model = Depends(filter_tree_params_model)) -> dict[str, Any]:
        """
            filter 筛选字段依赖
        :param filter_params:
        :return:
        """
        result = getattr(filter_params, settings.app_settings.DEFAULT_TREE_FILTER_FIELD, None)

        return result or None

    return filter_query


