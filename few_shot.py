import re
from main import call_model_chat_completions
from prompt import SYSTEM_PROMPT

def solve_with_few_shot(question: str):
    """
    Use the imported prompt and call_model_chat_completions function to solve the problem
    """
    result = call_model_chat_completions(
        prompt=question,
        system=SYSTEM_PROMPT,
    )

    if result["ok"]:
        print(f"Model Response:\n{result['text']}")
        return result['text']
    else:
        print(f"Error: {result['error']}")
        return None

# # --- TEST RUNNER ---
# if __name__ == "__main__":
#     import json
#     # Test 1: Blocksworld (Should trigger Blocksworld Prompt)
#     with open("cse_476_final_project_test_data.json", "r") as file:
#         questions = json.load(file)
#     for i in range(3):
#         print(f"\n--- Test Question {i+1} ---")
#         q1 = questions[i]["input"]
#         solve_with_few_shot(q1)
