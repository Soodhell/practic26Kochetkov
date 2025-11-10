from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime

app = FastAPI(title="Simple Blog API", version="1.0.0")

# Временное хранилище в памяти
articles_db = []

# Модели данных
class ArticleCreate(BaseModel):
    title: str
    content: str
    author: str

class Article(ArticleCreate):
    id: str
    created_at: str

# Маршруты
@app.get("/")
async def root():
    return {"message": "Welcome to Simple Blog API"}

@app.post("/articles/", response_model=Article)
async def create_article(article: ArticleCreate):
    """Создание новой статьи"""
    article_id = str(uuid.uuid4())[:8]
    new_article = Article(
        id=article_id,
        title=article.title,
        content=article.content,
        author=article.author,
        created_at=datetime.now().isoformat()
    )
    articles_db.append(new_article)
    return new_article

@app.get("/articles/", response_model=List[Article])
async def get_all_articles():
    """Получение всех статей"""
    return articles_db

@app.get("/articles/{article_id}", response_model=Article)
async def get_article(article_id: str):
    """Получение статьи по ID"""
    for article in articles_db:
        if article.id == article_id:
            return article
    raise HTTPException(status_code=404, detail="Article not found")

@app.delete("/articles/{article_id}")
async def delete_article(article_id: str):
    """Удаление статьи по ID"""
    for i, article in enumerate(articles_db):
        if article.id == article_id:
            deleted_article = articles_db.pop(i)
            return {"message": f"Article '{deleted_article.title}' deleted"}
    raise HTTPException(status_code=404, detail="Article not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
