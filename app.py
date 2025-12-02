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
    page_title="PEP Merchandising Hub",
    page_icon="🔵",
    layout="wide",
    initial_sidebar_state="expanded"
)

def add_styling():
    st.markdown("""
        <style>
        /* PEP South Africa Official Brand Colors */
        :root {
            --pep-azure: #1180FA;
            --pep-azure-dark: #0D6DD9;
            --pep-loblolly: #C4CDD5;
            --pep-potters-clay: #945E3A;
            --pep-white: #FFFFFF;
            --pep-dark: #1F2937;
        }
        
        /* Clean background with Loblolly tint */
        .main {
            background-color: #F8F9FA;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
        }
        
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Primary buttons - Azure Radiance blue */
        .stButton > button {
            background: linear-gradient(135deg, #1180FA 0%, #0D6DD9 100%);
            color: white;
            border-radius: 6px;
            border: none;
            padding: 6px 16px;
            font-size: 12px;
            font-weight: 600;
            letter-spacing: 0.2px;
            transition: all 0.3s ease;
            box-shadow: 0 2px 6px rgba(17, 128, 250, 0.2);
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, #0D6DD9 0%, #0A5AB8 100%);
            box-shadow: 0 6px 20px rgba(17, 128, 250, 0.35);
            transform: translateY(-2px);
        }
        
        .stButton > button:active {
            transform: translateY(0);
            box-shadow: 0 2px 8px rgba(17, 128, 250, 0.3);
        }
        
        /* Secondary buttons - Loblolly grey */
        .stButton > button[kind="secondary"] {
            background: white;
            color: #1F2937;
            border: 2px solid #C4CDD5;
            padding: 10px 24px;
            font-size: 13px;
            font-weight: 600;
            border-radius: 8px;
            box-shadow: none;
        }
        
        .stButton > button[kind="secondary"]:hover {
            background: #F0F4F8;
            border-color: #1180FA;
            color: #1180FA;
        }
        
        /* Sidebar - Clean with Loblolly accents */
        [data-testid="stSidebar"] {
            background: white;
            border-right: 1px solid #C4CDD5;
            box-shadow: 2px 0 12px rgba(196, 205, 213, 0.15);
        }
        
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            color: #1F2937;
            font-weight: 700;
            font-size: 0.9rem;
            letter-spacing: 0.5px;
            margin-bottom: 16px;
            padding-bottom: 8px;
            border-bottom: 3px solid #1180FA;
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
        
        
        /* Chat messages - modern card design */
        .stChatMessage {
            background: white;
            border: 2px solid transparent;
            border-radius: 10px;
            padding: 12px 16px;
            margin-bottom: 10px;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
            transition: all 0.2s ease;
        }
        
        .stChatMessage:hover {
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
            transform: translateY(-2px);
        }
        
        /* User messages - PEP Yellow accent */
        .stChatMessage[data-testid="user-message"] {
            background: linear-gradient(135deg, #FFFDF7 0%, #FFFFFF 100%);
            border: 2px solid #FFD100;
            border-left: 6px solid #FFD100;
        }
        
        /* Assistant messages - PEP Blue accent */
        .stChatMessage[data-testid="assistant-message"] {
            background: linear-gradient(135deg, #F8FBFF 0%, #FFFFFF 100%);
            border: 2px solid #1180FA;
            border-left: 6px solid #1180FA;
        }
        
        /* Chat message avatar styling */
        .stChatMessage [data-testid="chatAvatarIcon-user"],
        .stChatMessage [data-testid="chatAvatarIcon-assistant"] {
            width: 32px;
            height: 32px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            font-weight: 600;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
        }
        
        .stChatMessage [data-testid="chatAvatarIcon-user"] {
            background: linear-gradient(135deg, #FFD100 0%, #FFC700 100%);
            color: #1F2937;
        }
        
        .stChatMessage [data-testid="chatAvatarIcon-assistant"] {
            background: linear-gradient(135deg, #1180FA 0%, #0D6DD9 100%);
            color: white;
        }
        
        /* Text inputs - Azure focus */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            border: 2px solid #C4CDD5;
            border-radius: 8px;
            padding: 12px 16px;
            font-size: 14px;
            transition: all 0.2s;
        }
        
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: #1180FA;
            box-shadow: 0 0 0 3px rgba(17, 128, 250, 0.1);
            outline: none;
        }
        
        /* Chat input placeholder */
        .stChatInput input::placeholder {
            color: #9CA3AF;
            font-style: italic;
        }
        
        /* File uploader */
        [data-testid="stFileUploader"] {
            background: white;
            border: 2px dashed #C4CDD5;
            border-radius: 12px;
            padding: 24px;
            transition: all 0.3s;
        }
        
        [data-testid="stFileUploader"]:hover {
            border-color: #1180FA;
            background: #F0F7FF;
        }
        
        /* Messages */
        .stSuccess {
            background: #F0FDF4;
            border-left: 4px solid #10B981;
            border-radius: 8px;
            padding: 12px 16px;
        }
        
        .stInfo {
            background: #F0F7FF;
            border-left: 4px solid #1180FA;
            border-radius: 8px;
            padding: 12px 16px;
        }
        
        .stWarning {
            background: #FFF9F5;
            border-left: 4px solid #945E3A;
            border-radius: 8px;
            padding: 12px 16px;
        }
        
        /* Links */
        a {
            color: #1180FA;
            font-weight: 600;
            text-decoration: none;
            border-bottom: 2px solid transparent;
            transition: all 0.2s;
        }
        
        a:hover {
            border-bottom-color: #945E3A;
        }
        
        /* Metrics */
        [data-testid="stMetricValue"] {
            color: #1180FA;
            font-weight: 700;
        }
        </style>
    """, unsafe_allow_html=True)

def show_welcome_message(docs_exist, messages_exist):
    """Display contextual welcome message based on app state."""
    if not docs_exist and not messages_exist:
        st.markdown("""
            <div style='background: white; padding: 48px 40px; border-radius: 16px;
                        border: 2px solid #C4CDD5; margin-bottom: 32px;
                        box-shadow: 0 4px 20px rgba(196, 205, 213, 0.2);'>
                
                <div style='text-align: center; margin-bottom: 40px;'>
                    <div style='display: inline-block; background: linear-gradient(135deg, #1180FA 0%, #0D6DD9 100%); 
                                padding: 20px 40px; border-radius: 12px; margin-bottom: 20px;
                                box-shadow: 0 4px 16px rgba(17, 128, 250, 0.3);'>
                        <h1 style='color: white; margin: 0; font-size: 2.4rem; font-weight: 900; 
                                   letter-spacing: 3px;'>PEP</h1>
                    </div>
                    <h2 style='color: #1F2937; margin: 0 0 12px 0; font-size: 1.5rem; font-weight: 700;'>
                        Merchandising Knowledge Hub
                    </h2>
                    <p style='color: #6B7280; font-size: 1.05rem; line-height: 1.6; margin: 0;'>
                        Internal knowledge base for Buying, Planning & Merchandising teams
                    </p>
                </div>
                
                <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); 
                            gap: 20px; margin-top: 32px;'>
                    <div style='background: #FFFFFF; padding: 20px; border-radius: 12px; 
                                border-left: 5px solid #FFD100; box-shadow: 0 2px 8px rgba(0,0,0,0.05);
                                transition: all 0.2s;'
                         onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 4px 16px rgba(255,209,0,0.2)'"
                         onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 8px rgba(0,0,0,0.05)'">
                        <div style='font-size: 2rem; margin-bottom: 12px;'>📊</div>
                        <strong style='color: #000000; font-size: 1rem; font-weight: 700; 
                                      display: block; margin-bottom: 8px;'>Performance Metrics</strong>
                        <p style='color: #6B7280; font-size: 0.9rem; margin: 0; line-height: 1.5;'>
                            KPIs, stock turn, sell-through rates, GMROI benchmarks
                        </p>
                    </div>
                    <div style='background: #FFFFFF; padding: 20px; border-radius: 12px; 
                                border-left: 5px solid #FFD100; box-shadow: 0 2px 8px rgba(0,0,0,0.05);
                                transition: all 0.2s;'
                         onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 4px 16px rgba(255,209,0,0.2)'"
                         onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 8px rgba(0,0,0,0.05)'">
                        <div style='font-size: 2rem; margin-bottom: 12px;'>🏭</div>
                        <strong style='color: #000000; font-size: 1rem; font-weight: 700; 
                                      display: block; margin-bottom: 8px;'>Supplier Directory</strong>
                        <p style='color: #6B7280; font-size: 0.9rem; margin: 0; line-height: 1.5;'>
                            Vendor contacts, lead times, payment terms, ratings
                        </p>
                    </div>
                    <div style='background: #FFFFFF; padding: 20px; border-radius: 12px; 
                                border-left: 5px solid #FFD100; box-shadow: 0 2px 8px rgba(0,0,0,0.05);
                                transition: all 0.2s;'
                         onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 4px 16px rgba(255,209,0,0.2)'"
                         onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 8px rgba(0,0,0,0.05)'">
                        <div style='font-size: 2rem; margin-bottom: 12px;'>📝</div>
                        <strong style='color: #000000; font-size: 1rem; font-weight: 700; 
                                      display: block; margin-bottom: 8px;'>Procedures & Policies</strong>
                        <p style='color: #6B7280; font-size: 0.9rem; margin: 0; line-height: 1.5;'>
                            Purchase orders, approvals, quality standards
                        </p>
                    </div>
                    <div style='background: #FFFFFF; padding: 20px; border-radius: 12px; 
                                border-left: 5px solid #FFD100; box-shadow: 0 2px 8px rgba(0,0,0,0.05);
                                transition: all 0.2s;'
                         onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 4px 16px rgba(255,209,0,0.2)'"
                         onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 8px rgba(0,0,0,0.05)'">
                        <div style='font-size: 2rem; margin-bottom: 12px;'>💰</div>
                        <strong style='color: #000000; font-size: 1rem; font-weight: 700; 
                                      display: block; margin-bottom: 8px;'>Pricing Strategy</strong>
                        <p style='color: #6B7280; font-size: 0.9rem; margin: 0; line-height: 1.5;'>
                            Margin calculations, landed cost, promotional planning
                        </p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    elif docs_exist and not messages_exist:
        st.toast('✓ System Ready — Ask about suppliers, procedures, pricing, or performance', icon='✅')

def show_internal_contacts():
    """Display internal PEP department contacts for additional support."""
    st.markdown("""
        <div style='background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%); 
                    padding: 20px; margin-top: 20px; border-radius: 12px;
                    border: 2px solid #FFD100; box-shadow: 0 2px 8px rgba(255, 209, 0, 0.15);'>
            <p style='color: #000000; margin: 0 0 16px 0; font-weight: 700; font-size: 0.9rem; 
                      letter-spacing: 0.5px; display: flex; align-items: center;'>
                <span style='font-size: 1.2rem; margin-right: 8px;'>📞</span> Support Contacts
            </p>
            <div style='color: #1F2937; font-size: 0.9rem; line-height: 2;'>
                <p style='margin: 8px 0;'><strong>Buying Manager</strong> • Ext 2401</p>
                <p style='margin: 8px 0;'><strong>Merchandising Head</strong> • Ext 2405</p>
                <p style='margin: 8px 0;'><strong>Planning Director</strong> • Ext 2410</p>
                <p style='margin: 8px 0; padding-top: 8px; border-top: 1px solid #FDE68A;'>
                    <strong>✉️ Email:</strong> merchandising@pep.co.za
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)



def show_demo_disclaimer():
    """Display demo/POC disclaimer as toast notification."""
    st.toast('⚠️ Demo Version: Not connected to live PEP systems. Verify all information with official sources.', icon='⚠️')

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

# Apply custom styling
add_styling()

# Main banner at the top - Elevated Minimalism design
st.markdown("""
    <div style='background: linear-gradient(135deg, #F0F7FF 0%, #FFFFFF 100%); 
                border-radius: 14px; 
                margin-bottom: 24px;
                padding: 20px 32px;
                box-shadow: 0 2px 12px rgba(17, 128, 250, 0.12);
                border-left: 3px solid #1180FA;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                position: relative;'>
        <div style='display: flex; align-items: center; gap: 20px; flex-wrap: wrap;'>
            <div style='background: linear-gradient(135deg, #1180FA 0%, #0D6DD9 100%); 
                        width: 64px; 
                        height: 64px; 
                        border-radius: 12px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        flex-shrink: 0;
                        box-shadow: 0 4px 12px rgba(17, 128, 250, 0.25);
                        transition: transform 0.3s ease;'>
                <span style='color: #FFFFFF; 
                            font-size: 1.75rem; 
                            font-weight: 900; 
                            letter-spacing: 1px;'>PEP</span>
            </div>
            <div style='flex: 1; min-width: 280px;'>
                <h1 style='color: #1F2937; 
                          margin: 0 0 6px 0; 
                          font-size: 1.75rem; 
                          font-weight: 800;
                          line-height: 1.2;
                          letter-spacing: -0.02em;'>
                    Merchandising Knowledge Hub
                </h1>
                <p style='color: #6B7280; 
                         margin: 0; 
                         font-size: 1rem; 
                         font-weight: 500;
                         line-height: 1.5;'>
                    AI-Powered Intelligence for Buying, Planning & Merchandising Teams
                </p>
            </div>
            <div style='margin-left: auto;'>
                <span style='display: inline-block;
                            background: rgba(17, 128, 250, 0.1);
                            color: #1180FA;
                            padding: 6px 14px;
                            border-radius: 20px;
                            font-size: 0.8rem;
                            font-weight: 600;
                            letter-spacing: 0.3px;
                            border: 1px solid rgba(17, 128, 250, 0.2);'>
                    ✨ GPT-4
                </span>
            </div>
        </div>
    </div>
    <style>
        @media (max-width: 640px) {
            div[style*="flex-wrap: wrap"] > div:first-child {
                width: 56px !important;
                height: 56px !important;
            }
            div[style*="flex-wrap: wrap"] h1 {
                font-size: 1.5rem !important;
            }
            div[style*="flex-wrap: wrap"] p {
                font-size: 0.9rem !important;
            }
            div[style*="margin-left: auto"] {
                margin-left: 0 !important;
                width: 100%;
                text-align: center;
            }
        }
        @media (min-width: 641px) and (max-width: 1024px) {
            div[style*="flex-wrap: wrap"] > div:first-child {
                width: 60px !important;
                height: 60px !important;
            }
        }
    </style>
""", unsafe_allow_html=True)

show_demo_disclaimer()

# Sidebar
with st.sidebar:
    st.header("📤 KNOWLEDGE BASE")
    
    # Initialize upload tracking
    if "processed_uploads" not in st.session_state:
        st.session_state.processed_uploads = {}
    
    if "upload_generation" not in st.session_state:
        st.session_state.upload_generation = 0
    
    # File uploader with generation-based key (auto-clears after save)
    uploaded = st.file_uploader(
        "Upload Documents",
        type=["txt", "pdf", "docx", "md"],
        accept_multiple_files=True,
        key=f"uploader_{st.session_state.upload_generation}",
        help="Accepted formats: TXT, PDF, DOCX, MD"
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

# Add welcome greeting from assistant on first load (only if docs exist and no messages yet)
docs = get_document_list()
if docs and len(st.session_state.messages) == 0:
    welcome_message = """👋 **Welcome to PEP Merchandising Intelligence Hub!**

I'm your AI assistant, here to help you access critical merchandising information instantly.

**I can help you with:**
- 📊 Performance metrics, KPIs, and benchmarks
- 🏭 Supplier directory and vendor information
- 💰 Pricing strategies and margin calculations
- 📝 Buying procedures and compliance standards
- 📦 Merchandising guidelines and policies

**Just ask me anything!** For example:
- "What are the approved suppliers for footwear?"
- "How do I calculate retail pricing?"
- "What are the target stock turn rates?"

How can I assist you today?"""
    
    st.session_state.messages.append({"role": "assistant", "content": welcome_message})

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
    avatar = "👤" if message["role"] == "user" else "⚡"
    with st.chat_message(message["role"], avatar=avatar):
        st.write(message["content"])

# Chat input - disabled if no documents
if not chain:
    st.info("📤 Upload knowledge base documents in the sidebar to begin")
    st.chat_input("Upload documents first...", disabled=True)
elif user_input := st.chat_input("💬 Ask about suppliers, procedures, pricing, KPIs, compliance..."):
    # Add user message to session state and display it
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="👤"):
        st.write(user_input)
    
    # Generate and display assistant response
    with st.chat_message("assistant", avatar="⚡"):
        try:
            with st.spinner("⚡ Searching knowledge base..."):
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
