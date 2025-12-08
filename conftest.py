import pytest
import pytest_html
import os
from pages.douban_page import DoubanTop250Page

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call): #item:测试项对象 call:测试调用的上下文（setup、call、teardown）
    outcome = yield #接收返回结果
    report = outcome.get_result()#拿到测试结果，report是一个对象，里面有用例信息

    # 失败时自动截图
    if report.failed and "page" in item.funcargs:
        page = item.funcargs["page"]
        #截图保存
        screenshot_path = f"screenshots/{item.name}.png"
        page.screenshot(path=screenshot_path)

        # 3️⃣ 页面 HTML dump 保存
        html_path = f"screenshots/{item.name}.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(page.content())

        # 4️⃣ 注入报告
        report.extra = getattr(report, "extra", [])
        report.extra.append(pytest_html.extras.image(screenshot_path))
        report.extra.append(pytest_html.extras.text(f"DOM Snapshot saved: {html_path}"))

        # 追加 trace 下载链接
        trace_file = f"traces/{item.name}.zip"
        if os.path.exists(trace_file):
            report.extra.append(pytest_html.extras.url(trace_file, name="trace"))

@pytest.fixture
def douban(page):
    """提供 Douban 页面对象，支持依赖注入"""
    douban_page = DoubanTop250Page(page)

    return douban_page

@pytest.fixture(autouse=True)
def record_trace(page, request):
    """
    自动录制 Playwright trace：
    每个测试前开始录制，结束时保存 trace.zip
    """
    # 开始录制 trace
    page.context.tracing.start(
        screenshots=True,
        snapshots=True,
        sources=True
    )

    yield  # 执行测试主体

    # 测试完成后保存 trace 文件
    test_name = request.node.name  # 取测试函数名
    trace_dir = "traces/"
    os.makedirs(trace_dir, exist_ok=True)
    trace_path = os.path.join(trace_dir, f"{test_name}.zip")

    page.context.tracing.stop(path=trace_path)
    print(f"[TRACE] saved → {trace_path}")