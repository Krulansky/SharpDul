# Game design notes - the travelling notebook

> **Home since 2026-10-26: the SharpDul repo.** Moved here from FerryHeist (last version there:
> commit `6213474`) so the notebook lives in the one place that grows with every project and
> feeds SharpDul's quizzes. Projects link here instead of keeping a copy.

**This file is not about any one game.** It holds what we learn about game design and game feel
in general, so every following project can use it. We are a learning organisation:
when something is understood, or tried and found to work, it gets a short entry here.

Rules for this file:

- One entry per idea. Say **what it is**, **why it works**, and **how we used it**.
- Keep the source, so it can be looked up again.
- If we tried it and it did *not* work, say so. A failed experiment is worth as much.

---

## 1. Diminishing returns: the armour formula

**Source:** Candlesan, *The Simple Math Hiding in Your Favorite Games*
([short](https://www.youtube.com/shorts/IzHAjV8YEW4)) and
*How to tune the Armor formula for YOUR game* ([part 2](https://www.youtube.com/watch?v=HecTqtkoWyg)),
seen 2026-10-01. Used by League of Legends, Warcraft III and World of Warcraft.

### The formula

```
mitigation % = Armor / (Armor + K)
```

`K` is a single number the designer picks. It is the amount of armour that gives **exactly
50%** mitigation.

### What it does

With `K = 100`:

| Armour | Mitigation | Gain over the row above | Hits to kill |
|---|---|---|---|
| 0 | 0% | - | 10 |
| 100 | 50% | +50 | 20 |
| 200 | 67% | +17 | 30 |
| 300 | 75% | +8 | 40 |
| 400 | 80% | +5 | 50 |
| 500 | 83% | +3 | 60 |
| 1000 | 91% | +1 | 110 |

### The insight worth keeping

The *percentage* shows diminishing returns - each 100 armour is worth less than the last -
but **hits to kill grows in a perfectly straight line**: +10 every time, for ever. So:

- The player feels the classic "more armour is worth less" curve, which keeps the numbers
  readable and stops anyone reaching 100% immunity.
- The designer still gets a clean linear knob: **effective health is directly proportional to
  the stat**. Balance stays easy to reason about no matter how large the numbers get.
- It can never divide by zero and never reaches 100%. Free safety.

### How to pick K (the four steps from part 2)

1. **Decide the goal.** What mitigation should a fully equipped player have? e.g. 25%.
2. **Decide what gear gives.** Simple, consistent numbers per slot per level, e.g. 4 each for
   chest, helmet and legs.
3. **Add it up.** A full set at the target level, e.g. 28 armour.
4. **Solve for K.** From `0.25 = 28 / (28 + K)` -> `K = 84`.

Notes: Warcraft III uses a small `K` (about 17) because unit armour values are small; World of
Warcraft scales `K` with the *attacker's* level, so a player's mitigation stays about the same
as they level up instead of inflating. The same formula converts any raw growing stat into a
meaningful percentage (Genshin Impact uses it for Elemental Mastery). Mixing is allowed:
some sources flat, some percentage-based - that is where interesting build choices live.

### Where we used it

Not yet in a shipped mechanic. **Candidates:** hull armour upgrades, cargo-securing upgrades
(the stat that fights sliding), and engine upgrades - anything the player buys repeatedly and
where we do not want a hard cap or a runaway.

---

## 2. Diminishing returns on *repeats*: the salvage rule

**Ours** (FerryHeist, 2026-10-01). A different shape with the same intent, so do not confuse
the two. The formula above is about **how much of a stat you have**. This one is about
**how often you do the same thing in a row**.

```
value = base * fraction ^ (how many of this kind were taken in a row before)
```

With `base = 20%` and `fraction = 0.5`, a run of the same kind pays **20, 10, 5, 2.5...**, and
taking a *different* kind clears the counter.

| What the player does | Total |
|---|---|
| wood, wood, wood | 20 + 10 + 5 = **35** |
| wood, metal, wood | 20 + 20 + 20 = **60** |

**Why it works:** the player is never punished for taking something, only rewarded for
**variety**. It turns a pickup into a routing puzzle ("which piece do I take first?") without
any extra UI, and the numbers stay obvious in the head. It is also self-balancing: hoovering
up one kind cannot trivialise the level.

**Where we used it:** FerryHeist, floating salvage (planks and metal sheet) that repairs the
hull mid-crossing.

**Open:** whether the counter should also decay over time, so wood ... (a long while) ... wood
is worth full value again. Untested.

---

## 3. Fantasy supports mechanics, and mechanics support fantasy

**Source:** Candlesan on *Dave the Diver*, 2026-09-29 (full notes in FerryHeist's
`DESIGN_BRIEF.md` section 14).

Design every mechanic so it also expresses what the player is pretending to be. The payoff
runs both ways: the fantasy makes a penalty feel *fair* rather than designer-imposed. Nobody
argues with running out of oxygen while diving. Test for new mechanics: **"would the person
I am pretending to be actually worry about this?"**

Related, same source:

- **Risk and reward must be the player's own choice.** Randomness decides *what is offered*;
  the player decides *how greedy to be*. If the dice decide the risk, a loss feels unfair.
- **Failure should be a playable beat, not a dead end.** Dave keeps one item when he runs out
  of air. Losing should cost something and continue, not reset.
- **Menus can be objects in the world** (Dave's phone, our captain's logbook). One frame, many
  pages: a new screen is a new page, not a new UI design.
- **Sometimes design is what you leave out.** No minimap adds exploration.

---

## 3b. Make the game for one kind of player, not "for everyone"

**Source:** Evaluz Luna (Product Designer at GDevelop), "Why Your Game Isn't 'For Everyone':
The Power of Targeted Game Design", GDevelop newsletter *The GDeveloper*, 2026-10-16. The
email carries only the first half; the rest (two more of the four parameters) is on the
GDevelop blog - look it up and complete this entry.

**The idea.** "Anyone can enjoy it" sounds like the widest market, but it backfires:

- **Design:** trying to please every kind of player ends in a patchwork of mechanics that
  fully satisfies nobody. Good products *choose* which features matter.
- **Budget:** a small team spreads itself thin over too many features instead of polishing
  the core - and the money that should have gone to marketing is gone.
- **Marketing:** without knowing who the players are, what they want and where they gather,
  no message hits and promotion money is wasted.
- **Testing:** feedback from "everyone" pulls in every direction and skews the data.

Successful examples served one audience deeply: *Stardew Valley* (relaxed farming and
relationships), *Celeste* (hard platforming with a meaningful story), *Among Us* (social
deduction with a dash of chaos - not also a story game or a skill game). Start narrow, in an
underserved niche; widen only when the team and budget grow.

**Defining the ideal player - four parameters (two in the email):**

1. **Preferred play style** - pick the one the game serves: *fast and intense* (reflexes,
   high stakes), *strategic and thoughtful* (planning, careful decisions), *chaotic and silly*
   (laughs, unpredictable moments), *relaxed and wholesome* (low stress), *narrative and
   immersive* (story, world). A wholesome game cannot also satisfy someone after a
   competitive rush.
2. **Session length and context** - how much time players have and where they play. The same
   person can be a high-stakes gamer at night and a short-session casual player on the commute
   by day; the game does not have to serve both.
3. and 4. - *in the full article on the GDevelop blog; not read yet.*

**How to use it.** At the start of a project, write one sentence: "This game is for a player
who likes ___, plays in sessions of ___, and ___." Test every new feature and every
playtest note against it: does it serve *that* player? Feedback from people outside the
target is still useful, but it is not a mandate.

**Where we used it:** not yet. Open question for FerryHeist (for the director): which style
is it - strategic and thoughtful (loading, balance, route and risk choices), or chaotic and
silly (cargo flying off, pirates piling into rocks)? And what session length - one crossing
is a few minutes, which suits short sessions.

---

## 4. Game feel: the small things that make one action satisfying

**Source:** Candlesan's breakdown of the harpoon in *Dave the Diver*. Nine or ten tiny touches
on a **single action**, not one big effect. The general checklist, usable anywhere:

| Moment | What to add |
|---|---|
| Aiming | A precision indicator that also shows the limits |
| Aiming | The character visibly moves with the aim |
| Aiming | The camera eases in (anticipation) |
| Firing | A recoil animation - the power is in the reaction, not the projectile |
| Hitting | Knockback on the target |
| Hitting | Particles at the exact contact point |
| Travel | A trail that implies speed (bubbles, spray) |
| Struggle | A looping animation that says effort |
| Struggle | A light continuous camera shake |
| Finishing | The camera eases back out (release) |

**Lesson:** when an action feels flat, do not make the effect bigger. Add more small, separate
responses around it.

---

## 5. "Juicing": the standard toolkit for making UI and feedback feel alive

**Sources:** mii_misan and pebbles_dev reels on juicy health bars, damage numbers and menus
(2026-10-06), on top of the harpoon breakdown in section 4. The director's words: *we will use
this technique a lot, in UI and in other games.* So this is the general recipe, not one widget.

### The principle

**A value changing and a value *being seen to change* are two different things.** Plain UI
reports the new state; juiced UI shows the **transition** - how much, how fast, how bad. The
information is identical; only one of them lands. The reels prove it by showing the same
damage twice, plain on top and juiced below.

**It is cheap.** Everything below is `lerp`, `sin`, a spring and one particle system. No
packages, no paid tools.

### The eight moves

Reach for these in order; three of them already make something feel expensive.

| Move | What it does | Rough recipe |
|---|---|---|
| **1. Ease the change** | The eye can follow it, so the size of the change registers | `lerp` to the target over ~0.3-0.8 s, ease **out** (fast start, soft landing) |
| **2. Trailing ghost** | Shows **what was just lost** as a separate band behind the value | A second image at the old value, following ~0.4 s behind |
| **3. Flash** | Marks the exact moment of the hit | Colour to white for 1-2 frames, then back |
| **4. Shove and spring back** | The widget reacts physically, so it feels struck | Offset it, return with a damped spring (**fixed small steps**, see section 7) |
| **5. Colour by state** | The state is readable without reading a number | Thresholds, e.g. green -> amber at 50% -> red at 25% |
| **6. Pop and arc** | A number that leaps out of the *thing it happened to* | Spawn at the impact point, arc up, scale in, fade out |
| **7. Scale and severity** | Size and colour carry the magnitude, so no reading is needed | Map the value onto font size and colour |
| **8. Stagger by index** | A list arriving feels composed, not dumped | `delay = i * 0.15 s`, slide in with a `back_out` ease |

For menus specifically: **hover = scale** (`lerp` to ~1.15), a **growing underline**, **dim
the other entries** to ~0.3, a slow **float** (`sin(t * 1.5 + i * 0.8)`), a **marker that
lerps** to the selected row, **background particles** drifting with a sine sideways drift, and
a **cursor trail** of fading dots.

### Where it belongs, and where it does not

- **Juice the rare and important, not the constant.** A number that appears every second
  becomes noise and must be small and quiet; a number that appears three times a crossing
  must be unmissable. Pick the frequency first, then the loudness.
- **Take the idea, not the whole menu.** These reels are built for combat games. Copying all
  nine damage-number options into a game that shows damage twice a level is cargo-culting.
- **Never juice at the cost of legibility.** If the player cannot read the bar while it is
  animating, the animation lost.
- **One system, many widgets.** Build the eight moves once as small reusable pieces (an eased
  value, a trailing value, a flash, a spring offset). Every bar, counter and popup in every
  later project is then an hour of work, not a day.

### Where we used it

FerryHeist: the hull bar (all four health-bar moves), damage numbers for collisions and
cannonball hits only, menus when they are built. Spec: `DESIGN_BRIEF.md`, "Polish references".

---

## 6. Performance: draw calls, culling and cheap colliders

**Source:** the director's teacher warned about multi-material objects (2026-10-01); measured
and worked through in FerryHeist the same day.

### What actually costs performance

Not triangles. Modern hardware eats triangles. What costs is **draw calls** - how many
separate times the CPU has to tell the GPU "draw this". One draw call per renderer per
material, roughly. So:

| Asset | Objects | Materials | Verdict |
|---|---|---|---|
| A rock set | 10 | 1 | ideal |
| A temple | 140 | 6 | the expensive one, *even though* it has few triangles each |
| A book | 7 | 4 | 44,000 triangles but cheap to draw |

**A model split into 140 little objects is worse than one model with 44,000 triangles.**

**"Bake" means one of two things**, and both reduce draw calls:
1. **Merge the meshes** that share a material into one object.
2. **Atlas the textures** so the whole model needs a single material.

Design rule we adopted: **at most 3 materials per asset**, ideally one shared palette texture
for everything (written into FerryHeist's `ART_SPEC.md`).

### Culling: what is automatic and what is not

- **Frustum culling is always on.** Anything outside the camera's view is skipped, with no
  setting to enable. This is the one everybody means when they say "camera culling", and it
  is already doing its job in every Unity project.
- **Occlusion culling is opt-in** (Window > Rendering > Occlusion Culling, then Bake). The
  camera's "Occlusion Culling" tick box does nothing until data is baked, and it only ever
  hides **Static** objects behind other Static objects. **It is close to useless for a
  top-down or 3/4 game** - from above, almost nothing is hidden behind anything. Worth it for
  first-person games in corridors and cities, not for us.
- **Far clip plane** is free culling: anything beyond it is not drawn. Keep it as tight as the
  game allows.
- **Per-layer cull distances** (`Camera.layerCullDistances`) stop drawing small props beyond a
  chosen distance. Useful when a level has lots of little scenery.

### The two settings that do the work in URP

- **SRP Batcher** (on by default) - the big one. It batches by shader, so **fewer shader
  variants matters more than fewer materials**.
- **GPU instancing** (a tick box per material) - draws many copies of the *same mesh and
  material* in one call. Made for scattered props: rocks, crates, coins, trees. **But the two
  do not add up:** when a shader is SRP Batcher compatible (URP Lit and Unlit are), URP uses
  the batcher and **ignores the instancing tick box**. Instancing only takes over if the SRP
  Batcher is off or the material is incompatible with it. Instancing costs nothing visually -
  it is a saving, not an effect - but ticking it "to be safe" does nothing here.
- **Measure before optimising.** Run a build on the weakest machine available and read the
  numbers (FPS, draw calls in the Stats window / Frame Debugger) before changing anything.

### Colliders

Cheapest to most expensive: **circle/sphere, then box/capsule, then convex, then mesh**. A
circle is a distance check. For scattered scenery, a circle that is approximately right beats
an exact mesh collider every time - and the player cannot tell.

Caveat learned the same day: for a **tilted** camera, size the collider from the object's
footprint **at ground/water level**, not from its whole bounding box. A tall object is drawn
offset up-screen from where it actually stands, so a collider derived from its full height
feels wrong to the player.

---

## 7. Hard-won technical lessons

These start as project lessons and move here once they clearly apply to any project.

- **A spring (`v += (-x * k - v * d) * dt`) blows up on a frame hitch.** At a long `dt` the
  correction overshoots and grows for ever - the effect sticks on screen at maximum. Always
  integrate it in **small fixed steps**, and clamp `dt`. (FerryHeist, 2026-10-01: the first
  fender-squash effect stuck after the first hit.)
- **Squashing the whole screen is cheaper through the camera's projection matrix than through
  post-processing.** Multiply the projection in `LateUpdate`; nothing smears, the UI is
  untouched, and no render feature or shader is needed.
- **Growing a collider silently changes how a vehicle handles.** A physics engine derives
  rotational inertia from the collider's shape, so replacing a placeholder with a bigger model
  makes the thing turn sluggishly even though no handling value was touched. (FerryHeist: the
  hull collider went from 2.0 x 4.2 to 2.8 x 7.4 and inertia went 1.0 -> 3.33, so the boat
  turned 3.3x more slowly. It took the director several sessions to put a finger on it.)
  **Fix:** for an arcade vehicle, set the inertia **explicitly** from a tuned value instead of
  letting the collider decide (`rb.inertia = turnInertia * rb.mass`), and re-apply it after any
  mass change, which resets it. Handling then stays the designer's choice, not a side effect
  of the art.
- **Unity compiles in the background but only swaps the new code in when the window gets
  focus.** An editor script driven from outside (MCP, a CLI) keeps running the *old*
  assembly, so a freshly added `[SerializeField]` is "not found" and generators quietly wire
  nothing. `AssetDatabase.Refresh(ForceUpdate)` starts the compile but does not force the
  domain reload. **Check that the new code is live before trusting a generator**: add the
  component to a throwaway object and look for the new field. If it is missing, stop and ask
  for one click on the Editor window. (FerryHeist, 2026-10-06.)
- **A generator that wires references must survive a missing field.** When the old assembly
  is still live, `FindProperty` returns null; writing to it throws and leaves the scene half
  built. Log an error and carry on instead.
- **A following camera plus 3D sound is a bug waiting to happen.** Play SFX through one 2D
  `AudioSource` (`spatialBlend = 0`) with `PlayOneShot`. (From LuaLander.)
- **A `[SerializeField]` default applies only once - when the component is added.** After
  that the value saved in the scene wins, so changing the number in the script does nothing
  to objects already placed. (Falling Frenzy: the script says `spawnRangeX = 10f`, the scene
  holds 15, the game uses 15.) To change it everywhere, change it in the Inspector or the
  prefab - or reset the component.
- **`Time.timeScale = 0` stops physics and `Time.deltaTime`, not `Update`.** Input is still
  read and UI still runs, which is what makes a pause menu possible - but anything moved by
  hand without `deltaTime` keeps moving. It also survives a scene reload, so set it back to 1
  when a level starts. (Falling Frenzy's Game Over; LuaLander's `GameManager.Awake`.)
- **Most bugs in a Unity hobby project are scene wiring, not code.** A new `[SerializeField]`
  silently sits at `None`. Generating the scene from an editor script removes that whole class
  of bug: the wiring is code, so it is reviewable and repeatable. (FerryHeist's
  `GreyboxBuilder`.)

## Batching a hierarchy that is spawned, not placed

Unity's static batching is decided when the **scene** is built, so it does nothing for objects
that arrive at run time - a level instantiated from a prefab, anything spawned. Those still
cost a draw call each, and an art pack built out of many small meshes (a ruin modelled as 150
separate bricks) can quietly cost hundreds.

`StaticBatchingUtility.Combine(root)` does the same job on demand: call it once in `Start` on
a parent whose children will never move, and the whole subtree becomes one batched mesh.
Scenery, props and terrain dressing qualify; anything that moves, scales, or is switched off
and on again does not - batching welds it in place.

The cheaper fix is worth trying first, though: **fewer, bigger pieces**. Throwing away thirteen
of every fourteen bricks and growing the survivors cost a tenth of the meshes *and* read as a
stronger silhouette. Stylisation and performance pull the same way more often than not.

## A model's up axis is a measurement, not a convention

Two FBX files can declare the same axes in their header, carry the same -90 degree node
rotations, come out of the same exporter - and still arrive in the engine standing differently.
One of ours imported Y-up like everything else; one imported Z-up, and the project's one
blanket "model to game axes" rotation laid it on its side.

Reading the FBX binaries did not settle it: the header fields matched, and the node rotation
that looked like the culprit also appeared on models that looked right. What settled it in
seconds was an editor menu item that instantiates each model the way the build does and prints
its bounding box: **a standing prop is tallest on the up axis, and its base sits at zero.**

So: keep one blanket conversion for the common case, but give it an escape hatch per model,
and keep a one-click report that measures what actually happened. Guessing at an orientation
costs a rebuild and a round trip with whoever is testing; measuring it costs a click.

## The default audio import settings will stutter your game

Unity imports audio as **Decompress On Load with Preload Audio Data off**. Read that pair
carefully: the clip's data is not loaded when the scene loads, it is loaded the **first time
it plays** - and Decompress On Load then unpacks the entire compressed file to raw PCM on the
main thread, right then. A 90-second stereo recording is about 35 MB of unpacking in one
frame, and the player feels it as a hitch exactly when the thing that makes the sound shows up.

Set them by length and the problem disappears:

| Length | Load type | Preload |
|---|---|---|
| up to ~6 s (one-shots) | Decompress On Load | **on** - paid once, with the scene |
| ~6-30 s (loops, longer effects) | Compressed In Memory | on - small in RAM, decoded as it plays |
| over ~30 s (music, long takes) | Streaming | off - never in memory at all |

Worth doing as an **editor pass that runs on every build**, not by hand: audio arrives in
batches and nobody remembers to tick a box on the twelfth file.

And the general lesson: when something hitches at a particular moment, ask what is being
**loaded** at that moment before assuming it is what is being **drawn** or **spawned**.

## Setting velocity vs adding force: one Rigidbody, two game feels

**Source:** comparing LuaLander (CodeMonkey) with Falling Frenzy (GameDevTV *Unity
Fundamentals*), 2026-10-26.

The same component can feel completely different depending on one line:

| | `rb.linearVelocity = input * speed` | `rb.AddForce(force * dir)` |
|---|---|---|
| Start / stop | Instant | Builds up, coasts |
| Feel | Tight, arcade, "on rails" | Heavy, floaty, physical |
| Skill | Positioning, timing | Managing momentum |
| Used in | Falling Frenzy's catcher | LuaLander's lander, FerryHeist's boat |

**Why it works:** setting velocity throws away last frame's motion, so the player's input is
the whole story. Adding force keeps the motion and only nudges it, so the past matters - that
is momentum, and momentum is what makes landing a lander hard and satisfying.

**How to use it:** decide the feel first, then pick the line. A catcher, a menu cursor or a
platformer's horizontal run want velocity (often with a little smoothing). Vehicles, space
and water want force plus damping. Mixing them on one body (setting velocity *and* adding
force) makes the forces disappear every frame.

## Unity 2D: lessons from a complete combat course

**Source:** GameDev.tv, *Unity 2D RPG: Complete Combat System* (87 lectures), followed in
2DTopDownPixelCombat from 15 to 29 October 2026, plus every bug we hit along the way. The
project's own map of the systems is in `knowledge/2d-topdown-pixel-combat.md`; this section
keeps only what carries over to any Unity project.

### Patterns worth reusing

- **`Singleton<T>` base class** with `DontDestroyOnLoad` only on root objects; children are
  carried across scenes by a root parent. Every scene can then contain its own copy of the
  Player, UI and managers for testing, and the duplicates destroy themselves on load.
- **Interfaces for "anything that can X".** `IWeapon.Attack()` lets the inventory swap
  glaive, bow and staff without knowing which is which; `IEnemy.Attack()` lets one
  `EnemyAI` state machine (an `enum` + `switch`: Roaming, Attacking) drive a melee slime, a
  lobbing grape and a bullet-hell shooter.
- **ScriptableObject for data** (`WeaponInfo`: prefab, cooldown, damage, range). Balancing
  is editing an asset, not code.
- **One small component per behaviour:** `Knockback`, `Flash`, `DamageSource`,
  `Destructible`, `Indestructible`, `PickUpSpawner`, `SpriteFade`, `SelfDestroy`. Behaviour is
  assembled in the Inspector.
- **Fake height in top-down with an `AnimationCurve`.** Lerp the ground position linearly and
  add `curve.Evaluate(t) * height` on Y. The same 10 lines make loot pop out of bushes and a
  grape's projectile arc; a separate shadow lerps along the ground only.
- **Scene transitions by name.** An exit stores a transition name and loads a scene; in the
  new scene the entrance with the matching name moves the persistent player to itself. Two
  rules: an entrance name must be **unique within its scene** (two `West_Entrance`s means a
  random spawn point), and every `sceneToLoad` must exist **and be in Build Settings**, or the
  player is stuck behind the fade to black.
- **Bullet patterns from three numbers:** burst count, projectiles per burst, angle spread.
  Stagger and oscillate on top give spirals. Spawn at `centre + r * (cos a, sin a)` and set
  `bullet.transform.right` to point outward.

### Traps we fell into (look for these first)

- **`Destroy()` inside a base `Awake()` runs the child's `OnDisable()` before the child's own
  `Awake()` has finished.** Anything created after `base.Awake()` is still `null` there. Use
  `?.` in `OnDisable`, or create the object before calling `base.Awake()`.
- **Input System: every `Enable()` in `OnEnable` needs a `Disable()` in `OnDisable`.** Otherwise
  destroyed copies leave their actions enabled and the garbage collector later prints
  "This will cause a leak" - the error shows up at a random moment, far from the cause.
- **An animation event is not guaranteed to fire.** If the object is destroyed mid-animation
  (weapon switched mid-swing), "turn the damage collider off" never runs and the player gets
  invisible thorns. Undo state in `OnDestroy` / `OnDisable` as well.
- **A one-line `if` without braces** guards only the next statement: pickups were destroyed by
  touching *anything* because `Destroy()` sat outside the `if`.
- **`OnCollisionStay2D` damage runs every physics step.** It needs an invulnerability window
  (`canTakeDamage` + a recovery coroutine), or contact kills instantly.
- **`GameObject.Find("Name")`** silently returns `null` if the name differs by one character
  or the object is inactive. Keep such names in `const string` fields.
- **IDE auto-imports pick the wrong namespace.** `Image` from
  `Microsoft.Unity.VisualStudio.Editor` instead of `UnityEngine.UI` - no `.sprite`, and an
  editor-only `using` in a game script also breaks the build. For UI types, always
  `UnityEngine.UI`.
- **A script on the wrong object** (`GetComponent<Image>()` on an object with a
  SpriteRenderer) throws every frame. Search the Hierarchy with `t:ScriptName` to find every
  copy.
- **Enemy and player projectiles sharing one script** need the flag checked everywhere they
  are consumed: enemy bullets were breaking bushes because `Destructible` only checked
  "is it a Projectile".

### Tilemaps and rule tiles

- **A rule tile sees neighbours only on its own tilemap.** Paint one rule tile across two
  tilemaps and the edges at the boundary pick wrong pieces.
- **The editor shows a cached result; Play recalculates the rules.** If artefacts appear on
  Play and vanish on Ctrl+Z, the rules are what is wrong - Ctrl+Z only restores the cache.
  Tilemap component > ... > *Refresh All Tiles* shows the real result in the editor.
- **Two renderers with the same sorting layer and order draw in undefined order**, and the
  order can change between runs. Give every tilemap its own Order in Layer.

### Animation and particles (2D)

- **A clip that "stops working" usually has Loop Time off.** Check it first.
- **`SetTrigger("X")` on a parameter that does not exist** only warns, and if it is in a
  loop it floods the console with 999+ warnings.
- **Particles: Shape > Align To Direction is 3D.** It turns flat 2D sprites edge-on to the
  camera, so they disappear. In 2D, control travel direction with Shape rotation and sprite
  orientation with Start Rotation or Renderer Flip. *(Tried and failed, 2026-10-29.)*
- **A Shape scale of 0 on any axis** gives "trying to spawn on a mesh with zero surface area"
  and every particle spawns in one point. Keep scale Z at 1.
- **"Emit from four walls inwards" = four emitters**, one per wall. A single circle with
  negative start speed was suggested as a one-system alternative; it did not work in our
  setup and is not recommended. *(Failed experiment, 2026-10-29.)*

### Editor and tooling

- **`OnApplicationFocus` fires on OS-level focus (Alt+Tab), not when clicking between Unity's
  own windows.** Pressing Esc in Play mode shows the OS cursor until something hides it again.
- **GitHub Desktop "No content changes found"** on Unity settings files means only the file's
  timestamp changed (Unity re-saved identical content). Discard it; `git status` clears it.
- **Commit before an experiment.** A saved-over prefab came back in one command
  (`git restore <file>`) only because the last commit had it.
