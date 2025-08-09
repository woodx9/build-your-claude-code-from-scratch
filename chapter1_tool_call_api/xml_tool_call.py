from openai import OpenAI
import requests
import xml.etree.ElementTree as ET
import re

OPENROUTER_API_KEY = "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"  
MODEL = "anthropic/claude-sonnet-4"

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)


tool = """
[Some natural language explanation for the user]
<search_gutenberg_books>
  <search_terms>term1</search_terms>
  <search_terms>term2</search_terms>
  ...
</search_gutenberg_books>
"""

prompt = f"""
You are a helpful assistant.
When you decide to call a tool, output in this format:

{tool}

Rules:
1. The <search_gutenberg_books> block must be valid XML.
2. The explanation can be any helpful text for the user, but outside the XML tags.
3. Keep XML block on separate lines, do not nest other tags inside.

User request: What are the titles of some James Joyce books?
"""

messages = [ 
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": prompt}
    ]

# 第一次调用模型，获取自然语言 + XML 工具调用
resp_1 = client.chat.completions.create(
    model=MODEL,
    messages=messages,
)

model_text = resp_1.choices[0].message.content
print("模型原始输出:\n", model_text)
# OUTPUT
#  I'll search for books by James Joyce in the Project Gutenberg collection to find his available titles.

# <search_gutenberg_books>
#   <search_terms>James Joyce</search_terms>
# </search_gutenberg_books>

# 用正则提取 <search_gutenberg_books>...</search_gutenberg_books>
xml_match = re.search(r"<search_gutenberg_books>[\s\S]*?</search_gutenberg_books>", model_text)
if not xml_match:
    raise ValueError("未找到 <search_gutenberg_books> 标签")

xml_str = xml_match.group(0)
# OUTPUT
# <search_gutenberg_books>
#   <search_terms>James Joyce</search_terms>
# </search_gutenberg_books>

explanation = model_text.replace(xml_str, "").strip()
# OUTPUT
# I'll search for books by James Joyce in the Project Gutenberg collection to find his available titles.

# 解析 XML 里的参数
root = ET.fromstring(xml_str)
search_terms = [elem.text for elem in root.findall("search_terms")]

# 工具实现
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

# 调用工具
tool_result = search_gutenberg_books(search_terms)

# 第二次调用，把结果交给模型
follow_up = f"""
Here is the JSON result from the tool call:

{tool_result}

Please summarize these books for the user in a friendly tone.
"""

messages.append({
    "role": "user",
    "content": follow_up
})
resp_2 = client.chat.completions.create(
    model=MODEL,
    messages=messages
)

print("\n最终用户可见回答:\n", resp_2.choices[0].message.content)
#  I found several James Joyce books available in the Project Gutenberg collection! Here are the titles:

# **Major Works:**
# - **Ulysses** - Joyce's masterpiece and one of the most important novels of the 20th century
# - **A Portrait of the Artist as a Young Man** - A semi-autobiographical novel following Stephen Dedalus
# - **Dubliners** - A collection of short stories depicting life in Dublin (appears twice in different editions)

# **Other Works:**
# - **Chamber Music** - A collection of Joyce's early poetry (also appears in multiple editions)
# - **Exiles: A Play in Three Acts** - Joyce's only surviving play
# - **Index of the Project Gutenberg Works of James Joyce** - A helpful reference guide to his available works

# These represent some of Joyce's most significant contributions to literature, from his early poetry and short stories to his groundbreaking modernist novels. Ulysses, in particular, is considered one of the greatest novels ever written, though it's known for being quite challenging to read!