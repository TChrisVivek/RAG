# HR Policy Assistant

An AI-powered HR Policy Assistant built to understand and answer employee questions from company HR policy documents using **Retrieval-Augmented Generation (RAG)**.

The main goal of this project is not just to build a chatbot, but to understand how **RAG and Agentic AI systems work internally**, step by step.

---

# 1. Project Goal

HR teams receive many repetitive questions from employees:

- How many annual leaves do I get?
- How many sick leaves are available?
- How many days of paternity leave are provided?
- Can earned leave be carried forward?
- What is the notice period?
- What is the maternity leave policy?

Instead of requiring HR to answer the same questions repeatedly, this system allows employees to ask questions directly to an AI assistant.

The assistant searches the company's HR policy documents and generates an answer based only on the retrieved policy information.

---

# 2. Main Objective

The project is being built in two stages:

## Stage 1 — RAG

Build a reliable Retrieval-Augmented Generation system.

```text
HR Policy PDF
     ↓
PDF Extraction
     ↓
Text Chunking
     ↓
Embeddings
     ↓
Vector Database
     ↓
Semantic Search
     ↓
Relevant Context
     ↓
LLM
     ↓
Answer
