# 第一章：工具调用 API 基础

[English Version](./README.md)

## 本章内容

本章介绍大语言模型中工具调用的基础知识，通过两种不同的方法：

- **原生函数调用**：OpenAI 标准化的 JSON Schema 方法
- **XML 工具调用**：适用于任何文本模型的灵活 XML 工具调用

## 核心概念

### 原生函数调用
使用 JSON Schema 定义的结构化工具调用：

```python
tools = [{
    "type": "function",
    "function": {
        "name": "search_gutenberg_books",
        "description": "在古腾堡计划图书馆中搜索书籍",
        "parameters": {
            "type": "object",
            "properties": {
                "search_terms": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "用于查找书籍的搜索词列表"
                }
            },
            "required": ["search_terms"]
        }
    }
}]
```

**优势**：类型安全、结构化验证、可靠解析
**限制**：需要函数调用支持、依赖特定 API

### XML 工具调用
使用 XML 格式的自然语言工具调用：

```python
prompt = """
调用工具时，请使用以下格式：
<search_gutenberg_books>
  <search_terms>搜索词1</search_terms>
  <search_terms>搜索词2</search_terms>
</search_gutenberg_books>
"""
```

**优势**：通用兼容性、人类可读、灵活性强
**限制**：需要手动验证、解析复杂性

## 使用场景选择

| 使用原生函数调用 | 使用 XML 工具调用 |
|----------------|------------------|
| GPT-4、Claude 3.5+ 模型 | 任何文本生成模型 |
| 生产环境应用 | 快速原型开发 |
| 需要类型安全 | 结合自然语言解释 |
| 复杂工具链 | 简单工具交互 |

## 下一步

→ **第二章**：学习使用这些工具调用基础构建完整的 ReAct 智能体系统。
