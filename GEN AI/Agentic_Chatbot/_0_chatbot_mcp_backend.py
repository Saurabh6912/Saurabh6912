########################################################################
# LangGraph Chatbot Application Backend with MCP. NOTE MCP supports asynchronous execution only
#########################################################################

from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
import aiosqlite
import asyncio
import sys
import threading
from pathlib import Path

# for tools (Agentic System)
from langchain_core.tools import tool, BaseTool
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_community.tools import DuckDuckGoSearchRun

from langchain_mcp_adapters.client import MultiServerMCPClient

import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Dedicated asybc loop for backend tasks
_ASYNC_LOOP = asyncio.new_event_loop()
_ASYNC_THREAD = threading.Thread(target=_ASYNC_LOOP.run_forever, daemon=True)
_ASYNC_THREAD.start()

def _submit_async(coro):
    return asyncio.run_coroutine_threadsafe(coro, _ASYNC_LOOP)
def run_async(coro):
    return _submit_async(coro).result()
def submit_async_task(coro):
    """Schedule a coroutine on the backend event loop."""
    return _submit_async(coro)


#==========================================
# 1. Initialize the LLM
#==========================================
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")

#==========================================
# 2. Tools Definition
#==========================================

# i) Define predefined tool for searching the web using DuckDuckGo
search_tool = DuckDuckGoSearchRun(region="us-en")

# ii) Define a custom tool for fetching stock prices using Alpha Vantage API
@tool
def get_stock_price(symbol:str) -> dict:
    """
    Fetch latest stock price for a given symbol (e.g. 'AAPL', 'TSLA') 
    using Alpha Vantage with API key in the URL.
    """
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey=MP8BG7DF9C1GS1G3"
    r = requests.get(url)
    return r.json()

# Define a MCP server client to handle tool calls asynchronously
client = MultiServerMCPClient(
    {
        "arith": {
            "transport": "stdio",
            "command": sys.executable,
            "args": [str(Path(__file__).with_name("mcp_server_1.py"))],
        }
    }
)

# load mcp tools
def load_mcp_tools() -> list[BaseTool]:
    return run_async(client.get_tools())

mcp_tools = load_mcp_tools()

#==========================================
# 3. Tool Binding with llm
#==========================================
tools = [search_tool, get_stock_price, *mcp_tools] # combine all tools into a single list
llm_with_tools = llm.bind_tools(tools) if tools else llm


# -------------------
# 4. State
# -------------------
#Define the State of the graph
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages] #use reducer function add_messages

# -------------------
# 5. Nodes
# -------------------
# create function/node for graph ---> updated to use llm_with_tools instead of llm
async def chat_node(state: ChatState) -> ChatState:
    """LLM node that may answer or request a tool call."""
    messages = [
        SystemMessage(
            content=(
                "For arithmetic requests, use the matching arithmetic MCP tool "
                "(add, subtract, multiply, divide, or modulus) instead of "
                "calculating the result directly."
            )
        ),
        *state['messages'],
    ]
    response = await llm_with_tools.ainvoke(messages)
    return {"messages": [response]}

tool_node = ToolNode(tools) if tools else None

# -------------------
# 6. Checkpointer
# -------------------
async def _init_checkpointer():
    conn = await aiosqlite.connect(database="chatbot.db")
    return AsyncSqliteSaver(conn)

# checkpointer for memory of the graph
checkpointer = run_async(_init_checkpointer())

# -------------------
# 7. Graph
# -------------------
#Define Graph and Crreate Node/Edges for the Graph
graph = StateGraph(ChatState) 

graph.add_node("chat_node",chat_node)
graph.add_node("tools",tool_node)

graph.add_edge(START,"chat_node")
graph.add_conditional_edges("chat_node",tools_condition)
graph.add_edge("tools","chat_node")

chatbot = graph.compile(checkpointer=checkpointer)

# -------------------
# 8. Helper
# -------------------
async def _alist_threads():
    all_threads = set()
    async for checkpoint in checkpointer.alist(None): # given none means we want all the thread points that present in checkpointer
        all_threads.add(checkpoint.config['configurable']['thread_id'])
    return list(all_threads)

def retrieve_all_threads():
    return run_async(_alist_threads())
    

    



