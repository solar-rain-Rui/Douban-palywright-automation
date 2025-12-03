import re
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
from logger import create_logger
from pages.base_page import BasePage


class DoubanTop250Page(BasePage):
    URL = "https://movie.douban.com/top250"

    def __init__(self, page: Page):
        super().__init__(page)

    def goto(self):
        """
        打开页面并等待关键元素加载（最多等待 10s）。
        如果被重定向到 sec.douban.com，会截图并记录 page.content() 以便排查。
        """
        self.logger.info(f"打开豆瓣 Top250：{self.URL}")
        self.page.goto(self.URL)

        # 等待列表项出现（这是判断页面加载成功的关键）
        try:
            # 列表项的外层 class 通常是 div.item
            self.page.locator("div.item").first.wait_for(state="visible", timeout=10000)
            self.logger.info("豆瓣 Top250 列表项已出现")
        except PlaywrightTimeoutError:
            self.debug_failure("top250_timeout")
            raise

    def get_movie_titles(self):
        """
        返回当前页的所有电影标题（文本列表）。
        Selector 选择了 span.title（更稳定），并使用 BasePage.get_texts 封装。
        """
        # 更稳健的 selector：豆瓣电影标题在 <span class="title"> 内
        sel = "div.item div.info div.hd a span.title"
        self.logger.info(f"开始获取电影标题，selector: {sel}")
        titles = self.get_texts(sel)  # 依赖 BasePage.get_texts()
        self.logger.info(f"实际获取到 {len(titles)} 条标题")
        return titles
    #搜索
    def search(self, keyword: str):
        self.logger.info(f"执行搜索：{keyword}")
        search_input = self.locator("#inp-query")
        search_input.fill(keyword)

        # 点击搜索按钮
        self.locator(".inp-btn").click()

        # 等待结果出现
        self.wait_visible(".item")  # 搜索结果条目


