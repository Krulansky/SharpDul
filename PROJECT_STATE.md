# SharpDul - Project State

Session handoff between machines and sessions. Keep it short and current.

## Where we are (2026-10-27)

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
knowledge/   study notes per source project (e.g. falling-frenzy.md) - raw material for packs
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
4. Director builds Falling Frenzy in Unity with the course (own repo, e.g. FallingFrenzy).
   Quiz pack from it only for steps actually built.
