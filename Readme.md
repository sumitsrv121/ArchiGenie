# ArchiGenie 🤖🏗️  
**AI-Powered Software Architecture Generation Tool**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-0.1.0+-green.svg)](https://python.langchain.com/)

Automatically generate production-ready technical architectures using LLMs. Supports OpenAI GPT-4 and HuggingFace models with intelligent validation and caching.

![Demo](docs/demo-screenshot.png)

## Features ✨
- **Dual LLM Support** - OpenAI GPT-4 & HuggingFace models
- **Smart Validation** - Auto-retry with quality checks
- **Requirement Modes**  
  🧩 Functional (natural language input)  
  🔧 Technical (structured parameters)
- **Response Caching** - SQLite-based request caching
- **Production Ready** - Error handling & sanitization
- **Configurable** - Model parameters & providers

## Installation ⚙️

```bash
# Clone repository
git clone https://github.com/sumitsrv121/ArchiGenie.git
cd ArchiGenie

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env

```
## Configuration ⚙️ 

**Required for OpenAI**
OPENAI_API_KEY=sk-your-key-here

**Required for HuggingFace**
HUGGINGFACEHUB_API_TOKEN=your-hf-token-here

**Provider selection (openai/huggingface)**
AI_PROVIDER=openai

**Model specifics**
MODEL_NAME=gpt-4  # or tiiuae/falcon-7b-instruct