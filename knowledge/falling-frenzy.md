# Falling Frenzy - study notes

**Source:** GameDevTV, *Unity Fundamentals* course -
<https://gitlab.com/GameDevTV/unity-fundamentals/course/falling-frenzy> (branch `master`,
last commit `cd4f252` "Polish"). Unity `6000.3.0f1`, URP, new Input System.

> The course code belongs to GameDevTV and the repo has no licence file. This repo is public,
> so these notes are **our own summary** with short quotes for study. The full project stays
> in GitLab - read it there by commit.

## The game in one paragraph

Sheep fall from the sky. You move a catcher left/right with **A / D** and catch them.
Every sheep that reaches the ground is lost; after **5 lost sheep** a Game Over text appears
and the game freezes. 3D (KayKit sample assets + a sheep model), bouncy physics material.

## Lessons = commits

Each lecture of the course is one commit, so `git checkout <hash>` shows the project at the
end of that lecture.

| # | Commit | Lecture | What it adds |
|---|--------|---------|--------------|
| 1 | `00008e7` | Install Unity | Empty URP project |
| 2 | `6e97562` | Unity Engine Interface | Scene, objects, Inspector |
| 3 | `6ca37ac` | Programming Basics C# | `HelloWorld.cs`: `Start()` renames its GameObject |
| 4 | `1c267e9` | Unity Physics | `Rigidbody`, colliders, `FallingObject.OnCollisionEnter` logs a hit |
| 5 | `92700b9` | Player Input | `PlayerController`: A/D keys -> `rb.linearVelocity` |
| 6 | `27d6897` | Instantiating Objects | `SheepSpawner`: timer + `Instantiate` a prefab |
| 7 | `29833fe` | Trigger Colliders | Catch (`OnTriggerEnter` + `CompareTag("Sheep")` + `Destroy`), `SheepDestroyer` on the ground |
| 8 | `de4c9ff` | Design a Level | Level art, random spawn X |
| 9 | `7d72ce5` | Game Over UI | `GameManager`: sheep counter (TextMeshPro), Game Over, `Time.timeScale = 0` |
| 10 | `cd4f252` | Polish | Scene renamed `FallingFrenzy.unity`, post-processing volume |

## The four scripts

### `PlayerController.cs` - input in `Update`, physics in `FixedUpdate`

```csharp
private void Update()
{
    input = 0f;
    if (Keyboard.current.aKey.isPressed) { input = -1f; }
    if (Keyboard.current.dKey.isPressed) { input = 1f; }
}

private void FixedUpdate()
{
    Vector3 velocity = new Vector3(input * moveSpeed, 0f, 0f);
    rb.linearVelocity = velocity;
}
```

- **Read input every frame (`Update`), move the body on the physics step (`FixedUpdate`).**
  `input` is the bridge between the two. Same split as LuaLander.
- It **sets the velocity** directly (instant start/stop, arcade feel) instead of `AddForce`
  (LuaLander: momentum, floaty feel). Same Rigidbody, two very different game feels.
- Both keys held: D wins, because its `if` runs last.
- Reads the keyboard directly (`Keyboard.current`) - quick, but no gamepad/touch. LuaLander's
  `GameInput` with Input Actions is the scalable version.
- `public Rigidbody rb;` and `public float moveSpeed;` (Inspector value **20**). The later
  scripts use `[SerializeField] private`, the better habit.

### `SheepSpawner.cs` - a timer without coroutines

```csharp
timer = timer + Time.deltaTime;
if (timer > spawnInterval)
{
    float xPos = Random.Range(-spawnRangeX, spawnRangeX);
    Vector3 position = new Vector3(xPos, transform.position.y, transform.position.z);
    Instantiate(sheepPrefab, position, sheepPrefab.transform.rotation);
    timer = 0f;
}
```

- Count up with `Time.deltaTime`, fire when past the interval, reset to 0.
- `Random.Range(float, float)` - both ends inclusive for floats.
- **Inspector beats the script default:** the script says `spawnRangeX = 10f`, the scene
  stores **15**. A `[SerializeField]` default only applies when the component is first added.
- Spawns at the spawner's height and depth (`transform.position.y/z`), random X.

### `SheepDestroyer.cs` and the catch - triggers + tags

```csharp
void OnTriggerEnter(Collider other)
{
    if (other.gameObject.CompareTag("Sheep"))
    {
        gameManager.LostSheep();
        Destroy(other.gameObject);
    }
}
```

- The catcher (`PlayerController.OnTriggerEnter`) and the ground (`SheepDestroyer`) are both
  **trigger** colliders - things pass through and only a message is sent.
  Lecture 4 used `OnCollisionEnter` (solid collision) - know the difference.
- `CompareTag("Sheep")` instead of `tag == "Sheep"`: faster, and a typo in the tag name
  gives an error instead of silently never matching.
- The sheep prefab has tag **Sheep**, Rigidbody mass 1, gravity on, **Freeze Position Z**
  (constraints = 8) so sheep stay in the 2D play plane.
- Physics material *Falling Object*: **Bounciness 1**, friction 0.6 - sheep bounce off things.

### `GameManager.cs` - counter, UI and Game Over

```csharp
public void LostSheep()
{
    currentSheepLeft = currentSheepLeft - 1;
    UpdateText();

    if (currentSheepLeft <= 0)
    {
        gameOverText.SetActive(true);
        Time.timeScale = 0f;
    }
}
```

- `startingSheepLeft = 5` copied into `currentSheepLeft` in `Start` - keeps the designer
  value separate from the live value.
- UI: `TMP_Text.text = "Sheep Left: " + ...` and a hidden Game Over object shown with
  `SetActive(true)`.
- **`Time.timeScale = 0f` freezes physics and `Time.deltaTime`, but not `Update` itself.**
  `PlayerController.Update` still reads keys - only movement stops because it is physics.
  LuaLander had to reset `Time.timeScale = 1f` in `GameManager.Awake` for the same reason:
  timeScale survives a scene reload.
- `<= 0` rather than `== 0` - safe even if two sheep land in the same frame.

## How it is wired (compared with our architecture)

| Falling Frenzy | LuaLander / FerryHeist |
|----------------|------------------------|
| `SheepDestroyer` has a `[SerializeField] GameManager` and calls `gameManager.LostSheep()` directly | Singletons + C# events: the lander fires `OnLanded`, GameManager listens |
| Logic and UI in one class (`GameManager` updates the text) | Logic classes never touch UI; UI listens to events |
| Input read from `Keyboard.current` | `GameInput` wrapper over Input Actions |

The direct reference is simpler and fine for a 4-script game. It is also the classic
**scene-wiring trap**: if `gameManager` is left `None` in the Inspector, the first lost sheep
throws a `NullReferenceException` - no compile error.

## Quiz material (for a future content pack)

Easy (in game terms, answer visible in the snippet):

1. You hold A and D at the same time - which way does the catcher go? (D - last `if` wins)
2. `spawnInterval = 1` - how many sheep per second? (about one)
3. A sheep falls past the catcher and hits the ground - what happens? (`LostSheep`, counter -1, sheep destroyed)
4. The counter reaches 0 - what freezes the game? (`Time.timeScale = 0f`)
5. Script says `spawnRangeX = 10f`, the Inspector shows 15 - which one is used? (15)

Medium:

6. Why is input read in `Update` but velocity set in `FixedUpdate`?
7. `rb.linearVelocity = ...` vs `AddForce` - how does the catcher feel different from the lander?
8. Trigger vs collision - why does `OnCollisionEnter` never fire for the catcher?
9. Find the bug: the sheep tag is spelled `"sheep"` in the code.

## Rebuild plan (with the agent, after SharpDul's basics)

Build it as our own project, in **Unity `6000.3.14f1`** (our standard version), using our
architecture instead of copying the course:

1. Same mechanics, our structure: `GameInput` (Input Actions, keyboard + gamepad + touch),
   `GameManager` singleton with `OnSheepLost` / `OnGameOver` events, a separate `GameUI`.
2. Then make it ours: different falling things, score for catches, difficulty ramp
   (`spawnInterval` shrinking), particles on catch - a natural Particle Lab exercise.
3. Every step becomes SharpDul content: questions + a Mechanics Lab (sliders for
   `moveSpeed`, `spawnInterval`, `spawnRangeX`, bounciness).
