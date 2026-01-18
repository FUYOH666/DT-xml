# DT-XML: AI-Powered Search for Customs Declarations

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](https://opensource.org/licenses/Apache-2.0)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![Qdrant](https://img.shields.io/badge/Qdrant-Latest-orange.svg)](https://qdrant.tech/)
[![GitHub stars](https://img.shields.io/github/stars/FUYOH666/DT-xml?style=social)](https://github.com/FUYOH666/DT-xml)
[![GitHub forks](https://img.shields.io/github/forks/FUYOH666/DT-xml?style=social)](https://github.com/FUYOH666/DT-xml)
[![GitHub issues](https://img.shields.io/github/issues/FUYOH666/DT-xml)](https://github.com/FUYOH666/DT-xml/issues)
[![GitHub license](https://img.shields.io/github/license/FUYOH666/DT-xml)](https://github.com/FUYOH666/DT-xml/blob/main/LICENSE)

An innovative AI-powered semantic search system for customs declarations of the Eurasian Economic Union (EAEU) using embeddings, hybrid search, and adaptive reranking.

## 🎯 Problem

Large logistics companies process **thousands of customs declarations (GTD) annually**. When preparing new declarations, employees spend **2-4 hours** searching for similar previously issued declarations to:
- Verify correct completion
- Use proven formulations
- Avoid errors that were corrected before
- Follow precedents for specific manufacturers/products

**Current process**: Manual search in databases, Excel spreadsheets, paper archives - takes hours per declaration.

## ✨ Solution

DT-XML is an **AI-powered semantic search system** for historical customs declarations that:
- ⚡ **Instant search** across 10,000+ declarations in seconds
- 🧠 **Semantic understanding** - finds similar declarations even with different wording
- 🎯 **Precise filters** - by manufacturer, product, date, HS code
- 📊 **Explainability** - shows why a declaration is relevant
- 🌍 **Multilingual** - supports Russian, Kazakh, English
- 🔧 **Platform architecture** - customizable schemas for each tenant

## 💰 Business Impact

- **Time savings**: Reduce search time from hours to seconds (99.9% reduction)
- **Cost savings**: $500,000 - $750,000/year for companies processing 10,000 declarations
- **Error reduction**: 30-50% fewer errors using proven precedents
- **Knowledge preservation**: Centralized repository of company expertise
- **ROI**: 500-1000% return on investment in the first year

📖 [Read more about business value](docs/BUSINESS_VALUE.md)

## 🚀 Features

- 🔍 **Hybrid Search**: Combines BM25 (sparse) and vector (dense) search
- 🎯 **Adaptive Reranking**: Automatically selects reranker complexity based on query
- ⏰ **Temporal Awareness**: Accounts for EAEU rule changes over time
- 📊 **Explainability**: Metadata explaining result relevance
- 🌍 **Multilingual**: Supports Russian, Kazakh, English languages
- 🔧 **REST API**: Full-featured API for integration
- 📋 **Dynamic Schemas**: Customizable data schemas for each tenant
- 🔄 **OCR Support**: Process unstructured OCR text as fallback

## 🛠️ Tech Stack

- **Python 3.12+** with **uv** for dependency management
- **FastAPI** for REST API
- **Qdrant** for vector database
- **PostgreSQL** for metadata
- **SentenceTransformers** / **BCEmbedding** for embeddings
- **BGE-Reranker** for reranking

## 📦 Quick Start

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (package manager)
- Docker and Docker Compose

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/FUYOH666/DT-xml.git
cd DT-xml
```

2. **Install dependencies:**
```bash
uv sync
```

3. **Configure environment:**
```bash
cp .env.example .env
# Edit .env file with your settings
```

4. **Start infrastructure:**
```bash
docker-compose up -d
```

5. **Start the server:**
```bash
uv run python -m src.dt_xml.api.main
```

The API will be available at `http://localhost:8000`

## 📖 Usage Examples

### Index a Declaration

```bash
curl -X POST "http://localhost:8000/index" \
  -H "Content-Type: application/json" \
  -d '{
    "tenant_id": "default",
    "xml_content": "<declaration><declaration_number>12345</declaration_number>...</declaration>"
  }'
```

### Search Declarations

```bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Samsung smartphones 2023",
    "tenant_id": "default",
    "top_k": 10,
    "filters": {
      "manufacturer": "Samsung",
      "date_issued": {"gte": "2023-01-01", "lte": "2023-12-31"}
    }
  }'
```

### Python Client Example

```python
import requests

# Search for declarations
response = requests.post(
    "http://localhost:8000/search",
    json={
        "query": "Samsung smartphones",
        "tenant_id": "default",
        "top_k": 10,
        "filters": {"manufacturer": "Samsung"}
    }
)

results = response.json()
for result in results["results"]:
    print(f"Declaration: {result['declaration_id']}")
    print(f"Score: {result['score']}")
    print(f"Content: {result['content'][:100]}...")
```

## 📚 Documentation

- [API Specification](docs/api_spec.md)
- [Data Format Requirements](docs/data_format.md)
- [Architecture Overview](docs/architecture.md)
- [Business Value](docs/BUSINESS_VALUE.md)
- [Tenant Configuration](docs/tenant_configuration.md)
- [Mandatory Fields](docs/mandatory_fields.md)

## 🗺️ Roadmap

### v0.1.0 (Current)
- ✅ Basic search functionality
- ✅ XML/JSON/OCR support
- ✅ Dynamic schemas for tenants
- ✅ Hybrid search (BM25 + Vector)
- ✅ Adaptive reranking

### v0.2.0 (Planned)
- [ ] Web interface for search
- [ ] Export results to Excel/PDF
- [ ] Analytics and statistics
- [ ] Batch indexing

### v0.3.0 (Future)
- [ ] Integration with external systems
- [ ] Mobile application
- [ ] Advanced analytics dashboard

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🌟 Star History

If you find this project useful, please consider giving it a star ⭐

## 📊 Project Statistics

- 📦 **52 Python modules**
- 🔍 **Hybrid search** (BM25 + Vector)
- 🎯 **Adaptive reranking**
- 🌍 **Multilingual support**
- 📋 **Dynamic data schemas**

## 🏷️ Topics

`customs-declarations` `semantic-search` `vector-search` `rag` `logistics` `eaeu` `embeddings` `reranking` `fastapi` `qdrant` `python` `document-search` `ml` `nlp` `hybrid-search` `customs`

## 📞 Contact

- 🌐 Website: [https://scanovich.ai/](https://scanovich.ai/)
- 💬 Telegram: [@ScanovichAI](https://t.me/ScanovichAI)
- 💬 Issues: [GitHub Issues](https://github.com/FUYOH666/DT-xml/issues)
- 📖 Documentation: [docs/](docs/)

---

**Made with ❤️ for logistics companies**
