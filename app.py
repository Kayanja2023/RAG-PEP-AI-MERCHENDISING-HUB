import os
import hashlib
import streamlit as st
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime
from rag_engine import get_chat_chain, load_all_documents
from config import (get_document_list, delete_document, validate_file, 
                   clear_vector_store, atomic_write, get_unique_filename, DOCS_DIR)

load_dotenv()

# Page configuration for PEP Merchandising Assistant
st.set_page_config(
    page_title="PEP Merchandising Assistant",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

def add_styling():
    st.markdown("""
        <style>
        /* PEP Brand Colors */
        :root {
            --pep-red: #E30613;
            --pep-red-dark: #B30510;
            --pep-blue: #1E3A8A;
            --pep-blue-light: #3B82F6;
            --pep-gray: #4B5563;
            --pep-bg: #F8FAFC;
        }
        
        /* Main background - pure white */
        .main {
            background-color: #FFFFFF;
        }
        
        /* Primary buttons - PEP red with professional styling */
        .stButton > button {
            background-color: #E30613;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 6px 14px;
            font-size: 12px;
            font-weight: 500;
            box-shadow: 0 1px 4px rgba(227, 6, 19, 0.1);
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            background-color: #B30510;
            box-shadow: 0 2px 8px rgba(227, 6, 19, 0.18);
            transform: translateY(-1px);
        }
        
        /* Secondary delete buttons - light styling */
        .stButton > button[kind="secondary"] {
            background-color: #F5F5F5;
            color: #666666;
            border: 1px solid #E0E0E0;
            padding: 3px 8px;
            font-size: 11px;
            border-radius: 8px;
            box-shadow: none;
        }
        
        .stButton > button[kind="secondary"]:hover {
            background-color: #FEE2E2;
            color: #B30510;
            border-color: #E30613;
        }
        
        /* Sidebar - light blue/gray background */
        [data-testid="stSidebar"] {
            background-color: #F8FAFC;
            max-width: 280px;
            border-right: 2px solid #E5E7EB;
        }
        
        [data-testid="stSidebar"] > div:first-child {
            padding-top: 1rem;
        }
        
        /* Sidebar headers - PEP blue */
        [data-testid="stSidebar"] h2 {
            color: #1E3A8A;
            font-size: 0.95rem;
            font-weight: 600;
            margin-bottom: 0.4rem;
        }
        
        [data-testid="stSidebar"] h3 {
            color: #1E3A8A;
            font-size: 0.9rem;
            font-weight: 500;
            margin-bottom: 0.4rem;
        }
        
        /* File uploader styling */
        [data-testid="stFileUploader"] {
            border: 2px dashed #1E3A8A;
            border-radius: 10px;
            padding: 0.75rem;
            background-color: #FFFFFF;
        }
        
        /* Chat input styling */
        .stChatInput {
            border-color: #1E3A8A;
            border-radius: 16px;
        }
        
        /* Success messages */
        .stSuccess {
            background-color: #DBEAFE;
            color: #1E3A8A;
            border-left: 4px solid #3B82F6;
            border-radius: 16px;
        }
        
        /* Info messages */
        .stInfo {
            background-color: #F8FAFC;
            color: #1E3A8A;
            border-left: 4px solid #3B82F6;
            border-radius: 16px;
        }
        
        /* Dividers */
        hr {
            border-color: #E5E7EB;
        }
        
        /* Chat messages */
        .stChatMessage {
            border-radius: 10px;
            padding: 0.75rem;
            margin-bottom: 0.4rem;
        }
        
        /* User messages - light blue */
        [data-testid="stChatMessage"]:has([data-testid="stChatMessageContent"]:first-child) {
            background-color: #DBEAFE;
        }
        
        /* Headers */
        h1, h2, h3 {
            color: #333333;
        }
        
        /* Body text */
        p {
            color: #666666;
        }
        
        /* Links */
        a {
            color: #1E3A8A;
        }
        
        a:hover {
            color: #E30613;
        }
        </style>
    """, unsafe_allow_html=True)

def show_welcome_message(docs_exist, messages_exist):
    """Display contextual welcome message based on app state."""
    if not docs_exist and not messages_exist:
        # First-time user - no documents, no chat
        st.markdown("""
            <div style='background: linear-gradient(135deg, #F8FAFC 0%, #FFFFFF 100%);
                        padding: 18px;
                        border-radius: 10px;
                        border: 1px solid #E5E7EB;
                        margin-bottom: 16px;
                        text-align: center;'>
                <h2 style='color: #E30613; margin: 0 0 8px 0; font-size: 1.1rem; font-weight: 600;'>
                    <span style='font-size: 0.9rem;'>📊</span> Welcome to PEP Merchandising Assistant!
                </h2>
                <p style='color: #1E3A8A; font-size: 0.85rem; line-height: 1.4; margin: 6px 0;'>
                    Quick access to buying, planning, and merchandising information.
                </p>
                <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 10px; margin-top: 12px;'>
                    <div style='background: #FFFFFF; padding: 10px; border-radius: 6px; border: 1px solid #E5E7EB;'>
                        <div style='font-size: 1rem; margin-bottom: 4px;'>📊</div>
                        <strong style='color: #E30613; font-size: 0.85rem;'>Performance Data</strong>
                        <p style='color: #666666; font-size: 0.75rem; margin: 3px 0 0 0;'>KPIs, benchmarks, trends</p>
                    </div>
                    <div style='background: #FFFFFF; padding: 10px; border-radius: 6px; border: 1px solid #E5E7EB;'>
                        <div style='font-size: 1rem; margin-bottom: 4px;'>📦</div>
                        <strong style='color: #E30613; font-size: 0.85rem;'>Vendor Information</strong>
                        <p style='color: #666666; font-size: 0.75rem; margin: 3px 0 0 0;'>Contacts, lead times</p>
                    </div>
                    <div style='background: #FFFFFF; padding: 10px; border-radius: 6px; border: 1px solid #E5E7EB;'>
                        <div style='font-size: 1rem; margin-bottom: 4px;'>📋</div>
                        <strong style='color: #E30613; font-size: 0.85rem;'>Procedures & Policies</strong>
                        <p style='color: #666666; font-size: 0.75rem; margin: 3px 0 0 0;'>Workflows, approvals</p>
                    </div>
                    <div style='background: #FFFFFF; padding: 10px; border-radius: 6px; border: 1px solid #E5E7EB;'>
                        <div style='font-size: 1rem; margin-bottom: 4px;'>💰</div>
                        <strong style='color: #E30613; font-size: 0.85rem;'>Pricing & Margins</strong>
                        <p style='color: #666666; font-size: 0.75rem; margin: 3px 0 0 0;'>Calculations, guidelines</p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    elif docs_exist and not messages_exist:
        # Documents uploaded but no chat started
        st.markdown("""
            <div style='background: #DBEAFE;
                        padding: 20px 24px;
                        border-radius: 12px;
                        margin-bottom: 20px;
                        border-left: 4px solid #1E3A8A;'>
                <p style='color: #1E3A8A; margin: 0; font-size: 1rem;'>
                    ✨ <strong>Ready!</strong> Ask me about procedures, vendor info, pricing formulas, or performance benchmarks.
                </p>
            </div>
        """, unsafe_allow_html=True)

def show_internal_contacts():
    """Display internal PEP department contacts for additional support."""
    st.markdown("""
        <div style='background: #F8FAFC; padding: 14px; border-radius: 8px; 
                    border: 1px solid #E5E7EB; margin-top: 12px;'>
            <p style='color: #1E3A8A; margin: 0 0 10px 0; font-weight: 600; font-size: 0.85rem;'>ℹ️ Need Additional Support?</p>
            <div style='color: #666; font-size: 0.8rem; line-height: 1.6;'>
                <p style='margin: 5px 0;'><span style='font-size: 0.85rem;'>📞</span> <strong>Buying Manager:</strong> Ext 2401</p>
                <p style='margin: 5px 0;'><span style='font-size: 0.85rem;'>📞</span> <strong>Merchandising Head:</strong> Ext 2405</p>
                <p style='margin: 5px 0;'><span style='font-size: 0.85rem;'>📞</span> <strong>Planning Director:</strong> Ext 2410</p>
                <p style='margin: 5px 0;'><span style='font-size: 0.85rem;'>✉️</span> <strong>Email:</strong> merchandising@pep.co.za</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

def show_header():
    st.markdown("""
        <div style='background: linear-gradient(135deg, #E30613 0%, #B30510 100%); 
                    padding: 14px 20px; 
                    border-radius: 10px; 
                    margin-bottom: 16px;
                    box-shadow: 0 2px 8px rgba(227, 6, 19, 0.12);'>
            <div style='text-align: center;'>
                <h1 style='color: #FFFFFF; margin: 0; font-size: 1.2rem; font-weight: 600; letter-spacing: 0.3px;'>
                    📊 PEP Merchandising Assistant
                </h1>
                <p style='color: #FEE2E2; margin: 3px 0 0 0; font-size: 0.75rem; font-weight: 400;'>
                    Your Merchandising Knowledge Hub
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Helper function for file signature tracking
def get_file_signature(uploaded_file):
    """Create unique signature for uploaded file to track processing."""
    try:
        # Read first 1KB for content hash
        sample = uploaded_file.read(1024)
        uploaded_file.seek(0)  # Reset file pointer
        content_hash = hashlib.md5(sample).hexdigest()[:8]
    except Exception:
        # Fallback if file can't be read
        content_hash = "unknown"
    
    return (
        uploaded_file.name,
        uploaded_file.size,
        uploaded_file.type,
        content_hash
    )

def process_new_uploads(new_files):
    """Process and save new files that haven't been uploaded yet."""
    saved_count = 0
    errors = []
    
    for file in new_files:
        # Validate file
        is_valid, error_msg = validate_file(file.name, file.size)
        if not is_valid:
            errors.append(f"{file.name}: {error_msg}")
            continue
        
        # Check for duplicates and generate unique filename
        unique_name = get_unique_filename(file.name)
        if unique_name != file.name:
            st.info(f"📝 Renamed: {file.name} → {unique_name}")
        
        # Use atomic write to prevent corrupted files
        filepath = Path(DOCS_DIR) / unique_name
        success, msg = atomic_write(filepath, file.getbuffer())
        
        if success:
            saved_count += 1
        else:
            errors.append(f"{file.name}: {msg}")
    
    return saved_count, errors

st.set_page_config(page_title="Hollard Policy Assistant", page_icon="🛡️", layout="wide")

# Apply custom styling and header - v2
add_styling()
show_header()

# Sidebar
with st.sidebar:
    st.header("📤 Documents")
    
    # Initialize upload tracking
    if "processed_uploads" not in st.session_state:
        st.session_state.processed_uploads = {}
    
    if "upload_generation" not in st.session_state:
        st.session_state.upload_generation = 0
    
    # File uploader with generation-based key (auto-clears after save)
    uploaded = st.file_uploader(
        "Upload files",
        type=["txt", "pdf", "docx", "md"],
        accept_multiple_files=True,
        key=f"uploader_{st.session_state.upload_generation}",
        help="Files will be saved automatically when you select them."
    )
    
    # Process new uploads only (prevents infinite loop)
    if uploaded:
        try:
            # Create signatures for all uploaded files
            current_files = {get_file_signature(f): f for f in uploaded}
            
            # Filter out already-processed files
            new_files = [
                f for sig, f in current_files.items()
                if sig not in st.session_state.processed_uploads
            ]
            
            if new_files:
                # Show progress
                with st.spinner(f"Saving {len(new_files)} new file(s)..."):
                    saved_count, errors = process_new_uploads(new_files)
                
                # Display errors
                for error in errors:
                    st.error(error)
                
                # If any files saved successfully
                if saved_count > 0:
                    st.success(f"✅ Saved {saved_count} file(s). Rebuilding index...")
                    
                    # Mark all current files as processed
                    now = datetime.now().isoformat()
                    for sig in current_files.keys():
                        st.session_state.processed_uploads[sig] = now
                    
                    # Cleanup old entries (keep last 50)
                    if len(st.session_state.processed_uploads) > 50:
                        sorted_items = sorted(
                            st.session_state.processed_uploads.items(),
                            key=lambda x: x[1]
                        )
                        st.session_state.processed_uploads = dict(sorted_items[-50:])
                    
                    # Rebuild vector store
                    success, msg = clear_vector_store()
                    if not success:
                        st.warning(f"⚠️ Vector store clear issue: {msg}")
                    
                    st.cache_resource.clear()
                    
                    # Increment generation to reset uploader
                    st.session_state.upload_generation += 1
                    
                    # Rerun to show fresh uploader
                    st.rerun()
                else:
                    st.warning("⚠️ No files were saved. Check errors above.")
            else:
                # All files already processed
                st.info("ℹ️ These files have already been uploaded in this session.")
        except Exception as e:
            st.error(f"❌ Error processing files: {str(e)}")
    
    st.divider()
    
    # List docs
    docs = get_document_list()
    if docs:
        st.subheader(f"📁 Files ({len(docs)})")
        
        # List individual documents
        for doc in docs:
            col1, col2 = st.columns([4, 1])
            col1.text(doc)
            if col2.button("🗑️", key=f"del_{doc}", type="secondary"):
                if delete_document(doc):
                    # Store messages before any operations
                    messages_backup = st.session_state.get("messages", []).copy()
                    session_histories_backup = st.session_state.get("session_histories", {}).copy()
                    
                    # Clean up tracking for this file (allows re-upload)
                    sigs_to_remove = [
                        sig for sig in st.session_state.get("processed_uploads", {})
                        if sig[0] == doc  # sig[0] is filename
                    ]
                    for sig in sigs_to_remove:
                        st.session_state.processed_uploads.pop(sig, None)
                    
                    # Clear cache before restoring session state
                    st.cache_resource.clear()
                    
                    # Restore chat history after cache clear
                    st.session_state.messages = messages_backup
                    st.session_state.session_histories = session_histories_backup
                    
                    st.success(f"✅ Deleted {doc}. Index will be rebuilt.")
                    st.rerun()
                else:
                    st.error(f"❌ Failed to delete {doc}")
    else:
        st.info("No documents yet")

# Main chat
chain = get_chat_chain()

# Initialize messages in session state if not exists
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show contextual welcome message
docs = get_document_list()
show_welcome_message(docs_exist=bool(docs), messages_exist=bool(st.session_state.messages))

# Add clear chat button
if st.session_state.messages:
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        # Also clear the LangChain message history
        if "session_histories" in st.session_state:
            st.session_state.session_histories = {}
        st.rerun()

# Display all previous messages
for message in st.session_state.messages:
    avatar = "👤" if message["role"] == "user" else "📊"
    with st.chat_message(message["role"], avatar=avatar):
        st.write(message["content"])

# Chat input - disabled if no documents
if not chain:
    st.info("👋 Upload knowledge base documents to start!")
    st.chat_input("Upload documents first...", disabled=True)
elif user_input := st.chat_input("Ask about procedures, vendors, pricing, or benchmarks..."):
    # Add user message to session state and display it
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="👤"):
        st.write(user_input)
    
    # Generate and display assistant response
    with st.chat_message("assistant", avatar="📊"):
        try:
            with st.spinner("🔍 Searching knowledge base..."):
                response = chain.invoke(
                    {"input": user_input},
                    config={"configurable": {"session_id": "main"}}
                )
            # The response is already a string due to StrOutputParser
            st.write(response)
            # Add assistant message to session state
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            st.error(error_msg)
            import traceback
            st.error(traceback.format_exc())
            # Add error to session state so it persists
            st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Show internal contacts in sidebar (always visible)
with st.sidebar:
    show_internal_contacts()
