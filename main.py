import os, json, textwrap, re, time, ast, operator as op
from self_consistency import solve_with_self_consistency
from utils import call_model_chat_completions
import requests

# Testing
def agent_loop(question: str):
    """
        A simple agent loop that uses self-consistency to answer the question.
    """
    final_answer = solve_with_self_consistency(question, k=7)
    return final_answer

# Test the agent loop with sample questions
if __name__ == "__main__":
    import json
    with open("cse_476_final_project_test_data.json", "r") as f:
        test_questions = json.load(f)

    for question in test_questions[:7]:
        question = question["input"]
        print(f"Question: {question}")
        answer = agent_loop(question)
        print(f"Answer: {answer}")
