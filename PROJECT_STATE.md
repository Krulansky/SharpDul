# SharpDul - Project State

Session handoff between machines and sessions. Keep it short and current.

## Where we are (2026-10-25)

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
- Content: `lualander-easy.json` - 10 Easy questions from LuaLander.
- Look: neutral grey placeholders. The director designs the visual identity.

Verified in headless Chromium at iPhone 13 size, served under `/SharpDul/` like GitHub Pages:
a full Daily session, XP/active day saved across reload, export -> wipe -> import.
**Not yet verified on a real iPhone.**

## Layout

```
src/SharpDul.Pocket/
  Models/     content + progress data classes
  Logic/      pure rules: LeitnerScheduler, Progression, SessionBuilder (no UI, no storage)
  Services/   ContentLibrary (loads packs), ProgressStore (localStorage, export/import)
  Pages/      Home, Quiz, Backup (UI only - they call Services)
  wwwroot/content/   index.json + one JSON per content pack
.github/workflows/deploy-pages.yml   publish to GitHub Pages on every push to main
```

## Adding a content pack

1. Add `src/SharpDul.Pocket/wwwroot/content/<pack>.json` (same shape as `lualander-easy.json`).
2. List it in `wwwroot/content/index.json`.
3. Question ids must be unique and must never change - progress is stored by id.
4. List the correct answer first in `options` with `answerIndex: 0`; the quiz shuffles them
   (except True/False).

## Next

1. Director tests on the iPhone (Safari -> Share -> Add to Home Screen).
2. Mechanics Lab: lander simulation with sliders on the real `Lander.cs` values.
3. More LuaLander questions, then Medium level.
