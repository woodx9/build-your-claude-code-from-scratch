# Chapter 1: Tool Call API Fundamentals

[中文版本](./README_zh.md)

## What You'll Learn

This chapter introduces the fundamentals of tool calling in LLMs through two different approaches:

- **Native Function Call**: OpenAI's standardized JSON Schema approach
- **XML Tool Call**: Flexible XML-based tool calling for any text model

## Key Concepts

### Native Function Call
Structured tool calling using JSON Schema definitions:

```python
tools = [{
    "type": "function",
    "function": {
        "name": "search_gutenberg_books",
        "description": "Search for books in the Project Gutenberg library",
        "parameters": {
            "type": "object",
            "properties": {
                "search_terms": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of search terms to find books"
                }
            },
            "required": ["search_terms"]
        }
    }
}]
```

**Advantages**: Type safety, structured validation, reliable parsing
**Limitations**: Requires function calling support, API-dependent

### XML Tool Call
Natural language tool calling with XML format:

```python
prompt = """
When calling tools, use this format:
<search_gutenberg_books>
  <search_terms>term1</search_terms>
  <search_terms>term2</search_terms>
</search_gutenberg_books>
"""
```

**Advantages**: Universal compatibility, human-readable, flexible
**Limitations**: Manual validation required, parsing complexity

## When to Use Each Approach

| Use Native Function Call | Use XML Tool Call |
|--------------------------|-------------------|
| GPT-4, Claude 3.5+ models | Any text generation model |
| Production applications | Rapid prototyping |
| Type safety required | Combined with explanations |
| Complex tool chains | Simple tool interactions |

## Next Steps

→ **Chapter 2**: Learn to build a complete ReAct agent system using these tool calling foundations.
