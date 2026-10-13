# HR Policy Assistant

An AI-powered HR Policy Assistant that answers employee questions using company HR policy documents through **Retrieval-Augmented Generation (RAG)** and **Agentic AI**.

The goal is to understand and build RAG and agentic systems step by step, from document processing to intelligent tool usage.

## 1. Project Goal

HR teams receive repetitive questions from employees, such as:

- How many annual leave days are available?
- How many days of paternity leave are provided?
- Can earned leave be carried forward?
- What is the notice period?
- What is the maternity leave policy?

This application helps answer these questions by retrieving relevant information from HR policy documents and using an LLM to generate grounded responses.

## 2. Project Architecture

### Stage 1 — Retrieval-Augmented Generation (RAG)

The RAG pipeline processes policy documents and retrieves relevant context before generating an answer.

```text
HR Policy PDF
     ↓
PDF Text Extraction
     ↓
Text Chunking
     ↓
Embedding Generation
     ↓
ChromaDB Vector Store
     ↓
Semantic Search
     ↓
Relevant Context
     ↓
OpenAI GPT-4.1
     ↓
Grounded Answer
```

### Stage 2 — Agentic AI

The agent uses tools to answer questions, retrieve policy information, and look up employee information.

```text
User Question
     ↓
Agent (OpenAI GPT-4.1)
     ↓
Tool Selection
     ├── HR Policy Search
     └── Employee Information Lookup
     ↓
Tool Results
     ↓
Agent Response
```

The agent can also use conversation history to handle follow-up questions within a conversation.

## 3. Technology Stack

- **Language:** Python
- **Backend:** FastAPI
- **LLM:** OpenAI GPT-4.1
- **PDF Processing:** PyMuPDF
- **Embeddings:** Sentence Transformers (`all-MiniLM-L6-v2`)
- **Vector Database:** ChromaDB
- **API Testing:** FastAPI Swagger UI
- **Automated Testing:** pytest

## 4. Implemented Features

- Extract text from PDF documents.
- Split extracted text into chunks.
- Generate embeddings for semantic search.
- Store and retrieve document chunks using ChromaDB.
- Search HR policies using natural-language questions.
- Generate answers using retrieved context and an LLM.
- Look up employee information using employee IDs.
- Use agent tools to retrieve information.
- Maintain conversation history for follow-up questions.
- Handle empty inputs, missing results, and tool failures.
- Record application events using logging.
- Run automated tests for employee lookup and policy search.

## 5. API Endpoints

The backend includes the following main endpoints:

- `/agent-chat` — Interact with the AI agent.
- `/docs` — Explore and test the API through Swagger UI.

Other endpoints may be available for document uploads and direct chat, depending on the current application configuration.

## 6. Running the Project Locally

### Prerequisites

- Python 3.12
- An OpenAI API key

### Setup

```bat
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the appropriate backend configuration location and add your OpenAI API key:

```text
OPENAI_API_KEY=your_api_key_here
```

Never commit your actual API key to GitHub.

### Start the backend

```bat
uvicorn main:app --reload
```

Open the Swagger UI:

http://127.0.0.1:8000/docs

## 7. Automated Tests

Run the automated test suite from the `backend` directory:

```bat
pytest -v
```

The current test suite covers employee lookup and HR policy search, including successful results, invalid inputs, missing information, and search failures.

## 8. Project Status

- **RAG pipeline:** Implemented and tested.
- **Agent and tool integration:** Implemented.
- **Employee lookup and policy search tests:** Passing (8 tests in the current suite).

The project is being developed incrementally, with further improvements and testing planned.