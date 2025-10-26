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
        /* Nice colors for everything */
        .main {
            background-color: #FFFEF9;
        }
        
        /* Make buttons purple and cool */
        .stButton > button {
            background-color: #6366F1;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 10px 20px;
        }
        
        .stButton > button:hover {
            background-color: #4F46E5;
        }
        
        /* Style delete buttons (🗑️) with cream background */
        .stButton > button[kind="secondary"] {
            background-color: #FFF8E7;
            color: #8B7355;
            border: 1px solid #F5E6D3;
            padding: 4px 12px;
            font-size: 16px;
        }
        
        .stButton > button[kind="secondary"]:hover {
            background-color: #F5E6D3;
            color: #6B5744;
            border-color: #E6D5C3;
        }
        
        /* Make the sidebar look nice */
        [data-testid="stSidebar"] {
            background-color: #ffffff;
        }
        </style>
    """, unsafe_allow_html=True)

def show_header():
    st.markdown("""
        <div style='background: linear-gradient(90deg, #FFF8E7, #FFFDF5); 
                    padding: 30px; 
                    border-radius: 10px; 
                    text-align: center;
                    border: 2px solid #F5E6D3;
                    margin-bottom: 20px;'>
            <div style='display: flex; align-items: center; justify-content: center; gap: 15px; margin-bottom: 10px;'>
                <!-- Silvertree Logo -->
                <svg width="250" height="105" viewBox="0 0 233 49.17" xmlns="http://www.w3.org/2000/svg">
                    <style type="text/css">
                        .st0{fill:#262425;}
                    </style>
                    <g>
                        <path class="st0" d="M63.12,24.27c-0.24-0.32-0.54-0.59-0.9-0.81c-0.36-0.22-0.79-0.33-1.3-0.33c-0.48,0-0.9,0.11-1.26,0.33
                            c-0.36,0.22-0.53,0.54-0.53,0.96c0,0.34,0.1,0.61,0.31,0.82c0.2,0.21,0.45,0.38,0.73,0.51c0.28,0.13,0.58,0.23,0.9,0.29
                            c0.32,0.06,0.59,0.12,0.82,0.17c0.44,0.11,0.85,0.25,1.24,0.41c0.39,0.16,0.72,0.37,1,0.63c0.28,0.26,0.5,0.57,0.66,0.94
                            c0.16,0.37,0.24,0.82,0.24,1.36c0,0.65-0.13,1.2-0.39,1.66c-0.26,0.46-0.59,0.83-1,1.13c-0.41,0.29-0.87,0.5-1.39,0.63
                            c-0.52,0.13-1.05,0.19-1.58,0.19c-0.89,0-1.67-0.15-2.35-0.44c-0.67-0.29-1.27-0.82-1.8-1.6l1.54-1.36
                            c0.33,0.36,0.7,0.67,1.11,0.94c0.41,0.27,0.91,0.41,1.5,0.41c0.26,0,0.52-0.03,0.78-0.08c0.26-0.06,0.5-0.15,0.7-0.27
                            c0.2-0.12,0.37-0.27,0.5-0.46c0.13-0.19,0.19-0.4,0.19-0.64c0-0.32-0.09-0.59-0.28-0.8c-0.19-0.21-0.42-0.38-0.68-0.5
                            c-0.26-0.12-0.54-0.22-0.84-0.29c-0.29-0.07-0.56-0.13-0.78-0.18c-0.44-0.11-0.85-0.24-1.25-0.39c-0.39-0.15-0.74-0.34-1.04-0.58
                            c-0.3-0.24-0.54-0.55-0.73-0.92c-0.18-0.37-0.27-0.83-0.27-1.38c0-0.6,0.12-1.12,0.35-1.56c0.23-0.44,0.54-0.81,0.93-1.1
                            c0.39-0.29,0.82-0.51,1.31-0.65c0.49-0.15,0.99-0.22,1.48-0.22c0.73,0,1.42,0.15,2.08,0.44c0.66,0.29,1.19,0.77,1.59,1.45
                            L63.12,24.27z"/>
                        <path class="st0" d="M68.29,17.61c0-0.44,0.16-0.81,0.47-1.13c0.31-0.31,0.69-0.47,1.13-0.47c0.44,0,0.81,0.16,1.13,0.47
                            c0.31,0.31,0.47,0.69,0.47,1.13s-0.16,0.81-0.47,1.13c-0.31,0.31-0.69,0.47-1.13,0.47c-0.44,0-0.81-0.16-1.13-0.47
                            C68.45,18.42,68.29,18.05,68.29,17.61z M68.77,21.39h2.04v11.47h-2.04V21.39z"/>
                        <path class="st0" d="M75.53,16.2h2.04v16.67h-2.04V16.2z"/>
                        <path class="st0" d="M80.26,21.39h2.51l3.43,8.79l3.29-8.79h2.32l-4.49,11.47h-2.39L80.26,21.39z"/>
                        <path class="st0" d="M95.99,27.93c0,0.5,0.1,0.96,0.31,1.37c0.21,0.41,0.48,0.76,0.82,1.05c0.34,0.29,0.73,0.52,1.18,0.68
                            c0.45,0.16,0.91,0.24,1.39,0.24c0.65,0,1.21-0.16,1.69-0.47c0.48-0.31,0.92-0.73,1.32-1.25l1.58,1.26
                            c-1.16,1.57-2.78,2.35-4.87,2.35c-0.87,0-1.65-0.15-2.36-0.46c-0.7-0.31-1.3-0.73-1.79-1.27c-0.49-0.54-0.86-1.18-1.13-1.91
                            c-0.26-0.73-0.39-1.53-0.39-2.38c0-0.85,0.14-1.65,0.43-2.38c0.29-0.73,0.68-1.37,1.18-1.91c0.5-0.54,1.1-0.96,1.8-1.27
                            c0.7-0.31,1.45-0.46,2.27-0.46c0.97,0,1.8,0.18,2.47,0.53c0.67,0.36,1.23,0.82,1.66,1.39c0.43,0.57,0.75,1.22,0.94,1.94
                            c0.19,0.72,0.29,1.45,0.29,2.19v0.77H95.99z M102.58,26.19c-0.02-0.48-0.09-0.93-0.22-1.33c-0.13-0.4-0.33-0.75-0.59-1.05
                            c-0.26-0.3-0.59-0.53-0.99-0.7s-0.85-0.25-1.38-0.25c-0.51,0-0.98,0.1-1.4,0.3c-0.43,0.2-0.79,0.46-1.08,0.79
                            c-0.29,0.32-0.52,0.68-0.68,1.08c-0.16,0.4-0.24,0.79-0.24,1.17H102.58z"/>
                        <path class="st0" d="M108.17,21.39h2.19v1.77h0.05c0.15-0.31,0.34-0.58,0.58-0.83c0.24-0.25,0.52-0.46,0.82-0.64
                            c0.3-0.18,0.63-0.32,0.99-0.42c0.36-0.1,0.71-0.16,1.07-0.16c0.36,0,0.68,0.05,0.97,0.15l-0.1,2.35c-0.18-0.05-0.36-0.09-0.54-0.12
                            c-0.18-0.03-0.36-0.05-0.54-0.05c-1.07,0-1.89,0.3-2.46,0.9c-0.57,0.6-0.85,1.52-0.85,2.78v5.76h-2.19V21.39z"/>
                        <path class="st0" d="M124.2,23.28h-2.99v5.2c0,0.32,0.01,0.64,0.02,0.96c0.02,0.31,0.07,0.6,0.17,0.85
                            c0.1,0.25,0.26,0.45,0.46,0.61c0.21,0.15,0.51,0.23,0.92,0.23c0.25,0,0.5-0.02,0.77-0.07c0.26-0.05,0.5-0.14,0.72-0.27v1.98
                            c-0.25,0.15-0.57,0.25-0.96,0.3c-0.39,0.06-0.7,0.08-0.92,0.08c-0.8,0-1.43-0.12-1.87-0.35c-0.44-0.23-0.77-0.54-0.97-0.91
                            c-0.21-0.37-0.33-0.79-0.37-1.25c-0.04-0.46-0.06-0.92-0.06-1.39v-5.98h-2.41v-1.89h2.41v-3.22h2.09v3.22h2.99V23.28z"/>
                        <path class="st0" d="M127.06,21.39h2.09v1.77h0.05c0.14-0.31,0.32-0.58,0.56-0.83c0.23-0.25,0.49-0.46,0.78-0.64
                            c0.29-0.18,0.6-0.32,0.94-0.42c0.34-0.1,0.68-0.16,1.02-0.16c0.34,0,0.65,0.05,0.93,0.15l-0.09,2.35
                            c-0.17-0.05-0.34-0.09-0.51-0.12c-0.17-0.03-0.34-0.05-0.51-0.05c-1.02,0-1.8,0.3-2.34,0.9c-0.54,0.6-0.81,1.52-0.81,2.78v5.76
                            h-2.09V21.39z"/>
                        <path class="st0" d="M137.63,27.93c0,0.5,0.1,0.96,0.31,1.37c0.21,0.41,0.48,0.76,0.82,1.05c0.34,0.29,0.73,0.52,1.18,0.68
                            c0.45,0.16,0.91,0.24,1.39,0.24c0.65,0,1.21-0.16,1.69-0.47c0.48-0.31,0.92-0.73,1.32-1.25l1.58,1.26
                            c-1.16,1.57-2.78,2.35-4.87,2.35c-0.87,0-1.65-0.15-2.36-0.46c-0.7-0.31-1.3-0.73-1.79-1.27c-0.49-0.54-0.86-1.18-1.13-1.91
                            c-0.26-0.73-0.39-1.53-0.39-2.38c0-0.85,0.14-1.65,0.43-2.38c0.29-0.73,0.68-1.37,1.18-1.91c0.5-0.54,1.1-0.96,1.8-1.27
                            c0.7-0.31,1.45-0.46,2.27-0.46c0.97,0,1.8,0.18,2.47,0.53c0.67,0.36,1.23,0.82,1.66,1.39c0.43,0.57,0.75,1.22,0.94,1.94
                            c0.19,0.72,0.29,1.45,0.29,2.19v0.77H137.63z M144.22,26.19c-0.02-0.48-0.09-0.93-0.22-1.33c-0.13-0.4-0.33-0.75-0.59-1.05
                            c-0.26-0.3-0.59-0.53-0.99-0.7c-0.39-0.17-0.85-0.25-1.38-0.25c-0.51,0-0.98,0.1-1.4,0.3c-0.43,0.2-0.79,0.46-1.08,0.79
                            c-0.29,0.32-0.52,0.68-0.68,1.08c-0.16,0.4-0.24,0.79-0.24,1.17H144.22z"/>
                        <path class="st0" d="M151.59,27.93c0,0.5,0.1,0.96,0.31,1.37c0.21,0.41,0.48,0.76,0.82,1.05c0.34,0.29,0.73,0.52,1.18,0.68
                            c0.45,0.16,0.91,0.24,1.39,0.24c0.65,0,1.21-0.16,1.69-0.47c0.48-0.31,0.92-0.73,1.32-1.25l1.58,1.26
                            c-1.16,1.57-2.78,2.35-4.87,2.35c-0.87,0-1.65-0.15-2.36-0.46c-0.7-0.31-1.3-0.73-1.79-1.27c-0.49-0.54-0.86-1.18-1.13-1.91
                            c-0.26-0.73-0.39-1.53-0.39-2.38c0-0.85,0.14-1.65,0.43-2.38c0.29-0.73,0.68-1.37,1.18-1.91c0.5-0.54,1.1-0.96,1.8-1.27
                            c0.7-0.31,1.45-0.46,2.27-0.46c0.97,0,1.8,0.18,2.47,0.53c0.67,0.36,1.23,0.82,1.66,1.39c0.43,0.57,0.75,1.22,0.94,1.94
                            c0.19,0.72,0.29,1.45,0.29,2.19v0.77H151.59z M158.18,26.19c-0.02-0.48-0.09-0.93-0.22-1.33c-0.13-0.4-0.33-0.75-0.59-1.05
                            c-0.26-0.3-0.59-0.53-0.99-0.7c-0.39-0.17-0.85-0.25-1.38-0.25c-0.51,0-0.98,0.1-1.4,0.3c-0.43,0.2-0.79,0.46-1.08,0.79
                            c-0.29,0.32-0.52,0.68-0.68,1.08c-0.16,0.4-0.24,0.79-0.24,1.17H158.18z"/>
                        <path class="st0" d="M163.71,16.2h1.38v7.52h0.05c0.21-0.38,0.48-0.72,0.8-1c0.32-0.28,0.67-0.51,1.04-0.70
                            c0.38-0.18,0.77-0.32,1.18-0.41c0.41-0.09,0.82-0.13,1.22-0.13c0.81,0,1.56,0.14,2.24,0.43c0.68,0.29,1.27,0.69,1.77,1.21
                            c0.5,0.52,0.88,1.14,1.16,1.85c0.28,0.71,0.41,1.49,0.41,2.34c0,0.85-0.14,1.63-0.41,2.34c-0.28,0.71-0.66,1.33-1.16,1.85
                            c-0.5,0.52-1.09,0.92-1.77,1.21c-0.68,0.29-1.43,0.43-2.24,0.43c-0.4,0-0.8-0.04-1.22-0.13c-0.41-0.09-0.81-0.22-1.18-0.41
                            c-0.38-0.18-0.72-0.42-1.04-0.7c-0.32-0.28-0.59-0.61-0.8-1h-0.05v1.94h-1.38V16.2z M164.95,27.32c0,0.62,0.11,1.21,0.34,1.76
                            c0.23,0.55,0.54,1.03,0.94,1.44c0.4,0.41,0.86,0.73,1.4,0.97c0.54,0.24,1.12,0.36,1.74,0.36c0.64,0,1.22-0.12,1.74-0.36
                            c0.52-0.24,0.96-0.56,1.33-0.97c0.37-0.41,0.65-0.89,0.84-1.44c0.19-0.55,0.29-1.14,0.29-1.76c0-0.62-0.1-1.21-0.29-1.76
                            c-0.19-0.55-0.47-1.03-0.84-1.44c-0.37-0.41-0.81-0.73-1.33-0.97c-0.52-0.24-1.1-0.36-1.74-0.36c-0.63,0-1.21,0.12-1.74,0.36
                            c-0.54,0.24-1,0.56-1.4,0.97c-0.4,0.41-0.71,0.89-0.94,1.44C165.07,26.11,164.95,26.7,164.95,27.32z"/>
                        <path class="st0" d="M178.38,24.67c0-0.21-0.01-0.47-0.02-0.78c-0.02-0.3-0.03-0.61-0.03-0.93c-0.01-0.31-0.02-0.61-0.03-0.88
                            c-0.02-0.27-0.02-0.48-0.02-0.63h1.34c0.01,0.43,0.03,0.84,0.03,1.24c0.01,0.4,0.03,0.65,0.06,0.77c0.34-0.68,0.78-1.23,1.32-1.66
                            c0.54-0.43,1.19-0.64,1.96-0.64c0.13,0,0.26,0.01,0.39,0.04c0.13,0.02,0.26,0.05,0.39,0.09l-0.16,1.46
                            c-0.18-0.07-0.35-0.1-0.51-0.1c-0.58,0-1.08,0.1-1.5,0.31c-0.42,0.21-0.77,0.49-1.05,0.85c-0.28,0.36-0.48,0.79-0.61,1.27
                            c-0.13,0.49-0.2,1.01-0.2,1.57v6.23h-1.34V24.67z"/>
                        <path class="st0" d="M194.04,28.07c0,0.56,0,1.06,0.01,1.51c0.01,0.44,0.02,0.86,0.04,1.23c0.02,0.38,0.04,0.73,0.06,1.06
                            c0.02,0.33,0.06,0.66,0.11,0.99h-1.33c-0.09-0.56-0.14-1.18-0.14-1.85h-0.05c-0.41,0.74-0.92,1.28-1.53,1.63
                            c-0.61,0.35-1.38,0.52-2.31,0.52c-0.47,0-0.94-0.06-1.4-0.19c-0.46-0.12-0.87-0.32-1.23-0.59c-0.36-0.27-0.66-0.62-0.89-1.05
                            c-0.23-0.43-0.34-0.95-0.34-1.56c0-0.87,0.21-1.56,0.64-2.07c0.43-0.51,0.95-0.89,1.58-1.15c0.62-0.25,1.29-0.42,1.99-0.49
                            c0.7-0.07,1.32-0.11,1.86-0.11h1.66v-0.69c0-0.99-0.29-1.69-0.88-2.12c-0.58-0.43-1.32-0.64-2.21-0.64c-1.26,0-2.38,0.43-3.34,1.28
                            l-0.83-1.01c0.52-0.53,1.17-0.93,1.94-1.2c0.77-0.27,1.52-0.41,2.23-0.41c1.33,0,2.39,0.33,3.18,0.98c0.79,0.65,1.19,1.7,1.19,3.15
                            V28.07z M191.2,27.13c-0.6,0-1.18,0.04-1.74,0.12c-0.56,0.08-1.07,0.22-1.52,0.42c-0.45,0.2-0.81,0.46-1.08,0.79
                            c-0.27,0.33-0.4,0.74-0.4,1.23c0,0.35,0.07,0.65,0.23,0.93c0.15,0.27,0.34,0.49,0.58,0.67c0.24,0.17,0.5,0.3,0.79,0.39
                            c0.29,0.09,0.59,0.14,0.89,0.14c0.76,0,1.38-0.11,1.87-0.35c0.49-0.23,0.88-0.53,1.17-0.9c0.29-0.37,0.49-0.79,0.6-1.26
                            c0.11-0.47,0.17-0.94,0.17-1.42v-0.77H191.2z"/>
                        <path class="st0" d="M198.04,24.67c0-0.21-0.01-0.47-0.02-0.78c-0.02-0.3-0.03-0.61-0.03-0.93c-0.01-0.31-0.02-0.61-0.03-0.88
                            c-0.02-0.27-0.02-0.48-0.02-0.63h1.34c0.01,0.43,0.03,0.84,0.03,1.24c0.01,0.4,0.03,0.65,0.06,0.77h0.07
                            c0.27-0.63,0.71-1.17,1.34-1.62c0.62-0.45,1.35-0.68,2.18-0.68c0.8,0,1.46,0.14,1.96,0.42c0.51,0.28,0.9,0.65,1.19,1.1
                            c0.29,0.45,0.49,0.98,0.6,1.57c0.11,0.59,0.17,1.2,0.17,1.83v6.8h-1.34v-6.73c0-0.46-0.04-0.91-0.11-1.35
                            c-0.07-0.44-0.2-0.83-0.39-1.17c-0.19-0.35-0.45-0.62-0.78-0.83c-0.33-0.21-0.77-0.31-1.3-0.31c-0.49,0-0.96,0.1-1.39,0.28
                            c-0.44,0.19-0.82,0.48-1.14,0.87c-0.32,0.39-0.57,0.87-0.76,1.46c-0.19,0.59-0.28,1.27-0.28,2.07v5.71h-1.34V24.67z"/>
                        <path class="st0" d="M220.47,30.91h-0.05c-0.22,0.39-0.50,0.72-0.83,1c-0.33,0.28-0.69,0.52-1.08,0.70c-0.39,0.19-0.80,0.32-1.22,0.41
                            c-0.43,0.09-0.85,0.13-1.26,0.13c-0.84,0-1.62-0.15-2.33-0.43c-0.71-0.29-1.32-0.7-1.83-1.22c-0.51-0.52-0.90-1.14-1.19-1.86
                            c-0.29-0.72-0.43-1.5-0.43-2.36c0-0.85,0.14-1.64,0.43-2.36c0.29-0.72,0.68-1.34,1.19-1.86c0.51-0.52,1.12-0.93,1.83-1.22
                            c0.71-0.29,1.49-0.43,2.33-0.43c0.41,0,0.83,0.04,1.26,0.13c0.43,0.09,0.84,0.23,1.22,0.41c0.39,0.19,0.75,0.42,1.08,0.7
                            c0.33,0.28,0.61,0.62,0.83,1h0.05V16.2h1.43v16.67h-1.43V30.91z M220.61,27.29c0-0.63-0.12-1.22-0.36-1.78s-0.56-1.04-0.97-1.45
                            c-0.41-0.41-0.90-0.74-1.45-0.98c-0.56-0.24-1.16-0.36-1.81-0.36c-0.67,0-1.27,0.12-1.81,0.36c-0.54,0.24-1,0.57-1.38,0.98
                            c-0.38,0.41-0.67,0.89-0.87,1.45c-0.2,0.56-0.30,1.15-0.30,1.78c0,0.63,0.1,1.22,0.30,1.78c0.2,0.56,0.49,1.04,0.87,1.45
                            c0.38,0.41,0.84,0.74,1.38,0.98c0.54,0.24,1.14,0.36,1.81,0.36c0.65,0,1.25-0.12,1.81-0.36c0.55-0.24,1.04-0.57,1.45-0.98
                            c0.41-0.41,0.74-0.89,0.97-1.45C220.5,28.51,220.61,27.91,220.61,27.29z"/>
                        <path class="st0" d="M226.31,30.03c0.28,0.59,0.70,1.05,1.25,1.36c0.55,0.31,1.13,0.47,1.74,0.47c0.28,0,0.56-0.05,0.85-0.14
                            c0.28-0.10,0.53-0.23,0.76-0.41c0.22-0.18,0.40-0.39,0.55-0.64c0.14-0.25,0.21-0.53,0.21-0.85c0-0.51-0.15-0.9-0.46-1.16
                            c-0.30-0.26-0.68-0.46-1.13-0.60c-0.45-0.14-0.94-0.27-1.47-0.37c-0.54-0.10-1.03-0.26-1.47-0.48c-0.45-0.22-0.82-0.52-1.13-0.90
                            c-0.30-0.39-0.46-0.93-0.46-1.64c0-0.55,0.10-1.02,0.31-1.42c0.21-0.40,0.48-0.73,0.81-1c0.33-0.26,0.71-0.46,1.13-0.59
                            c0.42-0.13,0.84-0.19,1.27-0.19c0.85,0,1.58,0.17,2.2,0.51c0.62,0.34,1.10,0.87,1.44,1.59l-1.2,0.77c-0.25-0.51-0.57-0.9-0.95-1.17
                            c-0.38-0.26-0.87-0.4-1.48-0.40c-0.24,0-0.49,0.04-0.75,0.12c-0.26,0.08-0.49,0.19-0.70,0.34c-0.21,0.14-0.38,0.33-0.52,0.55
                            c-0.14,0.23-0.21,0.48-0.21,0.77c0,0.5,0.15,0.87,0.46,1.11c0.30,0.24,0.68,0.43,1.13,0.57c0.45,0.14,0.94,0.25,1.47,0.35
                            c0.53,0.10,1.03,0.25,1.47,0.47c0.45,0.22,0.82,0.53,1.13,0.94c0.30,0.41,0.46,0.99,0.46,1.75c0,0.58-0.10,1.08-0.30,1.50
                            c-0.20,0.43-0.48,0.78-0.82,1.07c-0.35,0.29-0.75,0.51-1.19,0.65c-0.45,0.14-0.91,0.22-1.40,0.22c-0.89,0-1.71-0.18-2.44-0.55
                            c-0.74-0.37-1.30-0.94-1.71-1.71L226.31,30.03z"/>
                    </g>
                    <path class="st0" d="M28.13,11l-3.43,3.14c-0.23,0.23-0.61,0.23-0.84,0L20.42,11c-0.23-0.23-0.23-0.61,0-0.84l3.43-5.38
                        c0.23-0.23,0.61-0.23,0.84,0l3.43,5.38C28.36,10.39,28.36,10.77,28.13,11z"/>
                    <path class="st0" d="M24.59,0C11.01,0,0,11.01,0,24.59c0,13.2,10.4,23.97,23.46,24.56v-0.4v-1.33v-29.6c0.01-0.1,0.01-0.19,0-0.27
                        c-0.46-3.26-6.98-7.5-6.98-7.5s-0.98,6.08,1.46,8.55c1.9,1.92,2.99,2.56,3.55,2.77v2.8l-8.13-6.63c0,0-1.26,6.27,1.46,8.55
                        c2.68,2.25,5.51,4.37,6.66,5.21v3.06L9.93,25.05c0,0-1.26,6.27,1.46,8.55c3.04,2.56,8.78,6.89,10.11,7.89v5.75
                        C10.33,45.73,1.71,36.17,1.71,24.59c0-12.62,10.23-22.85,22.85-22.85c12.62,0,22.85,10.23,22.85,22.85
                        c0,12.44-9.94,22.55-22.31,22.84v1.74C38.45,48.89,49.19,38,49.19,24.59C49.19,11.01,38.17,0,24.59,0z"/>
                    <path class="st0" d="M32.27,15.33c-0.11,4.28-7.16,8.47-7.16,8.47s-0.14-4.04,0-5.39c0.33-3.14,7.07-7.61,7.07-7.61
                        S32.3,13.98,32.27,15.33z"/>
                    <path class="st0" d="M37.83,33.19c-2.23,3.38-5.06,5.13-10.57,9.2C26.91,42.64,25.11,44,25.11,44l0,0
                        c-0.01-0.76-0.13-3.97-0.09-5.31c0.04-1.36,1.27-2.87,1.84-3.4c1.81-1.68,5.72-4.80,11.17-9.1C38.72,29.41,38.61,32,37.83,33.19z"/>
                    <path class="st0" d="M34.97,25.37c-1.24,1.76-1.95,2.61-7.64,6.84c-0.36,0.27-2.21,1.68-2.21,1.68l0,0c0-0.77-0.06-4.03,0-5.39
                        c0.06-1.38,1.34-2.94,1.94-3.49c1.87-1.73,2.61-2.29,8.25-6.76C35.94,21.52,35.81,24.17,34.97,25.37z"/>
                </svg>
            </div>
            <p style='color: #6B7280; margin: 5px 0 0 0; font-size: 1rem;'>
                "Consumer Brands with Purpose"
            </p>
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

st.set_page_config(page_title="Silvertree", page_icon="💬", layout="wide")

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

st.subheader("Chat")

# Initialize messages in session state if not exists
if "messages" not in st.session_state:
    st.session_state.messages = []

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
    avatar = "👤" if message["role"] == "user" else "🌳"
    with st.chat_message(message["role"], avatar=avatar):
        st.write(message["content"])

# Chat input - disabled if no documents
if not chain:
    st.info("👋 Upload documents to start chatting!")
    # Display disabled input to show chat is unavailable
    st.chat_input("Upload documents first...", disabled=True)
elif user_input := st.chat_input("Ask about your documents..."):
    # Add user message to session state and display it
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="👤"):
        st.write(user_input)
    
    # Generate and display assistant response
    with st.chat_message("assistant", avatar="🌳"):
        try:
            with st.spinner("Thinking..."):
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