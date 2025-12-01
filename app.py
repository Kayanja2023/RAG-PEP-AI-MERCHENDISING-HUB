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

def add_styling():
    st.markdown("""
        <style>
        /* Hollard Brand Colors */
        :root {
            --hollard-purple: #6B1E9E;
            --hollard-purple-dark: #5A1880;
            --hollard-purple-light: #E8D4F1;
            --hollard-purple-bg: #F9F5FC;
        }
        
        /* Main background - pure white */
        .main {
            background-color: #FFFFFF;
        }
        
        /* Primary buttons - Hollard purple with rounded corners */
        .stButton > button {
            background-color: #6B1E9E;
            color: white;
            border-radius: 16px;
            border: none;
            padding: 10px 20px;
            font-size: 14px;
            font-weight: 500;
            box-shadow: 0 2px 8px rgba(107, 30, 158, 0.15);
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            background-color: #5A1880;
            box-shadow: 0 4px 12px rgba(107, 30, 158, 0.25);
            transform: translateY(-1px);
        }
        
        /* Secondary delete buttons - light styling */
        .stButton > button[kind="secondary"] {
            background-color: #F5F5F5;
            color: #666666;
            border: 1px solid #E0E0E0;
            padding: 6px 12px;
            font-size: 13px;
            border-radius: 16px;
            box-shadow: none;
        }
        
        .stButton > button[kind="secondary"]:hover {
            background-color: #E8D4F1;
            color: #5A1880;
            border-color: #6B1E9E;
        }
        
        /* Sidebar - light purple background */
        [data-testid="stSidebar"] {
            background-color: #F9F5FC;
            max-width: 280px;
            border-right: 2px solid #E8D4F1;
        }
        
        [data-testid="stSidebar"] > div:first-child {
            padding-top: 1rem;
        }
        
        /* Sidebar headers - Hollard purple */
        [data-testid="stSidebar"] h2 {
            color: #6B1E9E;
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }
        
        [data-testid="stSidebar"] h3 {
            color: #5A1880;
            font-size: 1rem;
            font-weight: 500;
            margin-bottom: 0.5rem;
        }
        
        /* File uploader styling */
        [data-testid="stFileUploader"] {
            border: 2px dashed #6B1E9E;
            border-radius: 16px;
            padding: 1rem;
            background-color: #FFFFFF;
        }
        
        /* Chat input styling */
        .stChatInput {
            border-color: #6B1E9E;
            border-radius: 16px;
        }
        
        /* Success messages */
        .stSuccess {
            background-color: #E8D4F1;
            color: #5A1880;
            border-left: 4px solid #6B1E9E;
            border-radius: 16px;
        }
        
        /* Info messages */
        .stInfo {
            background-color: #F9F5FC;
            color: #5A1880;
            border-left: 4px solid #6B1E9E;
            border-radius: 16px;
        }
        
        /* Dividers */
        hr {
            border-color: #E8D4F1;
        }
        
        /* Chat messages */
        .stChatMessage {
            border-radius: 16px;
            padding: 1rem;
            margin-bottom: 0.5rem;
        }
        
        /* User messages - light purple */
        [data-testid="stChatMessage"]:has([data-testid="stChatMessageContent"]:first-child) {
            background-color: #E8D4F1;
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
            color: #6B1E9E;
        }
        
        a:hover {
            color: #5A1880;
        }
        </style>
    """, unsafe_allow_html=True)

def show_welcome_message(docs_exist, messages_exist):
    """Display contextual welcome message based on app state."""
    if not docs_exist and not messages_exist:
        # First-time user - no documents, no chat
        st.markdown("""
            <div style='background: linear-gradient(135deg, #F9F5FC 0%, #FFFFFF 100%);
                        padding: 32px;
                        border-radius: 16px;
                        border: 2px solid #E8D4F1;
                        margin-bottom: 24px;
                        text-align: center;'>
                <h2 style='color: #6B1E9E; margin: 0 0 16px 0; font-size: 1.8rem; font-weight: 600;'>
                    👋 Welcome to Hollard Policy Assistant!
                </h2>
                <p style='color: #5A1880; font-size: 1rem; line-height: 1.6; margin: 12px 0;'>
                    Get instant answers about Hollard insurance products and policies.
                </p>
                <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-top: 24px;'>
                    <div style='background: #FFFFFF; padding: 16px; border-radius: 12px; border: 1px solid #E8D4F1;'>
                        <div style='font-size: 2rem; margin-bottom: 8px;'>📋</div>
                        <strong style='color: #6B1E9E;'>Policy Information</strong>
                        <p style='color: #666666; font-size: 0.85rem; margin: 4px 0 0 0;'>Life, Disability, Business cover</p>
                    </div>
                    <div style='background: #FFFFFF; padding: 16px; border-radius: 12px; border: 1px solid #E8D4F1;'>
                        <div style='font-size: 2rem; margin-bottom: 8px;'>💬</div>
                        <strong style='color: #6B1E9E;'>Instant Answers</strong>
                        <p style='color: #666666; font-size: 0.85rem; margin: 4px 0 0 0;'>Claims, terms, products</p>
                    </div>
                    <div style='background: #FFFFFF; padding: 16px; border-radius: 12px; border: 1px solid #E8D4F1;'>
                        <div style='font-size: 2rem; margin-bottom: 8px;'>🔒</div>
                        <strong style='color: #6B1E9E;'>Secure & Private</strong>
                        <p style='color: #666666; font-size: 0.85rem; margin: 4px 0 0 0;'>Your data stays protected</p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    elif docs_exist and not messages_exist:
        # Documents uploaded but no chat started
        st.markdown("""
            <div style='background: #E8D4F1;
                        padding: 20px 24px;
                        border-radius: 12px;
                        margin-bottom: 20px;
                        border-left: 4px solid #6B1E9E;'>
                <p style='color: #5A1880; margin: 0; font-size: 1rem;'>
                    ✨ <strong>Great!</strong> Your policy documents are ready. Ask me anything about Hollard products or policies.
                </p>
            </div>
        """, unsafe_allow_html=True)

def show_header():
    st.markdown("""
        <div style='background: linear-gradient(135deg, #6B1E9E 0%, #5A1880 100%); 
                    padding: 20px 32px; 
                    border-radius: 16px; 
                    margin-bottom: 24px;
                    box-shadow: 0 4px 16px rgba(107, 30, 158, 0.2);
                    display: flex;
                    align-items: center;
                    gap: 16px;'>
            <div style='flex: 0 0 auto;'>
                <img src="https://www.hollard.co.za/_next/static/media/hollard-footer-default.9ed7fd46.svg" alt="Hollard" style="height: 45px; width: auto; display: block;">
            </div>
            <div style='flex: 1; text-align: left;'>
                <h1 style='color: #FFFFFF; margin: 0; font-size: 1.5rem; font-weight: 600; letter-spacing: 0.5px;'>
                    Hollard Policy Assistant
                </h1>
                <p style='color: #E8D4F1; margin: 4px 0 0 0; font-size: 0.85rem; font-weight: 400;'>
                    Your Policy Knowledge Partner
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
    avatar = "👤" if message["role"] == "user" else "🛡️"
    with st.chat_message(message["role"], avatar=avatar):
        st.write(message["content"])

# Chat input - disabled if no documents
if not chain:
    st.info("👋 Upload documents to start chatting!")
    # Display disabled input to show chat is unavailable
    st.chat_input("Upload documents first...", disabled=True)
elif user_input := st.chat_input("Ask about Hollard products or policies..."):
    # Add user message to session state and display it
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="👤"):
        st.write(user_input)
    
    # Generate and display assistant response
    with st.chat_message("assistant", avatar="🛡️"):
        try:
            with st.spinner("🔍 Analyzing your documents..."):
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