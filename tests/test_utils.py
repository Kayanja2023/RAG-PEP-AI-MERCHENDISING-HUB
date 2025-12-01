"""
Unit tests for utils.py module.
Tests text extraction functionality from various file formats.
"""

import unittest
import os
import tempfile
from pathlib import Path
from utils import extract_text_from_file


class TestExtractTextFromFile(unittest.TestCase):
    """Test text extraction from different file formats."""
    
    def setUp(self):
        """Create temporary directory for test files."""
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up temporary directory."""
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_extract_from_txt_file(self):
        """Should extract text from .txt files."""
        test_file = os.path.join(self.test_dir, "test.txt")
        test_content = "Hollard Insurance Policy Assistant\nProviding Better Futures"
        
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(test_content)
        
        result = extract_text_from_file(test_file)
        self.assertEqual(result, test_content)
    
    def test_extract_from_md_file(self):
        """Should extract text from .md (markdown) files."""
        test_file = os.path.join(self.test_dir, "readme.md")
        test_content = "# Hollard Policy Assistant\n\n## Features\n- Life Insurance\n- Claims Processing"
        
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(test_content)
        
        result = extract_text_from_file(test_file)
        self.assertEqual(result, test_content)
    
    def test_extract_empty_file(self):
        """Should handle empty text files."""
        test_file = os.path.join(self.test_dir, "empty.txt")
        
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("")
        
        result = extract_text_from_file(test_file)
        self.assertEqual(result, "")
    
    def test_extract_with_unicode(self):
        """Should handle Unicode characters in text files."""
        test_file = os.path.join(self.test_dir, "unicode.txt")
        test_content = "Hollard © 2025 • Better Futures™ → ✓"
        
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(test_content)
        
        result = extract_text_from_file(test_file)
        self.assertIn("Hollard", result)
        self.assertIn("2025", result)
    
    def test_extract_multiline_text(self):
        """Should preserve line breaks in text files."""
        test_file = os.path.join(self.test_dir, "multiline.txt")
        test_content = "Line 1\nLine 2\nLine 3\n"
        
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(test_content)
        
        result = extract_text_from_file(test_file)
        self.assertEqual(result.count('\n'), test_content.count('\n'))
    
    def test_unsupported_file_extension(self):
        """Should raise ValueError for unsupported file types."""
        test_file = os.path.join(self.test_dir, "image.png")
        
        with open(test_file, "wb") as f:
            f.write(b"fake image data")
        
        with self.assertRaises(ValueError) as context:
            extract_text_from_file(test_file)
        
        self.assertIn("Unsupported", str(context.exception))
    
    def test_nonexistent_file(self):
        """Should raise exception for non-existent files."""
        nonexistent_file = os.path.join(self.test_dir, "does_not_exist.txt")
        
        with self.assertRaises(Exception):
            extract_text_from_file(nonexistent_file)
    
    def test_extract_from_path_object(self):
        """Should accept Path objects as input."""
        test_file = Path(self.test_dir) / "pathtest.txt"
        test_content = "Testing with Path object"
        
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(test_content)
        
        result = extract_text_from_file(test_file)
        self.assertEqual(result, test_content)
    
    def test_extract_from_string_path(self):
        """Should accept string paths as input."""
        test_file = os.path.join(self.test_dir, "stringpath.txt")
        test_content = "Testing with string path"
        
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(test_content)
        
        result = extract_text_from_file(test_file)
        self.assertEqual(result, test_content)


class TestExtractTextEdgeCases(unittest.TestCase):
    """Test edge cases for text extraction."""
    
    def setUp(self):
        """Create temporary directory for test files."""
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up temporary directory."""
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_very_large_text_file(self):
        """Should handle large text files."""
        test_file = os.path.join(self.test_dir, "large.txt")
        # Create a file with ~100KB of text
        large_content = "Hollard Policy Information\n" * 5000
        
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(large_content)
        
        result = extract_text_from_file(test_file)
        self.assertGreater(len(result), 100000)
        self.assertIn("Hollard", result)
    
    def test_file_with_special_characters(self):
        """Should handle files with special characters in content."""
        test_file = os.path.join(self.test_dir, "special.txt")
        special_content = "Amount: R1,000,000.00\nEmail: info@hollard.co.za\nPhone: +27 (0)11 555-1234"
        
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(special_content)
        
        result = extract_text_from_file(test_file)
        self.assertIn("R1,000,000.00", result)
        self.assertIn("info@hollard.co.za", result)
    
    def test_file_with_tabs_and_spaces(self):
        """Should preserve tabs and spaces."""
        test_file = os.path.join(self.test_dir, "whitespace.txt")
        content = "Column1\tColumn2\tColumn3\n    Indented line\n\tTab indented"
        
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(content)
        
        result = extract_text_from_file(test_file)
        self.assertIn("\t", result)
        self.assertIn("    ", result)


if __name__ == '__main__':
    unittest.main()
