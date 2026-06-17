AI Study Companion (StudyGenie AI) is an intelligent learning assistant designed to help students improve their study experience through Artificial Intelligence and Natural Language Processing (NLP). The system allows users to upload study materials such as notes, syllabus documents, and previous year question papers (PYQs), and automatically generates personalized learning resources including quizzes, flashcards, important topics, summaries, and study plans.

The project integrates modern AI technologies such as Sentence Transformers, Retrieval-Augmented Generation (RAG), Tesseract-OCR, and Ollama Large Language Models (LLMs) to provide accurate and context-aware educational assistance.

🎯 Problem Statement

Students often face difficulties in:

Understanding lengthy syllabus content
Identifying important exam topics
Organizing study materials effectively
Creating study plans
Practicing with relevant questions

StudyGenie AI addresses these challenges by automatically analyzing educational content and generating intelligent study resources.

✨ Key Features
Upload Notes, Syllabus, and PYQs
OCR-based Text Extraction from Scanned Documents
Semantic Search using Sentence Transformers
AI-powered Question Answering
Quiz Generation
Flashcard Generation
Important Topic Identification
Study Plan Creation
Study Material Summarization
Retrieval-Augmented Generation (RAG)
🏗️ System Architecture
User
  ↓
Streamlit Frontend
  ↓
FastAPI Backend
  ↓
Document Upload
  ↓
Tesseract-OCR
  ↓
Text Preprocessing
  ↓
Sentence Transformer
(all-MiniLM-L6-v2)
  ↓
Vector Database
(FAISS / ChromaDB)
  ↓
RAG Pipeline
  ↓
Ollama LLM
  ↓
Generated Response
  ↓
User Interface
🛠️ Technologies Used
Frontend
Streamlit
Backend
FastAPI
Uvicorn
Artificial Intelligence & NLP
Sentence Transformers
Hugging Face
Ollama
Tesseract-OCR
NLTK
spaCy
Vector Database
FAISS
ChromaDB
Data Processing
Pandas
NumPy
PyPDF2
pdfplumber
Development Tools
Visual Studio Code
Jupyter Notebook
GitHub
🤖 Models Used
1. Sentence Transformer

Model: sentence-transformers/all-MiniLM-L6-v2

Purpose:

Generate semantic embeddings
Similarity search
Topic matching
Context retrieval
2. Ollama LLM

Purpose:

Quiz generation
Flashcard generation
Study plan generation
Summarization
Question answering
3. Tesseract-OCR

Purpose:

Extract text from scanned PDFs
Read image-based notes
OCR processing
🔄 Working of the System
User uploads notes, PDFs, syllabus, or PYQs.
Tesseract-OCR extracts text from scanned documents.
Text preprocessing is performed.
Sentence Transformer generates embeddings.
Embeddings are stored in FAISS/ChromaDB.
Relevant content is retrieved using semantic search.
RAG builds contextual prompts.
Ollama generates intelligent responses.
Results are displayed through Streamlit.
📋 Generated Outputs

The system can generate:

Quiz Questions
Flashcards
Study Summaries
Important Topics
Personalized Study Plans
AI-generated Answers
💻 Software Requirements
Windows 10/11
Python 3.10+
Streamlit
FastAPI
Ollama
Tesseract-OCR
FAISS/ChromaDB
⚙️ Hardware Requirements
Minimum
Intel i3 Processor
8 GB RAM
256 GB Storage
Recommended
Intel i5/i7 Processor
16 GB RAM
SSD Storage
🚀 Future Scope
Multi-language support
Voice-based learning assistant
Mobile application integration
Personalized learning analytics
Cloud deployment
Advanced LLM integration
Real-time collaborative learning
✅ Advantages
Saves study time
Improves exam preparation
Generates personalized learning resources
Supports scanned and digital documents
Enhances learning efficiency
Easy-to-use interface
📖 Conclusion

AI Study Companion (StudyGenie AI) is an AI-powered educational platform that combines OCR, NLP, semantic search, and Large Language Models to provide intelligent learning support. By automating content analysis and study material generation, the system helps students learn more efficiently and effectively.

👨‍💻 Developed By

Mohit Kumar Datta
B.Tech (Computer Science Engineering)
IKGPTU, Hoshiarpur

Project: AI Study Companion (StudyGenie AI)
Year: 2025-2026
