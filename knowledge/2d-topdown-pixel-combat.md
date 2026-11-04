# 2DTopDownPixelCombat - course map

Working title since 2026-11-04: **Outer Lands** (the repo keeps its name for now).

**Source:** the director's own project `github.com/Krulansky/2DTopDownPixelCombat`, built along the
GameDev.tv course **Unity 2D RPG: Complete Combat System** (87 lectures), finished 2026-10-29
(commit `a040944` "KURZ HOTOVY!"). Unity `2022.3.62f2`, URP 2D Renderer, new Input System.
The hero is the director's own Illidan-style demon hunter with a warglaive and green fel fire.

This file is an English copy of the director's `COURSE_NOTES.md` (Slovak, in the project repo),
plus the director's own systems built after the course and a section on the design patterns the
code uses. The project's plans live in its own `ROADMAP.md` and `HANDOVER.md`. General lessons
belong in `GAMEDEVNOTES.md` in this repo.

---

## Architecture

- **`Singleton<T>`** (`Scripts/SceneManagement/Singleton.cs`) - base for things that exist once.
  A duplicate destroys itself in `Awake`. Only root objects get `DontDestroyOnLoad`; children
  travel with their parent. Careful: on a duplicate, `OnDisable` runs before the rest of
  `Awake` finishes, so use `?.` in `OnDisable`.
- **Singletons:** `PlayerController`, `PlayerHealth`, `Stamina`, `ActiveWeapon`, `ActiveInventory`,
  `SceneManagement`, `UIFade`, `CameraController`, `ScreenShakeManager`, `EconomyManager`, `BaseSingleton`.
- **Every scene has its own copies** of the `Player`, `UI_Canvas`, `Managers` and `Cameras`
  prefabs, so any scene can be started on its own. On a scene change the duplicates destroy
  themselves.
- **Interfaces:** `IWeapon` (Attack, GetWeaponInfo) for weapons, `IEnemy` (Attack) for enemy types.
- **Data:** `WeaponInfo` (ScriptableObject, *Create > New Weapon*): prefab, cooldown, damage, range.

## Player (`Scripts/Player`)

| Script | What it does |
|---|---|
| `PlayerController` | Movement (`rb.MovePosition` in FixedUpdate), facing the mouse, dash (costs 1 stamina, fel fire trail). |
| `PlayerHealth` | HP, `Health Slider`, knockback + flash + screen shake on hit, invulnerability for `damageRecoveryTime`, death -> `Death` animation -> after 2 s loads **Town**. |
| `Stamina` | 3 orbs in `Stamina Container`, refill every 3 s, full stamina after death. |
| `ActiveWeapon` | Holds the current weapon, cooldown between attacks, holding the button repeats the attack. |
| `DamageSource` | On the player's `WeaponCollider` - deals damage from the current weapon's `WeaponInfo`. |
| `MagicLaser` | The staff's laser, grows to `weaponRange`, stopped by `Indestructible`. |
| `Player Controls.cs` | **Generated** Input System class (never edit by hand). |

## Inventory and weapons

- `ActiveInventory` - keys 1-5 switch slots and spawn the weapon prefab under `ActiveWeapon`.
  `EquipStartingWeapon` is called from `PlayerController.Start`.
- `InventorySlot` - each UI slot has its own `WeaponInfo` (empty slot = no weapon).
- `Glaive` - the swing (turns `WeaponCollider` on, animation events flip the slash and turn it
  off). `OnDestroy` turns the collider off (fixes "thorns" after switching weapons).
- `Bow` - fires an `Arrow` with `Projectile`, range from `WeaponInfo`.
- `Staff` - an animation event spawns `MagicLaser`.
- `Projectile` - shared by arrows and enemy bullets; `isEnemyProjectile` decides whom it damages.
  `Destructible` reads `IsEnemyProjectile` (enemy bullets do not break bushes).
- `GlaiveHitSparks`, `MouseFollow` - the director's own additions (sparks at the hit point,
  turning towards the mouse).

## Enemies (`Scripts/Enemies`)

- `EnemyAI` - state machine (`Roaming` / `Attacking`), attacks through `IEnemy` when the player
  is closer than `attackRange`.
- `EnemyPathfinding` - movement and sprite facing.
- `EnemyHealth` - HP, knockback, flash, death VFX, `PickUpSpawner.DropItems()`.
- Types: **Slime** (melee, attackRange 0), **Grape** (`Grape` + `GrapeProjectile` in an arc
  along an AnimationCurve + `GrapeLandSplatter`), **Ghost** (`Shooter` - bursts, spread,
  stagger, oscillate).

## World and helpers (`Scripts/Misc`)

- `Destructible` (bushes) - broken by the player's weapon or projectile, drops loot.
- `Indestructible` - stops projectiles and the laser (trees, walls).
- `PickUp` + `PickUpSpawner` - loot (gold, health, stamina, **FelFire**) pops out along a curve
  and is pulled to the player. FelFire is only a `Debug.Log` so far (no rage yet).
- `EconomyManager` - gold in `Gold Amount Text` (format 000).
- `TransparentDetection` - trees/canopy turn see-through when the player is behind them.
- `Flash`, `Knockback`, `SpriteFade`, `SelfDestroy`, `RandomIdleAnimation`, `Parallax`,
  `ScreenShakeManager` (Cinemachine Impulse).
- Cursor: **Project Settings > Player > Default Cursor** (`Sprites/UI/cursor.png`, Texture Type
  *Cursor*, hotspot 16,16). The course's UI cursor (`CursorManager` + *Custom Cursor* object)
  was removed on 2026-10-29: it doubled up with the hardware cursor and would lag behind the
  mouse in a web build.

## Scene transitions (`Scripts/SceneManagement`)

- `AreaExit` - trigger: stores `sceneTransitionName`, fades to black, after 1 s
  `LoadScene(sceneToLoad)`.
- `AreaEntrance` - in the new scene: if its `transitionName` matches, moves the player to
  itself, sets the camera, fades to clear.
- Rule: an exit's `sceneTransitionName` = the entrance's `transitionName` **in the target
  scene**. Entrance names must be **unique** in a scene, and the target scene must be in
  **Build Settings**.
- Prefabs: `AreaExit` (base), `AreaExit Variant`, `AreaExit_DarkPortal` (variant with a portal
  and fel VFX).

## Scenes (Build Settings)

`Town` (0, start and respawn after death), `Scene_1`, `Scene_2`, `Scene_3`. The state of the
gates is in the project's `HANDOVER.md`.

## Known quirks

- `Shooter.OnValidate`: both lines set `stagger = true` (`if (oscillate)` and `if (!oscillate)`),
  so stagger can never be switched off in the Inspector. Probably meant `stagger = false` in the second.
- `Shooter`: with an even `projectilesPerBurst` the cone has no bullet in its centre - the Ghost's
  8 over 165° never hit a player who stands still. `projectilesPerBurst = 1` with `angleSpread > 0`
  divides by zero (`angleStep` = Infinity) and the one bullet flies along the cone's edge.
- After death Town loads, but `SceneManagement` remembers the last transition name. If it
  matches an entrance in Town, the player respawns at that gate instead of the start.
- `Player Controls.cs` lives in `Scripts/Player`, not next to its `.inputactions`. The importer's
  `wrapperCodePath` points there, so regenerating writes the same file (checked 2026-11-01 when
  the Abilities map was added).

---

## Own systems after the course (2026-10-31 to 2026-11-01)

Design and status: the project's `ROADMAP.md` ("Rage + Fel a Demon forma"). All new scripts are
added beside the course code, not inside it.

| Script | On | What it does |
|---|---|---|
| `Fel` | Player | Fel 0-100, static event `OnFelChanged`, `AddFel`, `TrySpendFel`. A FelFire Globe adds 10. |
| `Rage` | Player | Rage 0-100 (`float`), static event `OnRageChanged`. Gains: weapon hit +3 (every `DamageSource` carrier - glaive, arrow, laser), kill +5, damage taken +10. No gain while a Rage ability runs, half gain above 50, decay -2/s after 5 s out of combat. |
| `Stamina` | Player | Rewritten as a `float` bar: continuous regen (1 dash / 3 s), `CanDash`, static event `OnStaminaChanged`. |
| `FelBar`, `RageBar`, `StaminaBar` | UI sliders | Listen to the event, call `SmoothBar.SetValue`. Health still uses the course path (`GameObject.Find`). |
| `SmoothBar` | UI sliders | Eased fill (exponential approach in `Update`), lagging ghost slider, health-only flinch and danger colours. |
| `FelShield` | Player | Key 4 (Abilities map): costs 50 Fel, 5 s, shows `Shield Visual`, 3 absorb charges via `TryAbsorbHit()` called from `PlayerHealth.TakeDamage`. An absorbed hit costs no HP, gives no Rage, no knockback, but still starts the invulnerability window. |
| `AuraDamage` | Shield Visual, Glaive Tornado prefab | While enabled: hits enemies in a radius on entry, then per enemy every `hitInterval` (dictionary of next-hit times, `OverlapCircleNonAlloc`); breaks `Destructible`s. |
| `RageHold` + `IRageWeapon` | Player; Glaive, Bow | Hold RMB (Combat > RageAbility) with Rage >= 50 to run the active weapon's Rage ability, draining 10 Rage/s. Switching weapon ends it. |
| Glaive tornado | `Glaive` + `Glaive Tornado` prefab (`AuraDamage` + `Spin`) | Spawned under the player while RMB is held; the held glaive hides and stops swinging. |
| Bow Rapid Fire | `Bow` | Coroutine fires an arrow every 0.15 s while RMB is held; left click is ignored meanwhile. |
| `RageFrame` | UI image behind the slots | Shown when Rage >= 50 and the held weapon is an `IRageWeapon`; follows `ActiveInventory.OnActiveSlotChanged`. Look still being tuned. |
| `EnemyPathfinding.Daze` | enemies | Speed multiplier for a duration; a `[ContextMenu]` test stays until the Demon Form nova uses it. |

---

## Design patterns already in this code (for the patterns course)

Checked against the scripts on 2026-10-29. "Close to" = the idea is there, not the textbook form.

| Pattern | Where | Notes |
|---|---|---|
| Singleton | `Singleton<T>` and its 11 users | Generic base class with duplicate destruction - more robust than LuaLander's `Instance = this`. |
| State | `EnemyAI` (`enum State` + `switch`) | The simplest form. The pattern's class-per-state version pays off once enemies get more states (Riddle of Steel's guards and bosses). |
| Strategy | `IWeapon`, `IEnemy`, `IRageWeapon` | Each weapon/enemy type plugs its own `Attack()` behind one interface; `RageHold` asks `as IRageWeapon` and runs whatever ability the held weapon has. |
| Component / composition | `AuraDamage`, `Spin` | One damage-in-a-radius component serves the FelFire Shield, the glaive tornado and later the Demon Form's claws. |
| Type Object / data-driven | `WeaponInfo` ScriptableObject | Numbers live in assets, not in code. |
| Factory (close to) | `PickUpSpawner.DropItems()` | Decides what to create; callers do not. |
| Observer (added 2026-10-31) | `Fel.OnFelChanged`, `Rage.OnRageChanged`, `Stamina.OnStaminaChanged`, `ActiveInventory.OnActiveSlotChanged` | Static C# events: the Player is destroyed on death and recreated in Town while the UI survives, so bars subscribe once and hear every new Player. Each source broadcasts its starting value in `Start`. The course code itself still calls scripts directly. |
| **Object Pool - missing** | `Projectile`, death VFX | Created with `Instantiate`, removed with `Destroy`. Fine at this size; Riddle of Steel's crowds of enemies are where pooling matters. |
