# 百度文心一言聊天API简单封装
这是一个针对百度文心一言api的简单封装，主要是针对
ErnieBot请求地址：https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions
ErnieBot-turbo请求地址： https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant
的简单封装

# 安装
使用pip进行安装
```
pip install erniechatbotsdk
```

## 请求示例
```python
from erniebotchat import Erniebot

json_str='{"messages": [{"role": "user", "content": "介绍一下自已"}]}'
if __name__ == '__main__':

    enrniebot = Erniebot("apikey","secretkey")
    resp = enrniebot.chat(json_str,"erniebot")
    print(resp)

```

# 输出示例
```
{
  "id": "as-bcmt5ct4iy",
  "object": "chat.completion",
  "created": 1680167072,
  "result": "您好，我是百度研发的知识增强大语言模型，中文名是文心一言，英文名是ERNIE Bot。我能够与人对话互动，回答问题，协助创作，高效便捷地帮助人们获取信息、知识和灵感。",
  "need_clear_history": false,
  "usage": {
    "prompt_tokens": 7,
    "completion_tokens": 67,
    "total_tokens": 74
  }
}
```

