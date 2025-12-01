from playwright.sync_api import Page
from logger import create_logger
from pages.base_page import BasePage


class DoubanTop250Page(BasePage):
    URL = "https://movie.douban.com/top250"

    def __init__(self, page: Page):
        super().__init__(page)


    def goto(self):
        self.page.goto(self.URL)

    def get_movie_titles(self):
        # 每个电影标题的 CSS 选择器
        self.logger.info("获取电影标题列表")
        items = self.page.locator("div.info > div.hd > a > span:nth-child(1)")
        titles = items.all_text_contents()
        self.logger.info(f"共获取到 {len(titles)} 条电影标题")
        return titles
