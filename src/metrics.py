import ast, py_compile, re, sys
from pathlib import Path

SRC = Path("../examples/target_file.py")                # adjust if needed
TEST = Path("../examples/target_file_tests.py")         # adjust if needed

def compile_ok(p: Path) -> bool:
    try: py_compile.compile(str(p), doraise=True); return True
    except Exception: return False

def source_funcs(p: Path):
    tree = ast.parse(p.read_text(encoding="utf-8"))
    return {n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)}

def top_level_pytest_count(p: Path) -> int:
    # count def test_* at module top level
    tree = ast.parse(p.read_text(encoding="utf-8"))
    return sum(
        1 for n in tree.body
        if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")
    )

def called_funcs(p: Path):
    code = p.read_text(encoding="utf-8")
    tree = ast.parse(code)
    called=set()
    class V(ast.NodeVisitor):
        def visit_Call(self, node):
            if isinstance(node.func, ast.Name):
                called.add(node.func.id)
            self.generic_visit(node)
    V().visit(tree)
    return called

def import_correct(p_test: Path, src_mod: str, funcs: set) -> bool:
    # Accept single combined import line like: from src_mod import f1, f2, ...
    m = re.search(rf'(?m)^from\s+{re.escape(src_mod)}\s+import\s+(.+)$', p_test.read_text(encoding="utf-8"))
    if not m: return False
    names = [x.strip() for x in m.group(1).split(",") if x.strip()]
    return bool(names) and set(names).issubset(funcs)

if __name__ == "__main__":
    src_funcs = source_funcs(SRC)
    mod = SRC.stem

    compile_okay = compile_ok(TEST)
    tests_collected = top_level_pytest_count(TEST)
    called = called_funcs(TEST)
    coverage_hits = len(src_funcs & called)
    coverage_pct = round(100 * coverage_hits / len(src_funcs), 1) if src_funcs else 0.0
    imports_ok = import_correct(TEST, mod, src_funcs)
    edge_cases = len(re.findall(r"pytest\.raises", TEST.read_text(encoding="utf-8")))

    print(f"Compile OK: {compile_okay}")
    print(f"Top-level pytest tests: {tests_collected}")
    print(f"Functions exercised: {coverage_hits}/{len(src_funcs)} ({coverage_pct}%)")
    print(f"Edge-case tests (pytest.raises): {edge_cases}")
    print(f"Import correctness: {imports_ok}")
