"""Korean text of the Falling Frenzy course. Unity menu paths and gamedev terms stay English.
Run: python3 tools/falling_frenzy_course_ko.py
"""
import json
import pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "src/SharpDul.Pocket/wwwroot/content/courses/falling-frenzy.ko.json"

steps = {
    "01-project": dict(
        title="프로젝트와 무대 만들기",
        goal="카메라가 플레이 영역을 바라보는 빈 Unity 프로젝트.",
        actions=[
            "Unity Hub > Projects > New project. Editor Version: 6000.3.14f1. Template: Universal 3D. Project name: FallingFrenzy. Create project를 클릭하세요.",
            "Project 창 > Assets > Scenes: SampleScene을 우클릭 > Rename > FallingFrenzy. Unity가 reload를 물으면 확인하세요.",
            "Hierarchy > Main Camera. Inspector > Transform > Position: X 0, Y 9, Z -62. Rotation: 0, 0, 0.",
            "Main Camera를 선택한 채로: Inspector > Camera > Field of View: 20.",
            "File > Save (Ctrl+S).",
        ],
        why=[
            "게임은 3D지만 하나의 평면 위에서 진행돼요 (X = 좌우, Y = 위아래). 카메라가 멀리 (Z -62) 좁은 Field of View (20)로 서 있어서 평면이 거의 평평하게 보여요 - 2D 게임처럼 보이지만 3D 모델과 조명을 쓸 수 있어요.",
            "모든 PC에서 같은 Unity 버전 (6000.3.14f1)을 쓰세요 - 새 버전이 저장한 파일을 옛 버전이 못 읽을 수 있어요 (LuaLander의 URP asset 교훈).",
        ],
        check="Play를 누르면: 빈 회청색 scene, Window > General > Console에 에러 없음.",
    ),
    "02-player": dict(
        title="플레이어 (캐처) 배치하기",
        goal="화면 아래쪽에 양을 받을 납작한 상자.",
        actions=[
            "Hierarchy > + > 3D Object > Cube. 이름을 Player로 바꾸세요 (우클릭 > Rename). Hierarchy의 root에 있어요.",
            "Player > Inspector > Transform > Position: X 0, Y -1, Z 0. Scale: X 3, Y 0.5, Z 1.",
            "File > Save.",
        ],
        why=[
            "Cube에는 Mesh Filter + Mesh Renderer (보이는 것)와 Box Collider (물리가 느끼는 것)가 있어요. 서로 다른 component라서, 보이지만 충돌하지 않는 것도, 안 보이지만 충돌하는 것도 만들 수 있어요.",
            "Scale은 collider도 바꾸니까, 3 x 0.5 상자는 곧 3 x 0.5 크기의 받는 영역이에요.",
        ],
        check="Game view에서 납작한 상자가 아래 가운데에 있어요.",
    ),
    "03-first-script": dict(
        title="첫 번째 C# script",
        goal="게임이 시작될 때 실행되어 자신의 GameObject를 바꾸는 script.",
        actions=[
            "Project 창 > Assets: 우클릭 > Create > Folder, 이름은 Scripts.",
            "Assets > Scripts 안에서: 우클릭 > Create > Scripting > MonoBehaviour Script, 이름은 HelloWorld.",
            "HelloWorld를 더블클릭해서 여세요. Start() 안에 gameObject.name = \"I am game dev!\"; 를 쓰고 파일을 저장하세요.",
            "Project 창의 HelloWorld를 Hierarchy의 Player 위로 드래그하세요.",
            "Play를 누르고 Hierarchy를 본 다음, Play를 다시 눌러 멈추세요.",
            "정리: Player > Inspector > Hello World (Script) > ⋮ > Remove Component. 그리고 Assets > Scripts > HelloWorld를 삭제하세요 (우클릭 > Delete).",
        ],
        why=[
            "MonoBehaviour는 Transform이나 Box Collider 같은 component예요. Unity는 Start()를 첫 frame 전에 한 번, Update()를 매 frame 호출해요.",
            "gameObject는 script가 붙어 있는 객체예요. Play mode에서 바꾼 것은 멈추면 되돌아가요 - 그래서 이름이 원래대로 돌아와요.",
        ],
        check="Play mode에서 Player 이름이 \"I am game dev!\"로 바뀌고, Stop 후에는 다시 Player예요.",
    ),
    "04-physics": dict(
        title="물리: 떨어지고 튀는 양",
        goal="양 (지금은 구)이 떨어져서 플레이어에 튕기고 충돌을 알려요.",
        actions=[
            "Hierarchy > + > 3D Object > Sphere. 이름을 Sheep으로. Transform > Position: X 0, Y 15, Z 0.",
            "Sheep > Inspector > Add Component > Rigidbody. Rigidbody > Constraints에서 Freeze Position Z를 체크하세요.",
            "Project 창 > Assets: 우클릭 > Create > Folder Physics Materials. 그 안에서: 우클릭 > Create > Physics Material, 이름은 Bouncy. Inspector: Bounciness 1.",
            "Bouncy를 Sheep > Inspector > Sphere Collider > Material로 드래그하세요.",
            "Assets > Scripts: 우클릭 > Create > Scripting > MonoBehaviour Script FallingObject. 아래 코드를 쓰고 Sheep에 드래그하세요.",
            "Play를 누르세요.",
        ],
        why=[
            "Rigidbody는 객체를 물리 엔진에 맡겨요: 중력, 속도, 충돌. Rigidbody가 없으면 구는 그냥 배경이에요.",
            "Freeze Position Z는 양을 평평한 플레이 평면 위에 붙잡아서, 카메라 쪽이나 반대쪽으로 굴러가지 않게 해요.",
            "OnCollisionEnter는 단단한 collider 두 개가 닿고 그중 하나 이상에 Rigidbody가 있을 때 실행돼요. Collision 파라미터가 무엇에 부딪혔는지 알려줘요.",
            "양의 Bounciness 1과 플레이어의 0을 평균하면 0.5 (Bounce Combine = Average)라서, 튈 때마다 높이가 대략 절반이 돼요.",
        ],
        check="구가 떨어져서 Player 위에서 몇 번 튀고, Console에 \"Sheep hit Player\"가 찍혀요.",
    ),
    "05-input": dict(
        title="A와 D로 플레이어 움직이기",
        goal="캐처가 좌우로 움직이고, 키를 놓으면 바로 멈춰요.",
        actions=[
            "Assets > Scripts: 아래 코드로 MonoBehaviour Script PlayerController를 만들고 Player에 드래그하세요.",
            "Player > Inspector > Add Component > Rigidbody. Use Gravity 체크 해제. Constraints: Freeze Position Y와 Z, Freeze Rotation X, Y, Z를 체크하세요.",
            "Player Inspector의 Rigidbody component (제목 표시줄)를 PlayerController > Player Rigidbody로 드래그하세요. None으로 남으면 안 돼요.",
            "PlayerController > Move Speed: 20.",
            "Play를 누르고 A / D를 누르고 있으세요.",
        ],
        why=[
            "입력은 Update에서 읽고 (매 frame, 키 입력을 놓치지 않도록), 몸체는 FixedUpdate (물리 step)에서 움직여요. moveInput field가 둘 사이에서 값을 전달해요.",
            "linearVelocity를 설정하면 이전 움직임이 사라져요: 바로 출발, 바로 정지 - 아케이드 느낌. LuaLander는 대신 AddForce를 써서 관성이 생겨요. 아래 Lab 미리보기에서 둘 다 해 보세요.",
            "A와 D를 동시에 누르면 오른쪽으로 가요: D 검사가 마지막에 실행되어 이겨요.",
            "새 [SerializeField]는 Inspector에 None으로 나타나요. Play mode에서 NullReferenceException이 날 때까지 아무 경고가 없으니 바로 연결하세요.",
        ],
        check="A는 상자를 왼쪽으로, D는 오른쪽으로 움직이고, 놓으면 바로 멈춰요. 양은 여전히 그 위에서 튀어요.",
    ),
    "06-spawner": dict(
        title="Prefab과 spawner: 끝없는 양",
        goal="매초 새 양이 위쪽 가운데에서 떨어져요.",
        actions=[
            "Sheep > Inspector > Falling Object (Script) > ⋮ > Remove Component (log는 이제 필요 없어요).",
            "Project 창 > Assets: Prefabs 폴더를 만드세요. Hierarchy의 Sheep을 Assets > Prefabs로 드래그하세요. Hierarchy에서 파랗게 변해요 - 이제 prefab이에요.",
            "Hierarchy에서 Sheep을 삭제하세요 (우클릭 > Delete). Assets > Prefabs의 prefab은 남아요.",
            "Hierarchy > + > Create Empty. 이름을 Sheep Spawner로. Transform > Position: X 0, Y 20, Z 0.",
            "아래 SheepSpawner script를 만들어 Sheep Spawner에 드래그하세요. Assets > Prefabs > Sheep을 Sheep Prefab 칸에 드래그하세요.",
            "Play를 누르세요.",
        ],
        why=[
            "Prefab은 저장된 GameObject 템플릿이에요. Instantiate는 그것의 살아 있는 복사본을 scene에 만들어요 - 모든 양은 같은 prefab의 클론이에요.",
            "timer는 실제 초 (Time.deltaTime)를 세고, spawnInterval을 넘으면 실행한 뒤 0으로 돌아가요. coroutine이 필요 없어요.",
            "sheepPrefab.transform.rotation을 넘기면 각 복사본이 prefab과 같은 방향을 유지해요.",
        ],
        check="매초 위쪽 가운데에 구가 나타나 떨어져요. 플레이어에서 튀고 쌓이거나 떨어져 나가요.",
    ),
    "07-triggers": dict(
        title="받기와 놓치기: trigger와 tag",
        goal="캐처에 닿은 양은 사라지고, 놓친 양은 화면 아래에서 파괴돼요.",
        actions=[
            "prefab에 tag 달기: Assets > Prefabs > Sheep을 더블클릭. Inspector > Tag > Add Tag... > + > Sheep 입력 > Save. Sheep prefab을 다시 선택하고 Tag: Sheep으로 설정하세요. Hierarchy의 < 화살표로 prefab에서 나오세요.",
            "Player > Inspector > Box Collider: Is Trigger를 체크하세요.",
            "아래 OnTriggerEnter method를 PlayerController에 추가하세요.",
            "Hierarchy > + > Create Empty, 이름은 Sheep Destroyer. Position: X 0, Y -10, Z 0. Add Component > Box Collider: Is Trigger 체크, Size X 100, Y 1, Z 100.",
            "아래 SheepDestroyer script를 만들어 Sheep Destroyer에 드래그하세요.",
            "Play를 누르세요.",
        ],
        why=[
            "trigger collider는 아무것도 막지 않아요 - 물체가 통과하고 Unity는 OnTriggerEnter만 호출해요. 단단한 collider는 OnCollisionEnter를 호출하고 튕겨요. 그래서 양이 더 이상 튀지 않아요.",
            "CompareTag(\"Sheep\")는 tag == \"Sheep\"보다 빠르고, tag 이름 오타를 조용히 무시하지 않고 에러로 알려줘요.",
            "destroyer는 화면 아래에 있고 아주 커서 (100 x 100) 어떤 양도 놓칠 수 없어요. 없으면 놓친 양이 영원히 떨어지며 메모리에 쌓여요.",
        ],
        check="상자에 닿은 양은 사라져요. 놓친 양은 화면 밖으로 떨어지고, Hierarchy에서 클론이 생겼다 사라지는 게 보여요.",
    ),
    "08-random-x": dict(
        title="무작위 위치: 레벨 디자인",
        goal="양이 화면 전체 너비의 무작위 위치에서 떨어져요.",
        actions=[
            "SheepSpawner를 아래 코드로 바꾸세요.",
            "Sheep Spawner > Inspector > Sheep Spawner (Script) > Spawn Range X: 15.",
            "선택: Hierarchy > + > 3D Object > Cube를 몇 번 추가해 배경 장식으로 쓰세요 (예: Z 80 먼 뒤쪽의 높은 기둥). 플레이 평면에는 닿지 않아요.",
            "Play를 누르세요.",
        ],
        why=[
            "Random.Range(-spawnRangeX, spawnRangeX)는 -15와 15 사이의 float을 줘요 (양 끝 포함). Y와 Z는 spawner에서 가져오니까 X만 바뀌어요.",
            "script에는 10, Inspector에는 15 - 게임은 15를 써요. [SerializeField] 기본값은 component를 처음 추가할 때만 적용되고, 그 뒤에는 scene에 저장된 값이 이겨요.",
        ],
        check="양이 위쪽 가장자리 전체에서 떨어져요. 받기가 더 어려워져요.",
    ),
    "09-game-over": dict(
        title="양 카운터와 Game Over",
        goal="\"Sheep Left: 5\"가 놓친 양마다 줄어들고, 0이 되면 GAME OVER가 뜨고 멈춰요.",
        actions=[
            "Hierarchy > + > UI > Text - TextMeshPro. Unity가 물으면 Import TMP Essentials를 클릭하고 창을 닫으세요. Canvas와 EventSystem이 생겨요. 텍스트 이름을 Sheep Left Text로 바꾸세요.",
            "Sheep Left Text > Inspector > Rect Transform: anchor preset 왼쪽 위 (사각형 클릭, Alt+Shift를 누른 채 왼쪽 위 선택). Font Size 36. Text: Sheep Left: 5.",
            "Canvas > 우클릭 > UI > Text - TextMeshPro를 한 번 더, 이름은 Game Over Text. Anchor: 가운데, Font Size 72, Alignment 가운데, Text: GAME OVER. 이름 옆 체크박스를 해제해 숨기세요.",
            "Hierarchy > + > Create Empty, 이름은 Game Manager. 아래 GameManager script를 만들어 드래그하세요.",
            "Game Manager > Inspector: Sheep Left Text를 Sheep Left Text 칸에, Game Over Text를 Game Over Text 칸에 드래그하세요. Starting Sheep Left: 5.",
            "SheepDestroyer를 아래 코드로 바꾸세요. Sheep Destroyer > Inspector: Game Manager를 Game Manager 칸에 드래그하세요.",
            "Play를 누르고 양 다섯 마리를 놓치세요.",
        ],
        why=[
            "startingSheepLeft는 디자이너의 숫자, sheepLeft는 실시간 값이에요. Start에서 복사하면 둘이 분리돼요.",
            "Time.timeScale = 0은 물리와 Time.deltaTime을 멈춰서 양이 얼고 spawner timer도 멈춰요. Update는 계속 실행돼요 - 그래서 pause 메뉴가 키를 읽을 수 있어요.",
            "== 0 대신 <= 0: 같은 frame에 양 두 마리가 떨어져도 안전해요.",
            "이 단계에는 새 Inspector 칸이 세 개 있어요. 하나라도 None으로 남으면 첫 번째로 놓친 양에서 NullReferenceException이 나요 - 전형적인 scene-wiring 버그예요.",
        ],
        check="양이 떨어질 때마다 카운터가 5, 4, 3, 2, 1, 0으로 줄고, 0에서 GAME OVER가 뜨고 모든 게 멈춰요.",
    ),
    "10-level-up": dict(
        title="Level up: 우리의 아키텍처 (singleton + event)",
        goal="같은 게임이지만 LuaLander와 FerryHeist처럼: GameManager는 세기만 하고, GameUI가 듣고 그려요.",
        actions=[
            "GameManager를 아래 코드로 바꾸세요. 텍스트 칸 두 개가 Inspector에서 사라져요 - 정상이에요.",
            "아래 GameUI script를 만들어 Canvas에 드래그하세요. Canvas > Game UI: Sheep Left Text와 Game Over Text를 칸에 드래그하세요.",
            "SheepDestroyer를 아래 코드로 바꾸세요. Game Manager 칸이 사라져요 - 더 이상 연결할 필요 없어요.",
            "Game Over Text: 이제 체크된 채로 둬도 돼요. GameUI가 시작할 때 숨겨요.",
            "Play를 누르고 Game Over까지 플레이하세요.",
        ],
        why=[
            "Singleton: GameManager가 Awake에서 자신을 static Instance에 저장하니까, 어떤 script든 GameManager.Instance로 접근해요 - 잊어버릴 Inspector 칸이 없어요.",
            "Event: GameManager는 \"남은 양이 바뀌었다\"와 \"game over\"만 알려요. GameUI가 듣고 텍스트를 바꿔요. 로직은 UI를 건드리지 않아요 - GameManager를 열지 않고도 UI를 다시 디자인할 수 있어요.",
            "Instance는 Awake에서 설정되고 listener는 Start에서 구독해요: 모든 Awake가 어떤 Start보다 먼저 실행되니까, GameUI가 물을 때 Instance가 준비돼 있어요.",
            "Awake의 Time.timeScale = 1: timeScale은 scene을 다시 로드해도 유지되니까, 나중에 Restart 버튼이 얼어붙은 게임을 로드하지 않게 해요 (LuaLander 교훈).",
        ],
        check="9단계 후와 똑같이 플레이돼요 - 바뀐 건 내부이고, Inspector에서 연결할 칸이 줄었어요.",
    ),
    "11-make-it-yours": dict(
        title="나만의 게임으로",
        goal="코스 게임이 완성됐어요. 이제 당신의 게임이에요 - 다음은 당신이 정해요.",
        actions=[
            "아이디어 하나를 골라 agent에게 말하세요 - 이 코스처럼 한 단계씩 함께 만들어요:",
            "Score: 받은 양마다 +1, Sheep Left 옆에 표시 (새 event OnSheepCaught).",
            "난이도 상승: 양을 받을 때마다 spawnInterval이 조금씩 줄어들어 최소값까지.",
            "Particles: 양을 받을 때 연기 효과 - 첫 Particle Lab 연습.",
            "Restart: Game Over 화면에서 scene을 다시 로드하는 버튼 (Time.timeScale = 1은 이미 처리됨).",
            "진짜 모델: 구와 큐브를 Blender로 만든 양과 캐처로 바꾸기.",
        ],
        why=[
            "모든 아이디어가 방금 만든 것을 다시 써요: event (score), timer (난이도), prefab (particles), scene과 timeScale (restart).",
            "한 부분을 만들고 나면 SharpDul이 그걸로 퀴즈를 낼 수 있어요 - 퀴즈는 직접 만든 것만 다뤄요.",
        ],
        check="처음부터 직접 만든 플레이 가능한 Falling Frenzy가 생겼어요.",
    ),
}

translation = dict(
    title="Falling Frenzy",
    description="GameDevTV Unity Fundamentals 게임을 Unity 6000.3.14f1에서 처음부터 만들어요: 물리, input, prefab, trigger, UI - 그리고 우리의 아키텍처.",
    steps=steps,
)
OUT.write_text(json.dumps(translation, indent=2, ensure_ascii=False) + "\n")
print("ko written")
