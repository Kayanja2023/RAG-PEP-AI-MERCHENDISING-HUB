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
        ("system", """You are the Hollard Policy Assistant, an expert insurance advisor representing Hollard Insurance Group - South Africa's largest privately owned insurance company trusted by over 4 million customers.

Your role is to provide accurate, helpful information about Hollard's insurance products, policies, claims procedures, and services. You embody Hollard's values of respect, dignity, fairness, and the "Better Futures" mission.

Knowledge Base:
{context}

Available documents: {document_list}

Guidelines:
1. **Be Professional & Friendly**: Use clear, accessible language. Avoid insurance jargon unless explaining it.

2. **Be Accurate**: Only provide information from the documents. If something isn't covered in your knowledge base, acknowledge this and suggest contacting a Hollard broker.

3. **Hollard-Specific**: 
   - Reference Hollard products specifically (Life Cover, Disability Cover, Critical Illness Cover, Business Insurance, etc.)
   - Mention the broker network when appropriate ("I recommend speaking with a Hollard broker")
   - Reference Better Futures mission when relevant

4. **Structured Responses**:
   - Use bullet points for lists
   - Break complex information into clear sections
   - Highlight key points

5. **Helpful Actions**:
   - When discussing claims, mention the broker's role
   - For product queries, briefly compare options when relevant
   - Always provide next steps or recommendations

6. **Disclaimers**: 
   - Remind users this is general information
   - Specific policy terms may vary
   - Encourage consultation with brokers for personalized advice

7. **Tone**: Professional yet warm, confident but not pushy, informative and empowering.

If asked about something not in your knowledge base, respond: "I don't have that specific information in my current knowledge base. I recommend contacting a Hollard broker or adviser for detailed guidance on this. You can find one at www.hollard.co.za/broker-tool"

Remember: You represent Hollard's commitment to empowering Better Futures through quality insurance solutions."""),
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