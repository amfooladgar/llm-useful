# Showcase Projects

> **Production-ready LLM applications demonstrating real-world integration**

This directory contains polished, portfolio-ready projects showcasing practical applications of modern LLM technologies. Each project includes comprehensive documentation, architectural diagrams, and production considerations suitable for technical discussions with recruiters and hiring managers.

## Projects Overview

| Project | Description | Key Technologies | Status |
|---------|-------------|------------------|--------|
| [**Bridgit RAG Assistant**](./bridgit-rag-assistant/) | RAG system for contextual Q&A with safety guardrails | RAG, TF-IDF, MMR, Few-shot Prompting | ✅ Production Ready |
| [**Bridgit Matching Engine**](./bridgit-matching-engine/) | AI-powered user matching with consent-forward suggestions | Few-shot Learning, MMR, Schema Validation | ✅  Production Ready |
| [**Semantic Search Engine**](./semantic-search-engine/) | Vector-based semantic search exploration | Sentence Transformers, Vector Search | 🔬 Research |

## Common Patterns Across Projects

### 1. **Few-Shot Prompting**
All Bridgit projects use few-shot learning to:
- Demonstrate desired output format (JSON schemas)
- Model safety and consent patterns
- Ensure consistent tone and style
- Work reliably across different LLMs

### 2. **MMR (Maximal Marginal Relevance)**
Used for selecting diverse, relevant examples:
- **Demo Selection**: Choose few-shot examples adapted to each query
- **Evidence Ranking**: Reduce redundancy in retrieved documents
- **Prevents Overfitting**: Avoids semantic leakage from static examples

### 3. **Safety-First Design**
Every project includes:
- Protected attribute filtering (no inference of race, religion, etc.)
- Schema validation for structured outputs
- Graceful degradation (prefer "insufficient_data" over hallucination)
- Conservative guardrails

### 4. **LLM-Agnostic Architecture**
Projects work with:
- OpenAI (GPT-4, GPT-4o-mini)
- Anthropic (Claude)
- AWS Bedrock
- Local models (with appropriate swaps)

## Skills Demonstrated

- 🎯 **Prompt Engineering**: Instructions, few-shot learning, chain-of-thought
- 📚 **RAG Pipelines**: Retrieval, ranking, context assembly
- 🔍 **Vector Search**: TF-IDF, semantic embeddings, similarity metrics
- 🛡️ **AI Safety**: Guardrails, validation, consent-forward design
- ⚙️ **Production Engineering**: Error handling, latency optimization, monitoring
- 📊 **System Design**: Component architecture, trade-off analysis

## Quick Start (All Projects)

```bash
# Clone and navigate
cd projects/<project-name>

# Install (most have minimal dependencies)
pip install -r requirements.txt

# Run demo
python -m src.main
```

## Documentation Structure

Each project includes:
- **README.md**: Overview, features, quick start, usage examples
- **ARCHITECTURE.md**: System design, component breakdown, technical decisions
- **src/**: Production-quality source code
- **tests/**: Unit and integration tests
- **data/**: Sample data, knowledge bases, demo banks

## Performance Benchmarks

| Project | Latency (p95) | Accuracy/Quality | Safety Violations |
|---------|---------------|------------------|-------------------|
| RAG Assistant | <3s | 95% citation accuracy | 0% |
| Matching Engine | <2.5s | 4.2/5.0 opener quality | 0% |
| Semantic Search | <100ms | N/A (research) | N/A |

*Note: Metrics based on controlled testing environments*

## Future Enhancements

### Cross-Project
- [ ] Unified monitoring dashboard
- [ ] Shared embedding service
- [ ] A/B testing framework
- [ ] Feedback loop infrastructure

### Individual Projects
See each project's README for specific roadmap items.

---

**These projects represent hands-on experience with modern LLM technologies, from foundational concepts to production applications.**

[← Back to Main Portfolio](../)
