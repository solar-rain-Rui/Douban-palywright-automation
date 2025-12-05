import pytest
from playwright.sync_api import Page
from pages.douban_page import  DoubanTop250Page


def test_douban_top250_titles(douban):
    """
    验证：豆瓣 Top250 页面电影标题是否加载成功
    """
    #douban = DoubanTop250Page(page)
    douban.goto()

    titles = douban.get_movie_titles()

    # 断言至少有 1 条电影标题
    print("实际抓取到数量：", len(titles))
    assert len(titles) > 0
    douban.screenshot("douban_top250")
    # 打印前 5 条标题（测试日志里能看到）
    print("\n前 5 条电影：")
    for t in titles[:5]:
        print(t)
