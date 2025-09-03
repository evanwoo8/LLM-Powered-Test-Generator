import ast


def extract_functions(source, parsed_file):
    functions = []

    for node in ast.walk(parsed_file):
        if isinstance(node, ast.FunctionDef):
            func_code = ast.unparse(node)
            functions.append({"name": node.name,
                              "docstring": ast.get_docstring(node),
                              "code": func_code,
                              "args": [arg.arg for arg in node.args.args]
                              })
    return functions

