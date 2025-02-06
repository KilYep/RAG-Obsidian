from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes
from rag_chain import rag_chain

app = FastAPI(
    title="笔记助手 API",
    version="1.1",
    description="基于 Obsidian 笔记的问答系统"
)

# CORS 中间件配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# 添加 RAG 链路由
add_routes(
    app,
    rag_chain,
)

# 添加健康检查端点
@app.get("/api/health")
def health_check():
    return {"status": "ok"}