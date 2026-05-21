# HR Policy RAG Chatbot — Built Without LangChain

> **RAG · OpenAI · Pinecone · Streamlit · Built from Scratch**

A production-style Retrieval-Augmented Generation (RAG) chatbot that answers questions about HR Policy documents — built **entirely from scratch without LangChain**, so every component of the RAG pipeline is handcrafted and fully understood.

> 🔗 Also see the LangChain version: [HR-Policy-RAG-Chatbot-using-Langchain](https://github.com/connectnataraj-boop/HR-Policy-RAG-Chatbot-using-Langchain)

---

## 📌 Table of Contents

- [Why I Built Two Versions](#-why-i-built-two-versions)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Tech Stack](#-tech-stack)
- [How It Works](#-how-it-works)
- [Sample Questions & Answers](#-sample-questions--answers)
- [Key Learnings — Building RAG Without a Framework](#-key-learnings--building-rag-without-a-framework)
- [Setup Instructions](#-setup-instructions)
- [Author](#-author)

---

## 🤔 Why I Built Two Versions

Most GenAI tutorials teach RAG by calling `LangChain` functions — `load_pdf()`, `split_documents()`, `RetrievalQA.from_chain_type()` — without explaining what happens inside.

I wanted to actually understand RAG, not just use it.

So I built it **twice**:

| Version | Approach | Purpose |
|---|---|---|
| **This repo** (Without LangChain) | Every component handwritten in Python | Understand what RAG actually does under the hood |
| [With LangChain](https://github.com/connectnataraj-boop/HR-Policy-RAG-Chatbot-using-Langchain) | LangChain abstractions | Learn the production framework used in real jobs |

Building without the framework first meant that when I used LangChain, I knew exactly what each function was replacing — and why. This also means I can debug production RAG pipelines instead of just calling abstractions.

> *"If you only know LangChain, you know the car. If you know RAG from scratch, you know the engine."*

---

## 🏗️ Architecture

### Indexing Pipeline (Run Once)

```
HR Policy PDF
      │
      ▼
┌─────────────┐
│  load_pdf   │  PyMuPDF — extracts raw text page by page
│    .py      │
└──────┬──────┘
       │  raw text
       ▼
┌─────────────┐
│  chunkers   │  Splits text into overlapping chunks
│    .py      │  chunk_size=500, overlap=50
└──────┬──────┘
       │  list of text chunks
       ▼
┌─────────────┐
│  embedder   │  OpenAI text-embedding-3-small
│    .py      │  converts each chunk → 1536-dim vector
└──────┬──────┘
       │  (chunk_text, embedding_vector) pairs
       ▼
┌─────────────┐
│  vectordb   │  Pinecone upsert
│    .py      │  stores vectors with chunk text as metadata
└─────────────┘
       │
  Pinecone Index  ← ready for querying
```

### Query Pipeline (Every User Question)

```
User Question (Streamlit UI)
       │
       ▼
┌──────────────────┐
│ query_processing │  embed question → 1536-dim vector
│      .py         │  cosine similarity search in Pinecone
└────────┬─────────┘
         │  top-k matching chunks (k=5)
         ▼
┌──────────────────┐
│    RAG_llm.py    │  builds prompt:
│                  │  "Answer using only this context: {chunks}
│                  │   Question: {user_question}"
│                  │  calls GPT-3.5-turbo
└────────┬─────────┘
         │  grounded answer
         ▼
    Streamlit UI  ←  displays answer to user
```

---

## 📂 Project Structure

```
HR-Policy-RAG-Chatbot-without-Langchain/
│
├── load_pdf.py          # PDF text extraction using PyMuPDF
├── chunkers.py          # Text splitting with overlap
├── embedder.py          # OpenAI embedding generation
├── vectordb.py          # Pinecone upsert and similarity search
├── query_processing.py  # Embeds user query, retrieves top-k chunks
├── RAG_llm.py           # Prompt construction + GPT-3.5-turbo call
├── app.py               # Streamlit UI — wires all components together
├── dataprocessor.py     # One-time pipeline: PDF → chunks → embeddings → Pinecone
│
├── resources/           # (gitignored) — add your HR Policy PDF here
├── .env                 # (gitignored) — API keys
├── .gitignore
├── requirements.txt
└── README.md
```

Each file has a **single responsibility** — no 300-line scripts with everything mixed together. This mirrors how real production AI systems are structured.

---

## 🛠️ Tech Stack

| Tool | Role |
|---|---|
| Python | Core language |
| PyMuPDF (fitz) | PDF text extraction |
| OpenAI text-embedding-3-small | Converts text to 1536-dim vectors |
| OpenAI gpt-3.5-turbo | Answer generation from retrieved context |
| Pinecone | Cloud vector database — stores and retrieves embeddings |
| Streamlit | Web UI for the chatbot |
| python-dotenv | Secure API key management |

---

## ⚙️ How It Works

### Step 1 — PDF Loading (`load_pdf.py`)
Reads the HR Policy PDF using PyMuPDF. Extracts raw text page by page, preserving structure.

### Step 2 — Chunking (`chunkers.py`)
Splits the full document text into overlapping chunks of ~500 characters with 50-character overlap. Overlap ensures that sentences at chunk boundaries are not lost during retrieval.

### Step 3 — Embedding (`embedder.py`)
Sends each chunk to OpenAI's `text-embedding-3-small` model. Returns a 1536-dimensional float vector for each chunk — a numerical representation of its meaning.

### Step 4 — Vector Storage (`vectordb.py`)
Upserts all (chunk_id, vector, metadata) tuples into Pinecone. The chunk text is stored as metadata so it can be retrieved alongside the vector.

### Step 5 — Query Processing (`query_processing.py`)
When the user asks a question, it is embedded using the same model. Pinecone performs cosine similarity search and returns the top-5 most relevant chunks.

### Step 6 — Answer Generation (`RAG_llm.py`)
The top-5 chunks are injected into a prompt instructing GPT-3.5-turbo to answer only from the provided context. This prevents hallucination — the model cannot make up answers outside the document.

### Step 7 — Streamlit UI (`app.py`)
User types a question → query pipeline runs → answer displays. Clean, minimal interface.

---

## 💬 Sample Questions & Answers

These are example queries the chatbot handles when loaded with an HR Policy document:

---

**Q: What is the leave policy for casual leave?**
> A: Employees are entitled to 12 days of casual leave per calendar year. Casual leave cannot be carried forward to the next year and must be applied at least 1 day in advance except in emergencies.

---

**Q: How many days of maternity leave are employees entitled to?**
> A: Female employees are entitled to 26 weeks of paid maternity leave as per the Maternity Benefit Act. This is applicable after completing 80 days of service in the 12 months preceding the expected delivery date.

---

**Q: What is the notice period for resignation?**
> A: The notice period is 30 days for employees below manager level and 60 days for manager level and above. The company may waive the notice period at its discretion.

---

**Q: Is work from home allowed?**
> A: Work from home is permitted up to 2 days per week for eligible roles, subject to manager approval. Employees must be reachable during core hours (10 AM – 4 PM) while working remotely.

---

**Q: What expenses are covered under the travel reimbursement policy?**
> A: Business travel expenses including airfare (economy class), hotel accommodation up to ₹4,000/night, and daily allowance of ₹500 for meals are reimbursable with supporting receipts submitted within 7 days of travel.

---

> **Note:** The above answers are illustrative. Actual answers depend on the HR Policy PDF you load. The chatbot answers strictly from the document — it will not fabricate information outside the uploaded policy.

---

## 🧠 Key Learnings — Building RAG Without a Framework

### 1. What chunking actually does — and why overlap matters
When I first chunked without overlap, questions about topics that spanned two chunks returned incomplete answers. Adding 50-character overlap fixed this. LangChain's `RecursiveCharacterTextSplitter` does the same thing — but I wouldn't have understood *why* without building it manually.

### 2. Embeddings are just vectors — similarity is just dot products
The "magic" of semantic search is cosine similarity between two vectors. Once I wrote the embedding and search logic myself, the mystery disappeared. I now understand why changing the embedding model changes retrieval quality.

### 3. Context window management is a real constraint
GPT-3.5-turbo has a token limit. If you pass too many chunks, the API throws an error. I learned to control `top_k` and chunk size together to stay within the limit — something LangChain handles automatically but invisibly.

### 4. Prompt design determines answer quality
The difference between *"Answer this question: {question}"* and *"Answer only using the context below. Do not use outside knowledge. Context: {chunks}. Question: {question}"* is the difference between hallucination and grounded answers. Prompt engineering is a real skill, not just wording.

### 5. Metadata storage in Pinecone is critical
Vectors alone are useless — you need the original chunk text to send to GPT. Storing chunk text as Pinecone metadata and retrieving it alongside vectors is the key architectural decision. Without this, you have the right vector but no text to pass to the LLM.

### 6. Separation of concerns makes debugging fast
Because each step is its own file, when retrieval quality was poor I could test `query_processing.py` independently. When answers were wrong, I isolated `RAG_llm.py`. Monolithic scripts make bugs invisible.

---

## 🚀 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/connectnataraj-boop/HR-Policy-RAG-Chatbot-without-Langchain.git
cd HR-Policy-RAG-Chatbot-without-Langchain
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Create a `.env` File
```
OPENAI_API_KEY=your_openai_key_here
PINECONE_API_KEY=your_pinecone_key_here
PINECONE_INDEX_NAME=your_index_name_here
```

### 4. Add Your HR Policy PDF
```
Create a resources/ folder in the project root
Place your HR Policy PDF inside it
Update the file path in dataprocessor.py and app.py
```

### 5. Run the Indexing Pipeline (Once)
```bash
python dataprocessor.py
```
This loads the PDF, chunks it, embeds it, and upserts to Pinecone. Only needs to run once unless the document changes.

### 6. Launch the App
```bash
streamlit run app.py
```

---


## 👤 Author

**S. Nataraj** — Deep Learning & AI Engineer
Tirupur, Tamil Nadu, India
📧 connectnataraj@outlook.com
🔗 [GitHub](https://github.com/connectnataraj-boop) · [LinkedIn](https://linkedin.com/in/your-profile)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

> *"Most people learn RAG by calling LangChain functions. I learned it by writing every function myself — and now I understand both."*
