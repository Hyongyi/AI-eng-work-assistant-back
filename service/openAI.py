import os
from groq import Groq
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import config as config
from fastapi.responses import StreamingResponse
from typing import AsyncIterator
import asyncio
import re


router = APIRouter()

class PromptRequest(BaseModel):
    promptTemplate: str
    sentence: str

# Groq 클라이언트 초기화
client = Groq(
    api_key=config.API_KEY
)


# Prompt 템플릿을 변수로 정의
correct_grammar_template = "당신은 영어 선생님으로 당신의 직무는 영어를 배우는 학생들을 가르치고 올바른 영어를 사용할 수 있게 도와주는 선생님입니다. 학생들은 한국인이기에 무조건 한국말을 사용해야 합니다. 한국어 외에 다른 언어로 설명하면 한국 학생들은 더이상 수업에 나오지 않을 겁니다. 다른 언어를 사용하지 않도록 주의하세요. 단, 학생이 제시한 문장은 영어 그대로 사용해주세요. 학생이 문장 혹은 문단을 제시하면 검수를 한 뒤, 틀린 문법이 있을시, 문법적으로 맞게 고치고 어디가 어떻게 틀렸는지 한국어로 설명해야 합니다. 다음은 학생이 당신에게 검수를 요청하는 내용입니다.\n {sentence} \n 다음 내용을 검수하고 틀린 부분이 있으면 문법 위주로 친절하게 단계별로 설명해주세요. "


summary_template = "당신은 영어 선생님으로 당신의 직무는 영어를 배우는 학생들을 가르치고 올바른 영어를 사용할 수 있게 도와주는 선생님입니다. 학생들은 한국인이기에 무조건 한국말을 사용해야 합니다. 한국어 외에 다른 언어로 설명하면 한국 학생들은 더이상 수업에 나오지 않을 겁니다. 다른 언어를 사용하지 않도록 주의하세요. 단, 학생이 제시한 문장은 영어 그대로 사용해주세요. 학생이 영어로 된 문장 혹은 문단을 제시하면 당신은 이 문장을 분석해서 요약하여 설명해주어야 합니다. 간결하게 설명하되, 내용이 누락되면 안됩니다. 다음은 학생이 당신에게 물어보는 내용입니다.\n {sentence} \n 다음 내용을 분석한 뒤, 한국어로 요약하여 전달해주세요. 문장은 끊어지지 않고 전체적으로 이어지게 만들어주세요."

translate_template = "당신 전문적인 영어 번역가로 당신의 직무는 영어를 올바르게 번역해주는 것입니다. 당신은 번역을 댓가로 돈을 받기 때문에 정확하고 올바르게 영어를 번역해주어야 합니다. 학생이 영어로 된 문장 혹은 문단을 제시하면 당신은 이 문장을 번역해주어야 합니다. 번역은 정확해야 하고 내용이 누락되면 안됩니다. 다음은 고객이 당신에게 요청하는 내용입니다.\n {sentence} \n 다음 내용을 분석한 뒤, 한국어로 번역하여 전달해주세요. 문장은 끊어지지 않고 전체적으로 이어지게 만들어주세요."


# @router.post("/callAI")
# async def groq_api(request: PromptRequest):
#     try:
#         prompt_template = prompt_format(prompt=description_template, sentence=request.sentence)
#         response_content = call_Groq_api(prompt_template)  # API 호출
#         return {"response": response_content}  # 전체 응답을 문자열로 반환
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))  # 예외 발생 시 오류 반환# 예외 발생 시 오류 반환



# def call_Groq_api(prompt):
#     response = client.chat.completions.create(
#         messages=[
#             {
#                 "role": "user",
#                 "content": prompt,
#             }
#         ],
#         model=config.LLM_MODEL,
#     )
    
    
#     return response.choices[0].message.content

# def prompt_format(prompt, sentence):
#     prompt_template = prompt.format(sentence=sentence)
#     return call_Groq_api(prompt_template)

@router.post("/callAI")
async def groq_api(request: PromptRequest):
    try:
        if (request.promptTemplate == 'correct_grammar_template'):
            templateName = correct_grammar_template
        elif (request.promptTemplate == 'translate_template'):
            templateName = translate_template
        elif (request.promptTemplate == 'summary_template'):
            templateName = summary_template
            
        prompt_template = prompt_format(prompt=templateName, sentence=request.sentence)
        
        async def event_stream() -> AsyncIterator[str]:
            async for chunk in call_Groq_api(prompt_template):
                yield chunk
        
        return StreamingResponse(event_stream(), media_type="text/event-stream")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def call_Groq_api(prompt: str) -> AsyncIterator[str]:
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=config.LLM_MODEL,
    )

    content = response.choices[0].message.content
    
    # 결과를 청크로 나눠서 반환 (예: 줄 바꿈 기준)
    for chunk in content.split():  # 필요에 따라 다른 기준으로 나누기
        await asyncio.sleep(0.1)  # 비동기 대기 (선택사항)
        yield chunk

def prompt_format(prompt: str, sentence: str) -> str:
    # 문장에 맞게 프롬프트를 형식화
    return prompt.format(sentence=sentence)