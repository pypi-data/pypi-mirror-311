from typing import Any, Dict, Set

from bs4 import Tag
from loguru import logger
from pydantic import BaseModel


def merge_parent_with_only_child(parent: Tag, child: Tag) -> Tag:
    child.attrs["id"] = child.get("id") if not parent.get("id") and child.get("id") else parent.get("id")
    child.attrs["class"] = parent.get("class", []) + child.get("class", [])
    parent.replace_with(child)
    return child


def clean_up_beautiful_soup(tag: Tag | None, exclude_tags: Set[str] | None = None) -> Tag | None:
    if tag is None:
        return None

    if exclude_tags and tag.name in exclude_tags:
        logger.debug(f"Removing excluded tag <{tag.name}>")
        tag.decompose()
        return None

    if tag.name not in {"img", "br", "hr", "input", "meta", "link"} and not tag.contents:
        logger.debug(f"Removing empty tag <{tag.name}>")
        tag.decompose()
        return None

    while True:
        children = [child for child in tag.contents if isinstance(child, Tag)]
        logger.debug(f"Processing <{tag.name}> with {len(children)} children")
        if len(children) != 1 or not isinstance(children[0], Tag) or children[0].name != "div":
            break

        only_child = children[0]
        logger.debug(f"Merging <{tag.name}> with its only child <{only_child.name}>")
        tag = merge_parent_with_only_child(tag, only_child)

    for child in list(tag.children):
        if isinstance(child, Tag):
            child = clean_up_beautiful_soup(child, exclude_tags)

            if child is None:
                continue

    return tag


def recursive_dump_base_model(model: BaseModel) -> Dict[str, Any]:
    """
    Recursively dumps a Pydantic model into a dictionary.

    Args:
        model (BaseModel): The Pydantic model to dump.

    Returns:
        Dict[str, Any]: The dumped dictionary.
    """

    def _dump(obj: Any) -> Any:
        if isinstance(obj, BaseModel):
            return {k: _dump(v) for k, v in obj.model_dump().items()}
        elif isinstance(obj, list):
            return [_dump(item) for item in obj]
        elif isinstance(obj, dict):
            return {k: _dump(v) for k, v in obj.items()}
        else:
            return obj

    return _dump(model)


def format_user_friendly_bytes(bytes: int) -> str:
    """
    Formats a byte count into a human-readable string.

    Args:
        bytes (int): The byte count to format.

    Returns:
        str: The formatted byte count.
    """
    if bytes < 1024:
        return f"{bytes} B"
    elif bytes < 1024 * 1024:
        return f"{bytes / 1024:.2f} KB"
    elif bytes < 1024 * 1024 * 1024:
        return f"{bytes / 1024 / 1024:.2f} MB"
    else:
        return f"{bytes / 1024 / 1024 / 1024:.2f} GB"
