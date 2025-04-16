import os
import re
import logging
import traceback
from typing import Optional
import random
from collections import Counter

# Document text extraction libraries
try:
    from docx import Document as DocxDocument
    import PyPDF2
except ImportError:
    logging.error("Missing document processing dependencies. Install python-docx and PyPDF2")

# Constants
MAX_SUMMARY_INPUT_LENGTH = 4096
MIN_SUMMARY_LENGTH = 30
MAX_SUMMARY_LENGTH = 150

def clean_text(text: str) -> str:
    """Removes excessive whitespace from text"""
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces/newlines with single space
    return text.strip()

def extract_text(filename: str) -> Optional[str]:
    """Extracts text from TXT, DOCX, or PDF files"""
    if not os.path.exists(filename):
        logging.error(f"File not found: {filename}")
        return None
    
    _, ext = os.path.splitext(filename)
    ext = ext.lower()
    
    logging.debug(f"Extracting text from '{filename}' ({ext})...")
    
    try:
        if ext == ".txt":
            with open(filename, "r", encoding="utf-8", errors='ignore') as f:
                return f.read()
                
        elif ext == ".docx":
            doc = DocxDocument(filename)
            return "\n".join([para.text for para in doc.paragraphs if para.text])
            
        elif ext == ".pdf":
            text_content = []
            with open(filename, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                num_pages = len(reader.pages)
                logging.debug(f"Found {num_pages} page(s) in PDF.")
                
                for i, page in enumerate(reader.pages):
                    page_text = page.extract_text()
                    if page_text:
                        text_content.append(page_text)
                        
            return "\n".join(text_content) if text_content else None
            
        else:
            logging.error(f"Unsupported file extension: {ext}")
            return None
            
    except Exception as e:
        logging.error(f"Error extracting text from {filename}: {e}")
        traceback.print_exc()
        return None

def simple_summarize(text, max_sentences=5):
    """
    A simple extractive summarization method that selects important sentences
    based on word frequency and sentence position.
    """
    if not text or len(text) < 50:  # Too short to summarize
        return text
    
    # Split text into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    if len(sentences) <= max_sentences:
        return text  # Text is already short enough
    
    # Remove punctuation and convert to lowercase for word frequency analysis
    clean_sentences = [re.sub(r'[^\w\s]', '', s).lower() for s in sentences]
    
    # Get word frequencies
    all_words = ' '.join(clean_sentences).split()
    word_freq = Counter(all_words)
    
    # Score sentences based on word frequency and position
    sentence_scores = []
    for i, (sentence, clean_sentence) in enumerate(zip(sentences, clean_sentences)):
        # Score based on word frequency
        words = clean_sentence.split()
        if len(words) == 0:
            continue
            
        freq_score = sum(word_freq[word] for word in words) / len(words)
        
        # Position score - favor sentences at beginning and end
        pos_score = 1.0
        if i < len(sentences) // 3:  # Beginning
            pos_score = 1.5
        elif i > 2 * len(sentences) // 3:  # End
            pos_score = 1.2
            
        # Combined score
        sentence_scores.append((i, freq_score * pos_score, sentence))
    
    # Select top sentences
    top_sentences = sorted(sentence_scores, key=lambda x: x[1], reverse=True)[:max_sentences]
    
    # Reorder sentences by original position
    summary_sentences = sorted(top_sentences, key=lambda x: x[0])
    
    # Join sentences into summary
    summary = ' '.join(s[2] for s in summary_sentences)
    
    return summary

def generate_summary(text_to_summarize: str) -> str:
    """Generates a summary of the text using simple extractive summarization"""
    if not text_to_summarize:
        return "No text content available to summarize."
    
    # Truncate input if too long
    input_text = text_to_summarize[:MAX_SUMMARY_INPUT_LENGTH]
    if len(text_to_summarize) > MAX_SUMMARY_INPUT_LENGTH:
        logging.warning(f"Input text truncated to {MAX_SUMMARY_INPUT_LENGTH} characters for summarization.")
    
    try:
        logging.debug(f"Summarizing text (input length: {len(input_text)} chars)...")
        summary = simple_summarize(input_text)
        logging.debug("Summarization complete.")
        return summary
    except Exception as e:
        logging.error(f"Error during summarization: {e}")
        traceback.print_exc()
        return "Error generating summary. Please try again later."
