"""
Network Notes Assistant - Enhanced RAG Version
Demonstrates "RAG-Lite" with keyword interactions and simple response evaluation.
"""

from google import genai
import re

# Initialize the Gemini client (uses GEMINI_API_KEY environment variable)
client = genai.Client()

def load_notes_chunks(notes_path="notes/network_notes.txt"):
    """
    Load notes and split them into logical chunks based on Markdown headers.
    Returns a dictionary: {header: content}
    """
    try:
        with open(notes_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: Notes file not found at {notes_path}")
        return None

    # Split by markdown headers (e.g., "## Header")
    # This regex finds lines starting with ##
    chunks = {}
    current_header = "General"
    current_content = []

    for line in text.splitlines():
        if line.strip().startswith("## "):
            # Save previous chunk
            if current_content:
                chunks[current_header] = "\n".join(current_content)
            # Start new chunk
            current_header = line.strip().replace("## ", "")
            current_content = [line] # Keep the header in the content
        else:
            current_content.append(line)
    
    # Save the last chunk
    if current_content:
        chunks[current_header] = "\n".join(current_content)
        
    return chunks

def find_relevant_sections(chunks, question, top_n=3):
    """
    Find the most relevant note sections based on keyword matching.
    Improved: Checks if significant question words appear in header/content.
    """
    question_lower = question.lower()
    # Extract words longer than 2 chars to avoid "is", "a", "to" matching everything
    question_words = [w for w in re.findall(r'\w+', question_lower) if len(w) > 2]
    
    scores = []
    for header, content in chunks.items():
        score = 0
        header_lower = header.lower()
        content_lower = content.lower()
        
        for word in question_words:
            # High score for matching the header (e.g. "VLAN" in "VLANs")
            if word in header_lower:
                score += 10
            # Low score for appearing in text
            elif word in content_lower:
                score += 1
        
        scores.append((header, score))
    
    # Sort by score descending
    scores.sort(key=lambda x: x[1], reverse=True)
    
    # Return top N sections (if they have any score > 0)
    best_sections = [chunks[header] for header, score in scores[:top_n] if score > 0]
    
    # Debug info
    retrieved_headers = [h for h, s in scores[:top_n] if s > 0]
    print(f"\n[Debug] Retrieved sections: {retrieved_headers}")
    
    if not best_sections:
        return ""
    
    return "\n\n---\n\n".join(best_sections)

def create_grounded_prompt(context_text, question):
    """Create a prompt that grounds the model to only use provided notes."""
    prompt = f'''You are a helpful assistant that answers questions STRICTLY 
    based on the notes provided.
    
    IMPORTANT RULES:
    1. Only use information from the notes below to answer questions
    2. Do not use your general knowledge or training data
    3. If the notes don't contain information to answer the question, respond EXACTLY with:
    "The provided notes do not contain information about this topic."
    4. Be concise and accurate
    
    RELEVANT NOTES FOUND:
    {context_text}
    
    QUESTION: {question}
    
    ANSWER:'''
    return prompt

def evaluate_response(answer):
    """
    Check if the answer is grounded or a refusal.
    Returns: (is_grounded, status_message)
    """
    refusal_phrase = "The provided notes do not contain information about this topic."
    
    if refusal_phrase in answer:
        return False, "❌ Not Found in Notes"
    return True, "✅ Grounded Answer"

def ask_question(chunks, question):
    """Retrieves context and asks Gemini."""
    
    # 1. Retrieve relevant chunks
    relevant_text = find_relevant_sections(chunks, question)
    
    if not relevant_text:
        return "The provided notes do not contain information about this topic."

    # 2. Create prompt
    prompt = create_grounded_prompt(relevant_text, question)
    
    # 3. Call API
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
    print("Network Notes Assistant (Enhanced RAG)")
    print("=" * 60)
    
    # Load notes chunks
    chunks = load_notes_chunks()
    if chunks is None:
        return
    
    print(f"✓ Loaded {len(chunks)} sections from notes.")
    print("Ready! Type 'quit' to exit.\n")
    
    while True:
        question = input("Enter your question:\n").strip()
        
        if question.lower() in ['quit', 'exit', 'q']:
            print("\nGoodbye!")
            break
        
        if not question:
            continue
        
        print("\nSearching notes...")
        answer = ask_question(chunks, question)
        
        # Evaluate
        is_grounded, status = evaluate_response(answer)
        
        print(f"\nAnswer:\n{answer}\n")
        print(f"[Evaluation]: {status}")
        print("-" * 60 + "\n")

if __name__ == "__main__":
    main()
