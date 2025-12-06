"""
Network Notes Assistant - RAG-Lite Version
A simple grounded AI assistant that answers questions based only on provided notes.
"""

from google import genai

# Initialize the Gemini client (uses GEMINI_API_KEY environment variable)
client = genai.Client()

def load_notes(notes_path="notes/network_notes.txt"):
    """Load the network notes from file."""
    try:
        with open(notes_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Notes file not found at {notes_path}")
        return None

def create_grounded_prompt(notes, question):
    """Create a prompt that grounds the model to only use provided notes."""
    prompt = f'''You are a helpful assistant that answers questions STRICTLY 
    based on the notes provided.

    IMPORTANT RULES:
    1. Only use information from the notes below to answer questions
    2. Do not use your general knowledge or training data
    3. If the notes don't contain information to answer the question, respond with:
    "The provided notes do not contain information about this topic."
    4. Be concise and accurate
    5. Quote or reference specific parts of the notes when answering

    NOTES:
    {notes}

    QUESTION: {question}

    ANSWER:'''
    return prompt

def ask_question(notes, question):
    """Send question to Gemini with grounded prompt."""
    prompt = create_grounded_prompt(notes, question)
    
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt,
            config={
                'temperature': 0.1,
                'max_output_tokens': 500,
            }
        )
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"

def main():
    """Main function to run the assistant."""
    print("=" * 60)
    print("Network Notes Assistant (RAG-Lite)")
    print("=" * 60)
    print("This assistant answers questions based on your network notes.")
    print("Type 'quit' or 'exit' to stop.\n")
    
    # Load notes
    notes = load_notes()
    if notes is None:
        return
    
    print(f"✓ Loaded {len(notes)} characters of network notes\n")
    
    # Interactive loop
    while True:
        question = input("Enter your question or exit to quit:\n").strip()
        
        if question.lower() in ['quit', 'exit', 'q']:
            print("\nGoodbye!")
            break
        
        if not question:
            print("Please enter a question.\n")
            continue
        
        print("\nThinking...\n")
        answer = ask_question(notes, question)
        print(f"Answer:\n{answer}\n")
        print("-" * 60 + "\n")

if __name__ == "__main__":
    main()
