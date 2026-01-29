# Caramel AI - MCP Chatbot

An AI-powered chatbot with Model Context Protocol (MCP) server for PDF reading capabilities.

## Features

- **Caramel AI Chatbot**: Interactive chatbot powered by Cerebras LLM
- **MCP PDF Reader Server**: MCP server for reading and processing PDF documents
- Supports multi-model AI interactions

## Project Structure

```
.
├── chatbot.py              # Main chatbot application
├── requirements.txt        # Python dependencies
├── mcp-server/            # MCP server for PDF processing
│   └── main.py           # PDF reader MCP server
└── mcp-client/           # MCP client directory
```

## Prerequisites

- Python 3.8 or higher
- API key for Cerebras (set in `.env` file)

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd MCP
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your Cerebras API key:
```
CEREBRAS_API_KEY=your_api_key_here
```

## Usage

### Running the Chatbot

```bash
python chatbot.py
```

Type your questions and interact with the AI. Type `exit` or `quit` to end the session.

### Running the MCP Server

```bash
python mcp-server/main.py
```

## Dependencies

- `mcp` - Model Context Protocol framework
- `pypdf` - PDF processing library
- `langchain-cerebras` - Cerebras LLM integration
- `python-dotenv` - Environment variable management

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## About

Developed by HERE AND NOW AI

---

**Note**: Make sure to keep your API keys secure and never commit them to the repository.
