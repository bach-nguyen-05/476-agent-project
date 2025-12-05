import os, json, textwrap, re, time, ast, operator as op
import requests
from collections import Counter
from main import call_model_chat_completions, API_BASE, API_KEY, MODEL

def extract_final_answer(text: str) -> str:

    # 1. Look for explicit tag defined in our prompt
    match = re.search(r"FINAL:\s*(.*)", text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    
    # 2. Fallback: specific number extraction if the answer is just a number
    numbers = re.findall(r"[-+]?\d+(?:\.\d+)?", text)
    if numbers:
        return numbers[-1]
        
    return "N/A"

def solve_with_self_consistency(question: str, k: int = 5):
    """
        question: The user query.
        k: Number of reasoning paths to generate (votes).
    """
    print(f"--- Question: {question} ---")
    
    cot_system_prompt = (
        "At the end, state your answer for the question exactly like this: FINAL: <answer>"
    )

    answers = []
    
    # Run the model k times
    for i in range(k):
        result = call_model_chat_completions(
            prompt=question,
            system=cot_system_prompt,
            temperature=0.7 
        )
        
        if result["ok"]:
            raw_text = result["text"]
            # Clean and extract the specific answer for voting
            parsed_ans = extract_final_answer(raw_text)
            answers.append(parsed_ans)
            print(f"Answer {i+1}: {parsed_ans}")
        else:
            print(f"Failed: {result['error']}")

    if not answers:
        print("No valid answers generated.")
        return None

    # Majority Vote
    vote_counts = Counter(answers)
    most_common_answer, count = vote_counts.most_common(1)[0]
    
    print(f"\nVote: {dict(vote_counts)}")
    print(f"Confidence: {count}/{len(answers)}")
    print(f">>> FINAL ANSWER: {most_common_answer}\n")
    return most_common_answer

# --- TEST RUNNER ---
if __name__ == "__main__":
    q1 = "What is (56 + 56)/0.03? Answer with just the number."
    solve_with_self_consistency(q1, k=5)
    print("Ground Truth: 112\n")