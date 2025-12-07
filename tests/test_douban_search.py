from playwright.sync_api import Page
from pages.douban_page import DoubanTop250Page
from common.data_loader import load_yaml
import pytest
import os

# 读取 YAML 数据
yaml_path = os.path.join(os.path.dirname(__file__), "data", "search_keywords.yaml")
cases = load_yaml(yaml_path)["search_cases"]


@pytest.mark.parametrize("case", cases)
def test_douban_search(page,case,douban):
    """验证搜索功能"""
    keyword = case["name"]
    expected_keywords = case["expected_keywords"]
    #douban = DoubanTop250Page(page)

    douban.goto()
    douban.wait_for_load()
    douban.search(keyword)

    results = douban.get_results()
    #断言1：搜索结果不为空
    assert len(results) > 0, f"搜索 {keyword} 结果为空"
    # 断言 2：结果至少包含 YAML 中的期望关键字
    assert any(
        any(exp in r for exp in expected_keywords)
        for r in results
    ), f"搜索 {keyword} 结果中未出现期望内容：{expected_keywords}"


    print("搜索结果前 3 条：", results[:3])
