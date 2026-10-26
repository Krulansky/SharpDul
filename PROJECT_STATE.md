# SharpDul - Project State

Session handoff between machines and sessions. Keep it short and current.

## Where we are (2026-10-26)

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
