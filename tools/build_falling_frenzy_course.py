"""Builds wwwroot/content/courses/falling-frenzy.json (English source of the course).

Code is written in our own house style (LuaLander/FerryHeist): [SerializeField] private
fields, braces on their own lines, logic separate from UI in the last steps. Lines starting
with '»' are marked as new/changed in that step (the marker is stripped).

Run: python3 tools/build_falling_frenzy_course.py
"""
import json
import pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "src/SharpDul.Pocket/wwwroot/content/courses"


def code(file, src):
    lines, highlight = [], []
    for i, line in enumerate(src.strip("\n").split("\n"), 1):
        if line.startswith("»"):
            highlight.append(i)
            line = line[1:]
        lines.append(line)
    return {"file": file, "text": "\n".join(lines), "highlight": highlight}


FALLING_OBJECT = """
using UnityEngine;

public class FallingObject : MonoBehaviour
{
»    private void OnCollisionEnter(Collision collision)
»    {
»        Debug.Log("Sheep hit " + collision.gameObject.name);
»    }
}
"""

PLAYER_5 = """
using UnityEngine;
using UnityEngine.InputSystem;

public class PlayerController : MonoBehaviour
{
»    [SerializeField] private Rigidbody playerRigidbody;
»    [SerializeField] private float moveSpeed = 20f;

»    private float moveInput;

»    private void Update()
»    {
»        // Read the keys every frame.
»        moveInput = 0f;
»        if (Keyboard.current.aKey.isPressed)
»        {
»            moveInput = -1f;
»        }
»        if (Keyboard.current.dKey.isPressed)
»        {
»            moveInput = 1f;
»        }
»    }

»    private void FixedUpdate()
»    {
»        // Move on the physics step.
»        playerRigidbody.linearVelocity = new Vector3(moveInput * moveSpeed, 0f, 0f);
»    }
}
"""

SPAWNER_6 = """
using UnityEngine;

public class SheepSpawner : MonoBehaviour
{
»    [SerializeField] private GameObject sheepPrefab;
»    [SerializeField] private float spawnInterval = 1f;

»    private float timer;

»    private void Update()
»    {
»        timer += Time.deltaTime;
»        if (timer > spawnInterval)
»        {
»            Instantiate(sheepPrefab, transform.position, sheepPrefab.transform.rotation);
»            timer = 0f;
»        }
»    }
}
"""

PLAYER_7 = """
    private void FixedUpdate()
    {
        // Move on the physics step.
        playerRigidbody.linearVelocity = new Vector3(moveInput * moveSpeed, 0f, 0f);
    }

»    private void OnTriggerEnter(Collider other)
»    {
»        if (other.CompareTag("Sheep"))
»        {
»            // Caught!
»            Destroy(other.gameObject);
»        }
»    }
}
"""

DESTROYER_7 = """
using UnityEngine;

public class SheepDestroyer : MonoBehaviour
{
»    private void OnTriggerEnter(Collider other)
»    {
»        if (other.CompareTag("Sheep"))
»        {
»            Destroy(other.gameObject);
»        }
»    }
}
"""

SPAWNER_8 = """
using UnityEngine;

public class SheepSpawner : MonoBehaviour
{
    [SerializeField] private GameObject sheepPrefab;
    [SerializeField] private float spawnInterval = 1f;
»    [SerializeField] private float spawnRangeX = 10f;

    private float timer;

    private void Update()
    {
        timer += Time.deltaTime;
        if (timer > spawnInterval)
        {
»            float x = Random.Range(-spawnRangeX, spawnRangeX);
»            Vector3 position = new Vector3(x, transform.position.y, transform.position.z);
»            Instantiate(sheepPrefab, position, sheepPrefab.transform.rotation);
            timer = 0f;
        }
    }
}
"""

GAME_MANAGER_9 = """
using TMPro;
using UnityEngine;

public class GameManager : MonoBehaviour
{
»    [SerializeField] private TMP_Text sheepLeftText;
»    [SerializeField] private GameObject gameOverText;
»    [SerializeField] private int startingSheepLeft = 5;

»    private int sheepLeft;

»    private void Start()
»    {
»        sheepLeft = startingSheepLeft;
»        UpdateText();
»    }

»    public void LostSheep()
»    {
»        sheepLeft--;
»        UpdateText();
»        if (sheepLeft <= 0)
»        {
»            gameOverText.SetActive(true);
»            Time.timeScale = 0f;
»        }
»    }

»    private void UpdateText()
»    {
»        sheepLeftText.text = "Sheep Left: " + sheepLeft;
»    }
}
"""

DESTROYER_9 = """
using UnityEngine;

public class SheepDestroyer : MonoBehaviour
{
»    [SerializeField] private GameManager gameManager;

    private void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("Sheep"))
        {
»            gameManager.LostSheep();
            Destroy(other.gameObject);
        }
    }
}
"""

GAME_MANAGER_10 = """
using System;
using UnityEngine;

public class GameManager : MonoBehaviour
{
»    public static GameManager Instance { get; private set; }

»    public event EventHandler OnSheepLeftChanged;
»    public event EventHandler OnGameOver;

    [SerializeField] private int startingSheepLeft = 5;

    private int sheepLeft;

»    private void Awake()
»    {
»        Instance = this;
»        Time.timeScale = 1f;
»        sheepLeft = startingSheepLeft;
»    }

    public void LostSheep()
    {
»        if (sheepLeft <= 0)
»        {
»            return;
»        }

        sheepLeft--;
»        OnSheepLeftChanged?.Invoke(this, EventArgs.Empty);
        if (sheepLeft <= 0)
        {
            Time.timeScale = 0f;
»            OnGameOver?.Invoke(this, EventArgs.Empty);
        }
    }

»    public int GetSheepLeft()
»    {
»        return sheepLeft;
»    }
}
"""

GAME_UI_10 = """
using System;
using TMPro;
using UnityEngine;

public class GameUI : MonoBehaviour
{
»    [SerializeField] private TMP_Text sheepLeftText;
»    [SerializeField] private GameObject gameOverText;

»    private void Start()
»    {
»        GameManager.Instance.OnSheepLeftChanged += GameManager_OnSheepLeftChanged;
»        GameManager.Instance.OnGameOver += GameManager_OnGameOver;
»        gameOverText.SetActive(false);
»        UpdateText();
»    }

»    private void GameManager_OnSheepLeftChanged(object sender, EventArgs e)
»    {
»        UpdateText();
»    }

»    private void GameManager_OnGameOver(object sender, EventArgs e)
»    {
»        gameOverText.SetActive(true);
»    }

»    private void UpdateText()
»    {
»        sheepLeftText.text = "Sheep Left: " + GameManager.Instance.GetSheepLeft();
»    }
}
"""

DESTROYER_10 = """
using UnityEngine;

public class SheepDestroyer : MonoBehaviour
{
    private void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("Sheep"))
        {
»            GameManager.Instance.LostSheep();
            Destroy(other.gameObject);
        }
    }
}
"""

steps = [
    dict(
        id="01-project",
        title="Create the project and the stage",
        goal="An empty Unity project with the camera looking at the play area.",
        actions=[
            "Unity Hub > Projects > New project. Editor Version: 6000.3.14f1. Template: Universal 3D. Project name: FallingFrenzy. Click Create project.",
            "Project window > Assets > Scenes: right-click SampleScene > Rename > FallingFrenzy. Confirm the reload if Unity asks.",
            "Hierarchy > Main Camera. Inspector > Transform > Position: X 0, Y 9, Z -62. Rotation: 0, 0, 0.",
            "Still on Main Camera: Inspector > Camera > Field of View: 20.",
            "File > Save (Ctrl+S).",
        ],
        code=[],
        why=[
            "The game is 3D but plays on one flat plane (X = left/right, Y = up/down). The camera stands far back (Z -62) with a narrow Field of View (20) so the plane looks almost flat - like a 2D game, but with 3D models and light.",
            "Use the same Unity version on every PC (6000.3.14f1) - a newer one can save files the older one cannot read (LuaLander's URP asset lesson).",
        ],
        check="Press Play: an empty grey-blue scene, no errors in Window > General > Console.",
        labStage=1,
    ),
    dict(
        id="02-player",
        title="Place the player (the catcher)",
        goal="A flat box near the bottom of the screen that will catch the sheep.",
        actions=[
            "Hierarchy > + > 3D Object > Cube. Rename it Player (right-click > Rename). It is at the root of the Hierarchy.",
            "Player > Inspector > Transform > Position: X 0, Y -1, Z 0. Scale: X 3, Y 0.5, Z 1.",
            "File > Save.",
        ],
        code=[],
        why=[
            "A Cube comes with a Mesh Filter + Mesh Renderer (what you see) and a Box Collider (what physics feels). They are separate components: you can see things that do not collide and collide with things you cannot see.",
            "Scale changes the collider too, so the 3 x 0.5 box is also a 3 x 0.5 catching area.",
        ],
        check="In the Game view the flat box sits near the bottom centre.",
        labStage=2,
    ),
    dict(
        id="03-first-script",
        title="Your first C# script",
        goal="A script that runs when the game starts and changes its own GameObject.",
        actions=[
            "Project window > Assets: right-click > Create > Folder, name it Scripts.",
            "Inside Assets > Scripts: right-click > Create > Scripting > MonoBehaviour Script, name it HelloWorld.",
            "Double-click HelloWorld to open it. In Start() write: gameObject.name = \"I am game dev!\"; then save the file.",
            "Drag HelloWorld from the Project window onto Player in the Hierarchy.",
            "Press Play, look at the Hierarchy, press Play again to stop.",
            "Clean up: Player > Inspector > Hello World (Script) > ⋮ > Remove Component. Then delete Assets > Scripts > HelloWorld (right-click > Delete).",
        ],
        code=[code("HelloWorld.cs", """
using UnityEngine;

public class HelloWorld : MonoBehaviour
{
»    private void Start()
»    {
»        gameObject.name = "I am game dev!";
»    }
}
""")],
        why=[
            "A MonoBehaviour is a component, like Transform or Box Collider. Unity calls its Start() once, before the first frame, and Update() every frame.",
            "gameObject is the object the script sits on. Changes made in Play mode are undone when you stop - that is why the name comes back.",
        ],
        check="In Play mode Player is renamed to \"I am game dev!\"; after Stop it is Player again.",
        labStage=0,
    ),
    dict(
        id="04-physics",
        title="Physics: a falling, bouncing sheep",
        goal="A sheep (for now a sphere) falls, bounces on the player and reports the hit.",
        actions=[
            "Hierarchy > + > 3D Object > Sphere. Rename it Sheep. Transform > Position: X 0, Y 15, Z 0.",
            "Sheep > Inspector > Add Component > Rigidbody. In Rigidbody > Constraints tick Freeze Position Z.",
            "Project window > Assets: right-click > Create > Folder Physics Materials. Inside it: right-click > Create > Physics Material, name it Bouncy. Inspector: Bounciness 1.",
            "Drag Bouncy onto Sheep > Inspector > Sphere Collider > Material.",
            "Assets > Scripts: right-click > Create > Scripting > MonoBehaviour Script FallingObject. Write the code below and drag it onto Sheep.",
            "Press Play.",
        ],
        code=[code("FallingObject.cs", FALLING_OBJECT)],
        why=[
            "A Rigidbody hands the object to the physics engine: gravity, velocity, collisions. Without it the sphere is just scenery.",
            "Freeze Position Z keeps the sheep on our flat play plane, so it never rolls towards or away from the camera.",
            "OnCollisionEnter runs when two solid colliders touch and at least one has a Rigidbody. The Collision parameter tells you what was hit.",
            "Bounciness 1 on the sheep and 0 on the player average to 0.5 (Bounce Combine = Average), so each bounce is about half as high.",
        ],
        check="The sphere drops, bounces on Player a few times and the Console prints \"Sheep hit Player\".",
        labStage=4,
    ),
    dict(
        id="05-input",
        title="Move the player with A and D",
        goal="The catcher slides left and right, stops instantly when you let go.",
        actions=[
            "Assets > Scripts: create a MonoBehaviour Script PlayerController with the code below and drag it onto Player.",
            "Player > Inspector > Add Component > Rigidbody. Untick Use Gravity. Constraints: tick Freeze Position Y and Z, and Freeze Rotation X, Y and Z.",
            "Drag the Rigidbody component (its title bar) from Player's Inspector into PlayerController > Player Rigidbody. It must not stay None.",
            "PlayerController > Move Speed: 20.",
            "Press Play and hold A / D.",
        ],
        code=[code("PlayerController.cs", PLAYER_5)],
        why=[
            "Input is read in Update (every frame, so no key press is missed); the body moves in FixedUpdate (the physics step). The moveInput field carries the value between the two.",
            "Setting linearVelocity throws away the old motion: instant start, instant stop - an arcade feel. LuaLander uses AddForce instead and gets momentum. Try both in the Lab preview below.",
            "Holding A and D together moves right: the D check runs last and wins.",
            "A new [SerializeField] shows up as None in the Inspector. Nothing warns you until Play mode throws a NullReferenceException - always assign it right away.",
        ],
        check="A moves the box left, D right; letting go stops it at once. The sheep still bounces on it.",
        labStage=5,
    ),
    dict(
        id="06-spawner",
        title="A prefab and a spawner: endless sheep",
        goal="A new sheep drops from the top centre every second.",
        actions=[
            "Sheep > Inspector > Falling Object (Script) > ⋮ > Remove Component (we no longer need the log).",
            "Project window > Assets: create a folder Prefabs. Drag Sheep from the Hierarchy into Assets > Prefabs. It turns blue in the Hierarchy - it is now a prefab.",
            "Delete the Sheep from the Hierarchy (right-click > Delete). The prefab in Assets > Prefabs stays.",
            "Hierarchy > + > Create Empty. Rename it Sheep Spawner. Transform > Position: X 0, Y 20, Z 0.",
            "Create the SheepSpawner script below and drag it onto Sheep Spawner. Drag Assets > Prefabs > Sheep into its Sheep Prefab field.",
            "Press Play.",
        ],
        code=[code("SheepSpawner.cs", SPAWNER_6)],
        why=[
            "A prefab is a saved GameObject template. Instantiate makes a live copy of it in the scene - every sheep is a clone of the same prefab.",
            "The timer counts real seconds (Time.deltaTime), fires when it passes spawnInterval and resets to 0. No coroutine needed.",
            "Passing sheepPrefab.transform.rotation keeps each copy turned the way the prefab is.",
        ],
        check="Every second a sphere appears at the top centre and falls. They bounce off the player and pile up or fall away.",
        labStage=6,
    ),
    dict(
        id="07-triggers",
        title="Catch and lose: triggers and tags",
        goal="Sheep that touch the catcher disappear; sheep that fall past it are destroyed below the screen.",
        actions=[
            "Tag the prefab: double-click Assets > Prefabs > Sheep. Inspector > Tag > Add Tag... > + > type Sheep > Save. Select the Sheep prefab again and set Tag: Sheep. Leave the prefab with the < arrow in the Hierarchy.",
            "Player > Inspector > Box Collider: tick Is Trigger.",
            "Add the OnTriggerEnter method below to PlayerController.",
            "Hierarchy > + > Create Empty, name it Sheep Destroyer. Position: X 0, Y -10, Z 0. Add Component > Box Collider: Is Trigger ticked, Size X 100, Y 1, Z 100.",
            "Create the SheepDestroyer script below and drag it onto Sheep Destroyer.",
            "Press Play.",
        ],
        code=[code("PlayerController.cs (end of the file)", PLAYER_7), code("SheepDestroyer.cs", DESTROYER_7)],
        why=[
            "A trigger collider does not block anything - objects pass through and Unity only calls OnTriggerEnter. A solid collider calls OnCollisionEnter and bounces. That is why the sheep stopped bouncing.",
            "CompareTag(\"Sheep\") is faster than tag == \"Sheep\" and reports a typo in the tag name as an error instead of silently never matching.",
            "The destroyer sits below the screen and is huge (100 x 100), so no sheep can miss it. Without it, missed sheep would fall forever and pile up in memory.",
        ],
        check="Sheep that hit the box vanish. Sheep that miss fall off the screen; in the Hierarchy you see clones appear and disappear.",
        labStage=7,
    ),
    dict(
        id="08-random-x",
        title="Random positions: design the level",
        goal="Sheep drop from random places across the whole width.",
        actions=[
            "Change SheepSpawner to the code below.",
            "Sheep Spawner > Inspector > Sheep Spawner (Script) > Spawn Range X: 15.",
            "Optional: Hierarchy > + > 3D Object > Cube a few times as background scenery (e.g. tall pillars far behind at Z 80). Give them a look; they do not touch the play plane.",
            "Press Play.",
        ],
        code=[code("SheepSpawner.cs", SPAWNER_8)],
        why=[
            "Random.Range(-spawnRangeX, spawnRangeX) gives a float between -15 and 15, ends included. Y and Z come from the spawner, so only X changes.",
            "The script says 10, the Inspector says 15 - the game uses 15. A [SerializeField] default applies only when the component is first added; after that the scene's saved value wins.",
        ],
        check="Sheep fall from all over the top edge. Catching them gets harder.",
        labStage=8,
    ),
    dict(
        id="09-game-over",
        title="Sheep counter and Game Over",
        goal="\"Sheep Left: 5\" counts down for every missed sheep; at 0 the game says GAME OVER and freezes.",
        actions=[
            "Hierarchy > + > UI > Text - TextMeshPro. If Unity asks, click Import TMP Essentials, then close the window. A Canvas and an EventSystem appear; rename the text Sheep Left Text.",
            "Sheep Left Text > Inspector > Rect Transform: anchor preset top-left (click the square, hold Alt+Shift, pick top-left). Font Size 36. Text: Sheep Left: 5.",
            "Canvas > right-click > UI > Text - TextMeshPro again, name it Game Over Text. Anchor: middle-centre, Font Size 72, Alignment centre, Text: GAME OVER. Untick the checkbox next to its name to hide it.",
            "Hierarchy > + > Create Empty, name it Game Manager. Create the GameManager script below and drag it onto it.",
            "Game Manager > Inspector: drag Sheep Left Text into Sheep Left Text, Game Over Text into Game Over Text. Starting Sheep Left: 5.",
            "Change SheepDestroyer to the code below. Sheep Destroyer > Inspector: drag Game Manager into its Game Manager field.",
            "Press Play and miss five sheep.",
        ],
        code=[code("GameManager.cs", GAME_MANAGER_9), code("SheepDestroyer.cs", DESTROYER_9)],
        why=[
            "startingSheepLeft is the designer's number; sheepLeft is the live one. Copying it in Start keeps the two apart.",
            "Time.timeScale = 0 stops physics and Time.deltaTime, so sheep freeze and the spawner timer stops. Update still runs - that is how a pause menu can still read keys.",
            "<= 0 instead of == 0: safe even if two sheep land in the same frame.",
            "This step has three new Inspector fields. If one stays None, the first lost sheep throws a NullReferenceException - the classic scene-wiring bug.",
        ],
        check="The counter goes 5, 4, 3, 2, 1, 0 as sheep fall past; at 0 GAME OVER appears and everything stops.",
        labStage=9,
    ),
    dict(
        id="10-level-up",
        title="Level up: our architecture (singleton + events)",
        goal="Same game, but built like LuaLander and FerryHeist: GameManager only counts, a GameUI listens and draws.",
        actions=[
            "Replace GameManager with the code below. Its two text fields disappear from the Inspector - that is expected.",
            "Create the GameUI script below and drag it onto Canvas. Canvas > Game UI: drag Sheep Left Text and Game Over Text into its fields.",
            "Replace SheepDestroyer with the code below. Its Game Manager field disappears - no more wiring.",
            "Check Game Over Text: it may stay ticked now; GameUI hides it at start.",
            "Press Play and play until Game Over.",
        ],
        code=[code("GameManager.cs", GAME_MANAGER_10), code("GameUI.cs", GAME_UI_10), code("SheepDestroyer.cs", DESTROYER_10)],
        why=[
            "Singleton: GameManager stores itself in a static Instance in Awake, so any script reaches it as GameManager.Instance - no Inspector field to forget.",
            "Events: GameManager only announces \"sheep left changed\" and \"game over\". GameUI listens and updates the text. Logic never touches UI - you can redesign the UI without opening GameManager.",
            "Instance is set in Awake, listeners subscribe in Start: every Awake runs before any Start, so Instance is ready when GameUI asks.",
            "Time.timeScale = 1 in Awake: timeScale survives a scene reload, so a future Restart button would otherwise load a frozen game (a LuaLander lesson).",
        ],
        check="The game plays exactly as after step 9 - the change is inside, and the Inspector has fewer fields to wire.",
        labStage=10,
    ),
    dict(
        id="11-make-it-yours",
        title="Make it yours",
        goal="The course game is done. Now it becomes your game - you decide what comes next.",
        actions=[
            "Pick one idea and tell the agent - we build it together, step by step like this course:",
            "Score: +1 for every caught sheep, shown next to Sheep Left (a new event OnSheepCaught).",
            "Difficulty ramp: spawnInterval shrinks a little after every catch, down to a minimum.",
            "Particles: a puff when a sheep is caught - a first Particle Lab exercise.",
            "Restart: a button on Game Over that reloads the scene (Time.timeScale = 1 is already handled).",
            "Real models: swap the sphere and cube for your own Blender sheep and catcher.",
        ],
        code=[],
        why=[
            "Every idea reuses what you just built: events (score), timers (difficulty), prefabs (particles), scenes and timeScale (restart).",
            "Once a part is built, SharpDul can quiz you on it - quizzes only cover what you have built yourself.",
        ],
        check="You have a playable Falling Frenzy built from scratch.",
        labStage=10,
    ),
]

course = dict(
    id="falling-frenzy",
    title="Falling Frenzy",
    description="Build GameDevTV's Unity Fundamentals game from scratch in Unity 6000.3.14f1: physics, input, prefabs, triggers, UI - and then our own architecture.",
    source="Based on GameDevTV, Unity Fundamentals - gitlab.com/GameDevTV/unity-fundamentals/course/falling-frenzy. Code rewritten in our house style.",
    labPath="lab/falling-frenzy",
    steps=steps,
)

OUT.mkdir(parents=True, exist_ok=True)
(OUT / "falling-frenzy.json").write_text(json.dumps(course, indent=2, ensure_ascii=False) + "\n")
(OUT / "index.json").write_text(json.dumps({"courses": ["falling-frenzy.json"]}, indent=2) + "\n")
print(f"{len(steps)} steps written")
