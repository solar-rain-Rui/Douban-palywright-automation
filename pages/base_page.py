from playwright.sync_api import Page


class BasePage:
    """所有页面的基类，封装通用方法"""

    def __init__(self, page: Page):
        self.page = page

    def goto(self, url: str):
        """打开指定 URL"""
        self.page.goto(url)

    def get_title(self) -> str:
        """获取当前页面标题"""
        return self.page.title()

    def screenshot(self, path: str):
        """截图"""
        self.page.screenshot(path=path)
