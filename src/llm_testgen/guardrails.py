import re, ast
from llm import query_llm

def is_valid_python(code):
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False

def clean_output(s):
    s = s.replace("```python", "").replace("```", "").replace("'''", "").strip()
    m = re.search(r"(?m)^(from\s+\S+\s+import\s+\S+|import\s+\S+|def\s+test_)", s)
    return s[m.start():] if m else s

def calls_target_function(code: str, func_name: str) -> bool:
    return re.search(rf"\b{re.escape(func_name)}\s*\(", code) is not None

def with_guardrails(prompt, func_name, model, max_tries: int = 2):
    last = ""
    for _ in range(max_tries):
        raw = query_llm(prompt, model)
        code = clean_output(raw)
        if is_valid_python(code) and calls_target_function(code, func_name) and "def test_" in code:
            return code
        prompt += (
            f"\n\nYour last output was invalid. Reprint ONLY valid pytest code.\n"
            f"- It must call `{func_name}`.\n"
            f"- No comments or markdown fences.\n"
            f"- Ensure `def test_...` unit test functions compile.\n"
        )
        last = code
    return last