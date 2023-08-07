# from typing import Union, Optional, Type, cast, List, Any
#
# from fastapi import Depends, Query
# from fastapi.types import DecoratedCallable
# from starlette.requests import Request
# from starlette.responses import JSONResponse
# from tortoise import Model, Tortoise
# from tortoise.expressions import Q
# from tortoise.queryset import QuerySet
#
# from fastgenerateapi.api_view.base_view import BaseView
# from fastgenerateapi.api_view.mixin.get_mixin import GetMixin
# from fastgenerateapi.controller import SearchController, BaseFilter, FilterController
# from fastgenerateapi.data_type.data_type import DEPENDENCIES
# from fastgenerateapi.deps import paginator_deps, filter_params_deps
# from fastgenerateapi.pydantic_utils.base_model import BaseModel
# from fastgenerateapi.schemas_factory import get_all_schema_factory, get_page_schema_factory, get_one_schema_factory, \
#     response_factory
# from fastgenerateapi.schemas_factory.get_all_schema_factory import get_list_schema_factory
# from fastgenerateapi.settings.register_settings import settings
#
#
# class SQLGetAllView(BaseView, GetMixin):
#
#     connection_name: Optional[str] = "default"
#     table_name: Optional[str] = None
#     sql_get_all_route: Union[bool, DEPENDENCIES] = True
#     sql_get_all_schema: Optional[Type[BaseModel]] = None
#     sql = None
#     include_fields = []
#     exclude_fields = []
#     search_fields: Union[None, list] = None
#     filter_fields: Union[None, list] = None
#     """
#     get_all_route: 获取详情路由开关，可以放依赖函数列表
#     get_all_schema: 返回序列化
#         优先级：
#             - 传入参数
#             - 模型层get_all_include和get_all_exclude(同时存在交集)
#             - get_one_schemas
#     """
#
#     @property
#     def conn(self):
#         return Tortoise.get_connection(self.connection_name)
#
#     async def sql_get_all(self, search: str, filters: dict, paginator, *args, **kwargs) -> Union[BaseModel, dict, None]:
#         new_sql = self.sql or await self.handler_sql(paginator)
#
#         data = await self.conn.execute_query_dict(new_sql)
#
#         data = await self.handler_data(data, paginator)
#         return data
#
#     async def handler_sql(self, paginator):
#         delete_field = settings.app_settings.WHETHER_DELETE_FIELD
#         active_value = 1 if settings.app_settings.ACTIVE_DEFAULT_VALUE else 0
#         where_str = f"WHERE {delete_field} = {active_value}"
#         if getattr(paginator, settings.app_settings.DETERMINE_WHETHER_PAGE_FIELD) == settings.app_settings.DETERMINE_NO_PAGE_VALUE:
#             sql = f"SELECT {','.join(self.fields)} {where_str} FROM {self.table_name}"
#         else:
#             current_num = getattr(paginator, settings.app_settings.CURRENT_PAGE_FIELD)
#             page_size = getattr(paginator, settings.app_settings.PAGE_SIZE_FIELD)
#             sql = f"SELECT {','.join(self.fields)} {where_str} FROM {self.table_name} OFFSET {cast(int, (current_num - 1) * page_size)} LIMIT {page_size}"
#         return sql
#
#     async def handler_data(self, data, paginator, count: int = None, fields: List[Union[str, tuple]] = None,) -> Union[dict, str, None]:
#         if not data:
#             return {}
#         data_list = []
#
#         for model in model_list:
#
#             if fields:
#                 data_list.append(await self.getattr_model(model=model, fields=fields))
#             else:
#                 data_list.append(self.get_all_schema.from_orm(model))
#
#         if not paginator or getattr(paginator, settings.app_settings.DETERMINE_WHETHER_PAGE_FIELD) == settings.app_settings.DETERMINE_NO_PAGE_VALUE:
#             return self.get_list_schema(**{
#                 settings.app_settings.LIST_RESPONSE_FIELD: data_list,
#             })
#         current_num = getattr(paginator, settings.app_settings.CURRENT_PAGE_FIELD)
#         page_size = getattr(paginator, settings.app_settings.PAGE_SIZE_FIELD)
#         count = count or await self.conn.execute_query_dict(self.sql)
#
#         return self.get_page_schema(**{
#             settings.app_settings.CURRENT_PAGE_FIELD: current_num,
#             settings.app_settings.PAGE_SIZE_FIELD: page_size,
#             settings.app_settings.TOTAL_SIZE_FIELD: count,
#             settings.app_settings.LIST_RESPONSE_FIELD: data_list,
#         })
#
#     def sql_get_all_decorator(self, *args: Any, **kwargs: Any) -> DecoratedCallable:
#         async def route(
#                 request: Request,
#                 paginator=Depends(paginator_deps()),
#                 search: str = Query(default="", description="搜索"),
#                 filters: dict = Depends(filter_params_deps(model_class=self.model_class, fields=self.filter_fields)),
#         ) -> JSONResponse:
#             data = await self.sql_get_all(
#                 paginator=paginator,
#                 search=search,
#                 filters=filters,
#                 request=request,
#                 *args,
#                 **kwargs
#             )
#
#             return self.success(data=data)
#         return route
#
#     def _handler_get_all_settings(self):
#         if self.table_name:
#             self.error(msg="table_name 不能为空")
#         def get_base_filter_list(fields: list) -> list:
#             if fields is None:
#                 return []
#             return [BaseFilter(field) if not isinstance(field, BaseFilter) else field for field in fields]
#
#         self.search_controller = SearchController(get_base_filter_list(self.search_fields))
#         self.filter_controller = FilterController(get_base_filter_list(self.filter_fields))
#         self.get_all_schema = self.get_all_schema or get_all_schema_factory(self.model_class) or self.get_one_schema if hasattr(self, "get_one_schema") else get_one_schema_factory(self.model_class)
#         self.get_page_schema = get_page_schema_factory(self.get_all_schema)
#         self.get_list_schema = get_list_schema_factory(self.get_all_schema)
#         self.get_all_response_schema = response_factory(self.get_page_schema, name="GetPage")
#
#         if self.get_all_route:
#             doc = self.get_all.__doc__
#             summary = doc.strip().split("\n")[0] if doc else "Get All"
#             path = f"/{settings.app_settings.ROUTER_GET_ALL_SUFFIX_FIELD}" if settings.app_settings.ROUTER_WHETHER_ADD_SUFFIX else ""
#             self._add_api_route(
#                 path=path,
#                 endpoint=self._get_all_decorator(),
#                 methods=["GET"],
#                 response_model=self.get_all_response_schema,
#                 summary=summary,
#                 dependencies=self.get_all_route,
#             )
#
#
#
#
#
#
#
#
#
#
#
#
