from typing import Generic, List, TypeVar
from pydantic import BaseModel, conint
from pydantic.generics import GenericModel


class PageParams(BaseModel):
    page: conint(ge=1) = 1
    size: conint(ge=1, le=100) = 10
    order_by: str = ""
    asc: bool = True


T = TypeVar("T")


class PagedResponse(GenericModel, Generic[T]):
    total: int
    page: int
    size: int
    results: List[T]
