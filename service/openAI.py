import os
from groq import Groq
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import config as config
from fastapi.responses import StreamingResponse
from typing import AsyncIterable

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


description_template = "당신은 영어 선생님으로 당신의 직무는 영어를 배우는 학생들을 가르치고 올바른 영어를 사용할 수 있게 도와주는 선생님입니다. 학생들은 한국인이기에 무조건 한국말을 사용해야 합니다. 한국어 외에 다른 언어로 설명하면 한국 학생들은 더이상 수업에 나오지 않을 겁니다. 다른 언어를 사용하지 않도록 주의하세요. 단, 학생이 제시한 문장은 영어 그대로 사용해주세요. 학생이 영어로 된 문장 혹은 문단을 제시하면 당신은 이 문장을 분석해서 요약하여 설명해주어야 합니다. 간결하게 설명하되, 내용이 누락되면 안됩니다. 다음은 학생이 당신에게 물어보는 내용입니다.\n {sentence} \n 다음 내용을 분석한 뒤, 한국어로 요약하여 전달해주세요. 문장은 끊어지지 않고 전체적으로 이어지게 만들어주세요."


@router.post("/callAI")
async def groq_api(request: PromptRequest):
    try:
        prompt_template = prompt_format(prompt=description_template, sentence=request.sentence)
        response_content = call_Groq_api(prompt_template)  # API 호출
        return {"response": response_content}  # 전체 응답을 문자열로 반환
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  # 예외 발생 시 오류 반환# 예외 발생 시 오류 반환



def call_Groq_api(prompt):
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=config.LLM_MODEL,
    )
    
    
    return response.choices[0].message.content

def prompt_format(prompt, sentence):
    prompt_template = prompt.format(sentence=sentence)
    return call_Groq_api(prompt_template)
