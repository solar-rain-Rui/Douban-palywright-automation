from playwright.sync_api import Page
from pages.douban_page import DoubanTop250Page
import pytest

@pytest.mark.parametrize("keyword", [
    "肖申克",
    "霸王别姬",
    "狮子王"
])
def test_douban_search(page,keyword):
    """验证搜索功能"""

    douban = DoubanTop250Page(page)

    douban.goto()
    douban.wait_for_load()

    douban.search(keyword)

    results = douban.get_results()

    assert len(results) > 0, f"搜索 {keyword} 结果为空"

    print("搜索结果前 3 条：", results[:3])
