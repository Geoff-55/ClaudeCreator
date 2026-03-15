# ClaudeCreator -- CLAUDE.md

This file is loaded by Claude Code at the start of every session.

---

## About This Project

ClaudeCreator is a multi-project workspace. The primary and current focus is
building a content creation tool/system. Additional projects will be added
over time under C:\Dev\.

---

## About Me

Name: Soll
Email: GeofferyEinstein-55@protonmail.com
Programming background: Some experience with Java, C#, and Lua. Understands
how programming works conceptually but not an expert in any single language.

---

## Project Structure

```
C:\Dev\ClaudeCreator\
  CLAUDE.md       -- this file
  .env            -- secrets (gitignored, never committed)
  config/         -- settings and non-secret config
  memory/         -- persistent memory (read at session start)
  docs/           -- notes and references
  src/            -- source code
  scripts/        -- utility scripts
  logs/           -- runtime logs
```

---

## How I Work

- Response length depends on the task -- match detail level to complexity.
  Simple tasks: short and direct. Complex tasks: explain as needed.
- After making changes, list what was done. Soll will flag anything that
  needs adjusting.
- Do not ask for approval before every small change -- just do it and report.
- Do ask before anything destructive (deleting files, force pushes, etc).

---

## Workflow Rules

1. Do not commit or push without explicit approval.
2. Do not delete files without asking first.
3. Do not install packages without asking first.
4. Never put secrets, tokens, or credentials in tracked files.
5. Git identity: Soll / GeofferyEinstein-55@protonmail.com

---

## Memory System

CC maintains persistent memory in the `memory/` directory:
- `memory/core.md` -- permanent facts (who I am, key decisions, preferences)
- `memory/sessions.md` -- session history (what was done each session)
- `memory/scratch.md` -- temporary working notes

## Session Protocol

At the start of every session:
1. Read memory/core.md, memory/sessions.md, and memory/scratch.md
2. Give a brief summary of where we left off (based on sessions.md)
3. Ask what I want to work on

At the end of every session (when I say "wrap" or "done"):
1. Update memory/sessions.md with what was accomplished
2. Update memory/core.md if any new permanent facts were learned
3. Commit if there are uncommitted changes (ask first)

---

## Security Rules

- Secrets (API keys, tokens, passwords) go in `.env` ONLY
- `.env` is gitignored -- verify with `git status` before any commit
- Never hardcode secrets in source files
- Before every `git add`, review what's being staged
- If a secret accidentally gets committed, consider it compromised
  and rotate it immediately -- git history is permanent
