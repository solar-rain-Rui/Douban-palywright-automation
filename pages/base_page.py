# pages/base_page.py
import os
from datetime import datetime
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
from logger import create_logger


class BasePage:
    """页面基类：封装常用操作、等待、截图、批量文本获取等"""

    def __init__(self, page: Page):
        self.page = page
        self.logger = create_logger()

    # ----- 页面基础 -----
    def goto(self, url: str):
        self.logger.info(f"打开页面：{url}")
        self.page.goto(url)

    def get_title(self) -> str:
        return self.page.title()

    # ----- 定位 + 操作 -----
    def locator(self, selector: str):
        self.logger.info(f"定位元素：{selector}")
        return self.page.locator(selector)

    def click(self, selector: str, timeout: int = 5000):
        self.logger.info(f"点击元素：{selector}")
        try:
            self.wait_visible(selector, timeout=timeout)
            self.page.locator(selector).click()
        except PlaywrightTimeoutError:
            self.logger.exception(f"点击前等待元素超时：{selector}")
            raise

    def fill(self, selector: str, text: str, timeout: int = 5000):
        self.logger.info(f"输入文本到元素：{selector} -> {text}")
        try:
            self.wait_visible(selector, timeout=timeout)
            self.page.locator(selector).fill(text)
        except PlaywrightTimeoutError:
            self.logger.exception(f"填充前等待元素超时：{selector}")
            raise

    # ----- 等待 -----
    def wait_visible(self, selector: str, timeout: int = 8000):
        """等待元素可见"""
        self.logger.info(f"等待元素可见: {selector}")
        try:
            self.page.locator(selector).wait_for(state="visible", timeout=timeout)
        except PlaywrightTimeoutError:
            self.logger.error(f"等待元素可见超时: {selector}")
            self.debug_failure(f"wait_visible_{self._safe_name(selector)}")
            raise

    def wait_for_load(self, timeout: int = 10000):
        """等待页面 load 完成"""
        self.logger.info("等待页面 load 完成")
        try:
            self.page.wait_for_load_state("load", timeout=timeout)
        except PlaywrightTimeoutError:
            self.logger.error("等待页面 load 超时")
            self.debug_failure("wait_for_load")
            raise

    # ----- 批量文本获取（batch_text 的实现） -----
    def get_texts(self, selector: str):
        """
        批量获取元素文本，返回 list[str]。
        这是我们实现的 batch_text（别名兼容）。
        """
        self.logger.info(f"批量获取文本：{selector}")
        try:
            # 等待至少有一个匹配项出现（短超时）
            self.page.locator(selector).first.wait_for(state="visible", timeout=5000)
        except PlaywrightTimeoutError:
            self.logger.warning(f"批量获取文本等待可见超时（可能无结果）：{selector}")
            # 不立刻 raise，返回空列表；调用方可断言
            return []

        # all_text_contents() 会返回元素文本数组（包括文本和子元素文本）
        try:
            texts = self.page.locator(selector).all_text_contents()
            # 清洗：去掉纯空白项并 strip
            texts = [t.strip() for t in texts if t and t.strip()]
            return texts
        except Exception as e:
            self.logger.exception(f"批量获取文本失败: {selector} -> {e}")
            self.debug_failure(f"get_texts_{self._safe_name(selector)}")
            raise

    # 兼容不同命名的别名
    batch_text = get_texts
    get_text_list = get_texts

    # ----- 截图与调试 -----
    def screenshot(self, name: str = "screenshot") -> str:
        report_dir = os.path.join(os.getcwd(), "reports")
        os.makedirs(report_dir, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(report_dir, f"{name}_{ts}.png")
        try:
            self.page.screenshot(path=path)
            self.logger.info(f"截图保存：{path}")
        except Exception:
            self.logger.exception("截图失败")
        return path

    def debug_failure(self, name: str = "debug"):
        """失败时统一调试产物：截图 + 保存 page.content() 小片段"""
        try:
            img = self.screenshot(name)
        except Exception:
            img = None
        try:
            content = self.page.content()[:5000]
            self.logger.error("页面 HTML 片段（前5k）：\n" + content)
        except Exception:
            self.logger.exception("获取页面 HTML 失败")
        return img




