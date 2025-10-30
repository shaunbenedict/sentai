# 🧠 SENTAI — AI Debate World

An interactive Streamlit application where multiple AI agents engage in dynamic debates on user-provided topics.

## 📅 Development Log

### 31.10.2025

#### Features Implemented

1. **Chat Interface Redesign**
   - Converted from custom HTML/CSS to native Streamlit chat components
   - Implemented `st.chat_message()` and `st.chat_input()` for better UX
   - Added unique emoji avatars for each AI agent

2. **Dynamic AI Agent System**
   - Load AI agents dynamically from `prompt.json` configuration file
   - Random selection of 2-3 agents per debate round
   - Support for multiple agent personalities:
     - 🤖 **LOGICA** - Logical and analytical
     - 💜 **CYNTHA** - Cynical and critical
     - ✨ **NOVA** - Creative and innovative
     - 📊 **DATA-PRIEST** - Data-driven and empirical

3. **Conversation History & Tracking**
   - Automatic conversation logging to JSON files
   - Files saved in `./conversations/` directory
   - Filename format: `{topic}_{timestamp}.json`
   - Tracks speaker, message, and timestamp for each entry
   - Maintains conversation context for coherent multi-turn debates

4. **AI Response Enhancement**
   - Filter out `<think>` tags from AI responses for cleaner output
   - Added conversation context to AI prompts for better continuity
   - Error handling for API failures

5. **Smart Conversation Management**
   - **Decider System**: AI determines which agent should respond next
   - **Concluder System**: AI detects when conversation reaches natural conclusion
   - Automatic verdict generation when debate concludes
   - Session state management for continuous conversations

6. **Environment & Configuration**
   - Integrated `python-dotenv` for API key management
   - Load Groq API credentials from `.env` file
   - Support for multiple LLM models (GPT, Llama, Qwen)
   - Random model selection for diverse responses

## 🏗️ Project Structure

```
sentai/
├── index.py                      # Main Streamlit application
├── services/
│   ├── __init__.py
│   ├── ai.py                     # Core AI interaction logic
│   └── decider.py                # Decision & conclusion system
├── system_files/
│   └── prompt.json               # AI agent configurations
├── conversations/                 # Conversation history logs
├── requirements.txt
├── .env                          # API keys (not in repo)
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Groq API Key

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your API key:
   ```
   Groq_APIKEY=your_api_key_here
   ```

4. Run the application:
   ```bash
   streamlit run index.py
   ```

## 🎯 Usage

1. Enter a debate topic in the chat input
2. Watch as 2-3 randomly selected AI agents discuss the topic
3. Agents will continue debating with context awareness
4. Conversation automatically concludes when consensus or natural ending is reached
5. View conversation history in the `conversations/` folder

## 🔧 Configuration

Edit `system_files/prompt.json` to add or modify AI agents:

```json
[
  {
    "ai_name": "AGENT_NAME",
    "prompt": "System prompt defining the agent's personality and behavior"
  }
]
```

## 📝 Technical Details

- **Frontend**: Streamlit with native chat components
- **AI Provider**: Groq API
- **Models**: Llama 3.1, Qwen 3, GPT (randomly selected)
- **Storage**: JSON file-based conversation history
- **State Management**: Streamlit session state

## 🔮 Future Enhancements

- User voting on best arguments
- Export conversations to different formats
- Real-time debate visualization
- Multi-language support
- Custom agent creation interface

---

**Last Updated**: October 31, 2025
