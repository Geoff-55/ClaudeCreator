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
- What requires approval depends on the current permission tier (see below).
- Do ask before anything destructive (deleting files, force pushes, etc) -- always, any tier.

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
2. Start the screenshot watcher silently in the background:
   `Start-Process powershell -ArgumentList "-ExecutionPolicy Bypass -WindowStyle Hidden -File C:\Dev\ClaudeCreator\scripts\watch_screenshots.ps1" -WindowStyle Hidden`
3. Announce current tier: **T1 (Observe)** — read-only by default
4. Give a brief summary of where we left off (based on sessions.md)
5. Ask what I want to work on

At the end of every session (when I say "wrap" or "done"):
1. Update memory/sessions.md with what was accomplished
2. Update memory/core.md if any new permanent facts were learned
3. Commit all changes automatically (no need to ask)

---

## Permission Tier System

At the start of every session, display:
> "Current tier: **T1 (Observe)** — read-only. I will ask before changes.
> To change tier, say: go T2 / go T3 / go T4, or bump up / drop down."

Default to **T1** until Soll sets a tier. The first time an action would
require asking, pause and offer: "Want to change tiers before I proceed?"

Tier changes take effect immediately:
- "go T2", "go T3", "go T4"
- "bump up" (one tier higher), "drop down" (one tier lower)
- "full autonomy" (go to T4)

### Tier Definitions

| Action | T1 Observe | T2 Guided | T3 Active | T4 Full |
|--------|:----------:|:---------:|:---------:|:-------:|
| Read files (any location) | auto | auto | auto | auto |
| Web search / fetch | auto | auto | auto | auto |
| git read (status / log / diff) | auto | auto | auto | auto |
| Edit / create files in `C:\Dev\ClaudeCreator` | ask | auto | auto | auto |
| Run safe shell commands | ask | auto | auto | auto |
| git add / commit / tag | ask | auto | auto | auto |
| Edit / create files outside project | ask | ask | auto | auto |
| Install packages | ask | ask | notify | notify |
| git push (non-main branch) | ask | ask | auto | auto |
| Delete files | ask | ask | ask | notify |
| git push to main | ask | ask | ask | auto |
| Modify system config | ask | ask | ask | auto |
| Destructive git (force push, reset) | ask | ask | ask | ask |

**auto** — proceed silently
**notify** — proceed and inform what was done
**ask** — pause and get explicit approval before acting

Destructive git (force push, reset --hard, clean -f) ALWAYS asks, any tier.

---

## Security Rules

- Secrets (API keys, tokens, passwords) go in `.env` ONLY
- `.env` is gitignored -- verify with `git status` before any commit
- Never hardcode secrets in source files
- Before every `git add`, review what's being staged
- If a secret accidentally gets committed, consider it compromised
  and rotate it immediately -- git history is permanent
