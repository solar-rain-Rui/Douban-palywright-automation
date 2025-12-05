from pages.base_page import BasePage

class MovieDetailPage(BasePage):

    def wait_loaded(self, timeout: int = 15000):
        """
        等待详情页主内容出现
        """
        try:
            self.page.wait_for_selector("#content", timeout=timeout)
        except Exception:
            self.debug_failure("movie_detail_wait_fail")
            raise

    def get_movie_title(self):
        """
        获取影片标题
        """
        titles = self.batch_text("h1")
        return titles[0] if titles else ""

    def get_rating(self):
        """
        获取评分（示例，用于扩展）
        """
        rating = self.batch_text(".rating_num")
        return rating[0] if rating else None
