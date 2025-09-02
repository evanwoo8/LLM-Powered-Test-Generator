from ollama import Client

def format_prompt(function_dictionary):
    return f"""
You are an expert Python tester. Generate a **pytest** module that tests exactly the function below.

Constraints (MUST follow all):
- Output only valid Python code (no markdown fences, no comments, no prose).
- The first non-blank line MUST be: from target_file import {function_dictionary['name']}
- Create a test for named test_{function_dictionary['name']} covering the best of the three (or more if needed): happy path, edge case, and error/exception (if applicable).
- You MUST call `{function_dictionary['name']}` directly in each test.
- Use deterministic asserts. If the function can raise, include pytest.raises. 
- Do NOT import or reference any symbols other than `{function_dictionary['name']}`

Target Function Name: {function_dictionary['name']}
Docstring: {function_dictionary['docstring']}
Function Signature Arguments: {', '.join(function_dictionary['args'])}

Function Code:
{function_dictionary['code']}

Return the pytest module now.""".strip()


client = Client(host='http://localhost:11434')

def query_llm(prompt: str, model='codellama:7b-instruct'):
    response = client.chat(model=model, messages=[{"role": "user", "content": prompt}], options={"temperature": 0.1})
    return response['message']['content']

def clean_output(llm_output):
    return (
        llm_output.replace("```python", "").replace("```", "").replace("'''", "").strip()
    )
