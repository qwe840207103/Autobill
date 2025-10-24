import os

import dashscope
import json
from dashscope import Generation


def prompts():
    messages = [
        {"role": "system", "content": "你是一个财务数据处理助手 请严格按照以下要求处理OCR识别结果"
                                      "## 输出要求"
                                      "- 仅输出标准的JSON格式数据，不要有任何额外的文字、说明或标记"
                                      "- 时间格式必须统一为：%Y-%m-%d %H:%M:%S"},
    ]
    return messages


class Ai(Generation):
    api_key =os.getenv("LLM_KEY")
    model = os.getenv("LLM_MODEL")
    api_url = os.getenv("LLM_API_URL")

    def exec(self,messages:list):
        dashscope.base_http_api_url = self.api_url

        print("=" * 20 + "请求内容" + "=" * 20)
        print(messages)
        response = Generation.call(
            api_key=self.api_key,
            model=self.model,
            messages=messages,
            result_format="message",
            response_format={'type': 'json_object'}
        )

        if response.status_code == 200:
            print("=" * 20 + "完整回复" + "=" * 20)
            print(response.output.choices[0].message.content)
            return json.loads(response.output.choices[0].message.content)
        else:
            print(f"HTTP返回码：{response.status_code}")
            print(f"错误码：{response.code}")
            print(f"错误信息：{response.message}")
