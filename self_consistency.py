import os, json, textwrap, re, time, ast, operator as op
import requests
from collections import Counter
from main import call_model_chat_completions, API_BASE, API_KEY, MODEL
from prompt import extract_final_answer, SYSTEM_PROMPT


def solve_with_self_consistency(question: str, k: int = 5, system_prompt: str = SYSTEM_PROMPT):
    """
        question: The user query.
        k: Number of responses for majority voting.
    """    
    
    answers = []
    
    # Run the model k times
    for i in range(k):
        result = call_model_chat_completions(
            prompt=question,
            system=system_prompt,
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
        print("No answers were generated.")
        return None

    # Majority Vote
    vote_counts = Counter(answers)
    most_common_answer, count = vote_counts.most_common(1)[0]
    
    print(f"\nVote: {dict(vote_counts)}")
    print(f">>> FINAL ANSWER: {most_common_answer}\n")
    return most_common_answer
