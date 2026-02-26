import os
import datetime
from typing import List
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase

# .envファイルを読み込む
load_dotenv()

# --- 設定 ---
# 環境変数 DATABASE_URL から接続情報を取得（例：postgresql://user:pass@localhost/dbname）
DB_URL = os.getenv("DATABASE_URL")
POSTS_DIR = "static/posts"

# PostgreSQL用エンジン設定
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

# --- モデル ---
class Like(Base):
    __tablename__ = "likes"
    post_id = Column(String, primary_key=True)
    count = Column(Integer, default=0)

class LikeLog(Base):
    __tablename__ = "like_logs"
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(String)
    ip = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.now)

# テーブル作成
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# DBセッション管理
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- APIエンドポイント ---

@app.get("/api/posts")
def get_post_list():
    if not os.path.exists(POSTS_DIR):
        return {"posts": []}
    files = [f for f in os.listdir(POSTS_DIR) if f.endswith(".html")]
    files.sort(reverse=True)
    return {"posts": files}

@app.get("/api/likes/{post_id}")
def get_likes(post_id: str, db: Session = Depends(get_db)):
    like = db.query(Like).filter(Like.post_id == post_id).first()
    return {"count": like.count if like else 0}

@app.post("/api/likes/{post_id}")
def post_like(post_id: str, request: Request, db: Session = Depends(get_db)):
    client_ip = request.client.host
    limit_time = datetime.datetime.now() - datetime.timedelta(hours=24)
    
    recent_log = db.query(LikeLog).filter(
        LikeLog.post_id == post_id, 
        LikeLog.ip == client_ip, 
        LikeLog.created_at > limit_time
    ).first()
    
    if recent_log:
        return {"status": "error", "message": "この記事へのいいねは24時間に1回までです"}

    like = db.query(Like).filter(Like.post_id == post_id).first()
    if not like:
        like = Like(post_id=post_id, count=1)
        db.add(like)
    else:
        like.count += 1
    
    db.add(LikeLog(post_id=post_id, ip=client_ip))
    db.commit()
    db.refresh(like)
    
    return {"status": "ok", "count": like.count}

# 静的ファイル配信
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)