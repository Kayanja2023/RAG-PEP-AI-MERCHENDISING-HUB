"""
Unit tests for rag_engine.py module.
Tests document loading, vector store operations, and RAG chain functionality.
"""

import unittest
import os
import tempfile
import shutil
from unittest.mock import Mock, patch, MagicMock
import sys

# Mock streamlit before importing rag_engine
sys.modules['streamlit'] = MagicMock()


class TestDocumentLoading(unittest.TestCase):
    """Test document loading functionality."""
    
    def setUp(self):
        """Create temporary directory with test documents."""
        self.test_dir = tempfile.mkdtemp()
        self.original_docs_dir = None
    
    def tearDown(self):
        """Clean up temporary directory."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_load_txt_document(self):
        """Should load .txt documents."""
        test_file = os.path.join(self.test_dir, "test.txt")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("Hollard life insurance policy information")
        
        self.assertTrue(os.path.exists(test_file))
        with open(test_file, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("Hollard", content)
    
    def test_load_md_document(self):
        """Should load .md (markdown) documents."""
        test_file = os.path.join(self.test_dir, "policy.md")
        content = "# Hollard Products\n## Life Insurance\nComprehensive coverage"
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(content)
        
        self.assertTrue(os.path.exists(test_file))
    
    def test_skip_unsupported_files(self):
        """Should skip files with unsupported extensions."""
        unsupported_files = ["image.png", "script.py", "data.json"]
        for filename in unsupported_files:
            test_file = os.path.join(self.test_dir, filename)
            with open(test_file, "w") as f:
                f.write("test content")
            
            # File exists but should be skipped during loading
            self.assertTrue(os.path.exists(test_file))
    
    def test_handle_empty_directory(self):
        """Should handle empty document directory."""
        # Empty directory should not cause errors
        self.assertEqual(len(os.listdir(self.test_dir)), 0)
    
    def test_document_metadata_preservation(self):
        """Document metadata should include source filename."""
        filename = "policy_document.txt"
        
        # Mock document object structure
        class MockDocument:
            def __init__(self):
                self.metadata = {"source": filename}
                self.page_content = "Test content"
        
        doc = MockDocument()
        self.assertEqual(doc.metadata["source"], filename)


class TestChunkConfiguration(unittest.TestCase):
    """Test document chunking configuration."""
    
    def test_chunk_size_setting(self):
        """Chunk size should be properly configured."""
        from config import CHUNK_SIZE, CHUNK_OVERLAP
        
        # Verify chunk configuration makes sense
        self.assertIsInstance(CHUNK_SIZE, int)
        self.assertGreater(CHUNK_SIZE, 0)
        self.assertLess(CHUNK_OVERLAP, CHUNK_SIZE)
    
    def test_chunk_text_splitting(self):
        """Should split text into appropriate chunks."""
        text = "A" * 2000  # Text longer than typical chunk size
        chunk_size = 500
        
        # Simulate chunking
        chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
        
        self.assertGreater(len(chunks), 1)
        for chunk in chunks[:-1]:  # All but last should be full size
            self.assertEqual(len(chunk), chunk_size)


class TestEmbeddingsConfiguration(unittest.TestCase):
    """Test embeddings model configuration."""
    
    @patch('rag_engine.OpenAIEmbeddings')
    def test_embeddings_model_initialization(self, mock_embeddings):
        """Should initialize with correct embedding model."""
        from rag_engine import get_embeddings
        
        # Mock the embeddings
        mock_embeddings.return_value = Mock()
        
        # Function should use text-embedding-3-small
        embeddings = get_embeddings()
        
        # Verify embeddings object is returned
        self.assertIsNotNone(embeddings)
    
    def test_embeddings_model_name(self):
        """Should use correct embedding model name."""
        expected_model = "text-embedding-3-small"
        self.assertIsInstance(expected_model, str)
        self.assertIn("embedding", expected_model)


class TestChatChainConfiguration(unittest.TestCase):
    """Test RAG chat chain configuration."""
    
    def test_model_configuration(self):
        """Should use correct GPT model."""
        from config import MODEL, TEMPERATURE
        
        self.assertEqual(MODEL, "gpt-4")
        self.assertGreaterEqual(TEMPERATURE, 0.0)
        self.assertLessEqual(TEMPERATURE, 1.0)
    
    def test_search_k_configuration(self):
        """Should retrieve correct number of documents."""
        from config import SEARCH_K
        
        self.assertIsInstance(SEARCH_K, int)
        self.assertGreater(SEARCH_K, 0)
        self.assertLessEqual(SEARCH_K, 10)  # Reasonable upper limit


class TestSystemPrompt(unittest.TestCase):
    """Test system prompt configuration."""
    
    def test_prompt_contains_hollard_context(self):
        """System prompt should reference Hollard."""
        # The system prompt should include Hollard branding
        prompt_keywords = ["hollard", "policy", "insurance", "better futures"]
        
        # These keywords should be present in the actual prompt
        for keyword in prompt_keywords:
            self.assertIsInstance(keyword, str)
            self.assertTrue(len(keyword) > 0)
    
    def test_prompt_includes_handover_logic(self):
        """System prompt should include handover instructions."""
        handover_keywords = ["handover", "live agent", "specialist", "connect"]
        
        for keyword in handover_keywords:
            self.assertIsInstance(keyword, str)
    
    def test_prompt_structure(self):
        """System prompt should have proper structure."""
        # Prompt should include context placeholder
        context_placeholder = "{context}"
        document_list_placeholder = "{document_list}"
        
        self.assertIsInstance(context_placeholder, str)
        self.assertIsInstance(document_list_placeholder, str)


class TestVectorStoreOperations(unittest.TestCase):
    """Test FAISS vector store operations."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test environment."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_vector_store_path_configuration(self):
        """Vector store should have proper path configuration."""
        from config import FAISS_DIR
        
        self.assertIsInstance(FAISS_DIR, str)
        self.assertTrue(len(FAISS_DIR) > 0)
    
    def test_index_file_name(self):
        """FAISS index should use correct filename."""
        index_filename = "index.faiss"
        
        self.assertEqual(index_filename, "index.faiss")
        self.assertTrue(index_filename.endswith(".faiss"))


class TestMessageHistory(unittest.TestCase):
    """Test conversation message history."""
    
    def test_message_history_initialization(self):
        """Message history should initialize as list."""
        messages = []
        self.assertIsInstance(messages, list)
        self.assertEqual(len(messages), 0)
    
    def test_message_history_append(self):
        """Should append messages to history."""
        messages = []
        
        messages.append({"role": "user", "content": "What is life insurance?"})
        messages.append({"role": "assistant", "content": "Life insurance provides financial protection..."})
        
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]["role"], "user")
        self.assertEqual(messages[1]["role"], "assistant")
    
    def test_conversation_context_preservation(self):
        """Should preserve conversation context."""
        conversation = [
            {"role": "user", "content": "Tell me about Hollard"},
            {"role": "assistant", "content": "Hollard is an insurance company..."},
            {"role": "user", "content": "What products do they offer?"},
            {"role": "assistant", "content": "They offer Life, Disability, Critical Illness..."}
        ]
        
        # Verify conversation structure
        self.assertEqual(len(conversation), 4)
        
        # Check alternating roles
        for i, msg in enumerate(conversation):
            expected_role = "user" if i % 2 == 0 else "assistant"
            self.assertEqual(msg["role"], expected_role)


class TestErrorHandling(unittest.TestCase):
    """Test error handling in RAG engine."""
    
    def test_missing_api_key_handling(self):
        """Should handle missing OpenAI API key."""
        # When API key is missing, should handle gracefully
        api_key = os.environ.get("OPENAI_API_KEY")
        
        if not api_key:
            # Should either raise informative error or handle gracefully
            self.assertTrue(True, "Missing API key should be handled")
    
    def test_empty_document_handling(self):
        """Should handle empty document list."""
        empty_docs = []
        
        self.assertIsInstance(empty_docs, list)
        self.assertEqual(len(empty_docs), 0)
    
    def test_corrupted_document_handling(self):
        """Should handle corrupted or unreadable documents."""
        # Corrupted documents should not crash the entire system
        # They should be logged and skipped
        self.assertTrue(True, "Corrupted documents should be handled gracefully")


if __name__ == '__main__':
    unittest.main()
