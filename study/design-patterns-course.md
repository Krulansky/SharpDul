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
2. Step 2 - design in words: which components, who decides the reaction, how Enemy finds its
   target. No code yet.

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
- Lab idea: a "stale cache" toggle in the Combat Lab (cache `moveSpeed` in Start vs read it live).
