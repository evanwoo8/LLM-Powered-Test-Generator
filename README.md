# LLM TestGen — Generate Pytest from Python Source (AST + Guardrails + Ollama)

[![CI](https://github.com/<evanwoo>/<your-repo>/actions/workflows/ci.yml/badge.svg)](https://github.com/<your-username>/<your-repo>/actions/workflows/ci.yml)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)

> **TL;DR**: A lightweight CLI that analyzes a Python file’s functions via **AST**, prompts a local **LLM (Ollama)** to generate tests, and **hardens** the output with **guardrails** so the resulting **pytest** suites compile and are ready for collection.

> **Demo (optional)**: add `docs/demo.gif` and link it here  
> ![Demo](docs/demo.gif)

---

## ✨ Features

- **AST static analysis**: extracts `FunctionDef` name/args/docstring/code for targeted prompts  
- **Local LLM via Ollama**: privacy-friendly; swap models with `--model` flag  
- **Guardrails**: code-fence stripping, `ast.parse` syntax check, import & target-call checks, single retry  
- **Smart append**: writes to `<module>_tests.py`, keeping a single combined import line (`from module import f1, f2, ...`)  
- **Metrics script**: quick report of compile success, test count, edge-case checks, function “exercise” count

---

## How It Works

1. **Parse** the source file with `ast` and gather function metadata  
2. **Prompt** the LLM per function (pytest only, no prose, import first line)  
3. **Clean** output (strip fences/prose) and **validate** (`ast.parse`, import, target-call)  
4. **Retry** up to 2 times with corrective instructions if validation fails  
5. **Append** tests into `<module>_tests.py` with deduped top import  
6. **Report** metrics (compile OK, top-level tests, edge-case assertions, etc)

---

## Requirements

- **Python 3.10+**
- **Ollama** installed and running: https://ollama.com/download  
  Pull a small model (works well on low-RAM laptops):
  ```bash
  ollama pull phi3:mini
  # also good:
  # ollama pull mistral:instruct
  # ollama pull codellama:7b-instruct
