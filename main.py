from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uuid
from datetime import datetime

app = FastAPI(title="Simple Blog API", version="1.0.0")

# Добавляем CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
@app.get("/", response_class=HTMLResponse)
async def root():
    return """

    <!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Система управления статьями</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        body {
            background-color: #f5f7fa;
            color: #333;
            line-height: 1.6;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        header {
            background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
            color: white;
            padding: 30px 0;
            text-align: center;
            border-radius: 0 0 10px 10px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            margin-bottom: 30px;
        }

        h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
        }

        .subtitle {
            font-size: 1.1rem;
            opacity: 0.9;
        }

        .content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
        }

        @media (max-width: 768px) {
            .content {
                grid-template-columns: 1fr;
            }
        }

        .section {
            background: white;
            border-radius: 10px;
            padding: 25px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        }

        .section-title {
            font-size: 1.5rem;
            margin-bottom: 20px;
            color: #2c3e50;
            border-bottom: 2px solid #f0f0f0;
            padding-bottom: 10px;
        }

        .form-group {
            margin-bottom: 20px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #2c3e50;
        }

        input, textarea {
            width: 100%;
            padding: 12px 15px;
            border: 1px solid #ddd;
            border-radius: 6px;
            font-size: 1rem;
            transition: border 0.3s, box-shadow 0.3s;
        }

        input:focus, textarea:focus {
            outline: none;
            border-color: #6a11cb;
            box-shadow: 0 0 0 3px rgba(106, 17, 203, 0.1);
        }

        textarea {
            min-height: 120px;
            resize: vertical;
        }

        .btn {
            background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 6px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(106, 17, 203, 0.3);
        }

        .btn:active {
            transform: translateY(0);
        }

        .btn:disabled {
            background: #cccccc;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }

        .articles-list {
            max-height: 600px;
            overflow-y: auto;
        }

        .article-item {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 15px;
            border-left: 4px solid #6a11cb;
            transition: transform 0.2s;
        }

        .article-item:hover {
            transform: translateX(5px);
        }

        .article-title {
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 8px;
            color: #2c3e50;
        }

        .article-content {
            color: #555;
            margin-bottom: 10px;
            line-height: 1.5;
        }

        .article-meta {
            display: flex;
            justify-content: space-between;
            font-size: 0.85rem;
            color: #777;
        }

        .loading {
            text-align: center;
            padding: 20px;
            color: #6a11cb;
        }

        .error {
            background: #ffecec;
            color: #d63031;
            padding: 15px;
            border-radius: 6px;
            margin-bottom: 20px;
            border-left: 4px solid #d63031;
        }

        .success {
            background: #e8f7ef;
            color: #00b894;
            padding: 15px;
            border-radius: 6px;
            margin-bottom: 20px;
            border-left: 4px solid #00b894;
        }

        .empty-state {
            text-align: center;
            padding: 40px 20px;
            color: #777;
        }

        .empty-state i {
            font-size: 3rem;
            margin-bottom: 15px;
            color: #ddd;
        }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>Практика 26 (отпарвка http запросов с мобилки)</h1>
            <p class="subtitle">Создал это чудо: Плешаков Роман Сергеевич</p>
        </div>
    </header>

    <div class="container">
        <div class="content">
            <div class="section">
                <h2 class="section-title">Добавить новую статью</h2>
                <form id="articleForm">
                    <div class="form-group">
                        <label for="title">Заголовок</label>
                        <input type="text" id="title" name="title" required>
                    </div>
                    <div class="form-group">
                        <label for="content">Содержание</label>
                        <textarea id="content" name="content" required></textarea>
                    </div>
                    <div class="form-group">
                        <label for="author">Автор</label>
                        <input type="text" id="author" name="author" required>
                    </div>
                    <button type="submit" class="btn" id="submitBtn">Опубликовать статью</button>
                </form>
                <div id="formMessage"></div>
            </div>

            <div class="section">
                <h2 class="section-title">Список статей</h2>
                <div class="articles-list" id="articlesList">
                    <div class="loading">Загрузка статей...</div>
                </div>
            </div>
        </div>
    </div>

    <script>
        const API_BASE_URL = 'https://practic26kochetkov.onrender.com/';

        // Элементы DOM
        const articleForm = document.getElementById('articleForm');
        const articlesList = document.getElementById('articlesList');
        const formMessage = document.getElementById('formMessage');
        const submitBtn = document.getElementById('submitBtn');

        // Функция для отображения сообщений
        function showMessage(message, type) {
            formMessage.innerHTML = `<div class="${type}">${message}</div>`;
            setTimeout(() => {
                formMessage.innerHTML = '';
            }, 5000);
        }

        // Функция для форматирования даты
        function formatDate(dateString) {
            const options = { 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            };
            return new Date(dateString).toLocaleDateString('ru-RU', options);
        }

        // Функция для загрузки статей
        async function loadArticles() {
            try {
                articlesList.innerHTML = '<div class="loading">Загрузка статей...</div>';
                
                const response = await fetch(`${API_BASE_URL}articles/`);
                
                if (!response.ok) {
                    throw new Error(`Ошибка HTTP: ${response.status}`);
                }
                
                const articles = await response.json();
                
                if (articles.length === 0) {
                    articlesList.innerHTML = `
                        <div class="empty-state">
                            <i>📝</i>
                            <h3>Статьи не найдены</h3>
                            <p>Создайте первую статью, используя форму слева</p>
                        </div>
                    `;
                    return;
                }
                
                articlesList.innerHTML = articles.map(article => `
                    <div class="article-item">
                        <div class="article-title">${article.title}</div>
                        <div class="article-content">${article.content}</div>
                        <div class="article-meta">
                            <span>Автор: ${article.author}</span>
                            <span>Опубликовано: ${formatDate(article.created_at)}</span>
                        </div>
                    </div>
                `).join('');
                
            } catch (error) {
                console.error('Ошибка загрузки статей:', error);
                articlesList.innerHTML = `
                    <div class="error">
                        <strong>Ошибка загрузки статей:</strong> ${error.message}
                    </div>
                `;
            }
        }

        // Обработчик отправки формы
        articleForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(articleForm);
            const title = formData.get('title');
            const content = formData.get('content');
            const author = formData.get('author');
            
            if (!title || !content || !author) {
                showMessage('Пожалуйста, заполните все поля', 'error');
                return;
            }
            
            // Блокируем кнопку отправки
            submitBtn.disabled = true;
            submitBtn.textContent = 'Отправка...';
            
            try {
                const response = await fetch(`${API_BASE_URL}articles/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ title, content, author })
                });
                
                if (!response.ok) {
                    const errorData = await response.json().catch(() => ({}));
                    throw new Error(errorData.message || `Ошибка HTTP: ${response.status}`);
                }
                
                const newArticle = await response.json();
                
                showMessage('Статья успешно создана!', 'success');
                articleForm.reset();
                
                // Обновляем список статей
                await loadArticles();
                
            } catch (error) {
                console.error('Ошибка создания статьи:', error);
                showMessage(`Ошибка создания статьи: ${error.message}`, 'error');
            } finally {
                // Разблокируем кнопку отправки
                submitBtn.disabled = false;
                submitBtn.textContent = 'Опубликовать статью';
            }
        });

        // Загружаем статьи при загрузке страницы
        document.addEventListener('DOMContentLoaded', loadArticles);
    </script>
</body>
</html>

    """

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
