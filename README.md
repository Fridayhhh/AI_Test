# AI 驱动的接口自动化测试工具

## 项目简介
使用 Python 调用大模型 API，通过 Prompt 工程自动生成接口测试用例，
并自动执行用例、断言状态码与响应体字段，输出测试报告。

## 功能
- AI 自动生成覆盖正常、异常、边界的测试用例
- 支持多接口批量测试（/posts、/comments、/users）
- 双重断言：HTTP 状态码 + 响应体字段完整性
- 输出汇总测试报告

## 技术栈
- Python 3
- requests（发 HTTP 请求）
- OpenAI SDK（调用大模型）
- JSON（用例数据格式）

## 运行方式
1. 安装依赖：`pip install requests openai`
2. 在代码中填入你的 API Key
3. 运行：`python ai_test.py`

## 运行结果
<img width="720" height="767" alt="image" src="https://github.com/user-attachments/assets/dba65b04-e63c-4982-b4cc-b6fb6b619f1f" />

