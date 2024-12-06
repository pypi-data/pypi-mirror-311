from typing import Any, Type, Union

from bs4 import BeautifulSoup
from pydantic import BaseModel

from perse import models

default_model = "gpt-4o-mini-2024-07-18"

def reduce_html_content(
    content: Union[str, BeautifulSoup],
    exclude_tags: set[str] | None = None,
) -> BeautifulSoup: ...
def extract_content_tag(
    content: Union[str, BeautifulSoup],
    attribute: str,
    pattern: str,
) -> BeautifulSoup | None: ...
def extract_relevant_fields(
    content: Union[str, BeautifulSoup],
    model: str = default_model,
) -> models.FieldsInfo: ...
def build_pydantic_model(
    fields: list[models.FieldInfo],
) -> Type[BaseModel] | None: ...
def extract_json_fields(
    content: Union[str, BeautifulSoup], PydanticModel: Type[BaseModel], model: str = default_model
) -> dict[str, Any]: ...
