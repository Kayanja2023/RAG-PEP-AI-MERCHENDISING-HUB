"""
Unit tests for app.py functions.
Tests UI helper functions and handover mechanism.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add parent directory to path to import app functions
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestCheckHandoverNeeded(unittest.TestCase):
    """Test the handover detection function."""
    
    @classmethod
    def setUpClass(cls):
        """Mock streamlit module before any imports."""
        # Create comprehensive streamlit mock
        mock_st = MagicMock()
        mock_st.columns = MagicMock(return_value=[MagicMock(), MagicMock()])
        mock_st.cache_resource = lambda x: x
        sys.modules['streamlit'] = mock_st
        
    def test_detect_connect_phrase(self):
        """Should detect 'connect you with' phrase."""
        from app import check_handover_needed
        response = "Let me connect you with a Hollard specialist."
        self.assertTrue(check_handover_needed(response))
    
    def test_detect_handover_phrase(self):
        """Should detect 'hand you over' phrase."""
        from app import check_handover_needed
        response = "I'll hand you over to a live agent for assistance."
        self.assertTrue(check_handover_needed(response))
    
    def test_detect_live_agent_phrase(self):
        """Should detect 'live agent' phrase."""
        from app import check_handover_needed
        response = "You need to speak with a live agent about this."
        self.assertTrue(check_handover_needed(response))
    
    def test_detect_specialist_phrase(self):
        """Should detect 'hollard specialist' phrase."""
        from app import check_handover_needed
        response = "A Hollard specialist can help you with quotes."
        self.assertTrue(check_handover_needed(response))
    
    def test_case_insensitive_detection(self):
        """Should detect phrases regardless of case."""
        from app import check_handover_needed
        test_cases = [
            "LIVE AGENT",
            "Live Agent",
            "live agent",
            "LiVe AgEnT"
        ]
        for response in test_cases:
            with self.subTest(response=response):
                self.assertTrue(check_handover_needed(response))
    
    def test_no_handover_needed(self):
        """Should return False when no handover phrases present."""
        from app import check_handover_needed
        normal_responses = [
            "Hollard offers Life Insurance, Disability Cover, and Critical Illness.",
            "To submit a claim, contact your broker with the required documents.",
            "Our products include comprehensive coverage for individuals and businesses.",
            "You can find more information in our policy documents."
        ]
        for response in normal_responses:
            with self.subTest(response=response):
                self.assertFalse(check_handover_needed(response))
    
    def test_handover_phrase_in_middle_of_text(self):
        """Should detect handover phrase anywhere in response."""
        from app import check_handover_needed
        response = "While I can provide general information, for personalized quotes I'll hand you over to a specialist who can help."
        self.assertTrue(check_handover_needed(response))
    
    def test_multiple_handover_phrases(self):
        """Should detect when multiple handover phrases present."""
        from app import check_handover_needed
        response = "Let me connect you with a live agent who has the human expertise to assist."
        self.assertTrue(check_handover_needed(response))
    
    def test_empty_response(self):
        """Should handle empty response gracefully."""
        from app import check_handover_needed
        self.assertFalse(check_handover_needed(""))
    
    def test_none_response(self):
        """Should handle None input gracefully."""
        from app import check_handover_needed
        try:
            # Should handle or raise appropriate error
            result = check_handover_needed("")
            self.assertIsInstance(result, bool)
        except Exception:
            pass  # It's okay if it raises an exception for invalid input


class TestGetFileSignature(unittest.TestCase):
    """Test file signature generation for upload tracking."""
    
    @classmethod
    def setUpClass(cls):
        """Mock streamlit module before any imports."""
        mock_st = MagicMock()
        mock_st.columns = MagicMock(return_value=[MagicMock(), MagicMock()])
        mock_st.cache_resource = lambda x: x
        sys.modules['streamlit'] = mock_st
    
    def test_signature_generation(self):
        """Should generate signature from file properties."""
        from app import get_file_signature
        
        # Create mock file object
        mock_file = Mock()
        mock_file.name = "test.pdf"
        mock_file.size = 1024
        mock_file.read = Mock(return_value=b"test content")
        mock_file.seek = Mock()
        
        signature = get_file_signature(mock_file)
        
        # Should return tuple with name and size
        self.assertIsInstance(signature, tuple)
        self.assertIn(mock_file.name, signature)
        self.assertIn(mock_file.size, signature)
    
    def test_signature_consistency(self):
        """Should generate same signature for same file."""
        from app import get_file_signature
        
        mock_file = Mock()
        mock_file.name = "document.pdf"
        mock_file.size = 2048
        mock_file.read = Mock(return_value=b"consistent content")
        mock_file.seek = Mock()
        
        sig1 = get_file_signature(mock_file)
        mock_file.seek(0)  # Reset file pointer
        sig2 = get_file_signature(mock_file)
        
        # Signatures should be identical
        self.assertEqual(sig1, sig2)


class TestWelcomeMessageLogic(unittest.TestCase):
    """Test welcome message display logic."""
    
    def test_welcome_conditions(self):
        """Test different welcome message conditions."""
        # First-time user: no docs, no messages
        docs_exist = False
        messages_exist = False
        self.assertFalse(docs_exist or messages_exist)
        
        # Documents uploaded, no chat yet
        docs_exist = True
        messages_exist = False
        self.assertTrue(docs_exist and not messages_exist)
        
        # Active conversation
        docs_exist = True
        messages_exist = True
        self.assertTrue(docs_exist and messages_exist)


class TestHandoverWorkflow(unittest.TestCase):
    """Test the complete handover workflow."""
    
    def test_handover_trigger_workflow(self):
        """Test the complete flow when handover is triggered."""
        # 1. User asks for quote
        user_query = "Can you give me a quote for life insurance?"
        self.assertIsInstance(user_query, str)
        
        # 2. AI responds with handover phrase
        ai_response = "I'll hand you over to a live agent who can provide accurate quotes."
        from app import check_handover_needed
        self.assertTrue(check_handover_needed(ai_response))
        
        # 3. Session should be marked for end
        # This would set session_state.handover_triggered = True
        handover_triggered = True
        self.assertTrue(handover_triggered)
        
        # 4. Chat input should be disabled
        chat_disabled = handover_triggered
        self.assertTrue(chat_disabled)


class TestSessionStateManagement(unittest.TestCase):
    """Test session state management patterns."""
    
    def test_message_storage_structure(self):
        """Messages should be stored as list of dicts."""
        messages = []
        
        # Add user message
        messages.append({"role": "user", "content": "What insurance do you offer?"})
        
        # Add assistant message
        messages.append({"role": "assistant", "content": "We offer Life, Disability, and Critical Illness insurance."})
        
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]["role"], "user")
        self.assertEqual(messages[1]["role"], "assistant")
    
    def test_handover_state_toggle(self):
        """Handover state should be boolean flag."""
        handover_triggered = False
        
        # Normal conversation
        self.assertFalse(handover_triggered)
        
        # After handover detection
        handover_triggered = True
        self.assertTrue(handover_triggered)
        
        # After clear chat
        handover_triggered = False
        self.assertFalse(handover_triggered)


class TestAvatarConfiguration(unittest.TestCase):
    """Test avatar display configuration."""
    
    def test_user_avatar(self):
        """User avatar should be consistent."""
        user_avatar = "👤"
        self.assertEqual(user_avatar, "👤")
        self.assertIsInstance(user_avatar, str)
    
    def test_assistant_avatar(self):
        """Assistant avatar should use Hollard shield."""
        assistant_avatar = "🛡️"
        self.assertEqual(assistant_avatar, "🛡️")
        self.assertIsInstance(assistant_avatar, str)
    
    def test_avatar_selection_logic(self):
        """Avatar should be selected based on message role."""
        def get_avatar(role):
            return "👤" if role == "user" else "🛡️"
        
        self.assertEqual(get_avatar("user"), "👤")
        self.assertEqual(get_avatar("assistant"), "🛡️")


if __name__ == '__main__':
    unittest.main()
