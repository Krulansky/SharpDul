# Figma course notes (Korean source) - teaching guide

Source: `knowledge/Figma/` - Korean notes from a Figma beginner course, uploaded by the director
2026-11-03. The director asked: teach Figma **in Slovak, following these notes**.
The course PDF/video and installers are not in the repo (kept local, too large / not needed).

## How to teach from this

- Follow the course order below (01 -> 16). One topic per lesson, then a small hands-on task
  in the director's own Figma file (via the Figma MCP when connected).
- Explain in Slovak; Figma UI names and design terms stay **English** (Frame, Auto Layout,
  Constraints, Component, Prototype, Export, ...), same rule as the rest of SharpDul.
- The notes show an older Figma UI (2021-22: "Inspect" tab, Community "Beta", Mac shortcuts).
  The director is on **Windows**: say `Ctrl` for the Mac `Cmd` key, `Alt` for `Option`.
  Where today's Figma differs (e.g. Inspect -> Dev Mode), say so.
- Director's Figma account: Starter plan, **View** seat on both teams (checked 2026-11-03).
  Per note 03, a Viewer can only view, comment and export assets - editing team files needs an
  Editor seat. Drafts (own files) are the safe place to practise.
- Apply lessons to the director's games (Game Promo Kit, SharpDul UI) rather than the course's
  pizza / flag examples when possible.

## Course outline (what each note says)

| # | File | Topic | Key points |
|---|------|-------|-----------|
| 01 | `01. 가입하기.txt` | Sign up | Starter plan is free; student verification = Professional for free; Professional $12/mo, Organization $45/mo (yearly). |
| 02 | `02. 파일 브라우저 명칭.jpg` | File browser | Three areas: Sidebar (Recents, Drafts, Community, teams), Toolbar (Drafts / Deleted), List (new design file, new FigJam file, import, files). |
| 03 | `03. 피그마 팀 권한 종류.txt` | Team roles | Owner (everything), Admin (like Owner but cannot touch the Owner), Editor (all work + invite), Viewer (view, comment, export assets). |
| 04 | `04. 피그마 파일 구조.txt` | File structure | Team > Project > File > Page. |
| 05 | `05. 에디터 구성.jpg` | Editor layout | Toolbar (top), Layers panel (left: Layers / Assets / Pages), Canvas (middle), Properties panel (right: Design / Prototype / Inspect, Export at the bottom). |
| 06 | `06. 피그마 단축키.png` | Shortcuts | Essential: Show/Hide UI `Ctrl+\`, Pick color `I`(older: `Ctrl+C`), Search `Ctrl+/`. Tools: Move V, Frame F, Pen P, Pencil Shift+P, Text T, Rectangle R, Ellipse O, Line L, Arrow Shift+L, Comment C, Slice S. Group Ctrl+G, Frame selection Ctrl+Alt+G, Auto Layout Shift+A, Create component Ctrl+Alt+K, Zoom to fit Shift+1, Zoom to selection Shift+2, Pan Space+drag. |
| 07 | `07. 레이아웃 그리드 시스템 용어.txt` | Layout grid | Grid, Column (vertical), Row (horizontal), Margin (outer space), Gutter (space between columns/rows). |
| 08 | `08. 플러그인.txt` | Plugins | Content Reel (fake text data), Unsplash (photos), Arrow Auto (flow arrows), Better Font Picker, Clean Document (remove hidden layers, ungroup single-child groups, round decimals), Super Tidy (even spacing), Product Planner, Feather Icons, iOS Browser UI Kit. |
| 09a | `09. 등록할 수 있는 스타일 종류.txt` | Styles | Colors (fill, stroke, background), Text (family, size, line height, spacing), Effects (drop/inner shadow, layer/background blur), Layout Grids. |
| 09b | `09. 크롬 개발자 도구에서...txt` | Breakpoints | Mobile S 320, M 375, L 425, Tablet 768, Laptop 1024, Laptop L 1440, 4K 2560. statcounter.com for real device share. |
| 10 | `10. Constraints의 Fixed와 Hug Contents.txt` | Constraints, Fixed vs Hug | **File is empty** - teach from scratch (Fixed / Hug / Fill in Auto Layout; Constraints left/right/center/scale). |
| 11 | `11. 디스플레이 용어.txt` | Display terms | Screen size (diagonal, inches), resolution (px count), pixel density (ppi/dpi), pixel ratio (iPhone 11 Pro: 375x812 logical @3x = 1125x2436). |
| 12 | `12. 와이어프레임과 프로토타입.txt` | Wireframe vs prototype | Wireframe = elements as plain lines/boxes; prototyping = adding interactions so static screens behave like the real thing. |
| 13 | `13. 디지털 프로덕트 제작 프로세스.txt` | Product process | Requirements > Planning > Design > Development > Test & fix > Release. |
| 14 | `14. Interactions의 Trigger 의미.txt` | Triggers | On Click, On Drag, While Hovering (reverts), While Pressing, Key/Gamepad, Mouse Enter (stays), Mouse Leave, Touch Down, Touch Up, After Delay (top-level frames only). |
| 15 | `15. Interactions의 Action 의미.txt` | Actions | Navigate to, Open overlay, Scroll to, Swap overlay, Back, Close overlay, Open link. |
| 16 | `16. 디자인 에셋 추출하기.txt` | Export assets | Export section at the bottom of the Properties panel; add x1, x2, x3 (press + three times). |
| - | `! 참고/디자인 시스템과 아토믹 디자인.txt` | Design system, Atomic design | Design system = standardised principles, layout patterns, code; Atomic design = small elements combined into larger ones. |
| - | `! 참고/레퍼런스 사이트.txt` | References | Unsplash, Behance, Dribbble, Bestfolios, Cofolios, Awwwards, Medium, Brunch, noonnu (Korean fonts). |
| - | `! 예제/` | Example files | Course example `.fig` (Community) + pizza / Italy flag images. |

## Progress log

Figma file: **2D Combat - Game Promo Kit** (Drafts, Pavol Dulovič's team),
https://www.figma.com/design/OHULpqrLyylz8NnorNjJIp - Starter plan = max 3 pages, so the kit
uses pages `Cover & Brand`, `Promo Assets` (Sections: Key Art, Store Screenshots, Social Posts,
itch.io Page) and `Playground`.

Game working title: **Outer Lands** (director, 2026-11-03).
Brand colours (director's words, hex values chosen by the agent to match, editable styles):
`Brand/FelFire` #B8FF1F (intensely glowing yellow-green fel flame), `Brand/Demonic Purple`
#6B3FA0 (demon-hunter / night-elf purple), `Brand/Rage Red` #E8361C (red-amber rage flame).
Current sprites are course assets and will all be redrawn before release - colours may change.

Done (2026-11-03): lessons 04, 05, 07, 09, 10 - itch.io `Cover 630x500` frame with grid style
`Grid/Cover 6col`, FelFire fill, `OUTER LANDS` title (Inter Semi Bold 64, Rage Red) in a Hug
auto-layout frame with Constraints Center / Top.
Teaching lessons learned: the director needs exact panel locations one step at a time;
shortcuts fail while typing in a text box (Esc first); check which Layers row is selected
before editing (Shift+A selects the new wrapper frame).
Done later the same day: Effect style `Glow/FelFire` (drop shadow 0/0, blur 24, #B8FF1F 80%)
on the title, which the director recoloured to FelFire on a Demonic Purple cover (their call);
lesson 11 (Steam screenshots 1920x1080, export 2x for 4K) - `Screenshot 01 – Town` frame;
lesson 12 wireframe `Post 01 – Announce` 1080x1080 (Image / Title / CTA boxes, centred);
lessons 13-15 - CTA On click -> Navigate to Screenshot 01, Dissolve 300 ms, Flow 1, works in
Present. Steam rule noted: no text or marketing on store screenshots.
Lesson 08: Better Font Picker crashes in the 2026 UI - use the built-in font dropdown (live preview). Course plugins may be dead; test before recommending.
Title font: Metamorphous Regular 64, Text Style `Title/Hero` (director tried pixel fonts and rejected them). All 4 style kinds now exist.
Still to do: lesson 08 (other plugins), 16 (export, waits for an itch.io upload), real art in the frames.
Token tip from the director's teacher: verify via MCP reads, ask for screenshots only when stuck.
