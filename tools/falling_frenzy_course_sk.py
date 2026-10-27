"""Slovak text of the Falling Frenzy course. Unity menu paths and gamedev terms stay English.
Run: python3 tools/falling_frenzy_course_sk.py
"""
import json
import pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "src/SharpDul.Pocket/wwwroot/content/courses/falling-frenzy.sk.json"

steps = {
    "01-project": dict(
        title="Vytvor projekt a scénu",
        goal="Prázdny Unity projekt s kamerou namierenou na hraciu plochu.",
        actions=[
            "Unity Hub > Projects > New project. Editor Version: 6000.3.14f1. Template: Universal 3D. Project name: FallingFrenzy. Klikni Create project.",
            "Project okno > Assets > Scenes: pravý klik na SampleScene > Rename > FallingFrenzy. Ak sa Unity pýta na reload, potvrď.",
            "Hierarchy > Main Camera. Inspector > Transform > Position: X 0, Y 9, Z -62. Rotation: 0, 0, 0.",
            "Stále na Main Camera: Inspector > Camera > Field of View: 20.",
            "File > Save (Ctrl+S).",
        ],
        why=[
            "Hra je 3D, ale hrá sa na jednej rovnej ploche (X = doľava/doprava, Y = hore/dole). Kamera stojí ďaleko (Z -62) s úzkym Field of View (20), takže plocha vyzerá skoro rovno - ako 2D hra, ale s 3D modelmi a svetlom.",
            "Na každom PC používaj rovnakú verziu Unity (6000.3.14f1) - novšia vie uložiť súbory, ktoré staršia neprečíta (lekcia s URP assetom z LuaLandera).",
        ],
        check="Stlač Play: prázdna sivomodrá scéna, žiadne chyby vo Window > General > Console.",
    ),
    "02-player": dict(
        title="Polož hráča (chytač)",
        goal="Plochá kocka pri spodku obrazovky, ktorá bude chytať ovce.",
        actions=[
            "Hierarchy > + > 3D Object > Cube. Premenuj ju na Player (pravý klik > Rename). Je v roote Hierarchy.",
            "Player > Inspector > Transform > Position: X 0, Y -1, Z 0. Scale: X 3, Y 0.5, Z 1.",
            "File > Save.",
        ],
        why=[
            "Cube má Mesh Filter + Mesh Renderer (to, čo vidíš) a Box Collider (to, čo cíti fyzika). Sú to samostatné komponenty: môžeš vidieť veci, ktoré nekolidujú, a kolidovať s vecami, ktoré nevidíš.",
            "Scale mení aj collider, takže kocka 3 x 0.5 je zároveň plocha 3 x 0.5 na chytanie.",
        ],
        check="V Game view je plochá kocka dole v strede.",
    ),
    "03-first-script": dict(
        title="Tvoj prvý C# skript",
        goal="Skript, ktorý sa spustí pri štarte hry a zmení svoj vlastný GameObject.",
        actions=[
            "Project okno > Assets: pravý klik > Create > Folder, nazvi ho Scripts.",
            "V Assets > Scripts: pravý klik > Create > Scripting > MonoBehaviour Script, nazvi ho HelloWorld.",
            "Dvojklikom HelloWorld otvor. Do Start() napíš: gameObject.name = \"I am game dev!\"; a súbor ulož.",
            "Potiahni HelloWorld z Project okna na Player v Hierarchy.",
            "Stlač Play, pozri sa do Hierarchy, Play stlač znova na zastavenie.",
            "Upratanie: Player > Inspector > Hello World (Script) > ⋮ > Remove Component. Potom zmaž Assets > Scripts > HelloWorld (pravý klik > Delete).",
        ],
        why=[
            "MonoBehaviour je komponent, rovnako ako Transform či Box Collider. Unity zavolá jeho Start() raz pred prvým framom a Update() každý frame.",
            "gameObject je objekt, na ktorom skript sedí. Zmeny v Play mode sa po zastavení vrátia - preto sa meno vráti späť.",
        ],
        check="V Play mode sa Player premenuje na \"I am game dev!\"; po Stop je znova Player.",
    ),
    "04-physics": dict(
        title="Fyzika: padajúca, skákajúca ovca",
        goal="Ovca (zatiaľ guľa) padá, odrazí sa od hráča a ohlási zásah.",
        actions=[
            "Hierarchy > + > 3D Object > Sphere. Premenuj na Sheep. Transform > Position: X 0, Y 15, Z 0.",
            "Sheep > Inspector > Add Component > Rigidbody. V Rigidbody > Constraints zaškrtni Freeze Position Z.",
            "Project okno > Assets: pravý klik > Create > Folder Physics Materials. V ňom: pravý klik > Create > Physics Material, nazvi Bouncy. Inspector: Bounciness 1.",
            "Potiahni Bouncy na Sheep > Inspector > Sphere Collider > Material.",
            "Assets > Scripts: pravý klik > Create > Scripting > MonoBehaviour Script FallingObject. Napíš kód nižšie a potiahni skript na Sheep.",
            "Stlač Play.",
        ],
        why=[
            "Rigidbody odovzdá objekt fyzikálnemu enginu: gravitácia, rýchlosť, kolízie. Bez neho je guľa len kulisa.",
            "Freeze Position Z drží ovcu na našej rovnej hracej ploche, takže sa nikdy neodkotúľa ku kamere ani od nej.",
            "OnCollisionEnter beží, keď sa dotknú dva pevné collidery a aspoň jeden má Rigidbody. Parameter Collision ti povie, do čoho narazil.",
            "Bounciness 1 na ovci a 0 na hráčovi dá priemer 0.5 (Bounce Combine = Average), takže každý odraz je zhruba o polovicu nižší.",
        ],
        check="Guľa spadne, párkrát sa odrazí od Playera a Console vypíše \"Sheep hit Player\".",
    ),
    "05-input": dict(
        title="Hýb hráčom cez A a D",
        goal="Chytač sa posúva doľava a doprava a hneď zastane, keď pustíš kláves.",
        actions=[
            "Assets > Scripts: vytvor MonoBehaviour Script PlayerController s kódom nižšie a potiahni ho na Player.",
            "Player > Inspector > Add Component > Rigidbody. Odškrtni Use Gravity. Constraints: zaškrtni Freeze Position Y a Z a Freeze Rotation X, Y a Z.",
            "Potiahni komponent Rigidbody (jeho záhlavie) z Inspectora Playera do PlayerController > Player Rigidbody. Nesmie ostať None.",
            "PlayerController > Move Speed: 20.",
            "Stlač Play a drž A / D.",
        ],
        why=[
            "Vstup sa číta v Update (každý frame, aby sa žiadne stlačenie nestratilo); teleso sa hýbe vo FixedUpdate (fyzikálny krok). Field moveInput prenáša hodnotu medzi nimi.",
            "Nastavenie linearVelocity zahodí starý pohyb: okamžitý štart, okamžité zastavenie - arkádový pocit. LuaLander používa AddForce a má zotrvačnosť. Vyskúšaj oboje v Lab náhľade nižšie.",
            "Keď držíš A aj D naraz, ideš doprava: kontrola D beží posledná a vyhrá.",
            "Nový [SerializeField] sa v Inspectore ukáže ako None. Nič ťa neupozorní, kým Play mode nehodí NullReferenceException - vždy ho hneď priraď.",
        ],
        check="A posúva kocku doľava, D doprava; po pustení hneď zastane. Ovca sa od nej stále odráža.",
    ),
    "06-spawner": dict(
        title="Prefab a spawner: nekonečné ovce",
        goal="Každú sekundu spadne zhora zo stredu nová ovca.",
        actions=[
            "Sheep > Inspector > Falling Object (Script) > ⋮ > Remove Component (log už nepotrebujeme).",
            "Project okno > Assets: vytvor priečinok Prefabs. Potiahni Sheep z Hierarchy do Assets > Prefabs. V Hierarchy zmodrie - je z nej prefab.",
            "Zmaž Sheep z Hierarchy (pravý klik > Delete). Prefab v Assets > Prefabs ostáva.",
            "Hierarchy > + > Create Empty. Premenuj na Sheep Spawner. Transform > Position: X 0, Y 20, Z 0.",
            "Vytvor skript SheepSpawner nižšie a potiahni ho na Sheep Spawner. Do poľa Sheep Prefab potiahni Assets > Prefabs > Sheep.",
            "Stlač Play.",
        ],
        why=[
            "Prefab je uložená šablóna GameObjectu. Instantiate z nej spraví živú kópiu v scéne - každá ovca je klon toho istého prefabu.",
            "Timer počíta skutočné sekundy (Time.deltaTime), vystrelí, keď prekročí spawnInterval, a vynuluje sa. Žiadna coroutine netreba.",
            "sheepPrefab.transform.rotation zaručí, že každá kópia je otočená rovnako ako prefab.",
        ],
        check="Každú sekundu sa hore v strede objaví guľa a padá. Odrážajú sa od hráča a hromadia sa alebo padajú preč.",
    ),
    "07-triggers": dict(
        title="Chytiť a stratiť: triggery a tagy",
        goal="Ovce, ktoré sa dotknú chytača, zmiznú; ovce, ktoré ho minú, sa zničia pod obrazovkou.",
        actions=[
            "Otaguj prefab: dvojklik na Assets > Prefabs > Sheep. Inspector > Tag > Add Tag... > + > napíš Sheep > Save. Znova vyber prefab Sheep a nastav Tag: Sheep. Z prefabu odíď šípkou < v Hierarchy.",
            "Player > Inspector > Box Collider: zaškrtni Is Trigger.",
            "Pridaj do PlayerController metódu OnTriggerEnter nižšie.",
            "Hierarchy > + > Create Empty, nazvi Sheep Destroyer. Position: X 0, Y -10, Z 0. Add Component > Box Collider: Is Trigger zaškrtnuté, Size X 100, Y 1, Z 100.",
            "Vytvor skript SheepDestroyer nižšie a potiahni ho na Sheep Destroyer.",
            "Stlač Play.",
        ],
        why=[
            "Trigger collider nič neblokuje - objekty ním prejdú a Unity len zavolá OnTriggerEnter. Pevný collider volá OnCollisionEnter a odráža. Preto sa ovce prestali odrážať.",
            "CompareTag(\"Sheep\") je rýchlejší ako tag == \"Sheep\" a preklep v mene tagu nahlási ako chybu, namiesto toho, aby potichu nikdy nesedel.",
            "Destroyer je pod obrazovkou a je obrovský (100 x 100), takže ho žiadna ovca nemôže minúť. Bez neho by minuté ovce padali navždy a hromadili sa v pamäti.",
        ],
        check="Ovce, ktoré trafia kocku, zmiznú. Tie, čo ju minú, spadnú z obrazovky; v Hierarchy vidíš, ako sa klony objavujú a miznú.",
    ),
    "08-random-x": dict(
        title="Náhodné pozície: navrhni level",
        goal="Ovce padajú z náhodných miest po celej šírke.",
        actions=[
            "Zmeň SheepSpawner na kód nižšie.",
            "Sheep Spawner > Inspector > Sheep Spawner (Script) > Spawn Range X: 15.",
            "Voliteľné: Hierarchy > + > 3D Object > Cube párkrát ako kulisy v pozadí (napr. vysoké stĺpy ďaleko vzadu na Z 80). Daj im vzhľad; hraciu plochu nepreťínajú.",
            "Stlač Play.",
        ],
        why=[
            "Random.Range(-spawnRangeX, spawnRangeX) dá float medzi -15 a 15 vrátane krajov. Y a Z berie zo spawnera, takže sa mení len X.",
            "Skript hovorí 10, Inspector 15 - hra použije 15. Default pri [SerializeField] platí len pri prvom pridaní komponentu; potom vyhráva hodnota uložená v scéne.",
        ],
        check="Ovce padajú z celého horného okraja. Chytať ich je ťažšie.",
    ),
    "09-game-over": dict(
        title="Počítadlo oviec a Game Over",
        goal="\"Sheep Left: 5\" ubúda za každú minutú ovcu; pri 0 hra ukáže GAME OVER a zamrzne.",
        actions=[
            "Hierarchy > + > UI > Text - TextMeshPro. Ak sa Unity pýta, klikni Import TMP Essentials a okno zavri. Objaví sa Canvas a EventSystem; text premenuj na Sheep Left Text.",
            "Sheep Left Text > Inspector > Rect Transform: anchor preset vľavo hore (klikni na štvorec, drž Alt+Shift, vyber vľavo hore). Font Size 36. Text: Sheep Left: 5.",
            "Canvas > pravý klik > UI > Text - TextMeshPro ešte raz, nazvi Game Over Text. Anchor: stred, Font Size 72, Alignment na stred, Text: GAME OVER. Odškrtni checkbox vedľa mena, aby sa skryl.",
            "Hierarchy > + > Create Empty, nazvi Game Manager. Vytvor skript GameManager nižšie a potiahni ho naň.",
            "Game Manager > Inspector: potiahni Sheep Left Text do Sheep Left Text a Game Over Text do Game Over Text. Starting Sheep Left: 5.",
            "Zmeň SheepDestroyer na kód nižšie. Sheep Destroyer > Inspector: potiahni Game Manager do jeho poľa Game Manager.",
            "Stlač Play a nechaj prepadnúť päť oviec.",
        ],
        why=[
            "startingSheepLeft je číslo dizajnéra; sheepLeft je živá hodnota. Skopírovanie v Start ich drží oddelene.",
            "Time.timeScale = 0 zastaví fyziku aj Time.deltaTime, takže ovce zamrznú a timer spawnera stojí. Update stále beží - vďaka tomu vie pause menu čítať klávesy.",
            "<= 0 namiesto == 0: bezpečné, aj keď dve ovce dopadnú v tom istom frame.",
            "Tento krok má tri nové polia v Inspectore. Ak niektoré ostane None, prvá stratená ovca hodí NullReferenceException - klasický scene-wiring bug.",
        ],
        check="Počítadlo ide 5, 4, 3, 2, 1, 0, ako ovce prepadávajú; pri 0 sa objaví GAME OVER a všetko zastane.",
    ),
    "10-level-up": dict(
        title="Level up: naša architektúra (singleton + eventy)",
        goal="Tá istá hra, ale postavená ako LuaLander a FerryHeist: GameManager len počíta, GameUI počúva a kreslí.",
        actions=[
            "Nahraď GameManager kódom nižšie. Jeho dve textové polia z Inspectora zmiznú - to je v poriadku.",
            "Vytvor skript GameUI nižšie a potiahni ho na Canvas. Canvas > Game UI: potiahni Sheep Left Text a Game Over Text do jeho polí.",
            "Nahraď SheepDestroyer kódom nižšie. Jeho pole Game Manager zmizne - žiadne ďalšie prepájanie.",
            "Game Over Text: teraz môže ostať zaškrtnutý; GameUI ho na štarte skryje.",
            "Stlač Play a hraj až do Game Over.",
        ],
        why=[
            "Singleton: GameManager sa v Awake uloží do static Instance, takže každý skript sa k nemu dostane cez GameManager.Instance - žiadne pole v Inspectore, na ktoré by si zabudol.",
            "Eventy: GameManager len oznamuje \"zmenil sa počet oviec\" a \"game over\". GameUI počúva a aktualizuje text. Logika nikdy nesiahne na UI - UI môžeš prerobiť bez otvorenia GameManagera.",
            "Instance sa nastaví v Awake, listenery sa prihlasujú v Start: všetky Awake bežia pred akýmkoľvek Start, takže Instance je pripravená, keď sa GameUI pýta.",
            "Time.timeScale = 1 v Awake: timeScale prežije reload scény, takže budúce tlačidlo Restart by inak načítalo zamrznutú hru (lekcia z LuaLandera).",
        ],
        check="Hra sa hrá presne ako po kroku 9 - zmena je vnútri a Inspector má menej polí na prepájanie.",
    ),
    "11-make-it-yours": dict(
        title="Sprav ju svojou",
        goal="Kurzová hra je hotová. Teraz sa z nej stáva tvoja hra - ty rozhodneš, čo bude ďalej.",
        actions=[
            "Vyber jeden nápad a povedz ho agentovi - postavíme ho spolu, krok za krokom ako tento kurz:",
            "Score: +1 za každú chytenú ovcu, zobrazené vedľa Sheep Left (nový event OnSheepCaught).",
            "Stúpajúca obťažnosť: spawnInterval sa po každom chytení trochu skráti, až po minimum.",
            "Particles: obláčik, keď chytíš ovcu - prvé cvičenie do Particle Labu.",
            "Restart: tlačidlo pri Game Over, ktoré znova načíta scénu (Time.timeScale = 1 je už vyriešené).",
            "Skutočné modely: vymeň guľu a kocku za vlastnú ovcu a chytač z Blendera.",
        ],
        why=[
            "Každý nápad využije, čo si práve postavil: eventy (score), timery (obťažnosť), prefaby (particles), scény a timeScale (restart).",
            "Keď je časť postavená, SharpDul ťa z nej môže kvízovať - kvízy sú len z toho, čo si sám postavil.",
        ],
        check="Máš hrateľný Falling Frenzy postavený od nuly.",
    ),
}

translation = dict(
    title="Falling Frenzy",
    description="Postav hru z GameDevTV Unity Fundamentals od nuly v Unity 6000.3.14f1: fyzika, input, prefaby, triggery, UI - a potom naša architektúra.",
    steps=steps,
)
OUT.write_text(json.dumps(translation, indent=2, ensure_ascii=False) + "\n")
print("sk written")
