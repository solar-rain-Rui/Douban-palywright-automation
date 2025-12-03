import os
from datetime import datetime
from playwright.sync_api import Page
from logger import create_logger
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
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

    def click(self, selector):
        """点击功能"""
        self.logger.info(f"点击元素：{selector}")
        self.page.locator(selector).click()

    def fill(self, selector, text):
        """输入文本"""
        self.logger.info(f"输入 [{text}] 到元素：{selector}")
        self.page.locator(selector).fill(text)

    def get_text(self, selector):
        """获取单个元素文本"""
        self.logger.info(f"获取元素文本：{selector}")
        return self.page.locator(selector).inner_text()

    def get_texts(self, selector):
        """获取多个元素文本（重要用于列表）"""
        self.logger.info(f"批量获取文本：{selector}")
        return self.page.locator(selector).all_text_contents()

    def screenshot(self, name="screenshot"):
        """自动存到 reports文件夹，文件名带时间戳"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # 确保目录存在
        report_dir = os.path.join(os.getcwd(), "reports")
        os.makedirs(report_dir, exist_ok=True)

        file_path = os.path.join(report_dir, f"{name}_{timestamp}.png")

        self.page.screenshot(path=file_path)
        self.logger.info(f"截图保存：{file_path}")
        return file_path

    def debug_failure(self, name="debug"):
        self.logger.error("页面异常，保存调试信息")
        try:
            self.screenshot(f"{name}.png")
        except:
            pass
        try:
            content = self.page.content()[:5000]
            self.logger.error("页面HTML片段:\n" + content)
        except:
            self.logger.exception("获取 page.content 失败")

    def wait_visible(self, selector, timeout=5000):
        """
        等元素可见
        """
        self.logger.info(f"等待元素可见: {selector}")
        try:
            self.page.locator(selector).wait_for(state="visible", timeout=timeout)
        except PlaywrightTimeoutError:
            self.logger.error(f"等待元素超时: {selector}")
            self.page.screenshot(path="debug_wait_visible.png")
            raise

    def wait_loaded(self, timeout=5000):
        """
        等待页面加载完成（document.readyState=='complete'）
        """
        self.logger.info("等待页面加载完成")
        self.page.wait_for_load_state("load", timeout=timeout)

