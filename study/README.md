# Study inbox

The order of courses is in `study/path.md`.

This is where course material the director sends is sorted. A lecture, a slide or a comment
thread is not copied in whole. Each lesson gets one entry in its course log
(`study/<course>.md`), and every useful point in it goes to exactly one bucket:

| Bucket | Question | Where it goes |
|---|---|---|
| **P** - projects | Does it change something in Outer Lands, FerryHeist, Riddle of Steel...? | that project's `CLAUDE.md` (agent notes, as a *proposal* - the director decides) |
| **S** - skill | Does it close a gap in the director's own C# / coding understanding? | `study/skill-gaps.md` |
| **Q** - training | Can it become a quiz question or a Lab? | the backlog at the bottom of the course log, then a pack or Lab when the director asks |
| **N** - general | Is it a lesson for any game? | `GAMEDEVNOTES.md` (only if it is new; usually one short paragraph) |
| **-** - parked | Interesting, but none of the above now | one line in the log, nowhere else |

Rules:

- **Focus on one course at a time.** Material from a second source waits in the log as "parked"
  until the current course ends.
- **The log comes first.** Material is sorted in the log, then moved to the other files. Do not
  scatter it straight into the `.md` files.
- **Bucket S is based on evidence:** questions the director got wrong (from a backup export:
  `Cards` with a low box), topics they asked about, or bugs they hit. Do not guess.
- **Q items wait.** Build quizzes and Labs only when the director asks; until then they collect
  in the backlog.
- **Teaching style that works:** point at the exact line and give a skeleton with blanks.
  Open-ended "think about..." questions confused the director (challenge 1.7).
