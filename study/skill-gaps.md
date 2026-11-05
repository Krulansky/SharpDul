# Skill gaps (bucket S)

What the director is working to understand better, with the evidence for each item. Fed from the
course logs; used to choose quiz topics and Lab exercises.

| Topic | Evidence | Status |
|---|---|---|
| Interfaces vs base classes | `Bow` had the method but not `IRageWeapon` in its declaration (2026-11-01) | seen once |
| Who owns a behaviour (caller vs. receiver decides the reaction to a hit) | Challenge 1.5, question 5: "neviem" (2026-11-04) | working on it |
| Law of Demeter: reading a chain like `player.gun.ammo.roundsLeft` as "reaching through objects" | Challenge 1.7, attempt 1: did not know what a chain of dots means (2026-11-05) | working on it |
| Return types: `return ammo;` gives an `Ammo` object, not the `int` the method promises; an object vs a call on it | Challenge 1.7, attempt 2 (2026-11-05); the reverse case is `AddListener(ResetHealth)` without `()` (lesson Delegates/Actions/Events) | working on it |
| Cached values going stale (cache invalidation) | `ActiveWeapon` kept the old weapon's cooldown; `SceneManagement` keeps the transition name after death | Design Patterns course, lesson 2 |

Quiz results are not here yet: they live on the iPhone. A backup export (Backup > Export) sent
to the agent would show which questions keep falling back to box 1.
