# Session History

## Session 29 -- 2026-04-16

One Versus All — polish, bug fixes, impact/bounce overhaul, world health bar, player collision:

**Impact system fixes:**
- Bounce was being killed by duplicate trigger: `hrp.Touched` (async) and sphere-sweep (same frame) both called `onImpact`; the second hit the IMPACT_COOLDOWN debounce which had `flyVelocity = Vector3.zero` — removed that zero from debounce path so the first trigger's bounce survives
- Added `punchArmEnd + 0.2` guard to Touched handler: impact suppressed during/after punch swing to prevent close-range punch from triggering wall impact
- VFX anchor Parts (placed at hit positions in workspace) could fire `hrp.Touched` despite CanCollide=false (known Roblox quirk): added `CanTouch=false` + `CanQuery=false` to all VFX anchors; named them "VFXAnchor" and added to Touched name filter
- `ImpactBlastSphere` made fully invisible (Transparency=1, removed neon color/material)

**Player-player collision (spinning fix):**
- Physical HRP contact during flight caused Roblox physics separation impulses; tilt system read these as rapid direction changes → character spin visible to other clients
- Added PhysicsService "Players" collision group (server-side in CombatService): all character parts assigned on spawn, `CollisionGroupSetCollidable("Players","Players",false)` — players now phase through each other; all combat remains hitbox-based so nothing breaks

**World health bar:**
- Restructured billboard to double height (36px) with bar occupying top half only — bottom edge of bar now sits at StudsOffset anchor, preventing bar from clipping into opponent's head at close range
- Distance scaling: full size within 20 studs, shrinks to 55% minimum at long range (0.3%/stud beyond 20)
- Bar visibility tied to lock-on: shows only when right-click locked onto a player

**Screen health bar:**
- Removed default Roblox health bar (`SetCoreGuiEnabled(Health, false)`)
- Flash on damage (white overlay, 0.35s fade)
- Color now changes green→yellow→red via `worldBarColor()` (same function as world bar)
- HUD update moved before `if not flying then return end` so bars stay accurate during ragdoll/death

**Camera:**
- `LOOK_OFFSET`: 2 → 3.5 so player appears slightly below camera center

**Respawn state resets (enableFly):**
- Now resets: `stunEndTime=0`, `punchArmEnd=0`, `lastDashTime=-DASH_COOLDOWN` (dash ready on spawn), `lastImpactTime=-10`

**Dead code removed:**
- Client constants: `DASH_CRASH_RATIO`, `SLAM_MIN_SPEED` (client-side 150, never read), `IMPACT_SPEED_LOST`

**Touched handler (player filtering, layered):**
- Name filter: PunchHitbox, HitSphere, ImpactBlastSphere, VFXAnchor
- Own character: `IsDescendantOf(character)`
- Fast-path Humanoid: `hit.Parent:FindFirstChildOfClass("Humanoid")`
- Belt-and-suspenders: full `Players:GetPlayers()` loop with `IsDescendantOf`
- Punch suppression: `os.clock() < punchArmEnd + 0.2`

## Session 28 -- 2026-04-13

One Versus All — hitbox polish, leaderboard, SFX, cleanup:

**Momentum stopper fix:**
- `hrp.Touched` handler now also skips parts named `PunchHitbox` or `HitSphere`, and any part descending from the local character — prevents own hitboxes from triggering a momentum stop

**Leaderboard (Kills / Deaths):**
- `leaderstats` folder with `Kills` (IntValue, sorts first) and `Deaths` (IntValue) created on `PlayerAdded`
- `lastHitBy[targetPlayer]` tracks last attacker per player; credited a Kill when their target's `Humanoid.Died` fires, receiver gets a Death
- Player removal cleans up all references to prevent stale kill credits

**Barrel roll (added then removed):**
- Implemented A↔D flip barrel roll (decaying extra lean offset, additive); user decided to remove it

**Hand wind VFX (added then removed):**
- Attempted to clone `ReplicatedStorage.VFX.Small Wind` onto each hand and toggle Beams at 190+ speed; Beam attachment references broke in clone — removed

**Hitbox visibility:**
- `PunchHitbox` Transparency: 0.8 → 1 (fully invisible)
- `HitSphere` Transparency: 0.8 → 1 (fully invisible)

**Receiver SFX:**
- `resultType` now passed through `knockbackRemote` to the receiver
- Receiver plays punch SFX on hit/partial, block SFX on perfect block — same sounds as attacker
- `punchSFXTemplate`/`blockSFXTemplate` declarations moved above knockback handler (Lua scoping fix)

## Session 27 -- 2026-04-13

One Versus All — flight overhaul, punch hitbox tuning, tilt polish:

**Dash:**
- `DASH_BURST_SPEED`: 350 → 400
- WASD steering restored during burst and transition (direction follows input, speed stays at burst/blend level)
- Burst/transition now use same lerp system as normal flight (no hard-set) — seamless handoff

**Normal flight:**
- `FLY_SPEED`: 50 → 200 (new normal cruise max)
- `FLY_ACCEL`: 0.15 → 0.015 — W now slowly accelerates from 0 to 200 over ~2–3s
- Direction change rate kept fast (0.15) — camera turning is instant, separate from speed buildup
- W/A/S/D now fly in full camera direction including pitch (looking up + W = fly up)
- V/B restored as instant vertical boost added to `finalVel`, independent of WASD pitch movement
- Brake only affects `flyVelocity`, not V/B

**Tilt system unified:**
- Removed old `tiltFwd`/`tiltSide` angle-based system entirely
- Single system (`currentDashUp`/`currentDashLean`) always active, scaled by `speedFactor` (0 at rest → full at FLY_SPEED)
- Backwards diagonal lean (S+D, S+A): `targetLean` inverted when S held without W
- Coasting tilt: when no keys pressed but still moving, `fwdSign`/`sideSign` derived from velocity projected onto camera axes so tilt lingers; lerpRate `TILT_LERP*2` (was `*5`) when coasting

**Punch hitbox:**
- Size: 14×10×10 → 10×10×14 (narrower, longer)
- Offset: shifted 4 studs forward (0.5 → -3.5 local Z)
- Transparency: 0.2 → 0.8

## Session 26 -- 2026-04-12

One Versus All — dash rebalance + smooth transition:

- `DASH_BURST_SPEED`: 1500 → 350 (1.75× cruise speed of 200)
- Added `DASH_TRANSITION_TIME = 0.6s`: after the 1s burst, velocity linearly interpolates from 350 → 200 over 0.6s before handing off to normal control
- Cruise speed guard now also skips during transition phase (`not inBurst and not inTransition`)
- Burst phase still hard-locks velocity to `lastDashDir * DASH_BURST_SPEED` each frame

## Session 25 -- 2026-04-12

One Versus All — several polish/balance changes:

**No health regen:** CombatService waits for the default `Health` LocalScript in the character and disables it on every spawn.

**Slam removed entirely:** Momentum kill and damage both removed. Hitting geometry at any speed has no effect.

**Cursor hidden:** `UIS.MouseIconEnabled = false` enforced every RenderStepped frame so it can never re-appear.

**Health bar:** Background red (`160, 30, 30`), green fill (`60, 200, 60`). Dash cooldown bar stays white on dark.

**Dash overhaul:**
- Burst speed locked for the full 1-second window — `flyVelocity` set to `lastDashDir * 1500` every frame during burst, no lerp or brake can interfere
- `lastDashDir` stored at dash time so direction is preserved
- Cruise speed (`200`) only drops to normal after burst ends AND velocity bleeds below FLY_SPEED
- Cooldown: 10s → 5s

**Hitbox:** 14×10×10 (from previous session's 12×8×8)

**Controls (from session 24):** Space = block, right-click hold = lock-on, V/B = up/down at speed 40

## Session 24 -- 2026-04-12

One Versus All — control rebind + balance pass:

**Controls:**
- Block moved from M2 (right-click) to Space
- Right-click hold now activates lock-on (combat mode) — releases when button released; CapsLock toggle removed entirely
- Fly up: Space → V; fly down: B (unchanged)
- Vertical fly speed: 20 → 40

**Balance:**
- Punch hitbox: 8×6×6 → 12×8×8 studs
- Perfect block window: 0.3s → 0.5s (updated in both PlayerController and CombatService)
- Knockback per damage point: 4.5 → 7.0 (faster punches hit much harder)

## Session 23 -- 2026-04-12

One Versus All — polish pass: drift fix, ground clearance, ragdoll on death:

**Drift deadzone fix:**
- Added three-tier brake: fast (`FLY_BRAKE * 4`) above `FLY_SPEED * 2`, extra-fast (`FLY_BRAKE * 10`) below 8 studs/s, hard snap to `Vector3.zero` below 0.4 studs/s
- The snap kills residual drift that lerp asymptotically approaches but never actually reaches

**Ground clearance (leg clipping):**
- `MIN_GROUND_CLEARANCE` raised 3 → 5 studs (R15 legs reach ~3 studs below HRP center)
- Push velocity multiplier raised 10 → 15 for faster correction
- Added hard position teleport correction if ground distance drops below 2 studs (catches fast downward movement before velocity alone can respond)

**Ragdoll on death:**
- `doRagdoll(character)`: disables all Motor6Ds (limbs separate), enables CanCollide on all BaseParts, destroys BodyVelocity so momentum carries into the fall
- Connected to `humanoid.Died` inside `enableFly()` so it fires on every spawn/respawn

## Session 22 -- 2026-04-12

One Versus All (C:\Dev\OneVersusAll) — new game built from scratch this session:

**Project setup:**
- Rojo project at `C:\Dev\OneVersusAll` (aftman.toml: rojo 7.6.1)
- `default.project.json`: src/server → ServerScriptService/Scripts, src/client → StarterPlayerScripts, src/shared → ReplicatedStorage/Shared

**Always-on flight system:**
- `PlayerController.client.luau`: BodyVelocity-based flight, auto-enabled on spawn, `PlatformStand = true`
- WASD moves relative to camera yaw; Space/Shift = up/down; natural deceleration (`FLY_BRAKE`)
- Speed-dependent brake: `FLY_BRAKE * 4` when `flyVelocity.Magnitude > FLY_SPEED * 2` to kill drift after high-speed

**Dash system:**
- Double-tap WASD to dash (900 burst for 0.25s, then cruises at 300 constant — no decay until crash/stop)
- 2s cooldown; crashing into geometry triggers full stop (velocity check ratio)
- Wind SFX plays on dash; footstep sound volume zeroed while flying

**Camera modes:**
- Surf mode (default): free mouse look (yaw+pitch), no lock-on
- Combat mode (Caps Lock toggle): same shoulder-cam but auto-locks yaw+pitch toward nearest Humanoid in workspace (players, dummies, NPCs)
- `getNearestEnemy()` scans `workspace:GetChildren()` for any Humanoid with Health > 0
- Shortest-path yaw lerp: `((yawTarget - yaw + 180) % 360) - 180`
- `combatMode = false` forced in `enableFly()` to guard against OS CapsLock state on load

**3D dash tilt:**
- W dash: HRP tilts feet-toward-cam (up = camera LookVector)
- S dash: feet-away-from-cam (up = -LookVector)
- A/D dash: partial tilt (up = blend of world-up + camera look) + lean roll via `CFrame.fromAxisAngle`
- Gram-Schmidt orthonormalization builds clean basis; `currentDashUp`/`currentDashLean` lerped for smooth transitions

**M1 Punch:**
- Anchored Part hitbox (8×6×6, hidden, yaw-only, no tilt) placed 3.5 studs in front, updated per frame during PUNCH_DURATION (0.3s)
- Overlap via `workspace:GetPartsInPart()`, fires `PunchHit` RemoteEvent to server with target Humanoid + speed + direction + hitPos
- Arm pose: right shoulder Motor6D rotated forward (`C0 * CFrame.Angles(-π/2, 0, 0)`) for punch duration

**M2 Block:**
- `BlockChanged` RemoteEvent fires server on hold/release; server tracks `blockData[player] = {active, startTime}` using `os.clock()`
- Perfect block (first 0.3s): 0 damage; partial block (held): 50% damage; unblocked: full damage
- Knockback always uses `rawDamage` (pre-block) so blocking doesn't reduce momentum
- Arm pose: both shoulders rotated into crossed-arm stance while blocking

**CombatService.server.luau (new file):**
- Speed-scaled damage: `BASE_DAMAGE(10) + attackerSpeed * DAMAGE_PER_SPEED(0.15)`, capped at 100
- Knockback: `punchDir * (rawDamage * KNOCKBACK_PER_DAMAGE(4.5))`
- Player health: 3× default (300 MaxHealth), applied on CharacterAdded
- Server fires `PunchResult(resultType, hitPos)` to attacker for VFX routing
- Knockback delivered via `KnockbackHit` RemoteEvent to player clients; direct `AssemblyLinearVelocity` for NPCs

**VFX/SFX system:**
- `ReplicatedStorage.VFX.Punch.Punch` fires on normal hit; `ReplicatedStorage.VFX.Block.Finisher` on perfect block
- `ReplicatedStorage.SFX.Punch` / `SFX.Block` sounds play at hit position
- VFX anchored to temp Part in workspace, `emitter:Emit(12)`, `Debris:AddItem(anchor, 0.5)`
- Client `punchResult.OnClientEvent` drives VFX — server decides type, client spawns it

**Key bug fixes:**
- Hitbox using `hrp.CFrame` (tilted) → fixed to yaw-only: `CFrame.new(hrp.Position) * CFrame.Angles(0, math.rad(yaw), 0) * CFrame.new(0, 0, -3.5)`
- Combat mode toggling on load due to OS CapsLock state → fixed with `combatMode = false` in `enableFly()`
- VFX burst emitters needed `Emit(N)` not `Enabled = true`; multiple hits spawning stacked VFX fixed with `vfxSpawned` flag

## Session 21 -- 2026-04-07

Troll Mountain — shoe loot system, crate roll animation, speed/coin fixes, balance tuning:

**Bug fix — crate buying broken:**
- Root cause: `CrateService.server.luau` had an early `return` if ramps weren't found, which skipped the player inventory setup entirely. Moved `setupInventory` before the ramp detection block so buying always works.
- TrollService: added defensive inventory creation + `warn()` logs on buy failure.

**Shoe loot system:**
- Opening a crate rolls 90% Common / 10% Rare shoe; result stored in `player.Inventory.CommonShoe` / `RareShoe` (IntValues), equipped in `EquippedShoe` (StringValue)
- Common (green): ×1.5 speed, ×2 coins, sells for 5$; Rare (blue): ×2.5 speed, ×5 coins, sells for 50$
- `TrollService`: `OpenCrate` rolls result + fires `CrateResult` to client; `EquipShoe` + `SellShoe` RemoteEvents handle equip/sell
- Only one shoe equipped at a time; switching shoes correctly removes old effect before applying new
- Inventory → Shoes tab: card per shoe type with count, stats, EQUIPPED badge, Equip and Sell buttons

**Crate roll animation:**
- Full-screen overlay (transparent panel over dark dimmer); 32-slot reel scrolls left-to-right
- Items scale by distance from centre: centre = full size (100×134px), edges = 50% — driven by RunService.Heartbeat reading AbsolutePosition each frame
- Items are portrait (taller than wide) to prevent icon clipping; viewport has 8px top/bottom padding
- 5s Quart.Out tween — rushes fast then decelerates hard
- Skip button below reel during spin; snaps to result immediately

**Speed system overhaul:**
- `PlayerData.baseSpeed` tracks raw speed (no shoe mult); `WalkSpeed = baseSpeed × shoeSpeedMult` everywhere
- Speed/WinSpeed upgrades add to `baseSpeed` then recalculate — shoe mult preserved correctly
- Switching/selling shoes always applies cleanly via `baseSpeed × newMult`; no more `preShoeSpeed` needed
- `playerSpeeds` table removed; `CharacterAdded` restores from `data.baseSpeed × data.shoeSpeedMult`

**Coin multipliers:**
- Both `coinMultiplier` (upgrades) and `shoeCoinMult` (shoes) now apply to ramp pickups AND passive coin generator

**High-speed fix:**
- `HighSpeedController.client.luau`: sets `HumanoidRootPart.AssemblyLinearVelocity` directly each Heartbeat when moving — bypasses the humanoid hip motor cap (~100 WalkSpeed). Y velocity preserved for gravity/jumping.

**Balance / UI tweaks:**
- Starting speed: 1 (was 10); starting coins: 0 (was 100,000)
- Speed upgrade cost: `1 + level` (was `5 + level`); level display starts at Lv. 1
- HUD `maxSpeed` initial value fixed: 1 (was hardcoded 10)
- Coin/Win Shop: Upgrades tab now first (left); Win Shop Upgrades now has qty selector (1/10/100)
- RobloxGame initialized as its own git repo (was untracked)

## Session 20 -- 2026-04-06

Troll Mountain — shop overhaul, crate system, coin fade fix, win notification, speed control:

**Coin fade fix:**
- `ExpiresAt` attribute (server-synced timestamp) replaces old `Expiring` attribute signal — client Heartbeat compares `workspace:GetServerTimeNow()` to `ExpiresAt` each frame to start fade; no replication race
- Server sets `Collected = true` on hitbox before destroying on pickup; both animators check this in `AncestryChanged` — collected = instant vanish, expired = fade out naturally
- `CoinAnimator` and `CrateAnimator` both rewritten with this collected/expired distinction

**Troll removal + shop overhaul:**
- Trolls removed entirely from the game
- `TrollService.server.luau` replaced with CrateShopService: `BuyCrate("Coins"|"Wins", qty)` and `OpenCrate(crateType)` RemoteEvents
- `UpgradeService.server.luau`: added `PurchaseWinUpgrade` event, `WinUpgradeLevels` folder per player, `WinSpeed` upgrade (costs level+1 wins, gives +100 WalkSpeed)
- `Announcement.client.luau` gutted (no trolls), repurposed for win notification

**Crate system:**
- `CrateService.server.luau`: spawns CommonCrates on ramps (1/sec for testing, 60s lifetime, 5s fade, 5-stud collection radius), awards to `player.Inventory.CommonCrate` IntValue, defensive awardCrate (creates Inventory if missing)
- `CrateAnimator.client.luau`: bobs vertically (0.3 studs, 0.7 cyc/s), fades in 0.5s, fades out 5s before expiry, instant vanish on collection
- `workspace.Crates` folder; `CrateHitbox` parts with `ExpiresAt` and `CrateType` attributes

**Menu restructure (Menus.client.luau full rewrite):**
- Sidebar: Coin Shop (gold), Win Shop (teal), Inventory (purple)
- Coin Shop tabs: Crates (100 coins = 1 crate, qty selector) + Upgrades (existing)
- Win Shop tabs: Crates (1 win = 10 crates, qty selector) + Upgrades (WinSpeed card)
- Inventory tabs: Crates (CommonCrate count + Open button) + Shoes (Coming Soon)
- RemoteEvents for BuyCrate/OpenCrate/PurchaseWinUpgrade resolved lazily via task.spawn to prevent blocking UI creation

**Win notification:**
- `WinService.server.luau`: fires `PlayerWon` RemoteEvent to all clients on win
- `Announcement.client.luau`: gold banner slides in — "🏁 [name] reached the top!", winner's name highlighted gold

**HUD additions:**
- Coin timer bar moved to LEFT of coins chip
- Speed chip now shows `maxSpeed` (highest WalkSpeed from upgrades), not current WalkSpeed
- Speed control widget (bottom-right, 160×26px): "Speed | [textbox] | Max" — type any number ≤ maxSpeed to set current speed, Max button snaps back to full speed

**Starting coins:** 100,000 (was 10,000) for testing

**Known issues (carry to next session):**
- Coin/crate collection works (notification fires) but inventory count not updating reliably — investigate Inventory folder timing and Collected attribute replication

## Session 19 -- 2026-04-02

Troll Mountain — major feature expansion + bug fixes:

**New systems built:**
- `PlayerData.luau` (shared): per-player data store for `coinMultiplier` and `passiveCoinBonus`, auto-init on first access, cleared on PlayerRemoving
- `UpgradeService.server.luau`: data-driven UPGRADES table (Speed/CoinMult/PassiveCoins), IntValues under `UpgradeLevels` folder per player, prices scale per level
- `TrollService.server.luau`: data-driven TROLLS table (Slide/Fling), network ownership fix for server-side physics, CooldownEnds attributes on player for client countdown display
- `WinService.server.luau`: detects WinPad.Touched under workspace.Map, debounced per player, awards 10,000 coins + 1 Win, calls LoadCharacter after 0.5s
- `Announcement.client.luau`: TrollActivated RemoteEvent listener, banner slides in from above HUD, holds 3.5s, slides back off

**Upgrades rework:**
- Speed: +1 WalkSpeed per level, price = 5+level
- CoinMult: 2× multiplier stacks per level, price = 25×4^level
- PassiveCoins: +1 passive coin/interval per level, price = 10+(level×10)
- Speed persists through death: `playerSpeeds` table in init.server.luau tracks WalkSpeed changes, restored on CharacterAdded

**Trolls:**
- Slide: PlatformStand=true + push in look direction (55 force), 3s duration, then zero velocity + nudge up 3 studs + restore
- Fling: PlatformStand=true, random horizontal direction (180° arc), Vector3(cos×120, 240, sin×120), restore after 3.5s
- Network ownership: SetNetworkOwner(nil) before velocity, SetNetworkOwner(owner) after
- Activator excluded from effect (target ≠ player check)

**UI additions:**
- HUD: Wins chip added (🏁 icon, gold), 3-chip layout (423px container)
- Menus: Trolls (red), Upgrades (blue), Inventory (purple) sidebar buttons; qty selector (1/10/100) on Upgrades; cooldown countdown on Trolls; Inventory panel empty (placeholder)
- ProgressBar: tracks all players via PlayerAdded/Removing, local=44px white border, others=32px blue border; MAX_HEIGHT=5500 (5 ramps)
- Announcement banner positioning fixed to sit below HUD (Y≈80)

**CoinStack system:**
- 1/10 chance of CoinStack spawn (worth 10×), `CoinType` attribute on hitbox
- CoinAnimator loads both Coin and CoinStack templates from ReplicatedStorage.Models
- Both use same spin+hover animation; orientation left as-is from model

**Bug fixes:**
- ScreenGui ZIndex → DisplayOrder (invalid property was killing Menus script before buttons created)
- Trolls not applying: network ownership race condition fixed with SetNetworkOwner(nil)/restore
- Slide standing still: WalkSpeed=0 caused Humanoid to brake; fixed with PlatformStand=true
- ApplyStrokeMode.Border on buttons prevents text outline bleed
- "✕" close button not rendering → changed to plain "X" TextLabel
- Coins popping out of existence (no fade): AncestryChanged was destroying model immediately on collection; fixed by starting fade in AncestryChanged + task.delay for cleanup
- hitbox.Position access after destruction: fixed by caching pos = hitbox.Position in data table
- Coin spawn count raised from 200 → 300 → 500; coin lifetime randomized 15–20s (was fixed 20s)

**Testing:**
- Starting coins set to 10,000 for testing (TODO: remove before release)
- Trolls affect all players except activator

## Session 18 -- 2026-03-31

Troll Mountain fresh start — wiped all old scripts, rebuilt core systems:

**Cleared:**
- Deleted all old Luau scripts from src/server and src/client (DamagePart, TrollEvents, etc.)
- Removed Roblox/Troll Mountain sections from core.md memory

**Scripts rebuilt from scratch:**
- `init.server.luau`: leaderstats (Coins IntValue), default WalkSpeed=10, passive +1 coin every 10s, +1 WalkSpeed every 100s. Fires `CoinAwarded`, `PassiveCoin`, `SpeedBoosted` RemoteEvents
- `CoinService.luau` (shared): single `award(player, amount)` function used by all server scripts to give coins + fire popup event
- `HUD.client.luau`: two chips ($ coins, ⚡ speed) each with a small vertical timer bar to the right showing time until next award. Coin popup (+X$) floats at random screen position on award
- `ProgressBar.client.luau`: left-side vertical bar, player headshot icon, green→yellow→red gradient, MAX_HEIGHT=2000, mild ease-out curve (p^0.8), bar spans 18%-82% screen height, 28px wide
- `LoadingScreen.client.luau`: dark fullscreen overlay, gold progress bar, % counter, skip button, ContentProvider preload, fades out
- `Coins.server.luau`: 200 coins on ramp, 20s lifetime, fade warning 1.5s before expiry, proximity collection (5 studs), respawn at new position on collect or expiry
- `CoinAnimator.client.luau`: clones Coin model from ReplicatedStorage.Models.Coin, spin+hover animation, fades on expiry signal

**Known issues at wrap:**
- Coins not spawning on ramp — ramp is at workspace.Map.Ramp (confirmed via screenshot). Raycast approach tried multiple ways (world-Y, local-up-vector, include filter, no filter). Coins.server.luau not visible in Studio Explorer — user couldn't find it in ServerScriptService > Scripts. Suspect Rojo sync issue or explorer navigation confusion
- Root cause of double popup was duplicate scripts in StarterPlayerScripts — fixed by user manually deleting duplicates
- Rojo maps: src/server → ServerScriptService > Scripts, src/client → StarterPlayer > StarterPlayerScripts, src/shared → ReplicatedStorage > Shared

**Coin model:** ReplicatedStorage > Models > Coin (placed manually by user in Studio)

## Session 17 -- 2026-03-31

Troll Mountain (C:\Dev\RobloxGame) — full game system build:

**Project setup:**
- Deleted old test scripts (DamagePart, DamagePartMover) — were bleeding into new Studio places
- Identified issue: single Rojo project = all scripts sync to every place opened. Fix: separate folder per game next time (e.g. C:\Dev\TrollMountain)
- Renamed src/client/init.client.luau → main.client.luau to fix Rojo ClassName conflict

**Systems built:**
- `init.server.luau`: leaderstats Coins (+1/sec passive), CoinMultiplier NumberValue per player
- `ProgressBar.client.luau`: left-side vertical bar, avatar headshot icon moves up with height, green→red gradient, max Y=5000, mild curve
- `StatsDisplay.client.luau`: top-center chips showing live $ coins and ⚡ speed, IgnoreGuiInset=true
- `LoadingScreen.client.luau`: full-screen loading screen, ContentProvider preload, skip button, fade out
- `TrollEvents.server.luau`: Slide (50c, all players sit 3s + teleport reset), Fling (250c, launches all players), SpeedBoost (50c, +10% WalkSpeed stacks), CoinMultiplier (250c, +0.1x on collected coins)
- `TrollButtons.client.luau`: Trolls + Upgrades tab buttons on right, each opens a scrollable popup menu with items
- `Coins.server.luau`: invisible hitbox Parts in workspace.Coins, distance-based collection (5 studs), raycasts to ramp surface, 20 coins max, fades on expiry
- `CoinAnimator.client.luau`: client-owned T1COIN visuals in workspace.CoinVisuals (avoids server override), PivotTo spin+bob, +$5 popup on collect

**Known issue at wrap:**
- ProgressBar not appearing in game — likely a Rojo sync issue (user manually removed old scripts from Studio, may need reconnect + re-sync to pick up new scripts properly)
- Coin system rebuilt 3 times trying to fix animation/collection bugs; final architecture uses server hitbox + client visual to avoid server overriding client animation

**Ramp dimensions:** 100w × 4054l × 3002h (Y goes 0→3002 on ramp surface)
**Models:** T1COIN in ReplicatedStorage.Models (user places manually in Studio)

## Session 16 -- 2026-03-28

Survival game final session + Roblox continued:

**Survival (survival.html) — abyss world ending:**
- Both void world outcomes (portal return OR guardian contact) now send player to the abyss instead of surface
- Abyss = caveLevel 5: pitch black looping world (2 chunks), player wanders freely for 30s
- After 30s: 3s fade to black → 3s game over fade in, buttons locked until halfway through
- Survival moved from drafts to published; thumbnail = cheerful daytime scene (blue sky, trees, player with sword) — horror is a surprise

**Roblox / Rojo (C:\Dev\RobloxGame):**
- DamagePart script: Touched → TakeDamage(10) with 0.1s debounce per player
- DamagePartMover script: TweenService side-to-side movement (Sine easing, 15 studs, 2s sweep)
- Both working with live Rojo sync

## Session 15 -- 2026-03-28

Roblox Studio + Rojo integration setup:

- Installed Rojo VS Code extension (evaera.vscode-rojo v2.1.2) via `code --install-extension`
- Rojo binary installed via Aftman (managed by VS Code extension), downgraded to v7.6.1 to match Studio plugin
- Studio plugin: Rojo 7.6.1 by Rojo Foundation (installed manually via Toolbox)
- Project created at C:\Dev\RobloxGame with src/server, src/client, src/shared structure
- Fixed default.project.json: services use $ignoreUnknownInstances + nested folder paths to avoid duplicate service creation
- Gotcha: Rojo maps src/server into a "Scripts" folder inside ServerScriptService (not directly)
- Gotcha: must be in Edit mode (not Play mode) for Rojo to sync
- Gotcha: Studio requires script injection permission granted in Plugin Manager
- Test scripts: DamagePart (Touched damage + debounce) + DamagePartMover (TweenService side-to-side movement) — both working
- Claude can't see Studio Explorer directly; workarounds: screenshots, named path descriptions, or WaitForChild by name

## Session 14 -- 2026-03-24

Survival game (survival.html) — goblin camp visual overhaul + corrupt guardian chase system:

**Goblin camp overhaul (Round 1):**
  - Tents upgraded to PS=4 (bigger sprites)
  - Camps spread wider: surface WALL_R=158, cave1 WALL_R=132
  - Log palisade walls via `_genWall()`: 28 posts in a ring, 3 entrance gaps, precomputed segment pairs
  - `_drawWallPost`, `_drawCampWall`, `_drawCampPath`, `_drawSkullPole`, `_drawWeaponRack`, `_drawCampTorch` draw helpers added
  - Dirt paths from center to each entrance + first 3 tents
  - 2–4 skull poles + 1 weapon rack per camp as extras
  - 6 camp torches (2 flanking each entrance gap)
  - Camp campfires and torches now emit light during night overlay (`drawLightSources` calls in `drawNightOverlay`)

**Corrupt guardian chase system (Round 2):**
  - `drawAbyssCorrupt()` redesigned: humanoid shape (matches void altar guardian) with floating drift, wide pulsing dark aura, and orbiting halo rings
  - Void altar guardian (`_drawAltarGuardian`) now supports `altarGuardianChasing` state:
    - Proximity trigger: walking within 120px starts chase
    - Moves toward player at 140px/s; arms flail, eyes glow brighter, chase aura rings spin
    - Contact damage: 12 dmg, 1.0s cooldown
    - Auto-exits void world when player reaches return portal during chase
  - `updateAltarGuardian(dt, now)` function handles all chase movement/damage/exit logic
  - E-key void portal exit also triggers red tint if guardian was chasing
  - `abyssRedTint`: permanent subtle red overlay on surface (caveLevel 0 only, ~7% alpha with slow breathing pulse) — like the sun turned blood-red
  - New state vars: `altarGuardianChasing`, `_guardianCX/CY`, `abyssRedTint` — all reset in `restartGame()`

**Also discussed:**
  - Rojo integration for Roblox Studio (potential future project): Rojo syncs local .luau files into Studio in real-time; Claude handles scripting, user handles 3D world building

## Session 13 -- 2026-03-23

Survival game (survival.html) — goblin camp overhaul, portal/path fixes, water breathing:

**Glitch effect fixes:**
  - Clears instantly when it turns day (was lingering via decay timer)
  - Clears instantly when player moves > 500px from corrupt figure (was decaying slowly)

**Portal / void path:**
  - Players can now walk through all portals (void entrances, hell portal, corrupt return) — pushOut removed
  - `enforceVoidPathCollision` no longer called; player moves freely in void world
  - Void world winding path changed from filled rect corridors to a smooth 3-pass glow bezier curve (visual guide only)

**Goblin camp overhaul:**
  - Tents ~50% bigger (PS 2→3), with stripe accents
  - 5–7 normal/archer goblins + 1–2 brutes per spawn (was 3–4 + 1)
  - 2–3 chests per camp (was 1–2); all chests have campId
  - Archer towers (2 per camp): tall wooden posts + platform + railing + goblin archer on top; hatchet-only (6 hits), archer drops as alerted mob on collapse
  - Chest lock: yellow ✦ rune floats above locked chests until all camp goblins dead; gold particle burst on clear
  - Bone campfires emit warm radial light glow with flicker

**Water breathing system:**
  - 22s air supply; 6 bubble indicators above player head while submerged, drain as air depletes
  - Thin blue/red air bar below bubbles when not full
  - Drowning: 2 HP every 1.8s when out of air
  - Air refills in ~5s when out of water
  - Resets on restartGame

**Also (earlier in session, carried from Session 12 context):**
  - Cave Y-sort: `drawCaveYSorted()` combines rocks + stalagmites by Y for cave1/cave2
  - Fuel priority: coal consumed before sticks in all smelting recipes

## Session 12 -- 2026-03-23

Survival game (survival.html) — layering, fuel, and UI polish:

**Cave Y-sort:**
  - `drawCaveYSorted()` combines rocks + stalagmites into a single Y-sorted draw pass for cave1/cave2
  - Helper functions `_drawRockBase`, `_drawRockTop`, `_drawStagAt` used by combined function
  - Fixes stalagmites incorrectly overlaying ores/rocks based on screen position
  - Surface and hell (caveLevel 0/3) still use original separate draw paths

**Fuel priority:**
  - Coal now consumed before sticks in all smelting recipes (cooked chicken, bronze ingot, iron ingot)
  - Sticks only used if no coal available

**Lake on map:**
  - Confirmed already correctly gated by `lakeSeen` flag — no change needed

**Other (from earlier in session, carried over):**
  - 10 monoliths per level (30 total across surface/floor1/floor2)
  - 8 goblin camps total (4 surface + 4 cave1); altar scroll guaranteed in every camp
  - Item stacking bug fixed: items with `count: undefined` now normalized via `normalizeItem()`
  - Item count shown in PLACE/FOOD equip slots (torches, saplings, chicken, etc.)
  - Y-sorted draw order for player + mobs (top to bottom)
  - Corrupt Pendant trinket: magma zombie 15% drop, immunity to glitch effects and lava damage
  - More lava patches in hell (2–4 per chunk)
  - Damage indicator above player when taking damage (white "-N" floating numbers)
  - Green pixelated main menu (horror theming hidden behind "Start Setup" toggle)
  - Start Setup button on menu re-enables 3 mine entrances + starting gear circle

## Session 11 -- 2026-03-22

Survival game (survival.html) — trinkets, crits, void temple, main menu:

**Trinket system:**
  - 3 trinket equip slots in col 1 of inventory (below tools)
  - 6 trinkets, one per goblin camp (3 surface + 3 cave1, shuffled each game)
  - Bone Necklace (+20% dmg), Gold Charm (+15% crit), Hermes Boots (+20% spd)
  - Dragon Scale Cloak (+20% max HP, 75→90), Anklet of Earth (+25% tool dmg), Steel Shoulders (+15% def)
  - Trinket slots draw with gold border/label, bonus shown below label
  - `getTrinketBonuses()` + `getMaxPlayerHp()` used across all damage/regen/movement/HP bar

**Critical hits + damage numbers:**
  - 15% base crit chance (+critBonus from Gold Charm), 1.5x damage on crit
  - Floating damage numbers above hit targets: red small (normal), gold large "X!" (crit)
  - Applied to all sword types incl. void_sword; crits also affect corrupt creatures

**Void world temple:**
  - Winding S-curve pixel path (VOID_PATH rects) from spawn (5280, 4050) to altar
  - 6-step black temple with red neon outlines, rune lines on each step
  - Corrupt guardian at VOID_ALTAR_X/Y: dark humanoid with red eyes, 18dmg contact (1.2s cooldown)
  - enforceVoidPathCollision: axis-separated sliding, player locked to walkable path rects

**Miner zombies on surface:**
  - After entering floor 2, ~30% chance to spawn miner zombie instead of normal (cap 4)
  - `spawnSurfaceMiner()` function added

**Main menu redesign:**
  - Night sky gradient, 120 twinkling stars, blood moon (top-right)
  - Black tree silhouettes, campfire with flicker, zombie silhouette
  - Red dripping "SURVIVAL" title with blood drip animation

**Other:**
  - Goblin defPct now includes trinket defense bonus
  - HP bar shows "X/Y" (current/max), max HP grows with dragon cloak
  - `_altarGuardianLastDmg` and `damageNumbers` reset on restartGame

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
