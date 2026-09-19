# Agentic Chatbot

This folder contains a set of experiments and mini projects focused on building an agentic chatbot using LangGraph, LangChain, and Google Generative AI. The goal is to explore conversational AI with memory, streaming responses, and tool calling.

## What is included

- A basic chatbot graph using a language model
- Conversation memory with in-memory and SQLite-based persistence
- Streamlit frontends for chat interaction
- Multi-threaded conversation handling
- Agentic tool use for web search, arithmetic, and stock price lookup

## Main project flow

The chatbot is built with:

- LangGraph for workflow orchestration
- LangChain for message handling and tool integration
- Google Gemini models for generation
- Streamlit for user interface
- SQLite for saved conversation history

## Key files

- ` _0_chatbot_backend.py `: basic chatbot backend using a simple LangGraph flow
- ` _0_chatbot_database_backend.py `: chatbot backend with database-backed memory
- ` _0_chatbot_tool_backend.py `: agentic version with tools and function calling
- ` _0_chatbot_frontend.py `: simple frontend interface
- ` _0_chatbot_frontend_database.py `: frontend with database-based thread support
- ` _0_chatbot_frontend_streaming.py `: frontend with streaming responses
- ` _0_chatbot_frontend_threading.py `: frontend with conversation threading
- ` _0_chatbot_frontend_tools.py `: frontend for tool-enabled agent interactions

## Features

### Basic chatbot
A simple conversational assistant that takes user input and returns a model-generated response.

### Persistent chat history
The database-backed versions store conversation sessions and allow the user to revisit threads.

### Agentic capabilities
The tool-based implementation enables the chatbot to:

- Search the web using DuckDuckGo
- Perform basic arithmetic calculations
- Fetch stock prices using an API

## Environment setup

Before running the project, make sure the required Python packages are installed and that your environment variables are configured.

Example environment variables:

- Google API key for Gemini access
- Any required model or app configuration values

## How to run

Open the project folder and run any frontend file with Streamlit, for example:

```bash
streamlit run _0_chatbot_frontend.py
```

You can also try the tool-enabled or database-backed versions:

```bash
streamlit run _0_chatbot_frontend_tools.py
streamlit run _0_chatbot_frontend_database.py
```

## Notes

This project is mainly designed for learning and experimentation in agentic AI workflows. It demonstrates how a chatbot can evolve from a simple LLM call to a tool-using agent with memory and conversation management.
