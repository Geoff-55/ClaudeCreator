# Session History

## Session 8 -- 2026-03-16

Survival game (survival.html) — heavy development session:
  - Completed camera lock + open world (5×7 chunks, 4400×3430px) — fixed missing updateCamera/drawBorder calls in loop
  - Chunk boundary lines (dev aid) drawn slightly brighter than grid
  - Canvas border: subtle neon-glow border around the game element
  - Stamina system: Shift to sprint (1.75× speed), 40/s drain, regens instantly when still or after 3s of walking; stamina bar bottom-left, cyan when draining, purple when ready
  - Seeded world generation per chunk (chunkRNG): grass patches + trees always same position
  - Grass: 2 chunky variants (2-3 solid pixel-block blades, 4px wide), neon purple palette, 2–4 patches per chunk
  - Trees: 2D side-view style — large oval canopy (120×90px, 5px blocks), segmented wavy trunk (8px segs with ±6px drift per tree), neon purple rings with glow on outer edge; 35% spawn chance per chunk
  - Tree depth layering: trunk base drawn before player (player in front), canopy+upper trunk drawn after (player hidden behind)
  - Trunk collision: AABB circle vs rect, pushes player out of trunk base; player can walk behind canopy freely
  - Inventory system: E to open/close, 4×5 grid (20 slots), dark panel with neon purple border, semi-transparent world dimming; slots empty placeholders ready for items

Next session: add items / tree chopping interaction, or continue filling out the survival game world.

## Session 7 -- 2026-03-16

GeoDash (geodash.html) wrapped up:
  - Fixed uncommitted changes from previous session (grounded platforms, hold-to-jump) by pushing them properly
  - Rotation reduced to 0.28x → then tuned to 0.56x (~180° per jump at half speed)
  - Platform blocks now fill column to floor visually (solid grounded pillars)
  - Jump buffer (120ms tap-before-landing window) added
  - Structured obstacle patterns: predefined block/spike formations instead of random per-column heights
  - Speed arrows: full-speed arrows never spawn during fast sections
  - Pink jump pads: rare, launch 60% higher, always followed by 3 pink spikes then platform or spike group
  - Main menu added: GEO (green) / DASH (purple) stacked title, Endless Mode (DNF) button, Esc to return
  - Marked as DNF: button label "(DNF)", card in drafts faded/dimmed

GeoDash 2 (geodash2.html) started fresh:
  - New drafts card with GEO/DASH split thumbnail
  - Menu: Create Levels tab only (game modes coming later)
  - Level editor: 8 save slots (session-only), 4×2 grid of cards with mini tile previews
  - Editor tools: Block, Spike, ½ Spike, Eraser; 7 ROYGBIV color swatches; Clear All
  - Click/drag to place, right-click to erase, ghost preview on hover, neon glow
  - Esc: editor → slots → menu; levels auto-save to slot on back

Next session: continue GeoDash 2 (add play mode, more tile types, or other game modes).

## Session 6 -- 2026-03-15

Completed website setup: corecreate.dev is live on Cloudflare Pages, deployed via GitHub push to Geoff-55/ClaudeCreator.
Built out the site structure: dark neon theme (purple), homepage with Drafts (password protected) and Published Games tabs.
Added screenshot watcher system (scripts/watch_screenshots.ps1 + stop script) -- auto-starts each session.
Built Pong 2 (src/website/games/pong2.html) -- full-featured canvas game:
  - Title menu → mode select (AI easy/med/hard or PvP) → score select (3/5/10/Endless) → game
  - Modifier system: 5 types (speed, ball shrink, paddle shrink, random obstacle, field shrink), stackable, queue in middle 10%, rate scales with round time, resets on point
  - 3-2-1 countdown between rounds, mod sounds, field pulse on queue/activate
  - Background music (ambient drone + pentatonic melody), starts on first interaction
  - Left panel shows active modifiers, context-aware back button (?from=drafts/published)
  - Thumbnail in drafts shows "PONG 2" + glowing ball SVG
Next session: more games, or start building the drafts/published management system.

## Session 5 -- 2026-03-15

Scrapped launch script and wrap hook system -- deleted scripts/launch.ps1, .claude/hooks/wrap_detector.py, and .claude/settings.json.
Added Permission Tier System to CLAUDE.md (T1 default, T2/T3/T4 tiers with matrix). Updated session protocol and How I Work accordingly.
Started website setup: goal is corecreate.dev hosted on Cloudflare Pages, deployed via GitHub push.
Created placeholder src/website/index.html.
Installed GitHub CLI (gh) via winget. Shell needs to reload before gh is available.
Next session: restart terminal, run `gh auth login`, create GitHub repo, connect to Cloudflare Pages.

## Session 4 -- 2026-03-15

Troubleshot launch.ps1: positional argument `claude "Hi, ready to continue?"` was launching Claude but the greeting never appeared.
Switched to `claude -c` which resumes the most recent conversation directly -- confirmed working.
Content creation project still not started -- next session.

## Session 3 -- 2026-03-15

Fixed launch.ps1: `claude --message` is not a valid flag; corrected to `claude "Hi, ready to continue?"` (positional argument).
Created "full wrap" hook system: .claude/hooks/wrap_detector.py detects "full wrap" phrase (case insensitive) and injects auto-proceed instructions. Registered via .claude/settings.json. Hook confirmed working this session.
Content creation project still not started -- next session.

## Session 2 -- 2026-03-15

Updated desktop shortcut to auto-send "Hi, ready to continue?" on launch.
Created scripts/launch.ps1 (navigates to project dir, runs claude with greeting message).
Updated ClaudeCreator.lnk to call the launch script via PowerShell.
Content creation project still not started -- next session.

## Session 1 -- 2026-03-15

Bootstrap session. Set up full project structure at C:\Dev\ClaudeCreator.
Initialized git repo (user: Soll). Created CLAUDE.md, memory system, .gitignore,
and .env template. Installed Python 3.12.10 via winget. Created desktop shortcut
(with Run as Administrator + auto-launch claude) for quick access. Shortcut can
be pinned to taskbar. Content creation project not yet started -- next session.
