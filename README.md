# Three Techniques to Improve Agent Performance
This code introduce a pipeline including three inference-time techniques to improve the LLM reasoning capability:
1. CoT and Few Shot Prompting
2. Self-Refine
3. Self-Consistency (Majority Vote with k = 7)
## Reproduce the code
### Note:
Because the temperature is set to 0.7, the results will be similar but not exactly the same while reproducing.
### Implementation
```bash
git clone https://github.com/bach-nguyen-05/476-agent-project.git
python3 generate_answer_template.py
```