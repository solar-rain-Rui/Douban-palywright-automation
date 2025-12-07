import pytest
import os
from pages.douban_page import DoubanTop250Page
from pages.movie_detail_page import MovieDetailPage
from common.data_loader import load_yaml

# 1. 加载 YAML
yaml_path = os.path.join(os.path.dirname(__file__), "data", "movie_detail.yaml")
cases = load_yaml(yaml_path)["detail_cases"]


@pytest.mark.parametrize("case", cases)
def test_movie_detail(page, case):
    """
    验证搜索 → 点击详情 → 页面信息
    """
    keyword = case["title"]
    douban = DoubanTop250Page(page)
    detail = MovieDetailPage(page)

    # 1. 打开首页
    douban.goto()
    douban.wait_for_load()

    # 2. 搜索电影
    results = douban.search(keyword)
    assert len(results) > 0, f"搜索 {keyword} 结果为空"

    # 3. 点击第一个搜索结果
    douban.click_first_movie_result()

    # 4. 详情页加载
    detail.wait_loaded()

    # 5. 验证标题存在
    title = detail.get_movie_title()
    assert title, "详情页标题不存在"

    rating = detail.get_movie_rating()
    assert rating, "评分不存在"

    intro = detail.get_intro_text()
    assert intro, "简介内容不存在"

    print(f"{keyword} 详情页标题：", title)
