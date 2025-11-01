"""
FastAPI сервер для RAG системы
Предоставляет HTTP API для интеграции с веб-интерфейсом
"""

import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from src.rag import GOSTRAGSystem
from src.config import config

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Инициализация FastAPI
app = FastAPI(
    title="GOST RAG API",
    description="API для RAG системы анализа документов ГОСТ",
    version="0.4.0"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В production использовать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Инициализация RAG системы
rag_system: Optional[GOSTRAGSystem] = None


@app.on_event("startup")
async def startup_event():
    """Инициализация RAG системы при старте сервера"""
    global rag_system
    try:
        logger.info("Инициализация RAG системы...")
        rag_system = GOSTRAGSystem(config)
        rag_system.initialize_milvus(create_new=False)
        rag_system.load_index()
        logger.info("RAG система успешно инициализирована")
    except Exception as e:
        logger.error(f"Ошибка инициализации RAG системы: {e}")
        # Не падаем, чтобы health check работал
        rag_system = None


# Pydantic модели для запросов
class QueryRequest(BaseModel):
    question: str


class ExtractRequest(BaseModel):
    class_name: str


# Pydantic модели для ответов
class QueryResponse(BaseModel):
    result: str
    success: bool
    error: Optional[str] = None


class StatsResponse(BaseModel):
    documents: int
    vectors: int
    embedding_model: str
    device: str
    status: str


class HealthResponse(BaseModel):
    status: str
    message: str


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Проверка здоровья сервиса"""
    if rag_system is None:
        return HealthResponse(
            status="unhealthy",
            message="RAG система не инициализирована"
        )
    
    return HealthResponse(
        status="healthy",
        message="RAG система работает"
    )


@app.get("/stats", response_model=StatsResponse)
async def get_stats():
    """Получение статистики системы"""
    if rag_system is None:
        raise HTTPException(status_code=503, detail="RAG система не инициализирована")
    
    try:
        stats = rag_system.get_stats()
        return StatsResponse(
            documents=stats.get("documents", 0),
            vectors=stats.get("vectors", 0),
            embedding_model=stats.get("embedding_model", "unknown"),
            device=stats.get("device", "unknown"),
            status="ready"
        )
    except Exception as e:
        logger.error(f"Ошибка получения статистики: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """Выполнение запроса к документам"""
    if rag_system is None:
        raise HTTPException(status_code=503, detail="RAG система не инициализирована")
    
    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="Вопрос не может быть пустым")
    
    try:
        logger.info(f"Выполнение запроса: {request.question}")
        result = rag_system.query(request.question)
        return QueryResponse(
            result=result,
            success=True
        )
    except Exception as e:
        logger.error(f"Ошибка выполнения запроса: {e}")
        return QueryResponse(
            result="",
            success=False,
            error=str(e)
        )


@app.post("/extract", response_model=QueryResponse)
async def extract_class_info(request: ExtractRequest):
    """Извлечение информации о классе прочности"""
    if rag_system is None:
        raise HTTPException(status_code=503, detail="RAG система не инициализирована")
    
    if not request.class_name or not request.class_name.strip():
        raise HTTPException(status_code=400, detail="Название класса не может быть пустым")
    
    try:
        logger.info(f"Извлечение информации о классе: {request.class_name}")
        result = rag_system.extract_class_info(request.class_name)
        return QueryResponse(
            result=result,
            success=True
        )
    except Exception as e:
        logger.error(f"Ошибка извлечения информации: {e}")
        return QueryResponse(
            result="",
            success=False,
            error=str(e)
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
