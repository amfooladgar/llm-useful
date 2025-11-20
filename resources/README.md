# Resources

> **Supporting materials, reference guides, and sample data**

This directory contains reference materials and resources used across the learning notebooks and showcase projects.

## 📂 Contents

### [few_shot_templates.md](./few_shot_templates.md)
**Comprehensive Few-Shot Prompting Guide for Bridgit Social**

Production-ready prompting strategies covering four workloads:
- **Matching**: User-to-user suggestions with conversation starters
- **Classification**: Intent and context label assignment
- **Survey Parsing**: Free-text to structured JSON conversion
- **Support QA (RAG)**: Knowledge base Q&A with citations

**Includes**:
- Prompt templates with schema definitions
- Demo selection strategies (MMR)
- Safety guardrails and refusal patterns
- Evaluation plans and rollout strategies
- Bilingual support (English/Farsi)

**Use Cases**:
- Reference for prompt engineering best practices
- Production deployment templates
- Safety and policy guidelines
- Few-shot example design

---

### Sample Data Files

- **sample.txt**: Example text data for processing
- **elo_ratings.csv**: Sample Elo rating data for evaluation notebooks

---

## 🎯 How to Use

### For Learning:
- Study `few_shot_templates.md` to understand enterprise-grade prompt engineering
- Use sample data files to test implementations
- Reference prompt patterns when building your own applications

### For Projects:
- Adapt few-shot templates for custom use cases
- Use as starting point for prompt versioning and A/B testing
- Reference safety guidelines when building LLM applications

### For Interviews:
- Demonstrate understanding of prompt engineering principles
- Discuss trade-offs (few-shot vs zero-shot vs fine-tuning)
- Explain safety and guardrail strategies

---

## 📝 Notes

The few-shot templates document represents **production-quality prompt engineering** used in the Bridgit Social showcase projects. It demonstrates:
- Structured prompt design (Instructions > Evidence > Demos > Query)
- Safety-first guardrails
- Schema-validated outputs
- Rollout and evaluation strategies

This level of rigor is expected in real-world LLM applications where reliability, safety, and auditability matter.

---

[← Back to Main Portfolio](../)
