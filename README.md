# 🌐 Network RAG-Based Assistant (Enhanced RAG)

A simple **grounded AI assistant** that answers networking questions based **only** on provided notes, demonstrating RAG (Retrieval-Augmented Generation) principles, hallucination prevention, and prompt engineering.

## 🏗️ Architecture

```
User Question → Keyword Search → Retrieve Relevant Chunk → Grounded Prompt → Gemini API → Evaluation → Grounded Answer
```

### ❓ Why "Enhanced RAG"?
The Basic version sends *all* notes to the AI, which works for small files but fails for larger knowledge bases (context window limits). This **Enhanced Version** solves that by:
1.  **Saving Costs & Tokens:** Only sends the specific section relevant to your question.
2.  **Improving Accuracy:** Prevents the AI from getting confused by irrelevant information.
3.  **Verifying Grounding:** Automatically checks if the AI actually found the answer in the notes or had to guess.



## 📁 Project Structure

```
network-notes-assistant/
│
├── notes/
│   └── network_notes.txt      # Knowledge base (OSI, TCP/UDP, routing, etc.)
│
├── assistant.py                # Main application
├── requirements.txt            # Dependencies
└── README.md                   # This file
```

## 🚀 Setup & Installation

### Prerequisites

- Python 3.8+
- Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/gmoualla/network-RAG-Lite-assistant.git
   cd network-RAG-Lite-assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**
   
   **Windows (PowerShell):**
   ```powershell
   $env:GEMINI_API_KEY="your-api-key-here"
   ```
   
   **Linux/Mac:**
   ```bash
   export GEMINI_API_KEY="your-api-key-here"
   ```

4. **Run the assistant**
   ```bash
   python assistant.py
   ```

## � Switching Versions

This repository contains two versions of the assistant. You can switch between them using likely git commands:

- **Basic Version (Simple)**
  ```bash
  git checkout master
  ```

- **Enhanced RAG Version (Current)**
  ```bash
  git checkout enhanced-rag
  ```

## �💡 Usage Examples

### Example 1: Question Answered from Notes
```
Enter your question: What is the difference between TCP and UDP?

Searching notes...

[Debug] Retrieved sections: ['TCP vs UDP']

Answer:
TCP (Transmission Control Protocol) is connection-oriented and guarantees 
delivery of packets in correct order using a three-way handshake. It's slower 
but more reliable. UDP (User Datagram Protocol) is connectionless with no 
guarantee of delivery. It's faster but less reliable.

[Evaluation]: ✅ Grounded Answer
```

### Example 2: Question NOT in Notes
```
Enter your question: How does IPSec work?

Searching notes...

Answer:
The provided notes do not contain information about this topic.

[Evaluation]: ❌ Not Found in Notes
```



## 🔧 How It Works

### 1. **Smart Chunking**
The assistant loads `network_notes.txt` and intelligently splits it into logical sections based on headers (e.g., `## OSI Model`, `## TCP vs UDP`).

### 2. **Keyword Search (Retrieval)**
When you ask a question, the system scans the sections to find the most relevant one using keyword matching. This reduces token usage and "distracts" the model less.

### 3. **Grounded Prompting**
Creates a prompt involving **only** the retrieved text section.

### 4. **Response Evaluation**
The system automatically checks the answer. If the model says "The provided notes do not contain information...", it flags the result as **Not Found**. Otherwise, it's marked as **✅ Grounded**.


## 🤝 Contributing

Feel free to fork this project and add enhancements! Some ideas:
- Add more networking topics to the notes
- Implement semantic search
- Create a web interface
- Add support for multiple knowledge domains

## 📄 License

MIT License - feel free to use this for learning and portfolio purposes!

## 👤 Author

Created as **Project** in my Generative AI learning journey, combining:
- Generative AI fundamentals
- Python programming
- Networking knowledge

---