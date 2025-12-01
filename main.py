from playwright.sync_api import sync_playwright
from pages.douban_top250_page import DoubanTop250Page

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        douban = DoubanTop250Page(page)
        douban.goto()

        titles = douban.get_movie_titles()
        print("获取到电影数量：", len(titles))
        print("前 5 个标题：", titles[:5])

        browser.close()

if __name__ == "__main__":
    main()
