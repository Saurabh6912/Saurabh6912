from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver

from dotenv import load_dotenv

load_dotenv()

# Initialize the LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")

#Define the State of the graph
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages] #use reducer function add_messages


# create function/node for graph
def chat_node(state: ChatState) -> ChatState:
    messages = state['messages']
    response = llm.invoke(messages)
    return {"messages": [response]}

# checkpointer for memory of the graph
checkpointer = InMemorySaver()

#Define Graph and Crreate Node/Edges for the Graph

graph = StateGraph(ChatState) 

graph.add_node("chat_node",chat_node)

graph.add_edge(START,"chat_node")
graph.add_edge("chat_node",END)

chatbot = graph.compile(checkpointer=checkpointer)


