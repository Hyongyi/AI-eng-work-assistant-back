from fastapi import FastAPI
from routers import openAi  # openAi 라우터 import

app = FastAPI()

# 라우터 등록
app.include_router(openAi.router, prefix="/", tags=["openAi"])
# 각 라우터를 포함시킵니다.
