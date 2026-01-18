# Инструкция по созданию репозитория на GitHub

## Шаги для публикации проекта

### 1. Создание репозитория на GitHub

1. Перейдите на [GitHub](https://github.com/new)
2. Заполните форму:
   - **Repository name**: `DT-xml`
   - **Description**: `AI-powered semantic search system for customs declarations (EAEU). Helps logistics companies find similar historical declarations in seconds instead of hours.`
   - **Visibility**: ✅ Public
   - **Initialize**: Не отмечайте никаких опций (у нас уже есть файлы)
3. Нажмите **Create repository**

### 2. Добавление Topics (тегов)

После создания репозитория, добавьте следующие Topics в настройках репозитория:

```
customs-declarations
semantic-search
vector-search
rag
logistics
eaeu
embeddings
reranking
fastapi
qdrant
python
document-search
ml
nlp
hybrid-search
customs
ai
machine-learning
search-engine
```

### 3. Настройка репозитория

#### Описание репозитория (About section)

**Description:**
```
AI-powered semantic search for customs declarations. Saves 99.9% of search time for logistics companies. Built with FastAPI, Qdrant, and advanced ML models.
```

**Website:** `https://scanovich.ai/`

**Topics:** (добавьте теги из списка выше)

### 4. Инициализация Git и первый коммит

```bash
# Инициализация Git (если еще не инициализирован)
git init

# Добавление всех файлов
git add .

# Первый коммит
git commit -m "feat: Initial release - AI-powered semantic search for customs declarations

- Hybrid search (BM25 + Vector)
- Adaptive reranking
- Dynamic schemas for tenants
- OCR support
- Multilingual support (RU, KZ, EN)
- Platform architecture"

# Добавление remote репозитория
git remote add origin https://github.com/ScanovichAI/DT-xml.git

# Переименование ветки в main (если нужно)
git branch -M main

# Push в репозиторий
git push -u origin main
```

### 5. Настройка GitHub Pages (опционально)

Если хотите разместить документацию на GitHub Pages:

1. Settings → Pages
2. Source: Deploy from a branch
3. Branch: `main` / `docs/`
4. Save

### 6. Создание первого Release

1. Перейдите в **Releases** → **Create a new release**
2. **Tag version**: `v0.1.0`
3. **Release title**: `v0.1.0 - Initial Release`
4. **Description**:
```markdown
## 🎉 First Release

### Features
- ✅ Hybrid search (BM25 + Vector)
- ✅ Adaptive reranking
- ✅ Dynamic schemas for tenants
- ✅ OCR support
- ✅ Multilingual support (RU, KZ, EN)
- ✅ Platform architecture
- ✅ REST API

### Documentation
- Complete API documentation
- Quick start guide
- Business value analysis
- Examples and use cases

### Tech Stack
- Python 3.12+
- FastAPI
- Qdrant
- PostgreSQL
- SentenceTransformers
- BGE-Reranker
```

5. Нажмите **Publish release**

### 7. Настройка веток защиты (рекомендуется)

1. Settings → Branches
2. Add rule для `main`:
   - ✅ Require pull request reviews before merging
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date before merging

### 8. Настройка секретов для CI (если нужно)

Если CI требует секреты:
1. Settings → Secrets and variables → Actions
2. Добавьте необходимые секреты

### 9. Добавление README badges (обновление)

После создания репозитория, обновите badges в README.md:

```markdown
[![GitHub stars](https://img.shields.io/github/stars/ScanovichAI/DT-xml?style=social)](https://github.com/ScanovichAI/DT-xml)
[![GitHub forks](https://img.shields.io/github/forks/ScanovichAI/DT-xml?style=social)](https://github.com/ScanovichAI/DT-xml)
[![GitHub issues](https://img.shields.io/github/issues/ScanovichAI/DT-xml)](https://github.com/ScanovichAI/DT-xml/issues)
[![GitHub license](https://img.shields.io/github/license/ScanovichAI/DT-xml)](https://github.com/ScanovichAI/DT-xml/blob/main/LICENSE)
```

### 10. Продвижение проекта

#### Сообщества для публикации:

1. **Reddit**:
   - r/MachineLearning
   - r/Python
   - r/logistics

2. **Hacker News**:
   - Submit с описанием проекта

3. **LinkedIn**:
   - Пост о проекте с описанием бизнес-ценности

4. **Twitter/X**:
   - Твит с описанием и ссылкой

5. **Отраслевые форумы**:
   - Форумы логистических компаний
   - Сообщества таможенных брокеров

### 11. Мониторинг и поддержка

- Регулярно отвечайте на Issues
- Обновляйте документацию
- Публикуйте релизы с новыми фичами
- Участвуйте в обсуждениях

## Готово! 🎉

После выполнения этих шагов ваш проект будет красиво оформлен и готов к привлечению единомышленников!
