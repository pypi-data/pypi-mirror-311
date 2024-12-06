from typing import Any, Dict, Set

from bs4 import Comment, Tag
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
        # logger.debug(f"Removing excluded tag <{tag.name}>")
        tag.decompose()
        return None

    for comment in tag.find_all(string=lambda text: isinstance(text, Comment)):
        # logger.debug("Removing HTML comment")
        comment.extract()

    if tag.name not in {"img", "br", "hr", "input", "meta", "link"} and not tag.contents:
        # logger.debug(f"Removing empty tag <{tag.name}>")
        tag.decompose()
        return None

    while True:
        children = [child for child in tag.contents if isinstance(child, Tag)]
        logger.debug(f"Processing <{tag.name}> with {len(children)} children")
        if len(children) != 1 or not isinstance(children[0], Tag) or children[0].name != "div":
            break

        only_child = children[0]
        # logger.debug(f"Merging <{tag.name}> with its only child <{only_child.name}>")
        tag = merge_parent_with_only_child(tag, only_child)

    for child in list(tag.children):
        if isinstance(child, Tag):
            child = clean_up_beautiful_soup(child, exclude_tags)

            if child is None:
                continue

    return tag


def extract_tag_with_content(tag: Tag | None, attribute: str, pattern: str) -> Tag | None:
    if tag is None:
        return None

    matching_tags = tag.find_all(lambda tag: tag.has_attr(attribute) and pattern in tag[attribute])
    logger.debug(f"Found {len(matching_tags)} tags with {attribute} = {pattern}")

    if not matching_tags:
        return None

    def find_common_ancestor(tags):
        ancestors_lists = [[tag] + list(tag.parents) for tag in tags]

        first_ancestors_list = ancestors_lists[0]
        for ancestor in first_ancestors_list:
            all_tags_in_ancestor = True
            for tag in tags:
                logger.debug(f"Checking if {tag} is in {ancestor}, result: {tag in ancestor.descendants}")
                if tag not in ancestor.descendants:
                    all_tags_in_ancestor = False
                    break

            if all_tags_in_ancestor:
                return ancestor

    common_parent = find_common_ancestor(matching_tags)
    return common_parent


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
