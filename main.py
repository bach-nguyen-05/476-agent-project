import os, json, textwrap, re, time, ast, operator as op
from self_consistency import solve_with_self_consistency
from utils import call_model_chat_completions
import requests

# Testing
if __name__ == "__main__":
    import json
    with open("cse_476_final_project_test_data.json", "r") as f:
        test_questions = json.load(f)

    for question in test_questions[:5]:
        question = question["input"]
        print(f"Question: {question}")
        solve_with_self_consistency(question)
