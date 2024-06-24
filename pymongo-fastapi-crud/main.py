from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from dotenv import dotenv_values
from pymongo import MongoClient
from routes import router as book_router
from user_routes import router as user_router
from fastapi.middleware.cors import CORSMiddleware

# 환경 변수를 로드하고 가져올 수 있는 패키지
config = dotenv_values(".env")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# uvicorn 때 실행
@app.on_event("startup")
def startup_db_client():
    print("mongoDB 연결")
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]

# ctrl + c 때 실행 
@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

# tag - /docs 에 타이틀 부분의 이름을 설정할 수 있음 
app.include_router(book_router, tags=["books"], prefix="/book")
app.include_router(user_router, tags=["users"], prefix="/user")

# 정적 파일 제공 설정
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return {"message": "Hello World"}

