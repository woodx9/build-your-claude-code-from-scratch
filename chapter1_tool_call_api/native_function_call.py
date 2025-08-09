from openai import OpenAI
import json, requests

OPENROUTER_API_KEY = "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"
MODEL = "anthropic/claude-sonnet-4"

# 初始化客户端
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=OPENROUTER_API_KEY
)

messages = [
  {"role": "system", "content": "You are a helpful assistant."},
  {"role": "user", "content": "What are the titles of some James Joyce books?"}
]

# 定义工具接口 Schema
tools = [
  {
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
  }
]

# 向模型发起首次请求
request_1 = {
  "model": MODEL,
  "messages": messages,
  "tools": tools
}

response_1 = client.chat.completions.create(**request_1).choices[0].message
print("response_1:", response_1)
# OUTPUT
# response_1: ChatCompletionMessage(content="I'll search for books by James Joyce in the Project Gutenberg library.", 
#                                   refusal=None, 
#                                   role='assistant', 
#                                   annotations=None, 
#                                   audio=None, 
#                                   function_call=None, 
#                                   tool_calls=[ChatCompletionMessageFunctionToolCall(id='toolu_vrtx_01KZS8hVMefmiWfjAQKGXdZJ', 
#                                                                                     function=Function(arguments='{"search_terms": ["James Joyce"]}', 
#                                                                                                       name='search_gutenberg_books'), 
#                                                                                                       type='function', 
#                                                                                                       index=0)], 
#                                                                                                       reasoning=None)



# 以下伪函数示范对 Project Gutenberg 的查询实现
def search_gutenberg_books(search_terms):
    search_query = " ".join(search_terms)
    resp = requests.get("https://gutendex.com/books", params={"search": search_query})
    results = []
    for book in resp.json().get("results", []):
        results.append({
            "id": book.get("id"),
            "title": book.get("title"),
            "authors": book.get("authors")
        })
    return results

# 处理 LLM 返回的工具调用请求
messages.append(response_1)
for tool_call in response_1.tool_calls:
    args = json.loads(tool_call.function.arguments)
    tool_result = search_gutenberg_books(**args)
    messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "name": tool_call.function.name,
        "content": json.dumps(tool_result)
    })

request_2 = {
  "model": MODEL,
  "messages": messages,
  "tools": tools
}
response_2 = client.chat.completions.create(**request_2)
print(response_2.choices[0].message)
# ChatCompletionMessage(content='Based on the search results from Project Gutenberg, here are some of James Joyce\'s notable book titles:\n\n1. **Ulysses** - His most famous and complex novel\n2. **Dubliners** - A collection of short stories about life in Dublin\n3. **A Portrait of the Artist as a Young Man** - A semi-autobiographical novel\n4. **Chamber Music** - A collection of poems\n5. **Exiles: A Play in Three Acts** - A theatrical work\n\nThese represent some of Joyce\'s major works available in the Project Gutenberg digital library. Joyce is considered one of the most important modernist writers, with "Ulysses" being particularly renowned as a masterpiece of 20th-century literature.', 
#                       refusal=None, 
#                       role='assistant', 
#                       annotations=None, 
#                       audio=None, 
#                       function_call=None, 
#                       tool_calls=None, 
#                       reasoning=None)

