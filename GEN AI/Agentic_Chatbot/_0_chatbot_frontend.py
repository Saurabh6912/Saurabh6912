import streamlit as st
from _0_chatbot_backend import chatbot
from langchain_core.messages import HumanMessage

st.title("Agentic Chatbot")

#set a specif config for each session as st.session_state -> dict -> 
CONFIG = {'configurable': {'thread_id': 'thread-1'}}

#use session state to store the message history to display all the conversation in the frontend
#use st.session_state as list because stremlit does not support dict as session state, so we use list to store the message history
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

# loading the conversation history and showing it in the frontend
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

# take user input
user_input = st.chat_input('Type here')

#if user input is not empty, then send the user input to the backend and get the response from the backend
if user_input:

    # first add the message to message_history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    # call chatbot(llm) in the backend to get the response from the chatbot
    response = chatbot.invoke({'messages': [HumanMessage(content=user_input)]}, config=CONFIG)

    # Extract the last AI message only
    ai_message = response['messages'][-1].content

    # first add the message to message_history and then display the message in the frontend
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
    with st.chat_message('assistant'):
        st.text(ai_message)



