# 🌐 Network RAG-Based Assistant

A simple **grounded AI assistant** that answers networking questions based **only** on provided notes, demonstrating RAG (Retrieval-Augmented Generation) principles, hallucination prevention, and prompt engineering.



## 🏗️ Architecture

```
User Question → Load Notes → Create Grounded Prompt → Gemini API → Grounded Answer
```



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
   cd network-notes-assistant
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

## 💡 Usage Examples

### Example 1: Question Answered from Notes
```
Enter your question: What is the difference between TCP and UDP?

Answer:
TCP (Transmission Control Protocol) is connection-oriented and guarantees 
delivery of packets in correct order using a three-way handshake. It's slower 
but more reliable, with error checking and acknowledgment mechanisms. It's used 
for web browsing, email, and file transfer.

UDP (User Datagram Protocol) is connectionless with no guarantee of delivery 
or order. It's faster with lower overhead but has no error recovery. It's used 
for streaming video, online gaming, DNS queries, and VoIP.
```

### Example 2: Question NOT in Notes
```
Enter your question: How does IPSec work?

Answer:
The provided notes do not contain information about this topic.
```

## 🔧 How It Works

### 1. **Load Notes**
The assistant reads `network_notes.txt` containing networking fundamentals.

### 2. **Grounded Prompting**
Creates a special prompt that:
- Provides the full notes as context
- Instructs the model to ONLY use the notes
- Specifies what to say if information is missing

### 3. **Low Temperature**
Uses `temperature=0.1` for more factual, consistent responses.


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
