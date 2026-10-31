# SharpDul - Project State

Session handoff between machines and sessions. Keep it short and current.

## Where we are (2026-10-30)

**First prototype of SharpDul Pocket** (Blazor WebAssembly PWA, .NET 10):

- Home: level + XP bar, active days (last 7), Daily button, one card per content pack
  (Burst mode), link to Backup.
- Quiz: question, code snippet, shuffled options, feedback with explanation and the source
  file/lines in the original project.
- Spaced repetition: Leitner boxes 1-5, intervals 1/2/4/8/16 days; wrong answer -> box 1.
  "Mastered" = box 4 or higher.
- XP: Easy 10, Medium 20, Hard 30, wrong answer 2. Level N needs 50*N*(N-1) total XP.
- Backup: Export (iPhone share sheet -> Save to Files; download elsewhere) and Import
  (replaces progress on the device).
- Content: `lualander-easy.json` - 10 Easy questions from LuaLander, rewritten 2026-10-26
  after director feedback: each has context, highlighted answer lines and a hint
  ("Show hint" button, no XP penalty).
- Languages: EN / SK / KR switch on Home (saved with progress, so part of the backup).
  UI strings in `Localization/Strings.cs`; pack translations in `content/<pack>.<sk|ko>.json`.
- **Mechanics Lab · LuaLander** (`Pages/Lab.razor`, `Logic/LanderSim.cs`): a C# port of
  `Lander.cs` with the real Rigidbody2D values (mass 1, Linear Damping 1, Angular Damping 5,
  BoxCollider2D 0.92 x 1.47, 0.02 s fixed step). Hold-buttons (and arrow keys / WASD),
  sliders for force, turnSpeed, GRAVITY_NORMAL, fuelAmountMax, softLandingVelocityMagnitude,
  minDotVector. The matching code lines light up (live strip under the game + full code
  card). Same landing rules and score formula as the game (pad multiplier 1). Physics is a
  close approximation of Box2D, not bit-exact. An autopilot test landed successfully
  (speed 1.05, score 395).
- **Courses** (build-along, not quizzes): `Pages/CourseOverview.razor`, `CourseStepPage.razor`,
  `Services/CourseLibrary.cs`, content in `wwwroot/content/courses/`. Each step: goal, Unity
  click paths, code with new lines highlighted + Copy, why it works, Play-mode check, Lab
  preview, "I built it in Unity" (+25 XP once; stored in `CompletedSteps`).
  First course: **Falling Frenzy**, 11 steps (project setup -> physics -> input -> prefab +
  spawner -> triggers -> random X -> UI/Game Over -> our singleton+events architecture ->
  "make it yours"). Primitives instead of the course's models. EN/SK/KR. Sources:
  `tools/build_falling_frenzy_course.py`, `tools/falling_frenzy_course_sk.py`, `_ko.py`.
- **Mechanics Lab · Falling Frenzy** (`Pages/FrenzyLab.razor`, `Logic/FallingFrenzySim.cs`,
  `wwwroot/js/fallingfrenzy.js`): the game as it behaves after any course step (stage 1-10,
  `?stage=N`), A/D or hold-buttons, sliders for moveSpeed, spawnInterval, spawnRangeX,
  startingSheepLeft, and a velocity-vs-AddForce toggle; lit code lines.
- **Build Lab** (`Pages/BuildLab.razor`, `Logic/PuzzleBoard.cs`, `Services/BuildLibrary.cs`,
  content in `wwwroot/content/builds/`): the director assembles the game inside the app.
  Each script is a puzzle - tap shuffled lines into order, pick the right word in each
  `____`, avoid distractor lines; checked against the solution (plus listed alternative
  orders). A solved puzzle switches its `FrenzyFeature` on in the shared `Components/FrenzyGame.razor`
  (+20 XP once, `SolvedPuzzles`). Falling Frenzy: 11 puzzles, same code as the Unity course.
  Sources: `tools/build_falling_frenzy_puzzles.py`, `tools/falling_frenzy_puzzles_translations.py`.
  Verified: all 11 solved through the UI in headless Chromium, each unlocking its part.
- **Mechanics Lab · 2D Combat** (`Pages/CombatLab.razor`, `Logic/CombatSim.cs`, `wwwroot/js/combatlab.js`,
  2026-10-30): the Ghost fight from 2DTopDownPixelCombat. Ports EnemyAI (Roaming/Attacking),
  Shooter (ShootRoutine as a C# iterator that yields the WaitForSeconds times), Projectile,
  PlayerController (move + dash), PlayerHealth, Knockback, Flash and Stamina with the prefab
  values (Ghost: 6 bursts x 8, 165°, stagger + oscillate; Player moveSpeed 4, stamina refresh 2 s).
  Stick + Dash button (WASD / Space), sliders, pattern presets, a switch for the director's
  OnValidate (stagger can never be off - bug), lit code lines, five "Try this" tips.
  Verified in headless Chromium: 8 bullets over 165° never hit a player who stands still
  (no centre bullet); with 9 the player dies and respawns.
- **Quiz pack `combat2d-easy`** (2026-10-31): 16 Easy questions from 2DTopDownPixelCombat
  (dash, stamina + its event, damage recovery, knockback, EnemyAI, Shooter maths, Destructible,
  Singleton, scene transitions, the director's own Rage). Built by `tools/build_combat2d_pack.py`
  from the project on disk: source lines are found by anchor text, EN/SK/KR in one file.
  Verified: all 16 answered right through the UI in EN, SK and KR.
  Note: the 2D Combat Lab still has the course's Stamina (3 orbs, refill every 2 s); the project
  now regenerates 1/3 per second with an OnStaminaChanged event.
- Look: neutral grey placeholders. The director designs the visual identity.

Verified in headless Chromium at iPhone 13 size, served under `/SharpDul/` like GitHub Pages:
a full Daily session, XP/active day saved across reload, export -> wipe -> import.
Live at https://krulansky.github.io/SharpDul/ - director confirmed on the iPhone
(2026-10-26) that it installs and progress survives. Export to Files not yet confirmed.

## Layout

```
src/SharpDul.Pocket/
  Models/     content + progress data classes
  Logic/      pure rules: LeitnerScheduler, Progression, SessionBuilder, LanderSim (no UI, no storage)
  Localization/  Language, Strings (UI text EN/SK/KR), Localizer (current language)
  Services/   ContentLibrary (loads packs), ProgressStore (localStorage, export/import)
  Pages/      Home, Quiz, Backup, Lab (UI only - they call Services / Logic)
  wwwroot/content/   index.json + one JSON per content pack
GAMEDEVNOTES.md   the travelling notebook (moved from FerryHeist 2026-10-26)
knowledge/   study notes per source project (falling-frenzy.md, 2d-topdown-pixel-combat.md) - raw material for packs
.github/workflows/deploy-pages.yml   publish to GitHub Pages on every push to main
```

## Adding a content pack

1. Add `src/SharpDul.Pocket/wwwroot/content/<pack>.json` (same shape as `lualander-easy.json`).
2. List it in `wwwroot/content/index.json`.
3. Question ids must be unique and must never change - progress is stored by id.
4. List the correct answer first in `options` with `answerIndex: 0`; the quiz shuffles them
   (except True/False).
5. Follow the content rules in `CLAUDE.md`: context, snippet that contains the answer,
   `highlight` (1-based snippet lines), `hint`.

## Next

1. Director tries the Mechanics Lab and the language switch on the iPhone.
2. More LuaLander questions, then Medium level (`?.Invoke`, dot product, SetActive vs events).
3. Particle Lab (sandbox + "recreate this effect").
4. Director cracks the Falling Frenzy Build Lab on the iPhone, then builds it in Unity with the course (own repo, e.g. FallingFrenzy).
   Quiz pack from it only for steps actually built.
