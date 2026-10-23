# RAG Demo for VS Code

A beginner-friendly, end-to-end Retrieval-Augmented Generation (RAG) demonstration using:
- Python
- An existing PDF or TXT document
- OpenAI embeddings (`text-embedding-3-small`)
- NumPy cosine-similarity retrieval (visible and implemented locally)
- OpenAI Responses API for answer generation

## What the demo shows

1. Load PDF/TXT documents from `documents/`
2. Extract text and preserve source/page metadata
3. Split text into overlapping chunks
4. Generate embeddings with the OpenAI API
5. Save a local index (`data/rag_index.json`)
6. Embed a user question
7. Retrieve top matching chunks using cosine similarity
8. Add retrieved chunks to the prompt
9. Generate a grounded answer with the OpenAI API
10. Display retrieved evidence and similarity scores

## Requirements

- Python 3.10+ (recommended)
- An OpenAI API key with API access and available credits
- VS Code with the Python extension

## Setup in VS Code

### 1. Extract the ZIP and open the folder
Open `rag_demo_vscode` in VS Code.

### 2. Create a virtual environment

macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure your API key

macOS/Linux:
```bash
export OPENAI_API_KEY="YOUR_API_KEY"
```

Windows PowerShell:
```powershell
$env:OPENAI_API_KEY="YOUR_API_KEY"
```

Optional: choose a generation model available to your account:
```bash
# macOS/Linux
export OPENAI_MODEL="gpt-4.1"
```
```powershell
# Windows PowerShell
$env:OPENAI_MODEL="gpt-4.1"
```

Do not put your API key in source code or commit it to Git.

### 5. Add your own document
Put one or more `.pdf` or `.txt` files inside `documents/`.
A sample `sample_employee_handbook.txt` is already included so the demo can run against a sample knowledge base once the API key is configured.

### 6. Run the demo
```bash
python main.py
```

On first run, the program extracts text, chunks it, creates embeddings, and saves the local index. On later runs it reuses the index unless you choose to rebuild it.

## Suggested classroom demonstration

Ask:
- How many annual leave days are provided?
- Who approves casual leave?
- What should an employee do if a company laptop is stolen?
- Can passwords be shared?
- What is the work-from-home allowance?

The last question is deliberately not answered by the sample policy. Observe how the prompt tells the model to admit when the supplied context is insufficient.

## Important details

- PDF text extraction uses `pypdf`. Scanned/image-only PDFs require OCR before they can be processed.
- Embedding and answer generation use the OpenAI API and incur API usage charges.
- Retrieval is implemented locally with NumPy, so the similarity calculations are visible in the code.
- This is a teaching example, not a production-secure application. It does not include authentication, access control, robust evaluation, or a relevance threshold.
- The local JSON index contains extracted document text and embeddings. Keep it private if your documents are confidential.
