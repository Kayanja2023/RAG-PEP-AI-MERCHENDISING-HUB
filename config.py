import os
import shutil
from pathlib import Path

# Directory paths
DOCS_DIR = os.path.join(os.path.dirname(__file__), "data", "documents")
FAISS_DIR = os.path.join(os.path.dirname(__file__), "data", "faiss_store")

# Ensure directories exist
os.makedirs(DOCS_DIR, exist_ok=True)
os.makedirs(FAISS_DIR, exist_ok=True)

# RAG Configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
MODEL = "gpt-4"
TEMPERATURE = 0.7
SEARCH_K = 3

# File constraints
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_EXTENSIONS = ["txt", "pdf", "docx", "md"]


def atomic_write(dest_path, data):
    """Write file atomically using temp file + rename to prevent corruption."""
    dest_path = Path(dest_path)
    tmp = dest_path.with_name(dest_path.name + ".tmp")
    tmp.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(tmp, "wb") as f:
            f.write(data)
        tmp.replace(dest_path)  # Atomic on both POSIX and Windows
        return True, "File written successfully"
    except Exception as e:
        if tmp.exists():
            try:
                tmp.unlink()
            except:
                pass
        return False, f"Write failed: {str(e)}"


def get_unique_filename(filename):
    """Generate unique filename if file already exists by adding timestamp."""
    from datetime import datetime
    
    path = Path(DOCS_DIR) / filename
    if not path.exists():
        return filename
    
    # Add timestamp suffix before extension
    stem = path.stem
    suffix = path.suffix
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{stem}_{timestamp}{suffix}"


def get_document_list():
    """Get list of uploaded documents."""
    if not os.path.exists(DOCS_DIR):
        return []
    return [f for f in os.listdir(DOCS_DIR) if os.path.isfile(os.path.join(DOCS_DIR, f))]


def delete_document(filename):
    """Delete a document file and clear the vector store."""
    filepath = os.path.join(DOCS_DIR, filename)
    if os.path.exists(filepath):
        try:
            os.remove(filepath)
            # Also delete the FAISS vector store so it gets rebuilt
            clear_vector_store()
            return True
        except Exception as e:
            return False
    return False


def clear_vector_store():
    """Delete all FAISS vector store files to force rebuild."""
    faiss_path = Path(FAISS_DIR)
    
    if not faiss_path.exists():
        return True, "Vector store already cleared"
    
    errors = []
    for child in faiss_path.iterdir():
        try:
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()
        except Exception as e:
            errors.append(f"{child.name}: {str(e)}")
    
    if errors:
        return False, f"Partial clear. Errors: {'; '.join(errors)}"
    return True, "Vector store cleared successfully"


def delete_all_documents():
    """Delete all documents and clear the vector store."""
    if os.path.exists(DOCS_DIR):
        count = 0
        errors = []
        for file in os.listdir(DOCS_DIR):
            file_path = os.path.join(DOCS_DIR, file)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    count += 1
            except Exception as e:
                errors.append(f"{file}: {str(e)}")
        
        clear_vector_store()
        
        if errors:
            return count, f"Deleted {count} file(s) with errors: {'; '.join(errors)}"
        return count, f"Successfully deleted {count} file(s)"
    return 0, "No documents directory found"


def validate_file(filename, filesize):
    """Validate uploaded file."""
    if not filename or filesize == 0:
        return False, "File is empty or has no name"
    
    if filesize > MAX_FILE_SIZE:
        return False, f"File too large (max {MAX_FILE_SIZE / 1024 / 1024:.0f}MB)"
    
    ext = filename.split(".")[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False, f"Unsupported format. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
    
    return True, ""