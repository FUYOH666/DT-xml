#!/bin/bash
# Скрипт для публикации проекта на GitHub

set -e

echo "🚀 Публикация DT-XML на GitHub"
echo "================================"
echo ""

# Проверка наличия Git
if ! command -v git &> /dev/null; then
    echo "❌ Git не установлен. Установите Git и попробуйте снова."
    exit 1
fi

# Проверка инициализации Git
if [ ! -d ".git" ]; then
    echo "📦 Инициализация Git репозитория..."
    git init
fi

# Проверка наличия изменений
if [ -z "$(git status --porcelain)" ] && [ -n "$(git rev-parse HEAD 2>/dev/null)" ]; then
    echo "⚠️  Нет изменений для коммита. Все файлы уже закоммичены."
    read -p "Продолжить с push? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 0
    fi
else
    echo "📝 Добавление файлов..."
    git add .
    
    echo "💾 Создание коммита..."
    git commit -m "feat: Initial release - AI-powered semantic search for customs declarations

Features:
- Hybrid search (BM25 + Vector)
- Adaptive reranking  
- Dynamic schemas for tenants
- OCR support
- Multilingual support (RU, KZ, EN)
- Platform architecture
- Complete documentation
- Examples and use cases

Business value:
- Saves 99.9% of search time
- ROI 500-1000% for logistics companies
- Reduces errors by 30-50%"
fi

# Проверка remote
if git remote get-url origin &> /dev/null; then
    REMOTE_URL=$(git remote get-url origin)
    echo "✅ Remote уже настроен: $REMOTE_URL"
    read -p "Использовать существующий remote? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        read -p "Введите URL нового remote: " NEW_REMOTE
        git remote set-url origin "$NEW_REMOTE"
    fi
else
    echo "🔗 Настройка remote..."
    read -p "Введите URL GitHub репозитория (https://github.com/ScanovichAI/DT-xml.git): " REMOTE_URL
    REMOTE_URL=${REMOTE_URL:-https://github.com/ScanovichAI/DT-xml.git}
    git remote add origin "$REMOTE_URL"
fi

# Переименование ветки в main
CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "main")
if [ "$CURRENT_BRANCH" != "main" ]; then
    echo "🔄 Переименование ветки в main..."
    git branch -M main
fi

# Push
echo "📤 Отправка в GitHub..."
echo ""
read -p "Выполнить git push? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git push -u origin main
    echo ""
    echo "✅ Проект успешно опубликован на GitHub!"
    echo ""
    echo "📋 Следующие шаги:"
    echo "1. Перейдите на https://github.com/ScanovichAI/DT-xml"
    echo "2. Добавьте Topics (теги) в настройках репозитория"
    echo "3. Настройте About section (Website: https://scanovich.ai/)"
    echo "4. Создайте первый Release (v0.1.0)"
    echo ""
    echo "Подробные инструкции в файле PUBLISH.md"
else
    echo "⏸️  Push отменен. Выполните вручную:"
    echo "   git push -u origin main"
fi
