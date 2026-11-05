# Course log: Design Patterns (GameDev.tv, "Get Good at Unity" bundle)

Started 2026-11-04. See `study/README.md` for the buckets.

## Lesson 1 - Ten coding commandments

- **N** Written up in `GAMEDEVNOTES.md` > *Ten coding commandments* (2026-11-04).
- **P** Outer Lands `CLAUDE.md` > *Code style* + open refactor candidates (branch
  `claude/gamedev-coach-app-eu5x6k`, to merge).
- **Q** Quiz "which rule does this code break?" - director: later.

## Lesson 2 - Caching, cache invalidation, naming

Slides: Width/Height/Area (cached `area` goes stale when `DoubleWidthAndHeight()` forgets
it); signs of a cache: boolean flags, `GetComponent` stored in `Awake`, having to "remember" to
update something, updating variables on callbacks. Naming: WTFs per minute, classes are nouns,
methods are verbs, avoid Manager/Controller/Processor, be consistent (Get vs Fetch vs Retrieve).

From the comments (Brian Trotter, TA):
- Cache **references** (`GetComponent<Health>()`), never the **data** in them (current HP).
- Caching components on your own GameObject is safe; on other GameObjects it can go
  null when they are destroyed.
- `OnTriggerExit2D` does not fire when the object is destroyed inside the trigger: a list
  filled by Enter/Exit must also drop targets on their death event.
- Immutable records: undo a bad entry with a new entry, never by editing the old one (parked).

Sorted:
- **P** Outer Lands - stale caches already in the code:
  `PlayerController.startingMoveSpeed` is cached in `Start`, so changing `moveSpeed` in the
  Inspector during Play is undone by the next dash. `SceneManagement.sceneTransitionName` is never
  cleared on death (the known respawn quirk). The class name `SceneManagement` also collides with
  Unity's `UnityEngine.SceneManagement` namespace. Added to the agent's refactor candidates.
- **P** Outer Lands - done right already: `AuraDamage` checks the area every frame with
  `OverlapCircleNonAlloc` instead of keeping an Enter/Exit list, so it cannot hold a destroyed
  enemy. Bars get values through events instead of caching another script's numbers.
- **S** Cache invalidation added to `study/skill-gaps.md`.
- **N** One paragraph added to `GAMEDEVNOTES.md` (what to cache).
- **-** Immutable records / event sourcing: parked (no project needs it now).

## Lesson 1.5 - Sources of spaghetti code

Slides: static and global state (bugs, poor unit testability, hard to follow, multithreading,
"and now you need two..."). The example is `public static float mana` changed by `Update`,
`UseAbility` and `UseManaPotion` from anywhere. High cohesion / loose coupling (two apps that
talk through one link vs. lines crossing everywhere). Challenge: "Why are these classes bad?"
(`Character` with animator + audio + health; `Enemy` that `FindObjectOfType<Character>()`
and calls `KnockBack()`, `Shout()`, `TakeDamage()`).

- **Challenge:** the director rewrites the two classes, step by step. The agent guides and does
  not hand over a solution. Progress is kept below.
- **P** Outer Lands already splits what `Character` mixes: `Knockback`, `Flash` and
  `PlayerHealth` are separate components. Static events and singletons = this lesson's
  "global state" (see `CLAUDE.md` rule 6 caveat).
- **Q** The challenge itself is a good Build Lab puzzle later ("split Character into components").

Challenge progress:
1. (2026-11-04) Step 1 - the director lists what is wrong before anything is rewritten.
   Done. Got: 3 jobs; noticed Character never acts on its own. Missed: Enemy knows 3 method
   names and their order (not just the type); `FindObjectOfType` with two players returns an
   arbitrary one, not an error; magic number / string trigger. Unsure who should decide the
   reaction to a hit (-> skill gap: who owns behaviour).
2. Step 2 - design in words. Answered partly: listed Unity components (Animator,
   AudioSource) instead of own scripts, but felt TakeDamage belongs in its own class (right).
   Parameters: guessed the reactions, not the hit data (damage, source). Target lookup: did
   not remember. The instructor's solution: `IAttackable.TakeHit()` (Character reacts to the hit
   itself) + `Attack(IAttackable target)` (the target is passed in). It is a toy example: it
   still has 10 and the "KnockBack" string.
3. Next: wait for the rest of the instructor's lesson, then compare with Outer Lands
   (`PlayerHealth.TakeDamage(int, Transform)`, `Projectile.OnTriggerEnter2D`).

## Lesson 1.6 - Composition over inheritance

Slides: Animal > Mammal (MakeMilk) / Reptile (LayEggs) breaks on the Platypus, which needs both.
With components (`MilkMakingComponent`, `EggLayingComponent`) each animal picks what it has.
"Where does this go wrong?": `Character` (locomotion, attack, health) > `Player` / `Enemy`.

- **P** Outer Lands is already built this way: `Knockback` and `Flash` sit on the player and the
  enemies, `AuraDamage` serves three abilities, and weapons and enemies plug in through the
  `IWeapon` / `IEnemy` interfaces. The one inheritance is `Singleton<T>`. Nothing new to propose.
- **P** Riddle of Steel (paused): when its guards and bosses are designed, think in components
  (move, attack, health, AI) instead of an enemy class tree.
- **N** Already covered in `GAMEDEVNOTES.md` (rule 9 and "Composition beat a bespoke script").
- **Q** Backlog below.
- Question to the director (2026-11-05): where does `Character` > `Player` / `Enemy` break in
  Outer Lands? Answer: "Health? the player has it, and the enemy learns it hit when it drops?"
  That is a shared part, not a break, and it mixes in lesson 1.5 (the attacker does not need to
  know). Explained: the break is something with only part of `Character`, like a bush (health,
  no move, no attack) or a turret (attack, no move).

## Lesson 1.7 - Law (guideline) of Demeter

Slides: `enemy.GetCurrentTarget().GetHealthComponent().DoDamage()` vs
`enemy.DoDamageToCurrentTarget()`. Challenge "What's wrong with this picture?": `PlayerUI` and
`GunUI` each `FindGameObjectWithTag("Player").GetComponent<Player>()`, then read
`player.health` and `player.gun.ammo.roundsLeft`; `Player`, `Gun` and `Ammo` expose public fields.

- **Challenge:** the director finds the problem and fixes it. The agent gives hints only, with
  two attempts before the instructor's solution is posted. Progress is kept below.
- **P** Outer Lands: `(currentActiveWeapon as IWeapon).GetWeaponInfo().weaponDamage` in
  `DamageSource` is the same chain (already a refactor candidate in its `CLAUDE.md`).

Challenge progress:
1. (2026-11-05) Attempt 1 - hints given: count the dots, what GunUI must know, what is
   duplicated, who may change the public fields.
   Result: found Player and Ammo (missed that Gun counts too); wanted "someone who shouts the
   info to the UI" (Observer instinct, a later lesson); right that the public fields are not
   needed; mixed up GunUI (ammo) with health. Said the questions were confusing and did not
   know what "a chain of dots" meant. Lesson for the agent: abstract questions do not work,
   so show the line and give blanks.
2. Attempt 2 - fill-in skeleton: private `roundsLeft`, `GetRoundsLeft()` passed up through
   Ammo -> Gun -> Player, GunUI calls one method.
   Result: `ammo`, `gun`, `RedrawUI()`. Picked the right neighbour each time, but returned the
   object instead of calling its method (`ammo` vs `ammo.GetRoundsLeft()`), and called the UI's
   own method on the player. Shown the full answer; waiting for the instructor's solution.
3. Instructor's solution: `GunUI.RedrawUI(Gun gun)` gets the gun as a parameter from
   `PlayerUI` (`gunUI.RedrawUI(player.gun)`), so only one `FindGameObjectWithTag` is left;
   `Gun.GetRoundsLeft()` returns `ammo.roundsLeft`. Ours went through `Player.GetRoundsLeft()`
   and made `roundsLeft` private. The instructor's version also removes the duplicate search;
   ours hides more of the data. Comments: make fields private + `[SerializeField]`; LINQ and
   fluent APIs are the deliberate exception to "no chains".

## Module 2, lesson 1 - Observer pattern

Slides: "Rampage Mode" (a power-up makes the player invincible, enemies run away, health stops
taking damage, UI tints red). The naive version makes Rampage call every one of them, so it is
coupled to all of them and changes whenever any of them changes. "Flip It!": turn the arrows
around, so Rampage UI, Health and every Enemy AI depend on Rampage and Rampage knows none of
them. UML of the pattern: Subject (observerCollection, register/unregister/notify) and Observer
(update) with concrete observers. "Which principles does this improve?": loose coupling (8),
cohesion (7), one job (3). The director brought the instructor's answer; no challenge this time.

- **N** UML -> C# event mapping added to `GAMEDEVNOTES.md`.
- **Q** Backlog: read the UML (which arrow means what) and map it to `event` / `+=` / `-=` /
  `Invoke`.

- **P** Outer Lands (director, 2026-11-05): Demon Form gets a fear effect. When the demon
  spawns, enemies flee for 2 s; bosses and highlords are immune; name to be found (not
  "Rampage"). Written in its `ROADMAP.md` > Demon Form. `DemonForm.OnDemonFormChanged` already
  exists, so enemies only need to subscribe.

## Module 2, lesson 2 - Observers with UnityEvents

The instructor's sample project (Unity 2021.1.22f1): `Level` has a `UnityEvent` "On Level Up"
wired in the Inspector to `ParticleSystem.Play` and, as the task, to `Health.ResetHealth()`.
Comments: Simon thought Level still "calls" ResetHealth (tight coupling); Brian: the scripts
know nothing about each other in code, the link lives in the Inspector, so it is loose coupling.

- **N** UnityEvent vs C# event added to `GAMEDEVNOTES.md`.
- **P** Outer Lands uses C# events (code-checked, needed for runtime-spawned enemies). A
  UnityEvent fits one-off scene wiring (a trigger plays a sound, opens a gate).
- **Q** Backlog: "you rename `ResetHealth` to `RefillHealth` - what happens with a C# event,
  and what with a UnityEvent?" (Medium)
- Sample scripts read (2026-11-05, start of the lesson, before the UnityEvent is added):
  `Level` +10 XP every 0.2 s, level = XP / 200, so a level-up every 4 s; `Health` drains 2/s
  from 100; `Debugger` logs every second. Findings: `HealthDrain` loops `while (currentHealth > 0)`,
  so once health reaches 0 the coroutine ends and `ResetHealth()` no longer restarts the drain (a
  stale-state trap from the caching lesson). With these numbers health only falls by 8 between
  level-ups, so it never shows. `Debugger` polls every second, which is the opposite of an observer.
- **-** The director asked whether a very active commenter really understands the topic. Not
  judged (the comments were not sent); judge the claims, not the person.

## Outside the course

- **P** Outer Lands issue #1 (sword slash VFX, 5 tips): planned in its `ROADMAP.md` as the
  **Scythe** right after Elevation (director, 2026-11-04). It is a learning project and the
  first practical step towards the Shaders/VFX study phase.

## Quiz and Lab backlog (bucket Q)

- Area example: `SetWidth` updates `area`, the new `DoubleWidthAndHeight` forgets - what does
  `GetArea()` return? (Easy)
- `startingMoveSpeed`: you raise `moveSpeed` in the Inspector during Play, then dash - what speed
  do you walk at after the dash? (Medium, from `PlayerController.cs`)
- `ActiveWeapon.NewWeapon`: why must the new weapon's cooldown be read before anything else?
  (Medium)
- Enter/Exit target list + an enemy destroyed inside the trigger - what is left in the list?
  (Medium)
- Name review: `Roaming()` / `Attacking()` are not verbs; `knockBackFloat`; `SceneManagement`
  vs the Unity namespace. (Easy, "which name is better?")
- Platypus: with Mammal/Reptile classes, why can't it exist? Which components does it get? (Easy)
- Outer Lands: a bush has health but never moves - which components does it need, and
  what would a `Character` base class force on it? (Easy)
- Health drain: health reaches 0, then `ResetHealth()` runs - does the drain continue? (Medium,
  sample `Health.cs`)
- `return ammo;` in a method that returns `int` - what does the compiler say, and what is the fix?
  (Medium, from challenge 1.7)
- Law of Demeter: which of three lines reaches through objects (`player.gun.ammo.roundsLeft`,
  `gun.GetRoundsLeft()`, `transform.position.x`)? (Easy - the last one is a value, fine)
- UML: which part of the Observer diagram is `+=` / `-=` / `?.Invoke()` / the subscribed
  method? (Easy, with `Stamina` + `StaminaBar` as the code)
- Rampage: why does the naive version change every time Health or the UI changes? (Easy)
- Lab idea: a "stale cache" toggle in the Combat Lab (cache `moveSpeed` in Start vs read it live).
