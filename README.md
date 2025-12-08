# **Douban Playwright UI Automation Project**  
  
基于 Python + Playwright 实现豆瓣网 Web UI 自动化测试项目  

Playwright + Pytest + POM + 数据驱动 + 截图与 Trace 调试 + GitHub Actions CI

## 项目功能概述
✔ Page Object Model 设计
✔ Playwright Web UI 自动化
✔ YAML 数据驱动参数化测试
✔ pytest fixture 体系
✔ 自动失败截图 + 调试 trace 采集
✔ GitHub Actions CI 集成

## 技术栈
| 技术                | 作用       |
| ----------------- | -------- |
| Python            | 语言       |
| Playwright        | 浏览器自动化框架 |
| Pytest            | 测试用例框架   |
| Page Object Model | 页面对象抽象   |
| GitHub Actions    | 持续集成运行   |
| Playwright Trace  | 过程录制回放   |

### 功能点
✔ 搜索电影
✔ 验证 UI 展示
✔ 失败自动截图,自动保存 HTML 片段
✔ Trace Viewer 回放执行步骤
✔ GitHub Actions 云端执行
✔ Page Object 设计解耦页面逻辑
✔ 日志记录
✔ 支持基于YAML的参数化测试,实现测试数据与逻辑解耦，提高用例可维护性与可扩展性

#### 项目结构（示例）
```commandline
📦 Douban-playwright-automation
│
├─ 📂pages                           # Page Object 层（页面功能封装）
│   ├─ 📜base_page.py                # 所有页面的基类（封装通用方法）
│   ├─ 📜douban_top250_page.py       # 首页与搜索功能对象封装
│   ├─ 📜movie_detail_page.py        # 电影详情页封装（解析标题等元素）
│   └─ 📜search_result_page.py       # 搜索结果页封装（获取搜索文字）
│
├─ 📂tests                           # UI 自动化测试用例
│   ├─ 📜test_douban_search.py       # 搜索功能验证（数据驱动）
│   ├─ 📜test_douban_detail.py       # 电影详情页验证（验证标题匹配）
│   └─ 📜test_douban.py              # Top250 列表页验证
│
├─ 📂data                            # YAML 数据文件（数据驱动测试）
│   ├─ 📜search_keywords.yaml        # 搜索测试关键字（参数化）
│   └─ 📜detail_cases.yaml           # 详情页验证数据
│
├─ 📂reports                         # Playwright trace / 失败截图 / HTML 报告输出目录
│
├─ 📂screenshots                     # pytest 自动截图存放目录（失败时截图）
│
├─ 📂traces                          # Playwright trace 调试记录（通过 CI/本地收集）
│
├─ 📂.github
│   └─ 📂workflows
│       └─ 📜ui_test.yml             # GitHub Actions CI 配置文件（自动执行 UI 测试）
│
├─ 📜conftest.py                     # Pytest 的全局 fixture（浏览器启动、数据注入）
│
├─ 📜requirements.txt                # 项目依赖管理文件（CI 用 pip install -r requirements）
│
├─ 📜README.md                       # 项目说明文件（支持部署、运行说明等）
│
└─ 📜logger.py      # 工具封装（截图、日志输出、失败调试辅助）

```
##### 执行录制功能说明

项目默认开启 Playwright trace recording：

执行失败时，会保存 trace 文件到 reports/traces/

可本地使用 Playwright Trace Viewer 回放：`playwright show-trace trace.zip`


#### 如何运行测试
1. 本地环境
```commandline
pip install -r requirements.txt
playwright install
pytest -s --headed
```
2. GitHub Actions 自动运行
push 代码后自动执行 UI 测试：

✔ 运行浏览器
✔ 执行测试
✔ 失败自动截图
✔ trace 文件可从 workflow artifacts 下载回放
