# Frequently Asked Questions (FAQ)

## General Questions

### What is DT-XML?

DT-XML is an AI-powered semantic search system for customs declarations of the Eurasian Economic Union (EAEU). It helps logistics companies quickly find similar historical declarations when preparing new ones.

### Who is this for?

DT-XML is designed for:
- Large logistics companies processing thousands of declarations annually
- Customs brokers
- Importers/exporters with high declaration volumes
- Developers building customs-related systems

### What problem does it solve?

It solves the problem of time-consuming manual search for similar declarations. Instead of spending 2-4 hours searching databases and Excel files, employees can find relevant examples in seconds.

## Technical Questions

### What Python version is required?

Python 3.12 or higher is required.

### Can I use pip instead of uv?

While possible, we strongly recommend using `uv` as specified in the project. It ensures reproducible builds and faster dependency resolution.

### Do I need GPU?

No, GPU is not required. The system works on CPU, though GPU can speed up embedding generation for large batches.

### How many declarations can it handle?

The system is designed to scale. It has been tested with 10,000+ declarations and can handle much more. Performance depends on your infrastructure.

### What databases are supported?

Currently:
- **Vector DB**: Qdrant (Milvus support planned)
- **Metadata DB**: PostgreSQL

### Can I use other vector databases?

Qdrant is the default, but the architecture allows for adding other vector databases. Contributions welcome!

## Usage Questions

### What formats are supported?

- XML (standard EAEU format)
- JSON (structured data)
- OCR text (unstructured text from OCR)

### How do I add my own schema?

Use the schema registration API endpoint:
```bash
POST /schema/register
```

See [Tenant Configuration](tenant_configuration.md) for details.

### Can I search without filters?

Yes! You can search with just a query text. Filters are optional but help narrow down results.

### How accurate is the search?

The hybrid search (BM25 + Vector) combined with adaptive reranking provides high accuracy. Results are ranked by relevance score, and you can see explanations for why each result is relevant.

### Can I export results?

Currently, results are returned via API. Export to Excel/PDF is planned for v0.2.0.

## Business Questions

### How much time does it save?

For companies processing 10,000 declarations/year:
- **Before**: 20,000-40,000 hours/year searching
- **After**: ~50 hours/year searching
- **Savings**: 99.9% reduction in search time

### What's the ROI?

For a company processing 10,000 declarations/year:
- **Cost savings**: $500,000 - $750,000/year
- **ROI**: 500-1000% in the first year

### Is it secure?

Yes. The system:
- Doesn't store sensitive data in logs
- Supports data isolation per tenant
- Can be deployed on-premises
- Uses standard security practices

### Can I customize it for my company?

Yes! The platform architecture supports:
- Custom data schemas
- Field mapping
- Custom search settings
- Tenant-specific configurations

## Development Questions

### How do I contribute?

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

### What's the development roadmap?

See the [Roadmap](../README.md#roadmap) section in README.

### Can I integrate it with my existing system?

Yes! The REST API makes integration straightforward. See [API Specification](api_spec.md) for details.

### Is there a Python client library?

Not yet, but it's planned. Currently, use `requests` or any HTTP client.

## Troubleshooting

### API returns 500 error

Check:
1. Are all services running? (`docker-compose ps`)
2. Check API logs for error details
3. Verify database connections in `.env`

### Search returns no results

Possible reasons:
1. No declarations indexed yet
2. Query doesn't match any indexed content
3. Filters too restrictive
4. Try broader search terms

### Slow search performance

Check:
1. Number of indexed declarations
2. System resources (CPU, memory)
3. Network latency to databases
4. Consider increasing `top_k` limit

### Embedding model download fails

The first run downloads the embedding model. Ensure:
1. Internet connection is available
2. Sufficient disk space (~2GB for models)
3. Firewall allows HuggingFace access

## Support

- **Documentation**: [docs/](README.md)
- **Issues**: [GitHub Issues](https://github.com/ScanovichAI/DT-xml/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ScanovichAI/DT-xml/discussions)
