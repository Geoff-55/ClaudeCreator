# Core Memory

## Who I Am

Name: Soll
Email: GeofferyEinstein-55@protonmail.com
Programming background: Some experience with Java, C#, and Lua.
Understands how programming works but not an expert in any language.

## Key Decisions

- Project root: C:\Dev\ClaudeCreator
- Primary focus: Minigame website (with future content creation functionality planned)
- C:\Dev\ will house multiple projects over time
- Website: corecreate.dev -- hosted on Cloudflare Pages, deployed via GitHub push
- Website source: src/website/ in this repo

## Roblox Project
- Project root: C:\Dev\RobloxGame
- Rojo v7.6.1 (Aftman-managed, config at C:\Dev\RobloxGame\aftman.toml)
- Studio plugin: Rojo 7.6.1 by Rojo Foundation
- src/server → Scripts folder inside ServerScriptService, src/client → StarterPlayerScripts, src/shared → Shared folder in ReplicatedStorage
- Must be in Edit mode for Rojo to sync; Script Injection permission must be granted in Plugin Manager

## Gotchas

- gh CLI installed and working (auth'd as Geoff-55)
- GitHub repo: github.com/Geoff-55/ClaudeCreator (master branch → deploys to Cloudflare Pages)
- Screenshot watcher auto-starts each session; screenshots land in Screenshots/ (gitignored)
- Games live in src/website/games/, linked from drafts.html with ?from=drafts param
- geodash.html = original GeoDash, marked DNF (kept for reference)
- geodash2.html = new GeoDash in active development, level editor first
- survival.html = survival game, active development; open world, two mine floors (cave1/cave2), full crafting with tier-gated recipes (bronze→floor1, iron→floor2, monolith→???), iron armor/tools, miner zombie (also surface after floor 2), monoliths (iron pickaxe, red flash, ??? drop), void_entrance recipe, horror: shadow figure + chicken flip + torch flash + monolith night scare, surface/cave floor detail, butterflies (stop day 7), trinket system (7 trinkets in goblin camps, 3 equip slots), crits+damage numbers, void world temple (curvy guide path + 6-step altar + guardian that chases player, free movement), themed main menu, 8 goblin camps (4 surface + 4 cave1): big tents (PS=4), log palisade walls (28-post ring, 3 entrance gaps), dirt paths, skull poles, weapon racks, camp torches+campfire emit light, archer towers (hatchet-choppable, archer drops), chest lock (kill all goblins to unlock), bone campfire light, water breathing (22s air, bubbles, drowning damage), cave Y-sort (rocks+stalagmites sorted together), coal-priority fuel, corrupt guardian chase: approach altar in void world → guardian chases player → touch return portal → exit + permanent red sun tint on surface
