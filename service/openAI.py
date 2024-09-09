import os
from groq import Groq
import config as config

# Groq 클라이언트 초기화
client = Groq(
    api_key=Gconfig.API_KEY
)

prompt = f"다음의 문장을 문법적으로 맞게 고치고 어디가 어떻게 틀렸는지 한국어로 설명해줘. 한자는 쓰지 말아줘.{sentence}"

# API 호출
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model="llama-3.1-70b-versatile",
)

# 응답 출력
print(chat_completion.choices[0].message.content)