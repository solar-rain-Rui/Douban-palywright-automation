import pytest
import pytest_html


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call): #item:测试项对象 call:测试调用的上下文（setup、call、teardown）
    outcome = yield #接收返回结果
    report = outcome.get_result()#拿到测试结果，report是一个对象，里面有用例信息

    # 失败时自动截图
    if report.failed and "page" in item.funcargs:
        page = item.funcargs["page"]
        screenshot_path = f"screenshots/{item.name}.png"
        page.screenshot(path=screenshot_path)

        if screenshot_path:
            report.extra = getattr(report, "extra", [])
            report.extra.append(pytest_html.extras.image(screenshot_path))
