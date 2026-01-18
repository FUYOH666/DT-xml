#!/bin/bash
# Скрипт для создания репозитория на GitHub через GitHub CLI

set -e

echo "🚀 Создание репозитория DT-XML на GitHub"
echo "=========================================="
echo ""

# Проверка наличия GitHub CLI
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) не установлен."
    echo ""
    echo "Установите GitHub CLI:"
    echo "  macOS: brew install gh"
    echo "  Linux: https://cli.github.com/"
    echo ""
    echo "Или создайте репозиторий вручную:"
    echo "  1. Перейдите на https://github.com/new"
    echo "  2. Создайте репозиторий 'DT-xml' в организации 'ScanovichAI'"
    echo "  3. Используйте скрипт publish_to_github.sh для публикации"
    exit 1
fi

# Проверка авторизации
if ! gh auth status &> /dev/null; then
    echo "🔐 Авторизация в GitHub..."
    gh auth login
fi

# Создание репозитория
echo "📦 Создание репозитория..."
gh repo create ScanovichAI/DT-xml \
    --public \
    --description "AI-powered semantic search system for customs declarations (EAEU). Helps logistics companies find similar historical declarations in seconds instead of hours." \
    --homepage "https://scanovich.ai/" \
    --source=. \
    --remote=origin \
    --push

echo ""
echo "✅ Репозиторий создан и код отправлен!"
echo ""
echo "📋 Следующие шаги:"
echo "1. Добавьте Topics в настройках репозитория"
echo "2. Настройте About section"
echo "3. Создайте первый Release (v0.1.0)"
echo ""
echo "Репозиторий: https://github.com/ScanovichAI/DT-xml"
