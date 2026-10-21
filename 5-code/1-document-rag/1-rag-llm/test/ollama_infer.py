from ollama import chat
from input_text import input_text

response = chat(
  model='gpt-oss:20b',
  messages=[{'role': 'user', 'content': input_text}],
  think=True,
  stream=False,
)


with open("gpt_20_message.md", "w", encoding='utf-8') as f:
    f.write(response.message.content)

with open("gpt_20_thinkinh.md", "w", encoding='utf-8') as f:
    f.write(response.message.thinking)


# print('Thinking:\n', response.message.thinking)
# print('Answer:\n', response.message.content)