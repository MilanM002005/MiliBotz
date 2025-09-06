# MiliBotz 

**MiliBotz** is a WhatsApp-style AI chatbot powered by Groq API.  
It can answer general questions or healthcare-related queries through a sleek, interactive Streamlit interface.

---

##  Features

- **Real-time Chat**: Conversational interface similar to WhatsApp.
- **Async Responses**: Uses Groq API for AI-powered responses.
- **Session History**: Keeps track of your conversation in the session.
- **Clear Chat**: Easily reset the conversation.
- **Customizable Settings**: Sidebar info and configuration options.

---

##  Built With

- [Streamlit](https://streamlit.io/) - Frontend and UI
- [Groq API](https://www.groq.com/) - AI backend
- [httpx](https://www.python-httpx.org/) - Async HTTP requests
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation
- [Loguru](https://loguru.readthedocs.io/) - Logging
- [Python-dotenv](https://pypi.org/project/python-dotenv/) - Environment variable management

---

## ⚡ Getting Started

### **1. Clone the repository**

```bash
git clone https://github.com/yourusername/milibotz.git
cd milibotz


2. Install dependencies
pip install -r requirements.txt

3. Set up environment variables

Create a .env file:

GROQ_API_KEY=your_groq_api_key_here


Alternatively, you can set your API key as a Streamlit Secret when deploying.

4. Run the app locally
streamlit run app.py


Open your browser at http://localhost:8501 to interact with MiliBotz.
