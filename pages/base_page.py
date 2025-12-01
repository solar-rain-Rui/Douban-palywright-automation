from playwright.sync_api import Page
from logger import create_logger

class BasePage:
    """所有页面的基类，封装通用方法"""

    def __init__(self, page: Page):
        self.page = page
        self.logger = create_logger()  # 加载日志

    def goto(self, url: str):
        """打开指定 URL"""
        self.logger.info(f"打开页面：{url}")
        self.page.goto(url)

    def get_title(self) -> str:
        """获取当前页面标题"""
        return self.page.title()

    def locator(self, selector):
        self.logger.info(f"定位元素：{selector}")
        return self.page.locator(selector)

    def screenshot(self, path: str):
        """截图"""
        self.page.screenshot(path=path)
