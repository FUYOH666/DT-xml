# DT-XML: AI-Powered Search for Customs Declarations

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](https://opensource.org/licenses/Apache-2.0)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![Qdrant](https://img.shields.io/badge/Qdrant-Latest-orange.svg)](https://qdrant.tech/)
[![GitHub stars](https://img.shields.io/github/stars/FUYOH666/DT-xml?style=social)](https://github.com/FUYOH666/DT-xml)
[![GitHub forks](https://img.shields.io/github/forks/FUYOH666/DT-xml?style=social)](https://github.com/FUYOH666/DT-xml)
[![GitHub issues](https://img.shields.io/github/issues/FUYOH666/DT-xml)](https://github.com/FUYOH666/DT-xml/issues)
[![GitHub license](https://img.shields.io/github/license/FUYOH666/DT-xml)](https://github.com/FUYOH666/DT-xml/blob/main/LICENSE)

---

## 🎯 Что это такое?

**DT-XML** — это **AI-powered система семантического поиска** для таможенных деклараций Евразийского экономического союза (ЕАЭС). 

Вместо часов поиска в базах данных и Excel таблицах, система находит похожие декларации **за секунды**, понимая смысл запроса, а не требуя точных совпадений.

**🇷🇺 [Полное описание на русском](#русская-версия) | 🇬🇧 [Full English Description](#english-version)**

---

## 💡 Для кого это?

- ✅ **Логистические компании**, обрабатывающие тысячи деклараций в год
- ✅ **Таможенные брокеры**, готовящие декларации для клиентов  
- ✅ **Импортеры/экспортеры** с большим объемом деклараций
- ✅ **Разработчики**, создающие таможенные системы
- ✅ **Компании**, желающие сохранить и использовать историческую экспертизу

---

## 🔥 Какую проблему решает?

### ❌ Текущая ситуация

При подготовке новой таможенной декларации сотрудники тратят **2-4 часа** на поиск похожих ранее выпущенных деклараций:

- Ручной поиск в SQL базах данных (требует точных совпадений)
- Поиск в Excel таблицах (тысячи строк, нет семантики)
- Работа с бумажными архивами
- Консультации с коллегами ("помнишь, мы делали похожую?")

**Результат**: Потеря времени, ошибки, потеря экспертизы при уходе сотрудников.

### ✅ Решение DT-XML

- ⚡ **Поиск за секунды** вместо часов (**99.9% экономии времени**)
- 🧠 **Семантическое понимание** — находит "смартфоны" при запросе "мобильные телефоны"
- 🎯 **Точные фильтры** — по производителю, товару, дате, коду ТН ВЭД
- 📊 **Объяснимость** — показывает, почему декларация релевантна
- 🌍 **Многоязычность** — русский, казахский, английский
- 🔧 **Платформа** — настраивается под каждого заказчика

---

## 🚀 Чем отличается от обычных баз данных?

| **Обычные базы данных** | **DT-XML** |
|-------------------------|------------|
| ❌ Требуют точных совпадений полей | ✅ Понимает смысл и синонимы |
| ❌ SQL-запросы жесткие | ✅ Запросы на естественном языке |
| ❌ Не могут найти "похожие" элементы | ✅ Семантический поиск по сходству |
| ❌ Медленные при сложных запросах | ✅ Оптимизированный гибридный поиск |
| ❌ Не понимают контекст | ✅ AI-powered понимание контекста |
| ❌ Требуется ручная фильтрация | ✅ Интеллектуальный реранкинг |
| ❌ Не объясняют результаты | ✅ Показывает, почему результаты релевантны |

### Ключевые преимущества:

1. **Семантический поиск**: Находит "Samsung смартфоны" при запросе "мобильные телефоны Samsung"
2. **Гибридный подход**: Объединяет BM25 (ключевые слова) + векторные эмбединги
3. **Адаптивный реранкинг**: Автоматически улучшает качество результатов
4. **Временная осведомленность**: Учитывает изменения правил ЕАЭС во времени
5. **Объяснимость**: Показывает, какие поля совпали и почему результат релевантен

---

## 🤖 Интеграция с LLM (GPT, Claude и др.)

DT-XML готов к интеграции с большими языковыми моделями:

### 🔗 RAG (Retrieval Augmented Generation)
```
Пользователь → DT-XML находит релевантные декларации → LLM анализирует и генерирует ответ
```

### 💡 Примеры использования с LLM:

- **"Найди все декларации Samsung за 2023 и суммируй общие паттерны"**
  - DT-XML находит декларации → LLM анализирует и создает отчет

- **"Какие типичные ошибки в декларациях для кода ТН ВЭД 8517120000?"**
  - DT-XML находит похожие декларации → LLM анализирует и выделяет паттерны ошибок

- **"Сгенерируй шаблон декларации на основе похожих исторических примеров"**
  - DT-XML находит примеры → LLM создает шаблон

- **"Объясни, почему эта декларация была помечена и предложи исправления"**
  - DT-XML находит похожие случаи → LLM объясняет и предлагает решения

---

## 💰 Бизнес-эффект

Для компании, обрабатывающей **10,000 деклараций в год**:

| Метрика | До | После | Экономия |
|---------|-----|-------|----------|
| **Время на поиск** | 2-4 часа | 5 секунд | **99.9%** |
| **Время на декларацию** | 4-6 часов | 2-3 часа | **40-50%** |
| **Обработка 10,000 деклараций** | 40,000-60,000 часов | 20,000-30,000 часов | **20,000-30,000 часов** |

### 💵 Финансовый эффект:

- **Экономия времени**: 20,000-30,000 часов/год
- **Экономия средств**: **$500,000 - $750,000/год** (при ставке $25/час)
- **ROI**: **500-1000%** возврат инвестиций в первый год
- **Снижение ошибок**: На **30-50%** меньше ошибок

📖 [Подробнее о бизнес-ценности →](docs/BUSINESS_VALUE.md)

---

## 🛠️ Технологии

- **Python 3.12+** с **uv** для управления зависимостями
- **FastAPI** для REST API
- **Qdrant** для векторной базы данных
- **PostgreSQL** для метаданных
- **SentenceTransformers** / **BCEmbedding** для эмбедингов
- **BGE-Reranker** для реранкинга

---

## 🚀 Быстрый старт

```bash
# 1. Клонируйте репозиторий
git clone https://github.com/FUYOH666/DT-xml.git
cd DT-xml

# 2. Установите зависимости
uv sync

# 3. Настройте окружение
cp .env.example .env

# 4. Запустите инфраструктуру
docker-compose up -d

# 5. Запустите сервер
uv run python -m src.dt_xml.api.main
```

API будет доступен по адресу `http://localhost:8000`

📖 [Подробная инструкция по установке →](docs/QUICK_START.md)

---

## 📖 Пример использования

### Поиск деклараций

```python
import requests

# Поиск деклараций Samsung за 2023 год
response = requests.post(
    "http://localhost:8000/search",
    json={
        "query": "Samsung смартфоны",
        "tenant_id": "default",
        "top_k": 10,
        "filters": {
            "manufacturer": "Samsung",
            "date_issued": {"gte": "2023-01-01", "lte": "2023-12-31"}
        }
    }
)

results = response.json()
for result in results["results"]:
    print(f"Декларация: {result['declaration_id']}")
    print(f"Релевантность: {result['score']:.2f}")
    print(f"Почему найдено: {result['explanation']['reasons']}")
```

📚 [Больше примеров →](examples/)

---

## 🎯 Возможности

- 🔍 **Гибридный поиск**: BM25 (sparse) + Vector (dense)
- 🎯 **Адаптивный реранкинг**: Автоматический выбор сложности
- ⏰ **Временная осведомленность**: Учет изменений правил ЕАЭС
- 📊 **Объяснимость**: Метаданные о релевантности результатов
- 🌍 **Многоязычность**: Русский, казахский, английский
- 🔧 **REST API**: Полнофункциональный API для интеграции
- 📋 **Динамические схемы**: Настраиваемые схемы для каждого заказчика
- 🔄 **OCR поддержка**: Обработка неструктурированного текста

---

## 📚 Документация

- [📖 API Спецификация](docs/api_spec.md)
- [📋 Формат данных для клиентов](docs/data_format.md)
- [🏗️ Архитектура системы](docs/architecture.md)
- [💰 Бизнес-ценность](docs/BUSINESS_VALUE.md)
- [⚙️ Настройка схем заказчиков](docs/tenant_configuration.md)
- [❓ FAQ](docs/FAQ.md)

---

## 🤝 Участие в разработке

Мы приветствуем вклад в проект! 

- 📝 [Руководство для контрибьюторов](CONTRIBUTING.md)
- 🐛 [Сообщить об ошибке](https://github.com/FUYOH666/DT-xml/issues/new?template=bug_report.md)
- 💡 [Предложить фичу](https://github.com/FUYOH666/DT-xml/issues/new?template=feature_request.md)

---

## 📞 Контакты

- 🌐 **Website**: [https://scanovich.ai/](https://scanovich.ai/)
- 💬 **Telegram**: [@ScanovichAI](https://t.me/ScanovichAI)
- 💬 **Issues**: [GitHub Issues](https://github.com/FUYOH666/DT-xml/issues)
- 📖 **Документация**: [docs/](docs/)

---

## 📄 Лицензия

Этот проект лицензирован под Apache License 2.0 - см. файл [LICENSE](LICENSE) для деталей.

---

## 🌟 История звезд

Если вы находите этот проект полезным, пожалуйста, рассмотрите возможность поставить звезду ⭐

---

# 🇬🇧 English Version

## 🤔 What is DT-XML?

**DT-XML** is an **AI-powered semantic search system** for customs declarations of the Eurasian Economic Union (EAEU). It transforms how logistics companies work with historical declarations by enabling **instant semantic search** across thousands of documents.

Unlike traditional database queries that require exact matches, DT-XML understands **meaning and context**, finding relevant declarations even when wording differs. It combines the best of both worlds: **keyword search** (BM25) for precise matches and **vector embeddings** for semantic similarity.

## 👥 Who is this for?

- **Large logistics companies** processing thousands of customs declarations annually
- **Customs brokers** preparing declarations for clients
- **Importers/exporters** with high declaration volumes
- **Developers** building customs-related systems
- **Companies** looking to preserve and leverage their historical expertise

## 🎯 What problem does it solve?

**The Challenge**: When preparing a new customs declaration, employees need to find similar previously issued declarations to:
- Verify correct completion
- Use proven formulations
- Avoid errors that were corrected before
- Follow precedents for specific manufacturers/products

**Current Reality**: 
- Manual search in databases takes **2-4 hours per declaration**
- SQL queries require exact field matches
- Excel spreadsheets are hard to search semantically
- Paper archives are inaccessible
- Knowledge is lost when employees leave

**DT-XML Solution**:
- ⚡ **Search in seconds** instead of hours (99.9% time reduction)
- 🧠 **Semantic understanding** - finds similar declarations even with different wording
- 🎯 **Precise filters** - by manufacturer, product, date, HS code
- 📊 **Explainability** - shows why a declaration is relevant
- 🌍 **Multilingual** - supports Russian, Kazakh, English
- 🔧 **Platform architecture** - customizable for each tenant

## 🚀 Why is it better than traditional databases?

| Traditional Databases | DT-XML |
|----------------------|--------|
| ❌ Requires exact field matches | ✅ Understands meaning and synonyms |
| ❌ SQL queries are rigid | ✅ Natural language queries |
| ❌ Can't find "similar" items | ✅ Semantic similarity search |
| ❌ Slow with complex queries | ✅ Optimized hybrid search |
| ❌ No context understanding | ✅ AI-powered context awareness |
| ❌ Manual filtering required | ✅ Intelligent reranking |
| ❌ No explanation of results | ✅ Shows why results are relevant |

**Key Advantages**:

1. **Semantic Search**: Finds "smartphones" when you search for "mobile phones"
2. **Hybrid Approach**: Combines keyword search (BM25) + vector embeddings for best results
3. **Adaptive Reranking**: Automatically adjusts result quality based on query complexity
4. **Temporal Awareness**: Accounts for rule changes over time
5. **Explainability**: Shows which fields matched and why results are relevant
6. **Multilingual**: Works across Russian, Kazakh, and English

## 🤖 LLM Integration Ready

DT-XML is designed to work seamlessly with Large Language Models (LLMs):

- **RAG (Retrieval Augmented Generation)**: Use DT-XML to retrieve relevant declarations, then feed them to LLM for intelligent summarization
- **Query Enhancement**: LLM can rewrite user queries for better search results
- **Answer Generation**: LLM can generate answers based on retrieved declarations
- **Document Analysis**: LLM can analyze patterns across multiple declarations
- **Smart Suggestions**: LLM can suggest improvements based on historical data

**Example Use Cases with LLM**:
- "Find all Samsung declarations and summarize common patterns"
- "What are the typical issues with declarations for this product code?"
- "Generate a declaration template based on similar historical examples"
- "Explain why this declaration was flagged and suggest corrections"

## 💰 Business Impact

- **Time Savings**: 99.9% reduction (from hours to seconds)
- **Cost Savings**: $500,000 - $750,000/year for companies processing 10,000 declarations
- **Error Reduction**: 30-50% fewer errors using proven precedents
- **ROI**: 500-1000% return on investment in the first year

📖 [Read more about business value](docs/BUSINESS_VALUE.md)

---

## 🗺️ Roadmap

### v0.1.0 (Текущая версия)
- ✅ Базовая функциональность поиска
- ✅ Поддержка XML/JSON/OCR
- ✅ Динамические схемы для заказчиков
- ✅ Гибридный поиск (BM25 + Vector)
- ✅ Адаптивный реранкинг

### v0.2.0 (Планируется)
- [ ] Веб-интерфейс для поиска
- [ ] Экспорт результатов в Excel/PDF
- [ ] Аналитика и статистика
- [ ] Пакетная индексация

### v0.3.0 (Будущее)
- [ ] Интеграция с внешними системами
- [ ] Мобильное приложение
- [ ] Расширенная аналитика

---

**Made with ❤️ for logistics companies**
