import os, json, textwrap, re, time, ast, operator as op
import requests
from collections import Counter
from self_refine import solve_with_self_refinement


def solve_with_self_consistency(question: str, k: int = 5):
    """
        question: The user query.
        k: Number of responses for majority voting.
    """
    answers = []
    
    # Run the model k times
    for i in range(k):
        # Generate a response with self-refinement first before voting
        result = solve_with_self_refinement(question, temperature=0.7)
        answers.append(result)
        print(f"Answer {i+1}: {result}")

    if not answers:
        print("No answers were generated.")
        return None

    # Majority Voting
    vote_counts = Counter(answers)
    most_common_answer, count = vote_counts.most_common(1)[0]
    
    print(f"\nVote: {dict(vote_counts)}")
    print(f"FINAL ANSWER: {most_common_answer}\n")
    return most_common_answer
