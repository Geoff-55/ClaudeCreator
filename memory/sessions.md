# Session History

## Session 10 -- 2026-03-19

Survival game (survival.html) — world detail + progression + horror session:

**Monoliths:**
  - Spawn on surface after day 7 (cap 6 total across all levels, ~65% per cycle)
  - Also spawn in cave 1 and cave 2 (surface ~55%, cave1 ~23%, cave2 ~22%)
  - Pixel art obelisk: dark red/black body with red glow, rune marks, tapering spire
  - Requires iron pickaxe to mine (8 hits); drops 1 ??? item, -200 score, triggers red grid flash
  - Don't respawn at same spot; new ones spawn periodically at random positions

**??? item + recipe:**
  - ??? item = plain black square, drops from monoliths
  - ??? recipe (void_entrance): costs 15 iron ingots + 5 ??? items, requires crafting station
  - void_entrance item = red neon glowing mine entrance sprite
  - Recipe only visible after first monolith broken; red backdrop = can't craft, yellow = can craft
  - Recipe tier system: bronze recipes hidden until Floor 1 entered, iron until Floor 2 entered

**Horror effects updated:**
  - After breaking first monolith: ~5%/sec chance at night for corrupt player to flash directly next to player (0.07–0.17s)
  - Upside-down chicken 2.25× more frequent (0.00008 → 0.00018)
  - Butterflies stop spawning on day 7+

**World details:**
  - Surface: soil/moss patches (3–8 per chunk, dark green + dirt brown), 4-petal cross flowers (sparse, 8 colors), mushrooms kept
  - Cave 1 floor: pebble clusters (3–7/chunk), 0–2 stalagmites, floor cracks (60%), dark puddle smears (25%)
  - Cave 2 floor: scorch patches (2–6/chunk), 1–2 cracks (50% chance for two), ash piles (50%)

**Other changes:**
  - Miner zombies: always spawn in cave 2, 1/10 chance in cave 1
  - Plain rock nodes drop 3–5 rocks (was 2–4)

## Session 9 -- 2026-03-18

Survival game (survival.html) — polish + horror atmosphere session:
  - Phantom zombie: black body, red eyes, invincible (hp=999), rushes player, explodes into smoke on contact
    - Spawn rate: 1/12 zombies, day 3+, surface and underground
    - Ignores campfire flee logic
    - Contact damage: 4 (tiny, was 18)
  - Shadow figure (corrupt player): pops in/out instantly (no fade), shorter duration, smaller, darker colors
    - Triggers when player stands still 3.5s OR objects enter screen edge
    - Works underground (cave rocks as candidates)
    - More visible — object-edge positioning so figure is half-peeking
  - Armor system overhauled to % damage reduction (direct correlation):
    - Feather hat: 5%, bone shield: 10%, bone armor: 10%, feather pants: 5% (30% max)
    - Damage formula: dmg * (1 - defPct/100), min 1
    - Bone shield recipe added: 10 bones at crafting station, equips in shield slot
  - Defense display: "Defense: X%" centered at bottom of inventory panel
  - Sword damage reduced (iron: 5→3, bronze: 12→8), player HP reduced to 75
  - Crafting station cost: 5 rocks (was 10); mine entrance: 10 rocks (was 20)
  - Upside-down chicken easter egg: day 3+, rare chance, flips for 0.6–1.4s, sprite darkened (45% opacity)
  - Torches flash red briefly (0.08–0.18s) at rare random intervals after day 3
  - Sapling progress bar removed

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
