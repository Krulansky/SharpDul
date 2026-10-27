"""Builds wwwroot/content/builds/falling-frenzy.json: the Build Lab puzzles (English source).

Line format: "#" = given (locked) line; no "#" = a line the player taps into place.
"{{right|wrong|wrong}}" = a blank, first option right (the app shuffles the options).
Code matches the Unity course (tools/build_falling_frenzy_course.py).

Run: python3 tools/build_falling_frenzy_puzzles.py
"""
import json
import pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "src/SharpDul.Pocket/wwwroot/content/builds"


def lines(src):
    return src.strip("\n").split("\n")


puzzles = [
    dict(
        id="falling-object",
        title="FallingObject: report the hit",
        file="FallingObject.cs",
        context="The sheep already falls and bounces - a Rigidbody does that without any code. This script sits on the Sheep and writes to the Console when it hits something solid.",
        hint="Solid things hitting each other call OnCollisionEnter. OnTriggerEnter is for triggers - the player is not one yet. The name of what you hit is on its gameObject.",
        success="Every bounce now writes \"Sheep hit Player\" to the Console under the game.",
        lines=lines("""
#using UnityEngine;
#
#public class FallingObject : MonoBehaviour
#{
    private void OnCollisionEnter(Collision collision)
#    {
        Debug.Log("Sheep hit " + collision.gameObject.{{name|tag|layer}});
#    }
#}
"""),
        distractors=["    private void OnTriggerEnter(Collider other)"],
        alternatives=[],
        unlocks=["CollisionLog"],
    ),
    dict(
        id="player-input",
        title="PlayerController: read the keys",
        file="PlayerController.cs",
        context="This script sits on the Player. First half: every frame, turn the A and D keys into one number, moveInput (-1 left, 0 nothing, 1 right).",
        hint="Reset moveInput to 0 first, then let A set -1 and D set 1. Which Unity method runs every frame?",
        success="The keys are read - watch the code light up when you hold A or D. But the player does not move yet: nothing uses moveInput.",
        lines=lines("""
#using UnityEngine;
#using UnityEngine.InputSystem;
#
#public class PlayerController : MonoBehaviour
#{
#    [SerializeField] private Rigidbody playerRigidbody;
#    [SerializeField] private float moveSpeed = 20f;
#
#    private float moveInput;
#
#    private void {{Update|FixedUpdate|Start}}()
#    {
        moveInput = 0f;
        if (Keyboard.current.aKey.isPressed)
#        {
            moveInput = -1f;
#        }
        if (Keyboard.current.dKey.isPressed)
#        {
            moveInput = 1f;
#        }
#    }
#}
"""),
        distractors=[],
        # D block first, then A block: also correct (A would then win when both are held).
        alternatives=[[0, 3, 4, 1, 2]],
        unlocks=["ReadInput"],
    ),
    dict(
        id="player-move",
        title="PlayerController: move on the physics step",
        file="PlayerController.cs",
        context="Second half of the same script: on every physics step, turn moveInput into a velocity for the Rigidbody.",
        hint="Speed = direction x how fast. Give the velocity to the Rigidbody - moving the transform directly would fight the physics.",
        success="The player moves! Arcade feel: it starts and stops at once, because linearVelocity replaces the old motion.",
        lines=lines("""
#public class PlayerController : MonoBehaviour
#{
#    // ... fields and Update() from before ...
#
#    private void FixedUpdate()
#    {
        Vector3 velocity = new Vector3(moveInput * {{moveSpeed|moveInput|Time.deltaTime}}, 0f, 0f);
        playerRigidbody.linearVelocity = velocity;
#    }
#}
"""),
        distractors=["        transform.position = velocity;"],
        alternatives=[],
        unlocks=["Move"],
    ),
    dict(
        id="sheep-spawner",
        title="SheepSpawner: a sheep every second",
        file="SheepSpawner.cs",
        context="An empty GameObject at the top of the screen. It counts time and, when spawnInterval has passed, makes a new copy of the Sheep prefab.",
        hint="Add the frame's time to the timer. When it is bigger than spawnInterval: Instantiate, then reset the timer.",
        success="Endless sheep from the top centre. The player is still solid, so they bounce off it.",
        lines=lines("""
#using UnityEngine;
#
#public class SheepSpawner : MonoBehaviour
#{
#    [SerializeField] private GameObject sheepPrefab;
#    [SerializeField] private float spawnInterval = 1f;
#
#    private float timer;
#
#    private void Update()
#    {
        timer += Time.{{deltaTime|time|frameCount}};
        if (timer > spawnInterval)
#        {
            Instantiate(sheepPrefab, transform.position, sheepPrefab.transform.rotation);
            timer = 0f;
#        }
#    }
#}
"""),
        distractors=[],
        alternatives=[[0, 1, 3, 2]],
        unlocks=["Spawner"],
    ),
    dict(
        id="player-catch",
        title="PlayerController: catch!",
        file="PlayerController.cs",
        context="The Player's Box Collider gets Is Trigger ticked, so sheep pass into it instead of bouncing. This method runs when something enters the trigger.",
        hint="Trigger colliders call OnTriggerEnter. Check the tag, then destroy what came in - careful: gameObject alone is the player itself.",
        success="Caught sheep vanish with a green puff. Missed ones fall off the screen... for ever, for now.",
        lines=lines("""
#public class PlayerController : MonoBehaviour
#{
#    // ... fields, Update() and FixedUpdate() from before ...
#
    private void OnTriggerEnter(Collider other)
#    {
        if (other.{{CompareTag|GetComponent|SetActive}}("Sheep"))
#        {
            Destroy(other.gameObject);
#        }
#    }
#}
"""),
        distractors=["            Destroy(gameObject);", "    private void OnCollisionEnter(Collision collision)"],
        alternatives=[],
        unlocks=["Catch"],
    ),
    dict(
        id="sheep-destroyer",
        title="SheepDestroyer: clean up the missed ones",
        file="SheepDestroyer.cs",
        context="A huge invisible trigger box far below the screen (y -10, 100 x 100). Every sheep that misses the player ends here.",
        hint="Same pattern as the catch: check the tag, destroy the other object. Destroy needs the whole GameObject, not one of its components.",
        success="Missed sheep are destroyed below the screen, so they no longer pile up in memory.",
        lines=lines("""
#using UnityEngine;
#
#public class SheepDestroyer : MonoBehaviour
#{
#    private void OnTriggerEnter(Collider other)
#    {
        if (other.CompareTag("Sheep"))
#        {
            Destroy(other.{{gameObject|transform|tag}});
#        }
#    }
#}
"""),
        distractors=[],
        alternatives=[],
        unlocks=["Destroyer"],
    ),
    dict(
        id="random-x",
        title="SheepSpawner: random positions",
        file="SheepSpawner.cs",
        context="Change the spawner: pick a random X between -spawnRangeX and spawnRangeX, keep the spawner's Y and Z.",
        hint="Random.Range(min, max). Build the position from x and the spawner's y and z, then spawn there instead of at transform.position.",
        success="Sheep rain from the whole width. Try the spawnRangeX slider - 0 puts them all back in the middle.",
        lines=lines("""
#    [SerializeField] private float spawnRangeX = 10f;
#
#    private void Update()
#    {
#        timer += Time.deltaTime;
#        if (timer > spawnInterval)
#        {
            float x = Random.Range({{-spawnRangeX|0f|spawnInterval}}, spawnRangeX);
            Vector3 position = new Vector3(x, transform.position.y, transform.position.z);
            Instantiate(sheepPrefab, {{position|transform.position|Vector3.zero}}, sheepPrefab.transform.rotation);
#            timer = 0f;
#        }
#    }
"""),
        distractors=[],
        alternatives=[],
        unlocks=["RandomX"],
    ),
    dict(
        id="game-manager",
        title="GameManager: count the sheep",
        file="GameManager.cs",
        context="An empty Game Manager object. It keeps the number of sheep left, shows it in the UI text, and ends the game at 0.",
        hint="Start: copy the starting value, then show it. LostSheep: one less, show it, and if none are left - show GAME OVER and stop time.",
        success="\"Sheep Left: 5\" is on screen. But it never goes down: nobody calls LostSheep() yet.",
        lines=lines("""
#using TMPro;
#using UnityEngine;
#
#public class GameManager : MonoBehaviour
#{
#    [SerializeField] private TMP_Text sheepLeftText;
#    [SerializeField] private GameObject gameOverText;
#    [SerializeField] private int startingSheepLeft = 5;
#
#    private int sheepLeft;
#
#    private void Start()
#    {
        sheepLeft = startingSheepLeft;
        UpdateText();
#    }
#
#    public void LostSheep()
#    {
        sheepLeft--;
        UpdateText();
        if (sheepLeft {{<=|==|>}} 0)
#        {
            gameOverText.SetActive(true);
            Time.timeScale = {{0f|1f|-1f}};
#        }
#    }
#
#    private void UpdateText()
#    {
#        sheepLeftText.text = "Sheep Left: " + sheepLeft;
#    }
#}
"""),
        distractors=[],
        alternatives=[[0, 1, 2, 3, 4, 6, 5]],
        unlocks=["Counter"],
    ),
    dict(
        id="destroyer-lost-sheep",
        title="SheepDestroyer: tell the GameManager",
        file="SheepDestroyer.cs",
        context="Connect the two: the destroyer gets a reference to the GameManager (assigned in the Inspector) and reports every missed sheep.",
        hint="A [SerializeField] field for the GameManager, then call its public method - the private UpdateText cannot be called from outside.",
        success="The counter counts down and at 0 the game freezes: Time.timeScale = 0. You built the whole game!",
        lines=lines("""
#using UnityEngine;
#
#public class SheepDestroyer : MonoBehaviour
#{
    [SerializeField] private GameManager gameManager;
#
#    private void OnTriggerEnter(Collider other)
#    {
#        if (other.CompareTag("Sheep"))
#        {
            gameManager.{{LostSheep|UpdateText|Start}}();
#            Destroy(other.gameObject);
#        }
#    }
#}
"""),
        distractors=[],
        alternatives=[],
        unlocks=["CounterLinked"],
    ),
    dict(
        id="level-up-events",
        title="Level up: GameManager as a singleton with events",
        file="GameManager.cs",
        context="Our architecture (LuaLander, FerryHeist): GameManager stores itself in a static Instance and only announces changes through an event. It no longer touches the UI.",
        hint="The static property holds the one GameManager; in Awake it stores itself. After counting down, fire the event - ?. so it is safe with no listeners.",
        success="Same game on screen - but now the logic only fires events. The SheepDestroyer reaches it as GameManager.Instance, no Inspector field.",
        lines=lines("""
#using System;
#using UnityEngine;
#
#public class GameManager : MonoBehaviour
#{
    public static GameManager Instance { get; private set; }
    public event EventHandler OnSheepLeftChanged;
#
#    [SerializeField] private int startingSheepLeft = 5;
#    private int sheepLeft;
#
#    private void Awake()
#    {
        Instance = {{this|null|gameObject}};
#        sheepLeft = startingSheepLeft;
#    }
#
#    public void LostSheep()
#    {
#        sheepLeft--;
        OnSheepLeftChanged{{?.|.|!}}Invoke(this, EventArgs.Empty);
#        // ... game over as before ...
#    }
#}
"""),
        distractors=["        sheepLeftText.text = \"Sheep Left: \" + sheepLeft;"],
        alternatives=[[1, 0, 2, 3]],
        unlocks=["Events"],
    ),
    dict(
        id="game-ui",
        title="GameUI: listen and draw",
        file="GameUI.cs",
        context="A new script on the Canvas. It subscribes to OnSheepLeftChanged and updates the text whenever the GameManager announces a change.",
        hint="Subscribe with += in the method that runs after every Awake. When the event fires, update the text.",
        success="Logic and UI are apart, the way all our games are built. Falling Frenzy is done - now build it for real in Unity with the course!",
        lines=lines("""
#using System;
#using TMPro;
#using UnityEngine;
#
#public class GameUI : MonoBehaviour
#{
#    [SerializeField] private TMP_Text sheepLeftText;
#
#    private void {{Start|Awake|OnDestroy}}()
#    {
        GameManager.Instance.OnSheepLeftChanged {{+=|=|-=}} GameManager_OnSheepLeftChanged;
        UpdateText();
#    }
#
#    private void GameManager_OnSheepLeftChanged(object sender, EventArgs e)
#    {
        UpdateText();
#    }
#
#    private void UpdateText()
#    {
#        sheepLeftText.text = "Sheep Left: " + GameManager.Instance.GetSheepLeft();
#    }
#}
"""),
        distractors=[],
        # UpdateText() before subscribing is also fine in Start.
        alternatives=[[1, 0, 2]],
        unlocks=["EventsUI"],
    ),
]

build = dict(
    id="falling-frenzy",
    title="Falling Frenzy",
    description="Crack the scripts one by one - every solved script switches its part of the game on.",
    courseId="falling-frenzy",
    puzzles=puzzles,
)

OUT.mkdir(parents=True, exist_ok=True)
(OUT / "falling-frenzy.json").write_text(json.dumps(build, indent=2, ensure_ascii=False) + "\n")
(OUT / "index.json").write_text(json.dumps({"builds": ["falling-frenzy.json"]}, indent=2) + "\n")
print(f"{len(puzzles)} puzzles written")
