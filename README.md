## **📝 프로젝트 개요**

![image](https://github.com/user-attachments/assets/3c0be41c-4f9a-4230-b357-8e7ecff770e0)


**📌 프로젝트명**: AI 영어 업무 도우미

**📌 프로젝트 목적**:

- AI 기술을 활용하여 사용자 맞춤형 영어 업무 지원
- 번역, 문법 교정, 단어 추천 기능을 통한 업무 효율 극대화
- 글로벌 환경에서 자연스러운 의사소통을 가능하게 지원

**📌 주요 기능**:

![image (1)](https://github.com/user-attachments/assets/d63d0566-d659-4e61-a66d-835fb86dd244)


✔ **영문 번역** - 사용자가 입력한 문장을 AI가 자연스럽게 번역

✔ **문법 및 작문 교정** - 문장의 문법 오류를 자동 수정

✔ **영문 요약 및 설명** - 긴 문장을 요약하고 의미를 설명

✔ **영단어 추천** - 업무 능력 향상을 위한 영단어 학습 프로그램

---

## **🚀 기술 스택**

### **Frontend**

- **React**
- **TypeScript**

### **Backend**

- **Python**

### AI Model

- **Llama3**
- **ChatGPT**

### **Database**

- **SqlLite**

---

## **📅 프로젝트 일정**

### **🔹 9월 (기획 & 설계)**

✅ 프로젝트 주제 확정 및 시장 조사

✅ 기능 목록 작성 및 우선순위 설정

✅ UI/UX 설계 및 프로토타입 제작

✅ 기술 스택 결정 및 LLM 모델 선택

### **🔹 10월 (초기 개발 & API 구축)**

✅ 프론트엔드 기본 레이아웃 및 디자인 시스템 구축

✅ FastAPI를 활용한 백엔드 환경 설정 및 기본 API 개발

✅ LLM 모델 테스트 및 응답 최적화

✅ DB 스키마 설계

✅ API 문서화 및 프론트엔드 연동 테스트 진행

### **🔹 11월 (개발 마무리 & 테스트)**

✅ 프론트엔드 개발 및 API 연동

✅ 기능별 유닛 테스트 및 버그 수정

✅ 통합 테스트 및 성능 최적화

✅ 최종 문서 작성 및 결과물 정리

---

## **📌 진행 내용**

🔹 **Backend 개발**:

- Jupyter Notebook에서 기능 테스트 후 FastAPI로 API 구축
- Streaming API 구현으로 자연스러운 답변 출력

🔹 **Frontend 개발**:

- React + TypeScript로 프론트 화면 구성
- UI/UX 직관성 향상을 위한 반응형 디자인 적용

🔹 **API 연동**:

- FastAPI를 활용한 RESTful API 개발
- 프론트엔드와 백엔드를 연결하여 AI 응답 처리

🔹 **LLM 선택**:

- 모델별 답변 및 성능 비교.

---

## **📌 개선 사항 및 향후 계획**

🔹 **AI 모델 개선**

- ChatGPT API 대신 Cloud 서비스를 사용하여 Open Source AI를 사용한 모델 기동

🔹 지원 언어 추가

- 영문 뿐만 아니라 다른 언어 지원 추가
- 언어별 출력을 위한 Prompt Engineering 개선

---

## **🎯 결과 및 성과**

✔ AI 기반 영어 학습 솔루션 개발 및 기능 구현 완료

✔ RESTful API 구축 및 프론트엔드 연동 성공

✔ UI/UX 최적화 및 사용자 경험 향상

✔ 기획부터 개발, 테스트까지 전 과정 수행

✔ Streaming을 사용한 비동기 text 출력

---

## 🖥️주요 코드

🔹 **Backend: AI 응답을 Chunk로 나누어 비동기 Streaming Response 처리**

**핵심 개념**

- AI 모델의 응답을 한꺼번에 반환하는 것이 아니라 **Chunk 단위**로 나누어 **비동기 스트리밍** 방식으로 처리
- FastAPI의 `StreamingResponse`를 활용하여 클라이언트가 응답을 **실시간으로 받을 수 주요 로직**

```python
@router.post("/callAIStreaming")
async def call_Ai_streaming(request: PromptRequest):
    try:
        async def event_stream() -> AsyncIterator[str]:
            async for chunk in call_chat_api_streaming(prompt_template):
                yield chunk  

        return StreamingResponse(event_stream(), media_type="text/event-stream")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

```

✅ **FastAPI의 `StreamingResponse`를 활용**하여 AI의 답변을 실시간으로 전송

✅ 내부의 `event_stream()`이 **비동기 제너레이터(Async Iterator)** 역할을 하여 한 번에 데이터를 처리하는 것이 아니라 **부분적으로 응답을 반환**

🔸 **AI 응답을 청크로 나누어 처리**

```python
async def call_chat_api_streaming(prompt: str) -> AsyncIterator[str]:
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model=config.LLM_MODEL,
    )
    content = chat_completion.choices[0].message.content

    # 응답을 공백 및 줄 바꿈 단위로 청크로 분리
    chunks = re.split(r'(\s+)', content)
    for chunk in chunks:
        if chunk:
            await asyncio.sleep(0.01)  # 작은 지연을 추가하여 자연스러운 스트리밍 효과 제공
            yield chunk
```

✅ AI 응답을 **공백 및 줄 바꿈 기준으로 작은 단위(Chunk)로 분리**

✅ `await asyncio.sleep(0.01)`을 사용하여 **자연스러운 스트리밍 효과 제공**

✅ `yield chunk`를 통해 **한 번에 전체 응답을 반환하는 것이 아니라 점진적으로 데이터를 전달**

---

### 🔹 **Frontend: 스트리밍된 데이터를 실시간으로 받아 화면에 표시**

🔸 **핵심 개념**

- `fetch()` API를 사용하여 **서버에서 Streaming으로 데이터를 받아와 실시간으로 화면에 출력**
- `ReadableStream`의 `getReader()`를 활용하여 데이터를 **청크 단위로 읽어 처리**

🔸 **주요 로직**

```tsx
const CallRestApi = async () => {
    setAnswer(""); 
    setLoading(true); 

    try {
        const response = await fetch(`${BASE_URL}/callAIStreaming`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                'promptTemplate': template,
                'sentence': prompt,
                'userAge': localStorage.getItem('userAge')
            }),
        });

        if (!response.ok) {
            const errorDetails = await response.json();
            throw new Error(`서버 오류: ${errorDetails.detail || '알 수 없는 오류'}`);
        }

        if (response.body) {
            const reader = response.body.getReader();
            const decoder = new TextDecoder('utf-8');

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value, { stream: true });

                setLoading(false); // 로딩 상태 비활성화
                setAnswer((prev) => prev + chunk); // 이전 응답에 이어서 출력

                await new Promise(resolve => setTimeout(resolve, 0.1)); 
            }
        } else {
            throw new Error('응답 본체가 없습니다.');
        }
    } catch (error) {
        console.error('API 호출 오류:', error);
    } finally {
        setLoading(false);
    }
};
```

✅ `fetch()`를 사용하여 **비동기 요청을 보내고 서버의 스트리밍 응답을 실시간으로 처리**

✅ `response.body.getReader()`를 활용하여 **청크 단위로 데이터를 읽어옴**

✅ `TextDecoder('utf-8')`를 사용하여 **데이터를 UTF-8 문자열로 변환**

✅ `setAnswer((prev) => prev + chunk)`를 통해 **이전 데이터에 이어서 텍스트를 출력**

✅ `await new Promise(resolve => setTimeout(resolve, 0.1))`을 통해 **부드러운 텍스트 출력 효과 제공**

---

### ✅ **결과: 자연스러운 AI 응답 출력 구현**

- **사용자가 입력한 질문에 대해 AI가 스트리밍 방식으로 응답**
- **긴 텍스트도 한꺼번에 출력되지 않고 점진적으로 화면에 표시**
- **실시간 인터랙션이 가능하여 더욱 자연스러운 사용자 경험 제공**

## 🎥시연 영상

✔[AI 영어 업무 도우미 시연 영상](https://youtu.be/91FtE7PvLUI)
