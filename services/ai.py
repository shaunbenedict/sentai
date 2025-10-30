import os
import random
import json
import re
from datetime import datetime
from groq import Groq
from dotenv import load_dotenv
from services.decider import modelname, concluder

# Load environment variables from .env file
load_dotenv()

llm_list = ['openai/gpt-oss-20b', 'llama-3.1-8b-instant', 'qwen/qwen3-32b']

groq = Groq(api_key=os.getenv("Groq_APIKEY"))

def sanitize_filename(topic):
    """Convert topic to a safe filename"""
    # Remove or replace invalid characters
    safe_name = re.sub(r'[<>:"/\\|?*]', '', topic)
    safe_name = safe_name.strip()[:100]  # Limit length
    return safe_name if safe_name else "conversation"

def get_conversation_file(topic):
    """Get the conversation file path for a topic"""
    os.makedirs("./conversations", exist_ok=True)
    filename = sanitize_filename(topic)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = f"./conversations/{filename}_{timestamp}.json"
    return filepath

def load_conversation_history(filepath):
    """Load existing conversation history"""
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_conversation_history(filepath, history):
    """Save conversation history to file"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

def get_conversation_context(history):
    """Get conversation context as a string"""
    context = ""
    for entry in history[-5:]:  # Last 5 messages for context
        context += f"{entry['speaker']}: {entry['message']}\n"
    return context

def generate_response(model_name, prompt, msg, context=""):
    """Generate AI response with optional conversation context"""
    user_message = f"Context:\n{context}\n\nNew message: {msg}" if context else msg
    
    response = groq.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_message}
        ],
        max_tokens=500,
        temperature=1,
    )
    content = response.choices[0].message.content or ""
    # Filter out everything inside <think> tags
    filtered_content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL)
    return filtered_content.strip()

def get_model_name():
    model = random.choice(llm_list)
    return model

def get_prompt(ainame):
    with open("./system_files/prompt.json") as prompts:
        lst = json.load(prompts)
    for a in lst:
        if a["ai_name"] == ainame:
            return a["prompt"]
    else:
        return None

def get_all_agent_names():
    """Get list of all available agent names"""
    with open("./system_files/prompt.json") as prompts:
        lst = json.load(prompts)
    return [a["ai_name"] for a in lst if a["ai_name"] != "Bear"]

def chatMSG(ai_name, msg, conversation_file=None):
    """
    Generate AI response and optionally save to conversation history
    Returns: (response, should_continue, next_speaker, conclusion)
    """
    model = get_model_name()
    prompt = get_prompt(ai_name)
    
    if prompt is None:
        return "Error", False, None, None
    
    # Load conversation history if file provided
    history = []
    context = ""
    if conversation_file:
        history = load_conversation_history(conversation_file)
        context = get_conversation_context(history)
    
    # Generate response
    response = generate_response(model, prompt, msg, context)
    
    # Save to conversation history
    if conversation_file:
        history.append({
            "speaker": ai_name,
            "message": response,
            "timestamp": datetime.now().isoformat()
        })
        save_conversation_history(conversation_file, history)
    
    # Check if conversation should conclude
    should_continue = True
    conclusion = None
    if len(history) >= 3:  # Check after at least 3 exchanges
        conclusion_check = concluder(get_conversation_context(history))
        if "CONCLUDE" in conclusion_check:
            should_continue = False
            conclusion = conclusion_check
    
    # Decide next speaker
    next_speaker = None
    if should_continue:
        all_agents = get_all_agent_names()
        agent_names = ", ".join(all_agents)
        next_speaker = modelname(agent_names, get_conversation_context(history))
        # Clean up the response to get just the name
        for agent in all_agents:
            if agent in next_speaker:
                next_speaker = agent
                break
    
    return response, should_continue, next_speaker, conclusion if not should_continue else None