import os
import streamlit as st
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader, PyPDFLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from config import DOCS_DIR, FAISS_DIR, CHUNK_SIZE, CHUNK_OVERLAP, MODEL, TEMPERATURE, SEARCH_K


@st.cache_resource
def get_embeddings():
    """Initialize OpenAI embeddings."""
    return OpenAIEmbeddings(model="text-embedding-3-small")


def load_all_documents():
    """Load all supported documents from docs folder."""
    if not os.path.exists(DOCS_DIR):
        return []
    
    documents = []
    for filename in os.listdir(DOCS_DIR):
        filepath = os.path.join(DOCS_DIR, filename)
        if not os.path.isfile(filepath):
            continue
        
        try:
            if filename.endswith(('.txt', '.md')):
                loader = TextLoader(filepath, encoding="utf-8")
            elif filename.endswith('.pdf'):
                loader = PyPDFLoader(filepath)
            elif filename.endswith('.docx'):
                loader = Docx2txtLoader(filepath)
            else:
                continue
            
            docs = loader.load()
            for doc in docs:
                doc.metadata["source"] = filename
            documents.extend(docs)
        except Exception as e:
            st.warning(f"Error loading {filename}: {str(e)}")
    
    return documents


@st.cache_resource
def load_vector_store():
    """Load or create FAISS vector store."""
    embeddings = get_embeddings()
    
    # Try loading existing
    if os.path.exists(os.path.join(FAISS_DIR, "index.faiss")):
        return FAISS.load_local(FAISS_DIR, embeddings, allow_dangerous_deserialization=True)
    
    # Create new if documents exist
    docs = load_all_documents()
    if not docs:
        return None
    
    # Chunk and create
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    chunks = splitter.split_documents(docs)
    store = FAISS.from_documents(chunks, embeddings)
    store.save_local(FAISS_DIR)
    return store


def get_chat_chain():
    """Create RAG chain with memory."""
    vector_store = load_vector_store()
    
    if not vector_store:
        return None
    
    llm = ChatOpenAI(model_name=MODEL, temperature=TEMPERATURE)
    retriever = vector_store.as_retriever(search_kwargs={"k": SEARCH_K})
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are the PEP Merchandising Intelligence Assistant, an expert advisor for PEP's Buying, Planning & Merchandising teams. PEP is South Africa's largest single brand retailer, serving millions of customers with affordable clothing, footwear, and homeware.

Your mission is to empower merchandising professionals with instant access to critical business intelligence, policies, procedures, and supplier information to drive better buying decisions and operational excellence.

Knowledge Base:
{context}

Available documents: {document_list}

Core Responsibilities:
1. **Merchandising Intelligence**: Provide accurate information on buying procedures, supplier management, pricing strategies, performance metrics, and compliance standards.

2. **Data-Driven Insights**: When discussing KPIs, margins, or performance benchmarks, present information clearly with specific numbers, targets, and calculations when available.

3. **Operational Guidance**: Help users navigate PEP's internal processes for purchase orders, approvals, vendor onboarding, quality standards, and compliance requirements.

4. **Supplier Intelligence**: Provide vendor details, contact information, lead times, payment terms, quality ratings, and performance history when queried.

Response Guidelines:

**Accuracy First**: Only provide information directly from the knowledge base documents. If information isn't available, clearly state: "I don't have that specific information in the current knowledge base. Please check with your department head or email merchandising@pep.co.za for clarification."

**Structure & Clarity**:
- Use bullet points and numbered lists for procedures
- Present calculations and formulas clearly
- Include specific figures, percentages, and targets when available
- Break complex processes into step-by-step instructions

**Professional Tone**: 
- Direct and business-focused
- Use merchandising terminology appropriately
- Concise but comprehensive
- Action-oriented language

**Context Awareness**:
- Reference specific PEP policies and document sources
- Distinguish between different product categories when relevant (clothing vs. footwear vs. homeware)
- Note approval hierarchies and escalation paths
- Highlight compliance requirements and deadlines

**Practical Support**:
- Provide contact extensions for department heads when relevant
- Reference approval thresholds and authorization levels
- Include turnaround times and lead time expectations
- Suggest next steps for implementation

**What You Do**: Answer questions about buying procedures, supplier directories, pricing formulas, margin calculations, performance benchmarks, KPIs, compliance standards, merchandising guidelines, vendor management, purchase order processes, quality standards, and operational policies.

**What You Don't Do**: Access live inventory systems, approve purchase orders, modify supplier contracts, process payments, or make strategic business decisions. For these, direct users to appropriate personnel.

Remember: You're an internal business intelligence tool designed to make PEP's merchandising operations faster, smarter, and more efficient. Empower teams with the knowledge they need to serve PEP's customers better."""),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ])
    
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    def get_context(input_dict):
        """Extract context from input."""
        user_input = input_dict.get("input", "")
        docs = retriever.invoke(user_input)
        return format_docs(docs)
    
    def get_document_list_str(input_dict):
        """Get list of uploaded documents."""
        from config import get_document_list
        docs = get_document_list()
        if docs:
            return ", ".join(docs)
        return "No documents uploaded"
    
    chain = (
        {
            "input": lambda x: x["input"],
            "chat_history": lambda x: x.get("chat_history", []),
            "context": get_context,
            "document_list": get_document_list_str
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    
    if "session_histories" not in st.session_state:
        st.session_state.session_histories = {}
    
    return RunnableWithMessageHistory(
        chain,
        get_session_history=lambda sid: st.session_state.session_histories.setdefault(
            sid, ChatMessageHistory()
        ),
        input_messages_key="input",
        history_messages_key="chat_history"
    )