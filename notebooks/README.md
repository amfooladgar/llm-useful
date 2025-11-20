# Learning Notebooks

> **Educational materials covering LLM concepts from fundamentals to advanced topics**

This directory contains hands-on Jupyter notebooks that build understanding of Large Language Models from the ground up. Each notebook includes implementations, explanations, and practical examples.

## 📖 Recommended Learning Path

```
01-Fundamentals → 02-Architectures → 03-Inference → 04-Evaluation → 05-Advanced
```

Work through sections sequentially for best comprehension, or jump to specific topics as needed.

---

## 📚 Sections

### [01 - Fundamentals](./01-fundamentals/)
**Core building blocks of LLMs**

- **Tokenization**: BPE algorithm, vocabulary building, encoding/decoding
- **Embeddings**: Skip-gram, Word2Vec, sentence transformers
- **Normalization**: Layer normalization vs batch normalization

**Prerequisites**: Basic Python, linear algebra  
**Time**: ~3-4 hours

---

### [02 - Architectures](./02-architectures/)
**Transformer components and optimizations**

- **Attention Mechanisms**: Self-attention, multi-head attention, cross-attention, masking  
- **Positional Encoding**: How transformers handle sequence order
- **Optimizations**: LoRA (Low-Rank Adaptation), FlashAttention

**Prerequisites**: 01-Fundamentals, matrix operations  
**Time**: ~5-6 hours

---

### [03 - Inference Techniques](./03-inference-techniques/)
**Generation strategies and prompting**

- **Beam Search**: Sequence generation beyond greedy decoding
- **Chain-of-Thought**: Step-by-step reasoning prompting
- **Synthetic Data**: Techniques for data augmentation

**Prerequisites**: Understanding of LLM basics  
**Time**: ~2-3 hours

---

### [04 - Evaluation](./04-evaluation/)
**Measuring model performance**

- **Evaluation Techniques**: Perplexity, BLEU, ROUGE, F1, task-specific metrics
- **Elo Rating System**: Pairwise model comparison

**Prerequisites**: Basic statistics  
**Time**: ~2 hours

---

### [05 - Advanced Concepts](./05-advanced-concepts/)
**Specialized topics**

- **Diffusion Models**: Generative modeling fundamentals

**Prerequisites**: Strong understanding of neural networks  
**Time**: ~3-4 hours

---

## 🎯 How to Use These Notebooks

### For Learning:
1. Start at [01-Fundamentals](./01-fundamentals/) if new to LLMs
2. Read code + explanations carefully
3. Run cells and experiment with parameters
4. Try modifying implementations
5. Reference [showcase projects](../projects/) to see concepts in production

### For Reference:
- Jump to specific topics as needed
- Use as implementation templates
- Compare with your own approaches

### For Interviews:
- Review implementations before technical discussions
- Understand trade-offs (e.g., why LoRA vs full fine-tuning)
- Practice explaining concepts clearly

---

## 🔗 Connections to Showcase Projects

| Notebook Topic | Related Project | Application |
|----------------|-----------------|-------------|
| Tokenization | All projects | Input processing |
| Embeddings | Semantic Search, RAG | Document retrieval |
| Attention | All projects | Understanding transformers |
| Few-Shot (resources/) | Matching, RAG | Prompt engineering |
| Evaluation | All projects | Quality metrics |

---

## 📂 Quick Navigation

```
notebooks/
├── 01-fundamentals/
│   ├── tokenization/
│   │   ├── Tokenization.ipynb
│   │   └── tokenizer_model/
│   ├── embeddings/
│   │   └── Embeddings.ipynb
│   └── normalization/
│       └── Layer_vs_batch_norm.ipynb
├── 02-architectures/
│   ├── attention/
│   │   ├── single_vs_multihead_SelfAttention.ipynb
│   │   ├── cross-attention.ipynb
│   │   ├── masking.ipynb
│   │   └── FlashAttention_implementation.ipynb
│   ├── positional-encoding/
│   │   └── positional_encoding.ipynb
│   └── optimizations/
│       └── lora_forwardPass.ipynb
├── 03-inference-techniques/
│   ├── BeamSearch.ipynb
│   ├── ChainOfThought.ipynb
│   └── Synthetic_Techniques.ipynb
├── 04-evaluation/
│   ├── Evaluation_techniques.ipynb
│   └── Elo_rating_system.ipynb
└── 05-advanced-concepts/
    └── diffusion/
        └── Diffusion_models.ipynb
```

---

## 💡 Tips

- **Jupyter Setup**: Install with `pip install jupyter` if needed
- **Dependencies**: Most notebooks have minimal requirements (numpy, matplotlib)
- **Runtime**: Use GPU for diffusion models if available
- **Modifications**: Feel free to experiment! Change hyperparameters, try different datasets

---

[← Back to Main Portfolio](../) | [View Showcase Projects](../projects/)
