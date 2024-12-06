import pytest
from bs4 import BeautifulSoup
from loguru import logger
from pydantic import BaseModel

from perse.utils import (
    clean_up_beautiful_soup,
    extract_tag_with_content,
    format_user_friendly_bytes,
    merge_parent_with_only_child,
    recursive_dump_base_model,
)


@pytest.fixture
def soup_with_multiple_tags():
    html = """
    <div>
        <div class="people">
            <div id="1" class="people">Person 1</div>
            <div id="2" class="people">Person 2</div>
        </div>
        <div class="items">
            <div id="1" class="items">
                <div class="item-detail">
                    <div class="item-name">Item 1</div>
                    <div class="item-price">$10</div>
                </div>
                <div class="item-links-container">
                    <div class="item-links">
                        <div class="item-link">
                            <p>Link 1</p>
                            <a href="https://example.com">Link 1</a>
                        </div>
                        <div class="item-link">
                            <p>Link 2</p>
                            <a href="https://example.com">Link 2</a>
                        </div>
                        <div class="item-link">
                            <p>Link 3</p>
                            <a href="https://example.com">Link 3</a>
                        </div>
                    </div>
                </div>
            </div>
            <div id="2" class="items">
                <div class="item-detail">
                    <div class="item-name">Item 2</div>
                    <div class="item-price">$20</div>
                </div>
            </div>
            <div class="item-detail">
                <div class="item-name">Item 3</div>
                <div class="item-price">$30</div>
            </div>
        </div>
    </div>
    """
    return BeautifulSoup(html, "html.parser")


def test_extract_tag_with_content(soup_with_multiple_tags):
    tag = extract_tag_with_content(soup_with_multiple_tags, "class", "item-price")
    assert tag is not None
    logger.info(tag.prettify())
    assert tag.name == "div"
    assert "people" not in str(tag)
    assert "items" in str(tag)
    assert "Item 1" in str(tag)
    assert "Item 2" in str(tag)
    assert "Item 3" in str(tag)

    tag = extract_tag_with_content(soup_with_multiple_tags, "href", "example.com")
    assert tag is not None
    logger.info(tag.prettify())
    assert tag.name == "div"
    assert "item-links" in str(tag)
    assert "items-links-container" not in str(tag)


@pytest.fixture
def soup_with_empty_tags():
    html = """
    <div class="container">
        <p>Hello</p>
        <div class="empty"></div>
        <div class="content">Hello</div>
        <div class="nested">
            <div class="empty-nested"></div>
            <span class="empty"></span>
        </div>
        <div class="div-with-only-child">
            <div class="child">Content</div>
        </div>
        <a href="https://example.com">
        <img src="test.jpg" alt="test">
    </div>
    """
    return BeautifulSoup(html, "html.parser")


def test_clean_up_beautiful_soup_empty_tags(soup_with_empty_tags):
    reduced_soup = clean_up_beautiful_soup(soup_with_empty_tags.div)
    assert reduced_soup is not None
    logger.info(reduced_soup.prettify())
    assert "empty" not in str(reduced_soup)
    assert "empty-nested" not in str(reduced_soup)
    assert "Hello" in str(reduced_soup)
    assert "div-with-only-child" in str(reduced_soup)
    assert "Content" in str(reduced_soup)
    assert "<123a" not in str(reduced_soup)
    assert "<a" in str(reduced_soup)
    assert "test.jpg" in str(reduced_soup)


@pytest.fixture
def soup_with_nested_empty_divs():
    html = """
    <div id="parent">
        <div id="child-1"></div>
        <div id="child-2"></div>
    </div>
    """
    return BeautifulSoup(html, "html.parser")


def test_clean_up_beautiful_soup_nested_empty_divs(soup_with_nested_empty_divs):
    reduced_soup = clean_up_beautiful_soup(soup_with_nested_empty_divs.div)
    assert reduced_soup is not None
    logger.info(reduced_soup.prettify())
    assert "child-1" not in str(reduced_soup)
    assert "child-2" not in str(reduced_soup)


def test_clean_up_beautiful_soup_exclude_tags():
    html = """
    <div>
        <script>console.log('test')</script>
        <style>.test{color:red}</style>
        <div>Content</div>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    reduced_soup = clean_up_beautiful_soup(soup.div, exclude_tags={"script", "style"})
    assert reduced_soup is not None
    logger.info(reduced_soup.prettify())
    assert "script" not in str(reduced_soup)
    assert "style" not in str(reduced_soup)
    assert "Content" in str(reduced_soup)


def test_clean_up_beautiful_soup_preserve_images():
    html = """
    <div class="container">
        <div class="image-wrapper">
            <img src="test.jpg" alt="test">
        </div>
        <div class="empty"></div>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    reduced_soup = clean_up_beautiful_soup(soup.div)
    assert reduced_soup is not None
    logger.info(reduced_soup.prettify())
    assert "img" in str(reduced_soup)
    assert "test.jpg" in str(reduced_soup)
    assert "empty" not in str(reduced_soup)


def test_merge_parent_with_only_child():
    html = """
    <div class="parent" id="parent-id">
        <div class="child" id="child-id">Content</div>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    parent = soup.div
    child = parent.div
    assert parent is not None
    assert child is not None
    result = merge_parent_with_only_child(parent, child)
    assert result["class"] == ["parent", "child"]
    assert result["id"] == "parent-id"
    assert result.string == "Content"


def test_clean_up_beautiful_soup_remove_comments():
    html = """
    <div>
        <!-- Comment 1 -->
        <p>Hello</p>
        <!-- Comment 2 -->
        <div>Content</div>
        <!-- Nested -->
        <div>
            <!-- Inner comment -->
            <span>Text</span>
        </div>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    reduced_soup = clean_up_beautiful_soup(soup.div)
    assert reduced_soup is not None
    logger.info(reduced_soup.prettify())
    assert "Comment 1" not in str(reduced_soup)
    assert "Comment 2" not in str(reduced_soup)
    assert "Nested" not in str(reduced_soup)
    assert "Inner comment" not in str(reduced_soup)
    assert "Hello" in str(reduced_soup)
    assert "Content" in str(reduced_soup)
    assert "Text" in str(reduced_soup)


def test_recursive_dump_base_model():
    class NestedModel(BaseModel):
        value: str

    class TestModel(BaseModel):
        name: str
        nested: NestedModel
        items: list[str]

    model = TestModel(name="test", nested=NestedModel(value="nested"), items=["a", "b"])
    result = recursive_dump_base_model(model)
    assert result == {"name": "test", "nested": {"value": "nested"}, "items": ["a", "b"]}


def test_format_user_friendly_bytes():
    assert format_user_friendly_bytes(500) == "500 B"
    assert format_user_friendly_bytes(1500) == "1.46 KB"
    assert format_user_friendly_bytes(1500000) == "1.43 MB"
    assert format_user_friendly_bytes(1500000000) == "1.40 GB"
