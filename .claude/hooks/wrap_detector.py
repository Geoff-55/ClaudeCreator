import sys
import json

try:
    data = json.load(sys.stdin)
    prompt = data.get("prompt", "")
except Exception:
    sys.exit(0)

if "full wrap" in prompt.lower():
    output = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": (
                "The user has requested a 'full wrap'. "
                "Perform the complete wrap protocol: update memory/sessions.md with what was accomplished this session, "
                "update memory/core.md if any new permanent facts were learned. "
                "Then commit ALL changes with git — do NOT ask for confirmation, do NOT ask 'shall I proceed', "
                "just do it automatically. Answer yes to yourself on all proceed questions and complete the full sequence."
            )
        }
    }
    print(json.dumps(output))

sys.exit(0)
