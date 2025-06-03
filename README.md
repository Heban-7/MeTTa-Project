# MeTTa-Project

# MeTTa ↔ LLM Summarization Project

This repository demonstrates how to integrate MeTTa (a declarative/functional knowledge‐graph DSL) with a Python‐backed LLM to:

1. **Load** raw gene atoms from `data/nodes.metta`.
2. **Extract** key fields for each gene (ID, name, type, chr, start, end, synonyms).
3. **Send** those fields to an LLM for summarization.
4. **Write** both the original fields and the LLM’s summary into `output/summaries.txt`.

---

## Repository Layout

