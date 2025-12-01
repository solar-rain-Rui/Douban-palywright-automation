from playwright.sync_api import Page

class DoubanTop250Page:
    URL = "https://movie.douban.com/top250"

    def __init__(self, page: Page):
        self.page = page

    def goto(self):
        self.page.goto(self.URL)

    def get_movie_titles(self):
        # 每个电影标题的 CSS 选择器
        title_elements = self.page.locator("div.info > div.hd > a > span:nth-child(1)")
        return title_elements.all_inner_texts()
