from service.openAI import router as openAi_router
from service.words import router as words_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
router = APIRouter()

app.include_router(openAi_router, tags=["openAi"])
app.include_router(words_router, tags=["words"])

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 출처 허용 (생산 환경에서는 특정 출처로 제한하는 것이 좋습니다)
    allow_credentials=True,
    allow_methods=["*"],  # 모든 메소드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)
