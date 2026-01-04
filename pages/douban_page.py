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
        super().goto(self.URL)

        # 等待列表项出现（这是判断页面加载成功的关键）
        try:
            # 列表项的外层 class 通常是 div.item
            self.page.locator("div.item").first.wait_for(state="visible", timeout=30000)
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
    def search(self, keyword: str, timeout: int = 15000):
        self.logger.info(f"执行搜索：{keyword}")

        try:
            search_url = f"https://search.douban.com/movie/subject_search?search_text={keyword}&cat=1002"
            self.page.goto(search_url)

            # 等 URL 变成搜索页
            self.page.wait_for_url(lambda url: "subject_search" in url, timeout=timeout)

            # 结果容器稳一点
            self.page.locator("div.item-root, div.result, .resul").first.wait_for(state="visible", timeout=timeout)

            self.logger.info("搜索结果已出现")
            # ← 这一句是关键：返回标题列表，否则调用它的人拿到 None
            return self.batch_text("div.detail a, div.result a, .item-root a, .title a")
        except Exception as e:
            self.logger.error(f"搜索失败：{repr(e)}")
            self.debug_failure("search_fail")
            raise

    def search_by_input(self, keyword: str):
        """
        通过页面搜索框执行搜索（语义化定位示例）
        """
        self.logger.info(f"通过搜索框搜索：{keyword}")

        search_input = self.page.get_by_placeholder("搜索")
        search_input.fill(keyword)

        search_button = self.page.get_by_role("button", name="搜索")
        search_button.click()

    def get_results(self):
        """
        返回搜索结果标题列表
        """
        try:
            # 改成匹配搜索页结构
            results = self.batch_text("div.detail a")
            self.logger.info(f"共提取到 {len(results)} 条结果")
            return results
        except Exception as e:
            self.logger.error("提取搜索结果失败：" + repr(e))
            return []

    def click_first_movie_result(self):
        """
        点击第一个搜索结果，等它可见，跳转到详情页
        """
        self.logger.info("点击第一个搜索结果进入详情页")

        first_item = self.page.locator("div.item-root a, div.result a, .item-root a, .title a").first
        first_item.wait_for(state="visible", timeout=8000)
        first_item.click()



