#!/usr/bin/env python3
"""
Mark — Agentic local-model routing CLI.

Mechanical tasks  → deepseek-coder:6.7b  (file injection + code-block apply)
Architectural     → qwen3:14b             (native tool-call loop)
Classification    → mistral:7b

Usage:  python mark.py [--dir /path/to/project]
"""

import json, os, re, subprocess, sys, textwrap, urllib.request
from pathlib import Path

# UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ── Constants ─────────────────────────────────────────────────────────────────

OLLAMA_URL      = "http://localhost:11434"
MAX_TOOL_ROUNDS = 20

MODELS = {
    "classifier":   "mistral:7b",
    "mechanical":   "deepseek-coder:6.7b",
    "architectural":"qwen3:14b",
}

# ── ANSI ──────────────────────────────────────────────────────────────────────

R="\033[0m"; CYAN="\033[36m"; YEL="\033[33m"; GRN="\033[32m"
RED="\033[31m"; GREY="\033[90m"; BOLD="\033[1m"
def c(t, col): return f"{col}{t}{R}"

# ── Ollama helpers ────────────────────────────────────────────────────────────

def _post(payload: dict) -> dict:
    data = json.dumps(payload).encode()
    req  = urllib.request.Request(
        f"{OLLAMA_URL}/api/chat", data=data,
        headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        return {"error": f"HTTP {e.code}: {body[:200]}"}
    except Exception as e:
        return {"error": str(e)}

def _stream(payload: dict):
    """Yield JSON chunks from a streaming response."""
    payload = {**payload, "stream": True}
    data = json.dumps(payload).encode()
    req  = urllib.request.Request(
        f"{OLLAMA_URL}/api/chat", data=data,
        headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            for line in r:
                line = line.decode().strip()
                if line:
                    try: yield json.loads(line)
                    except: pass
    except Exception as e:
        yield {"error": str(e), "done": True}

def strip_think(text: str) -> str:
    """Strip Qwen3 <think>...</think> blocks."""
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

def ollama_simple(model: str, messages: list) -> str:
    """Non-tool call — stream response to stdout, return full text."""
    full = ""
    print()
    for chunk in _stream({"model": model, "messages": messages}):
        if "error" in chunk:
            print(c(f"[error: {chunk['error']}]", RED))
            break
        token = chunk.get("message", {}).get("content", "")
        if token:
            clean = strip_think(token) if not full else token
            print(clean, end="", flush=True)
            full += token
        if chunk.get("done"):
            break
    print()
    return strip_think(full)

# ── Tools (qwen3 only) ────────────────────────────────────────────────────────

TOOLS = [
    {"type":"function","function":{
        "name":"read_file","description":"Read a file. Use relative paths from cwd.",
        "parameters":{"type":"object","properties":{"path":{"type":"string"}},"required":["path"]}}},
    {"type":"function","function":{
        "name":"write_file","description":"Write or overwrite a file.",
        "parameters":{"type":"object","properties":{"path":{"type":"string"},"content":{"type":"string"}},"required":["path","content"]}}},
    {"type":"function","function":{
        "name":"edit_file","description":"Replace a unique string in a file. old_string must appear exactly once.",
        "parameters":{"type":"object","properties":{"path":{"type":"string"},"old_string":{"type":"string"},"new_string":{"type":"string"}},"required":["path","old_string","new_string"]}}},
    {"type":"function","function":{
        "name":"run_bash","description":"Run a shell command. Returns stdout+stderr.",
        "parameters":{"type":"object","properties":{"command":{"type":"string"}},"required":["command"]}}},
    {"type":"function","function":{
        "name":"list_files","description":"Glob file listing (recursive).",
        "parameters":{"type":"object","properties":{"pattern":{"type":"string"},"base_dir":{"type":"string"}},"required":["pattern"]}}},
    {"type":"function","function":{
        "name":"search_code","description":"Regex search across files with line numbers.",
        "parameters":{"type":"object","properties":{"pattern":{"type":"string"},"path":{"type":"string"}},"required":["pattern"]}}},
]

WRITE_TOOLS = {"write_file", "edit_file", "run_bash"}

def resolve(raw: str) -> Path:
    p = Path(raw)
    return p if p.is_absolute() else Path(os.getcwd()) / p

def run_tool(name: str, args: dict, tier: int) -> str:
    if tier <= 1 and name in WRITE_TOOLS:
        print(c(f"\n  [T1] {name}({json.dumps(args)[:120]})", YEL))
        if input(c("  Allow? [y/N]: ", YEL)).strip().lower() != "y":
            return "Denied."

    if name == "read_file":
        p = resolve(args["path"])
        try:
            t = p.read_text(encoding="utf-8", errors="replace")
            return t[:20000] + ("\n...[truncated]" if len(t) > 20000 else "")
        except Exception as e: return f"Error: {e}"

    elif name == "write_file":
        p = resolve(args["path"])
        try:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(args["content"], encoding="utf-8")
            return f"Written {p}"
        except Exception as e: return f"Error: {e}"

    elif name == "edit_file":
        p = resolve(args["path"])
        try:
            t = p.read_text(encoding="utf-8")
            old, new = args["old_string"], args["new_string"]
            n = t.count(old)
            if n == 0: return f"old_string not found in {p}"
            if n > 1:  return f"old_string appears {n} times — be more specific"
            p.write_text(t.replace(old, new, 1), encoding="utf-8")
            return f"Edited {p}"
        except Exception as e: return f"Error: {e}"

    elif name == "run_bash":
        try:
            r = subprocess.run(args["command"], shell=True, capture_output=True,
                               text=True, timeout=60, cwd=os.getcwd(),
                               encoding="utf-8", errors="replace")
            out = (r.stdout + r.stderr).strip()
            return out or "(no output)"
        except subprocess.TimeoutExpired: return "Timed out"
        except Exception as e: return f"Error: {e}"

    elif name == "list_files":
        import glob as _g
        base = args.get("base_dir", os.getcwd())
        matches = _g.glob(os.path.join(base, args["pattern"]), recursive=True)
        return "\n".join(sorted(matches)) or "(none)"

    elif name == "search_code":
        path = args.get("path", os.getcwd())
        try:
            r = subprocess.run(["grep","-rn", args["pattern"], str(path)],
                               capture_output=True, text=True, timeout=15)
            return r.stdout.strip() or "(no matches)"
        except Exception:
            r = subprocess.run(f'findstr /s /n /r "{args["pattern"]}" "{path}"',
                               shell=True, capture_output=True, text=True, timeout=15)
            return r.stdout.strip() or "(no matches)"

    return f"Unknown tool: {name}"

# ── Qwen3 agentic loop ────────────────────────────────────────────────────────

def run_qwen(messages: list, tier: int) -> str:
    """Full tool-call loop with qwen3:14b."""
    msgs = list(messages)
    for _ in range(MAX_TOOL_ROUNDS):
        result = _post({"model": MODELS["architectural"], "messages": msgs,
                        "tools": TOOLS, "stream": False})
        if "error" in result:
            print(c(f"[qwen error: {result['error']}]", RED))
            return ""

        msg        = result.get("message", {})
        tool_calls = msg.get("tool_calls") or []
        content    = strip_think(msg.get("content") or "")

        if not tool_calls:
            if content:
                print(f"\n{content}")
            return content

        msgs.append({"role": "assistant", "content": content, "tool_calls": tool_calls})

        for tc in tool_calls:
            fn   = tc.get("function", {})
            name = fn.get("name", "")
            args = fn.get("arguments", {})
            if isinstance(args, str):
                try: args = json.loads(args)
                except: args = {}

            preview = ", ".join(f"{k}={repr(v)[:50]}" for k, v in args.items())
            print(c(f"  >> {name}({preview})", CYAN), flush=True)

            result_str = run_tool(name, args, tier)
            first_line = result_str.splitlines()[0][:100] if result_str else ""
            print(c(f"     {first_line}", GREY))

            if len(result_str) > 8000:
                result_str = result_str[:8000] + "\n...[truncated]"

            msgs.append({"role": "tool", "content": result_str})

    return "[max rounds]"

# ── Deepseek mechanical path ──────────────────────────────────────────────────

FILE_EXTS = re.compile(
    r'(?:^|[\s\'"/])([^\s\'"]+\.(?:lua|luau|py|js|ts|json|cs|java|md|txt|toml|yaml|yml|sh|ps1))',
    re.IGNORECASE
)

def auto_read_files(prompt: str) -> dict[str, str]:
    """Find file paths mentioned in the prompt and read them."""
    found = {}
    for m in FILE_EXTS.finditer(prompt):
        raw  = m.group(1).strip()
        path = resolve(raw)
        if path.exists() and path.is_file():
            try:
                content = path.read_text(encoding="utf-8", errors="replace")
                if len(content) > 15000:
                    content = content[:15000] + "\n...[truncated]"
                found[str(path)] = content
            except: pass
    return found

def parse_code_blocks(text: str) -> list[tuple[str, str]]:
    """Extract (lang_or_filename, code) pairs from markdown code fences."""
    blocks = []
    pattern = re.compile(r"```([^\n]*)\n(.*?)```", re.DOTALL)
    for m in pattern.finditer(text):
        header = m.group(1).strip()
        code   = m.group(2).rstrip()
        blocks.append((header, code))
    return blocks

def try_apply_blocks(response_text: str, injected_files: dict, tier: int):
    """
    If the model output code blocks that look like modified versions of injected files,
    offer to write them back.
    """
    blocks = parse_code_blocks(response_text)
    if not blocks:
        return

    for header, code in blocks:
        # Match header to an injected file path
        matched_path = None
        for fpath in injected_files:
            name = Path(fpath).name
            if name.lower() in header.lower() or header.lower() in fpath.lower():
                matched_path = fpath
                break

        if not matched_path:
            # Single injected file → assume the block is its replacement
            if len(injected_files) == 1:
                matched_path = next(iter(injected_files))

        if matched_path:
            if tier >= 2:
                Path(matched_path).write_text(code, encoding="utf-8")
                print(c(f"  [applied] {matched_path}", GRN))
            else:
                print(c(f"\n  [T1] Write {matched_path}?", YEL))
                if input(c("  Apply? [y/N]: ", YEL)).strip().lower() == "y":
                    Path(matched_path).write_text(code, encoding="utf-8")
                    print(c(f"  [applied] {matched_path}", GRN))

DEEPSEEK_SYSTEM = (
    "You are an expert code editor. When given file contents and a task:\n"
    "1. Output the complete modified file in a code block with the filename as the header.\n"
    "2. For small changes, you may use before/after diff format instead.\n"
    "3. Be direct. No explanations unless asked.\n"
    "Format: ```filename.ext\\n<full file content>\\n```"
)

def run_deepseek(prompt: str, history: list, tier: int) -> str:
    """Mechanical path: inject file contents, call deepseek, apply code blocks."""
    injected = auto_read_files(prompt)

    # Build enriched user message
    parts = []
    for path, content in injected.items():
        rel = os.path.relpath(path, os.getcwd())
        parts.append(f"File: {rel}\n```\n{content}\n```")
    if parts:
        user_msg = "\n\n".join(parts) + "\n\nTask: " + prompt
    else:
        user_msg = prompt

    messages = [{"role": "system", "content": DEEPSEEK_SYSTEM}] + history + \
               [{"role": "user", "content": user_msg}]

    response = ollama_simple(MODELS["mechanical"], messages)
    try_apply_blocks(response, injected, tier)
    return response

# ── Classifier ────────────────────────────────────────────────────────────────

CLASSIFY_SYS = (
    "Classify this task as exactly one word: mechanical or architectural.\n"
    "mechanical = single-function edits, boilerplate, renames, syntax fixes, "
    "small targeted code changes where the file is named.\n"
    "architectural = questions, explanations, new systems, multi-file refactors, "
    "unclear bugs, design, anything requiring searching/reading the codebase.\n"
    "Reply with one word only."
)

# Prompts starting with these words are questions → always need tool access → architectural
_QUESTION_WORDS = (
    "what","how","where","show","list","find","explain","which","who","why",
    "can you","does","is ","are ","do ","could","would","should","tell",
    "describe","summarize","check","look","search","read","give me",
)
# Prompts starting with these are clearly mechanical edits
_EDIT_WORDS = (
    "rename","fix ","change","add ","remove","update","edit","refactor",
    "move","delete","replace","rewrite","convert",
)

def classify(prompt: str) -> str:
    lo = prompt.lower().strip()

    # Questions always go to qwen3 (needs tools to explore codebase)
    if any(lo.startswith(q) for q in _QUESTION_WORDS):
        return "architectural"

    # Obvious single-file edits: short prompt + edit keyword → mechanical
    if any(lo.startswith(e) for e in _EDIT_WORDS) and len(prompt.split()) <= 15:
        return "mechanical"

    # Short prompts without a question word — check if a known file is mentioned
    if len(prompt.split()) <= 10:
        if FILE_EXTS.search(prompt):
            return "mechanical"
        return "architectural"  # short but no file ref → let qwen handle it

    # Long prompts: call classifier
    r = _post({"model": MODELS["classifier"], "stream": False,
               "messages": [{"role":"system","content":CLASSIFY_SYS},
                             {"role":"user","content":prompt}]})
    text = strip_think(r.get("message", {}).get("content", "")).lower()
    return "architectural" if "architect" in text else "mechanical"

# ── REPL ──────────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = (
    "You are Mark, an expert software engineering assistant.\n"
    "Working directory: {cwd}\n"
    "Use tools to read files before editing, make changes directly, then summarise briefly."
)

HELP = """
  /local /default /performance  — routing mode (local models only)
  t1 / t2 / t3 / t4            — permission tier
  /clear                        — clear history
  /status                       — current config
  /dir <path>                   — change working directory
  /quit                         — exit
"""

def banner(tier: int):
    print(c("=" * 52, GREY))
    print(c("  Mark  —  Local Routing CLI", BOLD))
    print(c(f"  Mechanical  -> {MODELS['mechanical']}", GREY))
    print(c(f"  Architectural -> {MODELS['architectural']}", GREY))
    print(c(f"  Classifier  -> {MODELS['classifier']}", GREY))
    print(c(f"  Tier: T{tier}  |  Dir: {os.getcwd()}", CYAN))
    print(c("=" * 52, GREY))
    print(c("  /help for commands\n", GREY))

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=os.getcwd())
    args = ap.parse_args()
    try: os.chdir(args.dir)
    except Exception as e: print(c(f"Warning: {e}", YEL))

    tier    = 1
    history = []   # user + assistant pairs only

    banner(tier)

    while True:
        try:
            prompt = input(c("You: ", BOLD)).strip()
        except (EOFError, KeyboardInterrupt):
            print(c("\nBye.", GREY)); break

        if not prompt: continue
        lo = prompt.lower()

        # Meta-commands
        if lo in ("/local", "/default", "/performance"):
            print(c(f"Mode noted: {lo} (all modes use same local models)", CYAN)); continue
        if lo == "/max":
            print(c("No cloud configured — using local models.", YEL)); continue
        if re.match(r"^(go\s+)?t[1-4]$", lo) or lo in ("t1","t2","t3","t4"):
            tier = int(re.search(r"[1-4]", lo).group())
            print(c(f"Tier -> T{tier}", CYAN)); continue
        if lo == "full autonomy":
            tier = 4; print(c("Tier -> T4", CYAN)); continue
        if lo == "/clear":
            history = []; print(c("Cleared.", GREY)); continue
        if lo == "/status":
            print(c(f"Tier: T{tier}  Dir: {os.getcwd()}", CYAN)); continue
        if lo.startswith("/dir "):
            nd = prompt[5:].strip()
            try: os.chdir(nd); print(c(f"Dir -> {os.getcwd()}", CYAN))
            except Exception as e: print(c(f"Error: {e}", RED))
            continue
        if lo in ("/help", "help"):
            print(HELP); continue
        if lo in ("/quit", "/exit", "quit", "exit"):
            break

        # Classify + route
        task_type = classify(prompt)
        print(c(f"  [{task_type} -> {MODELS['mechanical'] if task_type == 'mechanical' else MODELS['architectural']}]", GREY))

        # Build system message for qwen (deepseek doesn't use tool loop)
        sys_msg  = {"role": "system", "content": SYSTEM_PROMPT.format(cwd=os.getcwd())}

        if task_type == "mechanical":
            response = run_deepseek(prompt, history, tier)
        else:
            messages = [sys_msg] + history + [{"role": "user", "content": prompt}]
            response = run_qwen(messages, tier)

        # Update history
        history += [{"role": "user", "content": prompt},
                    {"role": "assistant", "content": response}]
        if len(history) > 40:
            history = history[-40:]
        print()

if __name__ == "__main__":
    main()
