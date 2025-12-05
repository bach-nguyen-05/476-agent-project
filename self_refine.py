import re
from utils import call_model_chat_completions
from prompt import extract_final_answer, CRITIC_PROMPT, SYSTEM_PROMPT


def solve_with_self_refinement(question: str, temperature: float = 0.7):
    # Step 1: Primitive Answer Generation
    # We generate the first draft.
    # print("Step 1 Generating Initial Answer")
    primitive = call_model_chat_completions(
        prompt=question,
        system=SYSTEM_PROMPT,
        temperature=temperature 
    )

    draft = primitive["text"]

    # Step 2: Critique and Refine
    # print("Step 2 Self-Refining")
    
    refinement = f"""
    Original Question: {question}
    
    Proposed Answer:
    {draft}
    
    Task: Review the Proposed Answer above. Check for calculation errors or logical mistakes. Keep the proposed answer as is if it's correct. 
    Provide the final correct answer by ending your response with the exact format: FINAL: <answer>
    Example for multiple choice: If the answer is "FINAL: A. Compensation", then the output should be "FINAL: A" only (use the letter only). The point is to keep the answer format concise for majority voting.
    """
    final_result = call_model_chat_completions(
        prompt=refinement,
        system=CRITIC_PROMPT,
        temperature=0.0 # Choose the deterministic output
    )

    if not final_result["ok"]:
        print(f"Error: {final_result['error']}")
        return None

    final_text = final_result["text"]
    final_ans = extract_final_answer(final_text)

    return final_ans