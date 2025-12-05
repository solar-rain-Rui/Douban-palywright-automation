from pages.base_page import BasePage


class SearchResultPage(BasePage):

    def wait_loaded(self, timeout: int = 15000):#用来确保至少一个结果出现
        """
        等待搜索结果页面加载至少一个结果
        """
        try:
            self.page.wait_for_selector("a,span", timeout=timeout)
        except Exception:
            self.debug_failure("search_result_wait_fail")
            raise

    def get_results(self):
        """
        返回搜索结果文本列表
        """
        return self.batch_text("a,span")

    def first_result_text(self):
        """
        返回第一个搜索结果文本（没有结果返回 None）
        """
        results = self.get_results()
        return results[0] if results else None
