# Riddle of Steel - notes (paused project)

A Conan-inspired 2D top-down game: a learning project where the director builds everything and
the agent teaches. The design lives in the Claude Concept Document
(https://claude.ai/artifact/PnpHoBvXNga7cv8XMiCsg6), filled in from the director's questionnaire.
This file collects what the courses add to it until work starts.

## Status

**The main game for Q1 2027** (director, 2026-11-14): goal is a full playable level demo by the
end of March 2027. Work starts after Outer Lands (end of November) and FerryHeist's basic crossing (end of 2026).

## From the Design Patterns course

- **Level up: definitely in** (director, 2026-11-05). Build it as an Observer: `Level` fires
  `OnLevelUp`, and health, UI, effects and talents subscribe; `Level` knows none of them
  (lesson "Observers with UnityEvents").
- Guards and bosses: compose them from components (move, attack, health, AI) rather than an
  enemy class tree (lesson "Composition over inheritance").
- Planned patterns: State (hero stages, enemy AI), Observer (events), Object Pool (crowds of
  enemies), ScriptableObjects (weapons, abilities) - see `study/path.md`.
