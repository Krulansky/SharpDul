"""Slovak and Korean text of the Falling Frenzy Build Lab puzzles. Code is never translated;
gamedev terms stay English.
Run: python3 tools/falling_frenzy_puzzles_translations.py
"""
import json
import pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "src/SharpDul.Pocket/wwwroot/content/builds"

sk = {
    "falling-object": dict(
        title="FallingObject: ohlás zásah",
        context="Ovca už padá a odráža sa - to spraví Rigidbody bez akéhokoľvek kódu. Tento skript sedí na Sheep a pri náraze do niečoho pevného zapíše do Console.",
        hint="Pevné veci, ktoré do seba narazia, volajú OnCollisionEnter. OnTriggerEnter je pre triggery - hráč zatiaľ nie je trigger. Meno toho, do čoho si narazil, je na jeho gameObject.",
        success="Každý odraz teraz zapíše \"Sheep hit Player\" do Console pod hrou.",
    ),
    "player-input": dict(
        title="PlayerController: čítaj klávesy",
        context="Tento skript sedí na Playerovi. Prvá polovica: každý frame premeň klávesy A a D na jedno číslo, moveInput (-1 doľava, 0 nič, 1 doprava).",
        hint="Najprv vynuluj moveInput, potom nech A nastaví -1 a D 1. Ktorá Unity metóda beží každý frame?",
        success="Klávesy sa čítajú - pozri, ako sa kód rozsvieti, keď držíš A alebo D. Hráč sa ale ešte nepohne: nikto moveInput nepoužíva.",
    ),
    "player-move": dict(
        title="PlayerController: hýb sa vo fyzikálnom kroku",
        context="Druhá polovica toho istého skriptu: v každom fyzikálnom kroku premeň moveInput na rýchlosť pre Rigidbody.",
        hint="Rýchlosť = smer x ako rýchlo. Daj ju Rigidbody - priame posúvanie transformu by bojovalo s fyzikou.",
        success="Hráč sa hýbe! Arkádový pocit: rozbehne sa aj zastaví okamžite, lebo linearVelocity nahradí starý pohyb.",
    ),
    "sheep-spawner": dict(
        title="SheepSpawner: ovca každú sekundu",
        context="Prázdny GameObject hore nad obrazovkou. Počíta čas, a keď uplynie spawnInterval, vytvorí novú kópiu prefabu Sheep.",
        hint="Pripočítaj k timeru čas framu. Keď je väčší ako spawnInterval: Instantiate, potom timer vynuluj.",
        success="Nekonečné ovce zo stredu hore. Hráč je stále pevný, takže sa od neho odrážajú.",
    ),
    "player-catch": dict(
        title="PlayerController: chytaj!",
        context="Box Collider Playera dostane zaškrtnuté Is Trigger, takže ovce do neho vojdú namiesto odrazu. Táto metóda beží, keď niečo vojde do triggera.",
        hint="Trigger collidery volajú OnTriggerEnter. Skontroluj tag a znič to, čo vošlo - pozor: samotné gameObject je hráč sám.",
        success="Chytené ovce zmiznú so zeleným obláčikom. Minuté padajú z obrazovky... zatiaľ navždy.",
    ),
    "sheep-destroyer": dict(
        title="SheepDestroyer: uprac minuté ovce",
        context="Obrovský neviditeľný trigger hlboko pod obrazovkou (y -10, 100 x 100). Každá ovca, ktorá minie hráča, skončí tu.",
        hint="Rovnaký vzor ako chytanie: skontroluj tag, znič druhý objekt. Destroy potrebuje celý GameObject, nie jeden z jeho komponentov.",
        success="Minuté ovce sa zničia pod obrazovkou, takže sa už nehromadia v pamäti.",
    ),
    "random-x": dict(
        title="SheepSpawner: náhodné pozície",
        context="Zmeň spawner: vyber náhodné X medzi -spawnRangeX a spawnRangeX, Y a Z nechaj zo spawnera.",
        hint="Random.Range(min, max). Poskladaj pozíciu z x a z y a z spawnera a spawnuj tam namiesto transform.position.",
        success="Ovce prší z celej šírky. Skús slider spawnRangeX - pri 0 sú zase všetky v strede.",
    ),
    "game-manager": dict(
        title="GameManager: počítaj ovce",
        context="Prázdny objekt Game Manager. Drží počet zostávajúcich oviec, ukazuje ho v UI texte a pri 0 ukončí hru.",
        hint="Start: skopíruj štartovaciu hodnotu a ukáž ju. LostSheep: o jednu menej, ukáž to, a ak už žiadne nie sú - ukáž GAME OVER a zastav čas.",
        success="\"Sheep Left: 5\" je na obrazovke. Ale nikdy neubúda: LostSheep() zatiaľ nikto nevolá.",
    ),
    "destroyer-lost-sheep": dict(
        title="SheepDestroyer: povedz to GameManagerovi",
        context="Prepoj ich: destroyer dostane referenciu na GameManager (priradenú v Inspectore) a ohlási každú minutú ovcu.",
        hint="[SerializeField] pole pre GameManager, potom zavolaj jeho public metódu - private UpdateText sa zvonku zavolať nedá.",
        success="Počítadlo odpočítava a pri 0 hra zamrzne: Time.timeScale = 0. Postavil si celú hru!",
    ),
    "level-up-events": dict(
        title="Level up: GameManager ako singleton s eventmi",
        context="Naša architektúra (LuaLander, FerryHeist): GameManager sa uloží do static Instance a zmeny len oznamuje cez event. Na UI už nesiaha.",
        hint="Static property drží jediný GameManager; v Awake sa doň uloží. Po odpočítaní vystreľ event - ?. aby to bolo bezpečné aj bez listenerov.",
        success="Na obrazovke tá istá hra - ale logika teraz len strieľa eventy. SheepDestroyer sa k nej dostane cez GameManager.Instance, bez poľa v Inspectore.",
    ),
    "game-ui": dict(
        title="GameUI: počúvaj a kresli",
        context="Nový skript na Canvase. Prihlási sa na OnSheepLeftChanged a aktualizuje text vždy, keď GameManager oznámi zmenu.",
        hint="Prihlás sa cez += v metóde, ktorá beží po všetkých Awake. Keď event vystrelí, aktualizuj text.",
        success="Logika a UI sú oddelené, presne ako vo všetkých našich hrách. Falling Frenzy je hotový - teraz ho postav naozaj v Unity s kurzom!",
    ),
}

ko = {
    "falling-object": dict(
        title="FallingObject: 충돌 알리기",
        context="양은 이미 떨어지고 튀어요 - 코드 없이 Rigidbody가 해 줘요. 이 script는 Sheep에 붙어서, 단단한 것에 부딪힐 때 Console에 기록해요.",
        hint="단단한 것끼리 부딪히면 OnCollisionEnter가 호출돼요. OnTriggerEnter는 trigger용이에요 - 플레이어는 아직 trigger가 아니에요. 부딪힌 것의 이름은 그 gameObject에 있어요.",
        success="이제 튈 때마다 게임 아래 Console에 \"Sheep hit Player\"가 찍혀요.",
    ),
    "player-input": dict(
        title="PlayerController: 키 읽기",
        context="이 script는 Player에 붙어요. 앞부분: 매 frame A와 D 키를 하나의 숫자 moveInput으로 바꿔요 (-1 왼쪽, 0 없음, 1 오른쪽).",
        hint="먼저 moveInput을 0으로, 그다음 A는 -1, D는 1로 설정하세요. 매 frame 실행되는 Unity method는?",
        success="키를 읽고 있어요 - A나 D를 누르면 코드가 빛나요. 하지만 플레이어는 아직 안 움직여요: 아무도 moveInput을 쓰지 않거든요.",
    ),
    "player-move": dict(
        title="PlayerController: 물리 step에서 움직이기",
        context="같은 script의 뒷부분: 물리 step마다 moveInput을 Rigidbody의 속도로 바꿔요.",
        hint="속도 = 방향 x 빠르기. 그 값을 Rigidbody에 주세요 - transform을 직접 옮기면 물리와 싸워요.",
        success="플레이어가 움직여요! 아케이드 느낌: linearVelocity가 이전 움직임을 덮어써서 바로 출발하고 바로 멈춰요.",
    ),
    "sheep-spawner": dict(
        title="SheepSpawner: 매초 양 한 마리",
        context="화면 위쪽의 빈 GameObject예요. 시간을 세다가 spawnInterval이 지나면 Sheep prefab의 새 복사본을 만들어요.",
        hint="timer에 이번 frame의 시간을 더하세요. spawnInterval보다 커지면: Instantiate, 그리고 timer를 0으로.",
        success="위쪽 가운데에서 양이 끝없이 나와요. 플레이어는 아직 단단해서 양이 튕겨 나가요.",
    ),
    "player-catch": dict(
        title="PlayerController: 받아라!",
        context="Player의 Box Collider에 Is Trigger를 체크해서, 양이 튕기지 않고 안으로 들어와요. 무언가 trigger에 들어오면 이 method가 실행돼요.",
        hint="trigger collider는 OnTriggerEnter를 호출해요. tag를 확인하고 들어온 것을 파괴하세요 - 주의: gameObject만 쓰면 플레이어 자신이에요.",
        success="받은 양은 초록색 연기와 함께 사라져요. 놓친 양은 화면 밖으로... 지금은 영원히 떨어져요.",
    ),
    "sheep-destroyer": dict(
        title="SheepDestroyer: 놓친 양 정리하기",
        context="화면 훨씬 아래 (y -10, 100 x 100)에 있는 거대한 보이지 않는 trigger 상자예요. 플레이어가 놓친 양은 모두 여기로 와요.",
        hint="받기와 같은 패턴: tag를 확인하고 상대 객체를 파괴하세요. Destroy에는 component 하나가 아니라 GameObject 전체가 필요해요.",
        success="놓친 양이 화면 아래에서 파괴되어 더 이상 메모리에 쌓이지 않아요.",
    ),
    "random-x": dict(
        title="SheepSpawner: 무작위 위치",
        context="spawner를 바꿔요: -spawnRangeX와 spawnRangeX 사이에서 무작위 X를 고르고, Y와 Z는 spawner 것을 써요.",
        hint="Random.Range(min, max). x와 spawner의 y, z로 위치를 만들고, transform.position 대신 거기에 spawn하세요.",
        success="양이 화면 전체에서 쏟아져요. spawnRangeX slider를 움직여 보세요 - 0이면 다시 모두 가운데예요.",
    ),
    "game-manager": dict(
        title="GameManager: 양 세기",
        context="빈 Game Manager 객체예요. 남은 양의 수를 갖고, UI 텍스트에 보여 주고, 0이 되면 게임을 끝내요.",
        hint="Start: 시작 값을 복사하고 보여 주세요. LostSheep: 하나 줄이고, 보여 주고, 남은 게 없으면 GAME OVER를 띄우고 시간을 멈추세요.",
        success="화면에 \"Sheep Left: 5\"가 나와요. 그런데 줄지 않아요: 아직 아무도 LostSheep()을 호출하지 않거든요.",
    ),
    "destroyer-lost-sheep": dict(
        title="SheepDestroyer: GameManager에게 알리기",
        context="둘을 연결해요: destroyer가 GameManager 참조를 받아서 (Inspector에서 연결) 놓친 양마다 알려요.",
        hint="GameManager용 [SerializeField] 칸을 만들고 public method를 호출하세요 - private인 UpdateText는 밖에서 호출할 수 없어요.",
        success="카운터가 줄어들고 0에서 게임이 멈춰요: Time.timeScale = 0. 게임 전체를 만들었어요!",
    ),
    "level-up-events": dict(
        title="Level up: singleton과 event를 쓰는 GameManager",
        context="우리의 아키텍처 (LuaLander, FerryHeist): GameManager가 자신을 static Instance에 저장하고, 변화는 event로만 알려요. 더 이상 UI를 건드리지 않아요.",
        hint="static property가 하나뿐인 GameManager를 담아요. Awake에서 자신을 저장하세요. 숫자를 줄인 뒤 event를 발생시키세요 - listener가 없어도 안전하게 ?.를 써요.",
        success="화면의 게임은 같지만, 이제 로직은 event만 보내요. SheepDestroyer는 Inspector 칸 없이 GameManager.Instance로 접근해요.",
    ),
    "game-ui": dict(
        title="GameUI: 듣고 그리기",
        context="Canvas에 붙는 새 script예요. OnSheepLeftChanged를 구독하고, GameManager가 변화를 알릴 때마다 텍스트를 바꿔요.",
        hint="모든 Awake 다음에 실행되는 method에서 +=로 구독하세요. event가 오면 텍스트를 바꾸세요.",
        success="로직과 UI가 분리됐어요, 우리 게임들처럼요. Falling Frenzy 완성 - 이제 코스를 따라 Unity에서 진짜로 만들어 보세요!",
    ),
}

texts = {
    "sk": (sk, "Rozlúskni skripty jeden za druhým - každý vyriešený skript zapne svoju časť hry."),
    "ko": (ko, "script를 하나씩 풀어 보세요 - 풀 때마다 게임의 그 부분이 켜져요."),
}
base = json.loads((OUT / "falling-frenzy.json").read_text())
for code, (puzzles, description) in texts.items():
    missing = {p["id"] for p in base["puzzles"]} - set(puzzles)
    assert not missing, (code, missing)
    data = dict(title="Falling Frenzy", description=description, puzzles=puzzles)
    (OUT / f"falling-frenzy.{code}.json").write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
print("translations written")
