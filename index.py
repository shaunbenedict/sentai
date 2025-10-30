import streamlit as st
import json
import random
from services.ai import chatMSG, get_conversation_file

st.set_page_config(page_title="SENTAI", layout="wide")

st.title("🧠 SENTAI — AI Debate World")

# Load AI agents from prompt.json
def get_ai_agents():
    with open("./system_files/prompt.json") as f:
        agents_data = json.load(f)
    
    agent_map = {
        "LOGICA": "🤖",
        "CYNTHA": "💜",
        "NOVA": "✨",
        "DATA-PRIEST": "📊",
        "Bear": "🐻"
    }
    
    agents = []
    for agent in agents_data:
        ai_name = agent["ai_name"]
        emoji = agent_map.get(ai_name, "🤖")
        agents.append((ai_name, emoji))
    
    return agents

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_file" not in st.session_state:
    st.session_state.conversation_file = None
if "should_continue" not in st.session_state:
    st.session_state.should_continue = True

# Display all messages in chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message.get("avatar")):
        st.markdown(message["content"])

# Chat input at the bottom
prompt = st.chat_input("Enter a topic to debate...")

if prompt:
    # Create new conversation file for this topic
    if st.session_state.conversation_file is None:
        st.session_state.conversation_file = get_conversation_file(prompt)
        st.session_state.should_continue = True
    
    # Add user message to chat
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "avatar": "🧑"
    })
    
    with st.chat_message("user", avatar="🧑"):
        st.markdown(prompt)
    
    # System message
    with st.chat_message("assistant", avatar="🌍"):
        st.markdown(f"**SYSTEM**: Initiating debate on topic: *{prompt}*")
    st.session_state.messages.append({
        "role": "assistant",
        "content": f"**SYSTEM**: Initiating debate on topic: *{prompt}*",
        "avatar": "🌍"
    })
    
    # Get all available agents and randomly select 2-3 for first round
    all_agents = get_ai_agents()
    # Filter out Bear from debate agents if desired
    debate_agents = [agent for agent in all_agents if agent[0] != "Bear"]
    
    # Randomly select 2 or 3 agents
    num_agents = random.randint(2, 3)
    selected_agents = random.sample(debate_agents, min(num_agents, len(debate_agents)))
    
    for agent_name, emoji in selected_agents:
        if not st.session_state.should_continue:
            break
            
        with st.chat_message("assistant", avatar=emoji):
            with st.spinner(f"{agent_name} is thinking..."):
                try:
                    response, should_continue, next_speaker, conclusion = chatMSG(
                        agent_name, 
                        prompt, 
                        st.session_state.conversation_file
                    )
                    st.markdown(f"**{agent_name}**: {response}")
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"**{agent_name}**: {response}",
                        "avatar": emoji
                    })
                    
                    st.session_state.should_continue = should_continue
                    
                    # If conversation concluded, show verdict
                    if not should_continue and conclusion:
                        with st.chat_message("assistant", avatar="🧩"):
                            verdict = f"**VERDICT**: {conclusion}"
                            st.markdown(verdict)
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": verdict,
                                "avatar": "🧩"
                            })
                        # Reset for next conversation
                        st.session_state.conversation_file = None
                        break
                    
                except Exception as e:
                    error_msg = f"**{agent_name}**: Error generating response - {str(e)}"
                    st.markdown(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg,
                        "avatar": emoji
                    })
    
    # Show continuation message if not concluded
    if st.session_state.should_continue:
        with st.chat_message("assistant", avatar="🧩"):
            verdict = "**SYSTEM**: Continue the conversation by adding more input..."
            st.markdown(verdict)
            st.session_state.messages.append({
                "role": "assistant",
                "content": verdict,
                "avatar": "🧩"
            })
