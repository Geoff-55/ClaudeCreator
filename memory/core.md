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

## Troll Mountain (Roblox)
- Game concept: climb a mountain, troll other players with purchased abilities
- Map: workspace.Map contains Ramp1–Ramp5 (5 ramps escalating in height, same general area) + WinPad
- Max climb height for progress bar: Y=5500 (5 ramps combined)
- Models: ReplicatedStorage.Models.Coin + ReplicatedStorage.Models.CoinStack (placed manually in Studio)
- Coin system: server hitbox (workspace.Coins folder, 500 coins) + client visual clone; CoinType attribute picks template
- Coin lifetime: 15–20s random; fades 3s before expiry; fades on collection too (AncestryChanged starts fade, task.delay cleans up)
- Starting speed: 1 WalkSpeed; starting coins: 0
- Upgrades: Speed (cost 1+level, +1/level, display starts Lv.1), CoinMult (2× stacks), PassiveCoins (+1/interval) — all data-driven in UpgradeService
- Speed system: PlayerData.baseSpeed tracks raw speed; WalkSpeed = baseSpeed × shoeSpeedMult everywhere (upgrades, equip, respawn). No playerSpeeds table.
- High-speed fix: HighSpeedController.client.luau sets HRootPart.AssemblyLinearVelocity each Heartbeat — bypasses humanoid motor cap at ~100
- Win condition: touch WinPad → 10,000 coins + 1 Win + LoadCharacter + fires PlayerWon RemoteEvent → all clients show "🏁 [name] reached the top!" banner
- HUD: 3 chips ($ coins, ⚡ speed shows maxSpeed, 🏁 wins), coin timer bar LEFT of coins chip, speed control widget bottom-right (type speed ≤ max, Max button)
- Menus: Coin Shop (Upgrades/Crates tabs, Upgrades first), Win Shop (Upgrades/Crates tabs, Upgrades first + qty selector), Inventory (Crates/Shoes tabs)
- Coin Shop: 100 coins = 1 crate; Win Shop: 1 win = 10 crates; Win Upgrades: WinSpeed (+100 WalkSpeed, costs level+1 wins, supports qty)
- Inventory: player.Inventory folder; CommonCrate, CommonShoe, RareShoe (IntValues), EquippedShoe (StringValue)
- Shoe system: OpenCrate rolls 90% Common / 10% Rare; Common (green) ×1.5 speed ×2 coins sells 5$; Rare (blue) ×2.5 speed ×5 coins sells 50$; only one equipped; both coinMult and shoeCoinMult apply to ramp pickups + passive coins
- Crate roll animation: 32-slot reel, items scale by distance from centre (Heartbeat loop), 5s Quart.Out, Skip button
- Crates: workspace.Crates folder, CrateHitbox parts, 60s lifetime, 5s fade, Collected attribute = instant vanish on pickup
- Coins: ExpiresAt attribute (server-synced), Collected attribute = instant vanish on pickup, natural expiry = 3s fade
- ProgressBar: all players tracked, height-based Y/5500
- IMPORTANT: duplicate scripts in StarterPlayerScripts caused double popups — watch for this after Rojo syncs
- RobloxGame has its own git repo at C:\Dev\RobloxGame (initialized session 21)

## Roblox Project
- Project root: C:\Dev\RobloxGame
- Rojo v7.6.1 (Aftman-managed, config at C:\Dev\RobloxGame\aftman.toml)
- Studio plugin: Rojo 7.6.1 by Rojo Foundation
- src/server → Scripts folder inside ServerScriptService, src/client → StarterPlayerScripts, src/shared → Shared folder in ReplicatedStorage
- Must be in Edit mode for Rojo to sync; Script Injection permission must be granted in Plugin Manager
- Output panel: View → Output in Studio menu bar

## Gotchas

- gh CLI installed and working (auth'd as Geoff-55)
- GitHub repo: github.com/Geoff-55/ClaudeCreator (master branch → deploys to Cloudflare Pages)
- Screenshot watcher auto-starts each session; screenshots land in Screenshots/ (gitignored)
- Games live in src/website/games/, linked from drafts.html with ?from=drafts param
- geodash.html = original GeoDash, marked DNF (kept for reference)
- geodash2.html = new GeoDash in active development, level editor first
- survival.html = survival game, FINAL — published at corecreate.dev; open world, two mine floors (cave1/cave2), full crafting with tier-gated recipes (bronze→floor1, iron→floor2, monolith→???), iron armor/tools, miner zombie (also surface after floor 2), monoliths (iron pickaxe, red flash, ??? drop), void_entrance recipe, horror: shadow figure + chicken flip + torch flash + monolith night scare, surface/cave floor detail, butterflies (stop day 7), trinket system (7 trinkets in goblin camps, 3 equip slots), crits+damage numbers, void world temple (curvy guide path + 6-step altar + guardian that chases player, free movement), themed main menu, 8 goblin camps (4 surface + 4 cave1): big tents (PS=4), log palisade walls (28-post ring, 3 entrance gaps), dirt paths, skull poles, weapon racks, camp torches+campfire emit light, archer towers (hatchet-choppable, archer drops), chest lock (kill all goblins to unlock), bone campfire light, water breathing (22s air, bubbles, drowning damage), cave Y-sort (rocks+stalagmites sorted together), coal-priority fuel, corrupt guardian chase: approach altar in void world → guardian chases player → touch return portal → exit + permanent red sun tint on surface
