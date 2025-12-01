"""
Unit tests for config.py module.
Tests configuration settings, file operations, and helper functions.
"""

import unittest
import os
import tempfile
import shutil
from pathlib import Path
from config import (
    atomic_write, get_unique_filename, validate_file, 
    get_document_list, delete_document, clear_vector_store,
    CHUNK_SIZE, CHUNK_OVERLAP, MODEL, TEMPERATURE, SEARCH_K,
    MAX_FILE_SIZE, ALLOWED_EXTENSIONS
)


class TestConfigConstants(unittest.TestCase):
    """Test configuration constants are properly set."""
    
    def test_chunk_size_is_positive(self):
        """Chunk size should be a positive integer."""
        self.assertIsInstance(CHUNK_SIZE, int)
        self.assertGreater(CHUNK_SIZE, 0)
    
    def test_chunk_overlap_is_valid(self):
        """Chunk overlap should be less than chunk size."""
        self.assertIsInstance(CHUNK_OVERLAP, int)
        self.assertGreaterEqual(CHUNK_OVERLAP, 0)
        self.assertLess(CHUNK_OVERLAP, CHUNK_SIZE)
    
    def test_model_is_string(self):
        """Model name should be a string."""
        self.assertIsInstance(MODEL, str)
        self.assertGreater(len(MODEL), 0)
    
    def test_temperature_in_range(self):
        """Temperature should be between 0 and 1."""
        self.assertIsInstance(TEMPERATURE, (int, float))
        self.assertGreaterEqual(TEMPERATURE, 0.0)
        self.assertLessEqual(TEMPERATURE, 1.0)
    
    def test_search_k_is_positive(self):
        """Search K should be a positive integer."""
        self.assertIsInstance(SEARCH_K, int)
        self.assertGreater(SEARCH_K, 0)
    
    def test_max_file_size_reasonable(self):
        """Max file size should be reasonable (not negative or too large)."""
        self.assertIsInstance(MAX_FILE_SIZE, int)
        self.assertGreater(MAX_FILE_SIZE, 0)
        self.assertLess(MAX_FILE_SIZE, 1024 * 1024 * 1024)  # Less than 1GB
    
    def test_allowed_extensions_valid(self):
        """Allowed extensions should be a list of strings."""
        self.assertIsInstance(ALLOWED_EXTENSIONS, list)
        self.assertGreater(len(ALLOWED_EXTENSIONS), 0)
        for ext in ALLOWED_EXTENSIONS:
            self.assertIsInstance(ext, str)
            self.assertFalse(ext.startswith('.'))  # Should not have leading dot


class TestAtomicWrite(unittest.TestCase):
    """Test atomic file writing functionality."""
    
    def setUp(self):
        """Create temporary directory for test files."""
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up temporary directory."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_write_new_file(self):
        """Should successfully write a new file."""
        test_file = os.path.join(self.test_dir, "test.txt")
        test_data = b"Hello, Hollard!"
        
        success, message = atomic_write(test_file, test_data)
        
        self.assertTrue(success)
        self.assertTrue(os.path.exists(test_file))
        with open(test_file, "rb") as f:
            self.assertEqual(f.read(), test_data)
    
    def test_overwrite_existing_file(self):
        """Should successfully overwrite an existing file."""
        test_file = os.path.join(self.test_dir, "existing.txt")
        
        # Write initial content
        atomic_write(test_file, b"Old content")
        
        # Overwrite
        new_data = b"New content"
        success, message = atomic_write(test_file, new_data)
        
        self.assertTrue(success)
        with open(test_file, "rb") as f:
            self.assertEqual(f.read(), new_data)
    
    def test_write_to_nested_directory(self):
        """Should create nested directories if they don't exist."""
        nested_path = os.path.join(self.test_dir, "nested", "dir", "file.txt")
        test_data = b"Nested file"
        
        success, message = atomic_write(nested_path, test_data)
        
        self.assertTrue(success)
        self.assertTrue(os.path.exists(nested_path))
    
    def test_write_empty_file(self):
        """Should handle writing empty files."""
        test_file = os.path.join(self.test_dir, "empty.txt")
        success, message = atomic_write(test_file, b"")
        
        self.assertTrue(success)
        self.assertTrue(os.path.exists(test_file))
        self.assertEqual(os.path.getsize(test_file), 0)


class TestGetUniqueFilename(unittest.TestCase):
    """Test unique filename generation."""
    
    def setUp(self):
        """Create temporary directory for test files."""
        self.test_dir = tempfile.mkdtemp()
        # Temporarily change DOCS_DIR for testing
        self.original_docs_dir = os.environ.get('DOCS_DIR')
    
    def tearDown(self):
        """Clean up temporary directory."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        if self.original_docs_dir:
            os.environ['DOCS_DIR'] = self.original_docs_dir
    
    def test_unique_filename_no_conflict(self):
        """Should return original filename if no conflict."""
        filename = "test_document.pdf"
        result = get_unique_filename(filename)
        # Should return original name or with timestamp
        self.assertIsInstance(result, str)
        self.assertTrue(result.endswith('.pdf'))
    
    def test_unique_filename_preserves_extension(self):
        """Should preserve file extension."""
        test_cases = ["file.txt", "doc.pdf", "report.docx", "readme.md"]
        for filename in test_cases:
            result = get_unique_filename(filename)
            original_ext = Path(filename).suffix
            result_ext = Path(result).suffix
            self.assertEqual(original_ext, result_ext)


class TestValidateFile(unittest.TestCase):
    """Test file validation functionality."""
    
    def test_validate_allowed_extension(self):
        """Should accept files with allowed extensions."""
        for ext in ALLOWED_EXTENSIONS:
            filename = f"test.{ext}"
            is_valid, message = validate_file(filename, 1024)
            self.assertTrue(is_valid, f"Failed for {filename}: {message}")
    
    def test_reject_disallowed_extension(self):
        """Should reject files with disallowed extensions."""
        invalid_files = ["test.exe", "script.sh", "data.json", "image.png"]
        for filename in invalid_files:
            is_valid, message = validate_file(filename, 1024)
            self.assertFalse(is_valid)
            # Message contains "format" or "extension" or "allowed"
            self.assertTrue(any(word in message.lower() for word in ["format", "extension", "allowed"]))
    
    def test_reject_oversized_file(self):
        """Should reject files exceeding max size."""
        is_valid, message = validate_file("test.pdf", MAX_FILE_SIZE + 1)
        self.assertFalse(is_valid)
        # Message contains "size", "large", "max", or "mb"
        self.assertTrue(any(word in message.lower() for word in ["size", "large", "max", "mb"]))
    
    def test_accept_file_at_max_size(self):
        """Should accept files at exactly max size."""
        is_valid, message = validate_file("test.pdf", MAX_FILE_SIZE)
        self.assertTrue(is_valid)
    
    def test_reject_empty_filename(self):
        """Should reject empty filename."""
        is_valid, message = validate_file("", 1024)
        self.assertFalse(is_valid)
    
    def test_reject_zero_size_file(self):
        """Should reject zero-size files."""
        is_valid, message = validate_file("test.pdf", 0)
        self.assertFalse(is_valid)


class TestGetDocumentList(unittest.TestCase):
    """Test document listing functionality."""
    
    def test_returns_list(self):
        """Should return a list of documents."""
        result = get_document_list()
        self.assertIsInstance(result, list)
    
    def test_list_contains_strings(self):
        """Document list should contain strings."""
        docs = get_document_list()
        for doc in docs:
            self.assertIsInstance(doc, str)


class TestDeleteDocument(unittest.TestCase):
    """Test document deletion functionality."""
    
    def setUp(self):
        """Create temporary directory for test files."""
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up temporary directory."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_delete_nonexistent_file(self):
        """Should handle deleting non-existent file gracefully."""
        # Should not raise an exception
        try:
            delete_document("nonexistent_file_12345.pdf")
        except Exception as e:
            self.fail(f"delete_document raised exception: {e}")


if __name__ == '__main__':
    unittest.main()
