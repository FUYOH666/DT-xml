# Quick Start Guide

This guide will help you get DT-XML up and running in minutes.

## Prerequisites

Before you begin, ensure you have:

- **Python 3.12+** installed
- **Docker** and **Docker Compose** installed
- **uv** package manager ([installation guide](https://github.com/astral-sh/uv))

## Step 1: Clone the Repository

```bash
git clone https://github.com/FUYOH666/DT-xml.git
cd DT-xml
```

## Step 2: Install Dependencies

```bash
uv sync
```

This will install all required Python packages.

## Step 3: Configure Environment

Copy the example environment file and edit it:

```bash
cp .env.example .env
```

Edit `.env` with your settings (defaults should work for local development).

## Step 4: Start Infrastructure

Start PostgreSQL and Qdrant using Docker Compose:

```bash
docker-compose up -d
```

Wait a few seconds for services to start. Verify they're running:

```bash
docker-compose ps
```

You should see both `postgres` and `qdrant` services running.

## Step 5: Start the API Server

```bash
uv run python -m src.dt_xml.api.main
```

The API will be available at `http://localhost:8000`

## Step 6: Verify Installation

### Check Health

```bash
curl http://localhost:8000/health
```

You should see a JSON response with status "healthy".

### View API Documentation

Open your browser and go to:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Step 7: Index Your First Declaration

### Using XML

```bash
curl -X POST "http://localhost:8000/index" \
  -H "Content-Type: application/json" \
  -d '{
    "tenant_id": "default",
    "xml_content": "<declaration><declaration_number>12345</declaration_number><date_issued>2023-06-15</date_issued><declaration_type>import</declaration_type><manufacturer>Samsung</manufacturer><product_code>8517120000</product_code><product_description>Smartphones</product_description></declaration>"
  }'
```

### Using JSON

```bash
curl -X POST "http://localhost:8000/index" \
  -H "Content-Type: application/json" \
  -d '{
    "tenant_id": "default",
    "json_data": {
      "declaration_number": "12345",
      "date_issued": "2023-06-15",
      "declaration_type": "import",
      "manufacturer": "Samsung",
      "product_code": "8517120000",
      "product_description": "Smartphones"
    }
  }'
```

## Step 8: Search Declarations

```bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Samsung smartphones",
    "tenant_id": "default",
    "top_k": 10
  }'
```

## Next Steps

- Read the [API Specification](api_spec.md) for detailed API documentation
- Check out [Examples](../examples/) for more use cases
- Review [Architecture](architecture.md) to understand the system design
- See [Business Value](BUSINESS_VALUE.md) for use cases

## Troubleshooting

### Port Already in Use

If port 8000 is already in use, change it in `.env`:
```
API_PORT=8001
```

### Docker Services Not Starting

Check Docker logs:
```bash
docker-compose logs
```

### Database Connection Errors

Ensure PostgreSQL is running:
```bash
docker-compose ps postgres
```

Check connection:
```bash
docker-compose exec postgres psql -U dt_xml_user -d dt_xml -c "SELECT 1;"
```

### Qdrant Connection Errors

Ensure Qdrant is running:
```bash
docker-compose ps qdrant
```

Check Qdrant health:
```bash
curl http://localhost:6333/health
```

## Getting Help

- Check [FAQ](FAQ.md) for common questions
- Open an [issue](https://github.com/yourusername/DT-xml/issues) for bugs or questions
- Review [Documentation](README.md) for detailed guides
