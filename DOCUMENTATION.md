# Hollard Policy Assistant - Technical Documentation

**Developer:** Junior Developer  
**Project Type:** RAG Chatbot MVP  
**Status:** Deployed (Proof of Concept)  
**Deployment:** Streamlit Community Cloud  

---

## Project Overview

This is a Retrieval-Augmented Generation (RAG) chatbot I built to help Hollard Insurance customers get instant answers about insurance products and policies. Instead of customers having to search through PDF documents or wait for support, they can just ask questions in plain English.

The assistant knows about life insurance, car insurance, claims procedures, and company information. When it detects that someone needs to actually buy something or needs personalized advice, it hands over to a real person.

---

## What I Built

### Core Features

1. **Smart Document Search**
   - Uploaded 5 markdown documents about Hollard (13,000+ words)
   - System breaks documents into chunks and creates vector embeddings
   - When user asks a question, it finds the most relevant chunks
   - Sends those chunks + question to GPT-4 for an accurate answer

2. **Conversation Memory**
   - Chat remembers previous messages in the conversation
   - Can handle follow-up questions naturally
   - Context is maintained throughout the session

3. **Handover Detection**
   - Automatically detects when user needs human help
   - Triggers: requesting quotes, purchases, complaints, account changes
   - Ends session cleanly and shows contact information
   - Prevents AI from trying to handle things it shouldn't

4. **Document Management**
   - Users can upload additional documents via sidebar
   - Supports TXT, PDF, DOCX, and Markdown files
   - Files are validated (size, format, duplicates)
   - Vector store rebuilds automatically when docs change

### UI/UX Decisions

**Branding:**
- Used Hollard's official purple colors (#6B1E9E) and logo
- Kept it professional - not too flashy or playful
- Compact sizing - hiring manager feedback led me to reduce all padding/fonts

**User Flow:**
- Welcome screen explains what the assistant can do
- Clear indication when documents are loading
- Chat disables when no documents uploaded
- Session ends gracefully when handover needed
- Simple "Clear Chat" button to reset

---

## Technical Architecture

### Stack Choice

I chose these technologies because they're what I could learn quickly and deploy for free:

- **Streamlit** - Fast prototyping, built-in chat UI, easy deployment
- **LangChain** - Handles the RAG pipeline complexity for me
- **OpenAI GPT-4** - Best quality answers, reliable API
- **FAISS** - Fast vector search, works locally and in cloud
- **Python 3.11** - What I'm most comfortable with

### How It Works

```
User Question
    ↓
Vector Search (find relevant document chunks)
    ↓
Retrieve Top 3 chunks
    ↓
Build prompt: System Context + Retrieved Chunks + Chat History + Question
    ↓
Send to GPT-4
    ↓
Get Answer
    ↓
Check if handover needed
    ↓
Display answer OR end session
```

### File Structure

```
app.py              - Main Streamlit UI and chat logic
rag_engine.py       - RAG pipeline: embeddings, vector store, chat chain
config.py           - Settings and file operations
utils.py            - Text extraction from different file types
requirements.txt    - Python dependencies
.env               - API keys (not in git)

data/
  documents/       - Knowledge base markdown files
  faiss_store/     - Vector embeddings (regenerates automatically)

tests/             - Unit tests (75 tests, 77% coverage)
```

---

## Challenges I Faced

### 1. Deployment Hell

**Problem:** First deployment to Streamlit Cloud failed with "no API key" error.

**What I learned:** Environment variables don't transfer from local .env files. Had to use Streamlit's Secrets feature.

**Solution:** Added `OPENAI_API_KEY` to Streamlit Cloud dashboard under Secrets.

---

### 2. Missing Knowledge Base

**Problem:** Second deployment worked but had no answers - vector store was empty.

**Root cause:** The `data/documents/` folder was in `.gitignore` so files never got pushed to GitHub.

**Solution:**
- Commented out `data/documents/` from `.gitignore`
- Created all 5 markdown knowledge base files
- Committed and pushed to GitHub
- App rebuilt vector store on deployment

---

### 3. Security Incident

**Problem:** Accidentally exposed my OpenAI API key in chat when asking for help.

**What I did:**
- Immediately replaced key in `.env` with placeholder
- Verified `.env` was never committed to git (it wasn't)
- Advised to revoke exposed key at OpenAI platform
- Created new API key

**Lesson learned:** Never share `.env` file contents, even in support chats.

---

### 4. UI Too Big

**Problem:** Hiring manager said UI looked "cartoonish" with oversized icons and text.

**Solution:** Went through 3 iterations of size reductions:
- Reduced header from 45px to 30px logo
- Reduced icons from 2rem to 1rem
- Reduced button padding and font sizes
- Tightened spacing throughout
- Result: More professional, business-appropriate look

---

## Testing Approach

I wrote 75 unit tests to make sure the core functionality works:

**test_config.py** - 22 tests
- File validation (extensions, size limits, empty files)
- Atomic file writes (prevents corruption)
- Configuration constants

**test_utils.py** - 10 tests
- Text extraction from PDF, DOCX, TXT, MD
- Unicode handling
- Edge cases

**test_rag_engine.py** - 18 tests
- Document loading
- Vector store creation
- Chat chain configuration
- System prompt validation

**test_app_functions.py** - 19 tests
- Handover detection logic
- Session state management
- UI component rendering (some failing due to Streamlit mocking issues)

**Coverage:** 77% overall

**How to run:**
```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

---

## Deployment Process

### Local Testing
```bash
# Set up environment
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# Add API key
echo OPENAI_API_KEY=your_key > .env

# Run locally
streamlit run app.py
```

### Streamlit Cloud Deployment

1. Pushed code to GitHub: `Kayanja2023/Rag`
2. Branch: `feature/policy-assistant-poc`
3. Connected to Streamlit Cloud
4. Added API key to Secrets:
   ```toml
   OPENAI_API_KEY = "sk-..."
   ```
5. App auto-deploys on git push

**Live URL:** ai-hollard.streamlit.app

---

## What I'd Improve With More Time

### Immediate Fixes
- Fix the 5 failing Streamlit UI tests (mocking issues)
- Add callback form that emails submissions to support team
- Better error handling when OpenAI API is down
- Loading states for document upload progress

### Future Enhancements
- **Analytics:** Track most-asked questions to improve knowledge base
- **Multi-language:** Support Afrikaans, Zulu, Xhosa
- **Voice Input:** For accessibility
- **Live Chat Integration:** Connect handover to actual support system
- **Better Search:** Implement hybrid search (keyword + semantic)

---

## Lessons Learned

1. **RAG is powerful but needs good content** - Spent more time writing knowledge base docs than coding
2. **Deployment is different from local** - Environment, paths, secrets all work differently
3. **UI matters** - Even for an MVP, professional appearance builds trust
4. **Test early** - Wish I'd written tests before deployment, would've caught the empty documents issue
5. **Git hygiene** - Double-check `.gitignore` before first commit

---

## Knowledge Base Content

I researched Hollard's website and created 5 comprehensive guides:

| File | Topic | Words |
|------|-------|-------|
| `hollard-products-overview.md` | All insurance products | ~2,800 |
| `hollard-faqs.md` | Common customer questions | ~1,800 |
| `life-insurance-basics.md` | Life insurance explained | ~3,500 |
| `claims-process.md` | How to file claims | ~3,000 |
| `about-hollard.md` | Company info, Better Futures | ~2,200 |

**Total:** 13,300 words of domain knowledge

---

## Performance Notes

**Response Time:** 2-4 seconds average (depends on OpenAI API)  
**Vector Search:** <100ms (FAISS is fast)  
**Accuracy:** Good when answer is in docs, correctly says "I don't know" when it isn't  

**Limitations:**
- Can't handle account-specific queries (by design - triggers handover)
- Limited to information in uploaded documents
- Requires internet connection for OpenAI API

---

## Git Workflow

I used feature branch workflow:

```bash
# Created feature branch
git checkout -b feature/policy-assistant-poc

# Multiple commits as I built features:
- Initial Hollard rebrand
- Added knowledge base documents
- Implemented handover mechanism
- Redesigned to minimalistic UI
- Added unit tests
- Fixed deployment issues
- UI refinements

# Pushed to GitHub
git push origin feature/policy-assistant-poc
```

**Commits:** 8 total on feature branch  
**Ready to merge:** Yes, once deployment verified

---

## Configuration

Key settings in `config.py`:

```python
CHUNK_SIZE = 1000           # How big to split documents
CHUNK_OVERLAP = 200         # Overlap for context continuity
MODEL = "gpt-4"             # OpenAI model to use
TEMPERATURE = 0.7           # Response creativity
SEARCH_K = 3                # Number of document chunks to retrieve
MAX_FILE_SIZE = 50MB        # Upload limit
```

These worked well, didn't need to tune much.

---

## Dependencies

Main libraries used:

```
streamlit==1.30.0           # UI framework
langchain==0.3.9            # RAG framework
langchain-openai           # OpenAI integration
faiss-cpu==1.13.0          # Vector search
openai                     # GPT-4 API
python-dotenv              # Environment variables
PyPDF2, python-docx        # Document parsing
```

Total: 97 packages including dependencies

---

## Questions I Can Answer

**Technical:**
- How does the RAG pipeline work?
- Why did you choose FAISS over alternatives?
- How does handover detection work?
- What's the test coverage strategy?

**Product:**
- How do users interact with the assistant?
- What happens when it doesn't know an answer?
- How do you add new knowledge to the system?

**Deployment:**
- What issues did you face going to production?
- How is it currently hosted?
- What would it take to scale this?

---

## Contact

**Repository:** https://github.com/Kayanja2023/Rag  
**Branch:** feature/policy-assistant-poc  
**Deployed App:** ai-hollard.streamlit.app  

---

*Built as a proof-of-concept for Hollard Insurance customer support automation.*
