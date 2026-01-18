# Инструкция по публикации проекта на GitHub

## Быстрый старт

### 1. Создайте репозиторий на GitHub

1. Перейдите на https://github.com/new
2. Заполните:
   - **Owner**: `ScanovichAI`
   - **Repository name**: `DT-xml`
   - **Description**: `AI-powered semantic search system for customs declarations (EAEU). Helps logistics companies find similar historical declarations in seconds instead of hours.`
   - **Visibility**: ✅ **Public**
   - **Не отмечайте** "Add a README file" (у нас уже есть)
3. Нажмите **Create repository**

### 2. Инициализация и первый push

Выполните следующие команды в терминале:

```bash
cd /Users/aleksandrmordvinov/devs/DT-xml

# Инициализация Git (если еще не инициализирован)
git init

# Добавление всех файлов
git add .

# Первый коммит
git commit -m "feat: Initial release - AI-powered semantic search for customs declarations

Features:
- Hybrid search (BM25 + Vector)
- Adaptive reranking
- Dynamic schemas for tenants
- OCR support
- Multilingual support (RU, KZ, EN)
- Platform architecture
- Complete documentation
- Examples and use cases"

# Добавление remote (замените URL на ваш)
git remote add origin https://github.com/ScanovichAI/DT-xml.git

# Переименование ветки в main
git branch -M main

# Push в репозиторий
git push -u origin main
```

### 3. Настройка репозитория на GitHub

После создания репозитория:

#### Добавьте Topics (теги)

В настройках репозитория (Settings → General → Topics) добавьте:

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

#### Настройте About section

- **Website**: `https://scanovich.ai/`
- **Description**: `AI-powered semantic search for customs declarations. Saves 99.9% of search time for logistics companies.`

### 4. Создайте первый Release

1. Перейдите в **Releases** → **Create a new release**
2. **Tag version**: `v0.1.0`
3. **Release title**: `v0.1.0 - Initial Release`
4. Скопируйте описание из `.github/REPOSITORY_SETUP.md`
5. Нажмите **Publish release**

### 5. Настройте GitHub Actions

CI/CD уже настроен в `.github/workflows/ci.yml`. После первого push он автоматически запустится.

### 6. Опционально: GitHub Pages

Если хотите разместить документацию:

1. Settings → Pages
2. Source: `Deploy from a branch`
3. Branch: `main` / folder: `/docs`
4. Save

## Готово! 🎉

Ваш репозиторий готов и красиво оформлен!

## Следующие шаги

1. ✅ Репозиторий создан и заполнен
2. 📢 Поделитесь в социальных сетях
3. 🌟 Пригласите единомышленников
4. 📝 Отвечайте на Issues и PR

## Продвижение проекта

### Сообщества для публикации:

- **Reddit**: r/MachineLearning, r/Python, r/logistics
- **Hacker News**: Submit с описанием проекта
- **LinkedIn**: Пост о проекте с бизнес-ценностью
- **Twitter/X**: Твит с описанием
- **Telegram**: @ScanovichAI

---

**Удачи с проектом! 🚀**
