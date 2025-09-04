# AI Math Placement Agent

An intelligent email processing system that identifies math placement inquiries and automatically responds using AWS Bedrock Knowledge Base.

## Features

- **Email Classification**: Automatically identifies math placement related emails using keyword detection
- **AI-Powered Responses**: Uses AWS Bedrock Knowledge Base to generate contextual responses
- **Batch Processing**: Handles multiple emails efficiently
- **Email Composition**: Creates professional email responses with proper formatting
- **Demo Mode**: Includes mock data for testing without actual email sending

## Files Overview

- `ai_agent.py` - Main AI agent class with email processing logic
- `rag.py` - AWS Bedrock Knowledge Base integration
- `config.py` - Configuration settings (AWS region, Knowledge Base ID)
- `mock_emails.json` - Sample emails for testing
- `run_demo.py` - Demo runner with detailed output
- `main.py` - Simple execution entry point
- `requirements.txt` - Python dependencies

## Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure AWS credentials**:
   ```bash
   aws configure
   ```

3. **Update config.py** with your Knowledge Base ID:
   ```python
   KNOWLEDGE_BASE_ID = "YOUR_KB_ID_HERE"
   ```

4. **Run the demo**:
   ```bash
   python3 run_demo.py
   ```

## How It Works

1. **Email Ingestion**: Loads emails from JSON file (or email server in production)
2. **Classification**: Scans subject and body for math placement keywords
3. **Knowledge Base Query**: Sends identified emails to AWS Bedrock for response generation
4. **Response Composition**: Creates professional email responses
5. **Email Sending**: Outputs responses (demo mode) or sends via SMTP

## Production Setup

To use with real emails:

1. **Email Integration**: Replace JSON loading with IMAP/POP3 email fetching
2. **SMTP Configuration**: Update email sending credentials in `ai_agent.py`
3. **Error Handling**: Add robust error handling for production use
4. **Logging**: Implement comprehensive logging system

## Demo Results

The demo processes 4 sample emails and correctly identifies 3 as math placement inquiries:
- ✅ "Question about MAPE" 
- ✅ "AP Calc confusion"
- ❌ "General enrollment" (correctly skipped)
- ✅ "MAPE location"

All responses are saved to `outbox_responses.json` for review.