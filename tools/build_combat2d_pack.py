"""Writes the 2D Combat quiz pack (EN + SK + KR) from the 2DTopDownPixelCombat project.

Usage: python3 tools/build_combat2d_pack.py [path to 2DTopDownPixelCombat]

Source line numbers are looked up in the project itself (by anchor text), so they always
match the commit the pack was built from. Edit this file, not the JSON.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "src", "SharpDul.Pocket", "wwwroot", "content")
PACK_ID = "combat2d-easy"
PROJECT = "2DTopDownPixelCombat"

PACK = {
    "en": ("2D Combat", "Easy questions from the 2D combat course: dash, stamina, knockback, enemy AI, bullet patterns and your own Rage."),
    "sk": ("2D Combat", "Easy otázky z 2D combat kurzu: dash, stamina, knockback, enemy AI, bullet patterns a tvoj vlastný Rage."),
    "ko": ("2D Combat", "2D combat 코스의 Easy 문제: dash, stamina, knockback, enemy AI, bullet pattern, 그리고 내가 만든 Rage."),
}

# Each question: id, type, code, highlight, source (file, first anchor, last anchor),
# then per language: context, prompt, hint, options (correct first), explanation.
QUESTIONS = [
    {
        "id": "combat2d.dash-speed",
        "type": "MultipleChoice",
        "code": """[SerializeField] private float moveSpeed = 1f;   // Player prefab: 4
[SerializeField] private float dashSpeed = 4f;

private void Dash()
{
    if (!isDashing && Stamina.Instance.CanDash)
    {
        Stamina.Instance.UseStamina();
        isDashing = true;
        moveSpeed *= dashSpeed;
        StartCoroutine(EndDashRoutine());
    }
}""",
        "highlight": [1, 2, 10],
        "source": ("Assets/Scripts/Player/PlayerController.cs", "private void Dash()", "StartCoroutine(EndDashRoutine());"),
        "en": {
            "context": "PlayerController runs Dash() when you press the dash button. On the Player prefab moveSpeed is 4.",
            "prompt": "While the dash lasts, how fast does the demon hunter move?",
            "hint": "Look at the line with *= - it multiplies moveSpeed (4) by dashSpeed (4).",
            "options": ["16 units per second", "8 units per second", "4 - the same as walking", "1 unit per second"],
            "explanation": "moveSpeed *= dashSpeed makes 4 x 4 = 16. EndDashRoutine sets it back to startingMoveSpeed (4) when the dash ends.",
        },
        "sk": {
            "context": "PlayerController spustí Dash(), keď stlačíš dash. Na Player prefabe je moveSpeed 4.",
            "prompt": "Ako rýchlo sa demon hunter hýbe počas dashu?",
            "hint": "Pozri riadok s *= - násobí moveSpeed (4) hodnotou dashSpeed (4).",
            "options": ["16 jednotiek za sekundu", "8 jednotiek za sekundu", "4 - rovnako ako chôdza", "1 jednotka za sekundu"],
            "explanation": "moveSpeed *= dashSpeed dá 4 x 4 = 16. Na konci dashu ho EndDashRoutine vráti na startingMoveSpeed (4).",
        },
        "ko": {
            "context": "dash 버튼을 누르면 PlayerController가 Dash()를 실행해요. Player prefab의 moveSpeed는 4예요.",
            "prompt": "dash 중에 demon hunter는 얼마나 빨리 움직일까요?",
            "hint": "*= 가 있는 줄을 보세요 - moveSpeed(4)에 dashSpeed(4)를 곱해요.",
            "options": ["초당 16 유닛", "초당 8 유닛", "4 - 걸을 때와 같아요", "초당 1 유닛"],
            "explanation": "moveSpeed *= dashSpeed 로 4 x 4 = 16이 돼요. dash가 끝나면 EndDashRoutine이 startingMoveSpeed(4)로 되돌려요.",
        },
    },
    {
        "id": "combat2d.dash-time",
        "type": "MultipleChoice",
        "code": """private IEnumerator EndDashRoutine()
{
    float dashTime = 0.2f;
    float dashCD = 0.25f;
    yield return new WaitForSeconds(dashTime);
    moveSpeed = startingMoveSpeed;
    yield return new WaitForSeconds(dashCD);
    isDashing = false;
}""",
        "highlight": [3, 4, 5, 6, 7, 8],
        "source": ("Assets/Scripts/Player/PlayerController.cs", "private IEnumerator EndDashRoutine()", "isDashing = false;"),
        "en": {
            "context": "Dash() starts this coroutine right after it boosts moveSpeed. Dash() refuses to run while isDashing is true.",
            "prompt": "How long is the speed boost, and when can you dash again?",
            "hint": "Two waits in a row: the first one ends the boost, the second one ends isDashing.",
            "options": ["Boost 0.2 s, next dash 0.25 s after the boost ends", "Boost 0.45 s, next dash right away", "Boost 0.25 s, next dash after 0.2 s", "The boost lasts until you let go of the button"],
            "explanation": "After 0.2 s moveSpeed goes back to normal. isDashing stays true for another 0.25 s, so the next dash is possible 0.45 s after the first one started.",
        },
        "sk": {
            "context": "Dash() spustí tento coroutine hneď, ako zvýši moveSpeed. Kým je isDashing true, Dash() sa nespustí.",
            "prompt": "Ako dlho trvá zrýchlenie a kedy môžeš dať dash znova?",
            "hint": "Dve čakania za sebou: prvé ukončí zrýchlenie, druhé ukončí isDashing.",
            "options": ["Zrýchlenie 0,2 s, ďalší dash 0,25 s po jeho konci", "Zrýchlenie 0,45 s, ďalší dash hneď", "Zrýchlenie 0,25 s, ďalší dash po 0,2 s", "Zrýchlenie trvá, kým nepustíš tlačidlo"],
            "explanation": "Po 0,2 s sa moveSpeed vráti na normál. isDashing ostane true ešte 0,25 s, takže ďalší dash ide 0,45 s po začiatku prvého.",
        },
        "ko": {
            "context": "Dash()는 moveSpeed를 올린 직후 이 coroutine을 시작해요. isDashing이 true인 동안 Dash()는 실행되지 않아요.",
            "prompt": "가속은 얼마나 지속되고, 언제 다시 dash할 수 있을까요?",
            "hint": "기다림이 두 번 이어져요: 첫 번째는 가속을 끝내고, 두 번째는 isDashing을 끝내요.",
            "options": ["가속 0.2초, 가속이 끝나고 0.25초 뒤 다음 dash", "가속 0.45초, 다음 dash는 바로", "가속 0.25초, 0.2초 뒤 다음 dash", "버튼을 뗄 때까지 가속"],
            "explanation": "0.2초 뒤 moveSpeed가 원래대로 돌아와요. isDashing은 0.25초 더 true라서, 다음 dash는 첫 dash 시작 후 0.45초에 가능해요.",
        },
    },
    {
        "id": "combat2d.dash-no-stamina",
        "type": "MultipleChoice",
        "code": """// Stamina.cs
[SerializeField] private float dashCost = 1f;
public bool CanDash => CurrentStamina >= dashCost;

// PlayerController.cs
private void Dash()
{
    if (!isDashing && Stamina.Instance.CanDash)
    {
        Stamina.Instance.UseStamina();
        isDashing = true;
        moveSpeed *= dashSpeed;
    }
}""",
        "highlight": [2, 3, 8],
        "source": ("Assets/Scripts/Player/Stamina.cs", "public bool CanDash", "[SerializeField] private float dashCost"),
        "en": {
            "context": "Your stamina bar is a little more than half full: CurrentStamina = 0.6. You press dash.",
            "prompt": "What happens?",
            "hint": "CanDash compares CurrentStamina with dashCost. Is 0.6 >= 1?",
            "options": ["Nothing - the dash does not happen", "A shorter, weaker dash", "The dash happens and stamina goes below 0", "The dash happens and costs health instead"],
            "explanation": "0.6 >= 1 is false, so CanDash is false and the whole if is skipped: no stamina is used, no speed boost.",
        },
        "sk": {
            "context": "Stamina bar máš trochu viac ako do polovice: CurrentStamina = 0,6. Stlačíš dash.",
            "prompt": "Čo sa stane?",
            "hint": "CanDash porovná CurrentStamina s dashCost. Platí 0,6 >= 1?",
            "options": ["Nič - dash sa nestane", "Kratší, slabší dash", "Dash sa stane a stamina klesne pod 0", "Dash sa stane a namiesto staminy stojí health"],
            "explanation": "0,6 >= 1 neplatí, takže CanDash je false a celý if sa preskočí: žiadna stamina sa neminie, žiadne zrýchlenie.",
        },
        "ko": {
            "context": "stamina bar가 절반보다 조금 더 차 있어요: CurrentStamina = 0.6. dash를 눌러요.",
            "prompt": "어떻게 될까요?",
            "hint": "CanDash는 CurrentStamina와 dashCost를 비교해요. 0.6 >= 1 인가요?",
            "options": ["아무 일도 없어요 - dash가 안 돼요", "더 짧고 약한 dash", "dash가 되고 stamina가 0 아래로 내려가요", "dash가 되고 대신 health가 줄어요"],
            "explanation": "0.6 >= 1 은 false라서 CanDash가 false이고 if 전체를 건너뛰어요: stamina도 안 쓰고 가속도 없어요.",
        },
    },
    {
        "id": "combat2d.stamina-regen",
        "type": "MultipleChoice",
        "code": """[SerializeField] private float dashCost = 1f;
[SerializeField] private float regenPerSecond = 1f / 3f;

private void Update()
{
    if (CurrentStamina < maxStamina && !PlayerHealth.Instance.IsDead)
    {
        SetStamina(CurrentStamina + regenPerSecond * Time.deltaTime);
    }
}""",
        "highlight": [1, 2, 8],
        "source": ("Assets/Scripts/Player/Stamina.cs", "[SerializeField] private float dashCost", "SetStamina(CurrentStamina + regenPerSecond"),
        "en": {
            "context": "You just used your last dash: CurrentStamina = 0. You pick up no stamina globe.",
            "prompt": "About how long until you can dash again?",
            "hint": "Time.deltaTime makes regenPerSecond really \"per second\". How many seconds of 1/3 does it take to reach dashCost 1?",
            "options": ["About 3 seconds", "About 1/3 of a second", "One frame", "Never - only a stamina globe refills it"],
            "explanation": "Each second adds 1/3 stamina, so after 3 seconds CurrentStamina reaches 1 = dashCost and CanDash is true again.",
        },
        "sk": {
            "context": "Práve si minul posledný dash: CurrentStamina = 0. Žiadny stamina globe nezoberieš.",
            "prompt": "Približne o koľko môžeš dať dash znova?",
            "hint": "Time.deltaTime robí z regenPerSecond naozaj \"za sekundu\". Koľko sekúnd po 1/3 treba na dashCost 1?",
            "options": ["Asi o 3 sekundy", "Asi o 1/3 sekundy", "O jeden frame", "Nikdy - doplní ju len stamina globe"],
            "explanation": "Každá sekunda pridá 1/3 staminy, takže po 3 sekundách je CurrentStamina 1 = dashCost a CanDash je znova true.",
        },
        "ko": {
            "context": "방금 마지막 dash를 썼어요: CurrentStamina = 0. stamina globe는 줍지 않아요.",
            "prompt": "대략 얼마 뒤에 다시 dash할 수 있을까요?",
            "hint": "Time.deltaTime 덕분에 regenPerSecond는 정말 \"초당\"이에요. 1/3씩이면 dashCost 1까지 몇 초가 걸릴까요?",
            "options": ["약 3초", "약 1/3초", "한 frame", "절대 안 돼요 - stamina globe만 채워요"],
            "explanation": "1초마다 stamina가 1/3씩 늘어서, 3초 뒤 CurrentStamina가 1 = dashCost가 되고 CanDash가 다시 true가 돼요.",
        },
    },
    {
        "id": "combat2d.stamina-event",
        "type": "WhatDoesItDo",
        "code": """// Stamina.cs
public static event Action<float, float> OnStaminaChanged;

private void SetStamina(float value)
{
    CurrentStamina = Mathf.Clamp(value, 0f, maxStamina);
    OnStaminaChanged?.Invoke(CurrentStamina, maxStamina);
}

// StaminaBar.cs
private void OnEnable()
{
    Stamina.OnStaminaChanged += UpdateBar;
}""",
        "highlight": [7, 13],
        "source": ("Assets/Scripts/Player/StaminaBar.cs", "private void OnEnable()", "Stamina.OnStaminaChanged -= UpdateBar;"),
        "en": {
            "context": "You dash and the stamina bar in the UI drops. These are the two scripts involved.",
            "prompt": "How does the stamina bar find out that stamina changed?",
            "hint": "One script calls Invoke, the other one wrote += in OnEnable.",
            "options": ["Stamina fires the OnStaminaChanged event, and StaminaBar, subscribed in OnEnable, runs UpdateBar", "StaminaBar reads Stamina.Instance every frame in Update", "Stamina finds the bar with GameObject.Find and sets its value", "PlayerController updates the bar after each dash"],
            "explanation": "This is the Observer pattern: Stamina does not know the bar exists. It only fires OnStaminaChanged, and whoever subscribed (StaminaBar) reacts. OnDisable unsubscribes with -=.",
        },
        "sk": {
            "context": "Dáš dash a stamina bar v UI klesne. Toto sú dva skripty, ktoré sa na tom podieľajú.",
            "prompt": "Ako sa stamina bar dozvie, že sa stamina zmenila?",
            "hint": "Jeden skript volá Invoke, druhý napísal += v OnEnable.",
            "options": ["Stamina vystrelí event OnStaminaChanged a StaminaBar, prihlásený v OnEnable, spustí UpdateBar", "StaminaBar každý frame v Update číta Stamina.Instance", "Stamina nájde bar cez GameObject.Find a nastaví mu hodnotu", "PlayerController po každom dashi aktualizuje bar"],
            "explanation": "Toto je Observer pattern: Stamina nevie, že bar existuje. Len vystrelí OnStaminaChanged a kto sa prihlásil (StaminaBar), zareaguje. OnDisable sa odhlási cez -=.",
        },
        "ko": {
            "context": "dash를 하면 UI의 stamina bar가 줄어들어요. 관련된 script 두 개예요.",
            "prompt": "stamina bar는 stamina가 바뀐 걸 어떻게 알까요?",
            "hint": "한 script는 Invoke를 호출하고, 다른 script는 OnEnable에서 += 를 썼어요.",
            "options": ["Stamina가 OnStaminaChanged event를 발생시키고, OnEnable에서 구독한 StaminaBar가 UpdateBar를 실행해요", "StaminaBar가 매 frame Update에서 Stamina.Instance를 읽어요", "Stamina가 GameObject.Find로 bar를 찾아 값을 설정해요", "PlayerController가 dash 후마다 bar를 갱신해요"],
            "explanation": "이게 Observer pattern이에요: Stamina는 bar가 있는지 몰라요. OnStaminaChanged만 발생시키고, 구독한 쪽(StaminaBar)이 반응해요. OnDisable에서 -= 로 구독을 해제해요.",
        },
    },
    {
        "id": "combat2d.damage-recovery",
        "type": "MultipleChoice",
        "code": """[SerializeField] private float damageRecoveryTime = 1f;

public void TakeDamage(int damageAmount, Transform hitTransform)
{
    if (!canTakeDamage) { return; }
    knockback.GetKnockedBack(hitTransform, knockBackThrustAmount);
    canTakeDamage = false;
    currentHealth -= damageAmount;
    StartCoroutine(DamageRecoveryRoutine());
}

private IEnumerator DamageRecoveryRoutine()
{
    yield return new WaitForSeconds(damageRecoveryTime);
    canTakeDamage = true;
}""",
        "highlight": [1, 5, 7, 15],
        "source": ("Assets/Scripts/Player/PlayerHealth.cs", "public void TakeDamage(", "canTakeDamage = true;"),
        "en": {
            "context": "A Ghost bullet hits you. Half a second later a second bullet hits you too.",
            "prompt": "How much health does the second bullet take?",
            "hint": "What is canTakeDamage after the first hit, and when does it become true again?",
            "options": ["None - you are still invulnerable", "1, like the first one", "2 - hits stack", "All of it - you die"],
            "explanation": "The first hit sets canTakeDamage = false for damageRecoveryTime (1 s). The second hit comes after 0.5 s, so TakeDamage returns at the first line.",
        },
        "sk": {
            "context": "Zasiahne ťa guľka od Ghosta. O pol sekundy ťa zasiahne aj druhá.",
            "prompt": "Koľko health ti zoberie druhá guľka?",
            "hint": "Aké je canTakeDamage po prvom zásahu a kedy bude znova true?",
            "options": ["Nič - si stále nezraniteľný", "1, ako prvá", "2 - zásahy sa sčítajú", "Všetko - zomrieš"],
            "explanation": "Prvý zásah nastaví canTakeDamage = false na damageRecoveryTime (1 s). Druhý príde po 0,5 s, takže TakeDamage skončí hneď na prvom riadku.",
        },
        "ko": {
            "context": "Ghost의 bullet에 맞았어요. 0.5초 뒤 두 번째 bullet에도 맞아요.",
            "prompt": "두 번째 bullet은 health를 얼마나 깎을까요?",
            "hint": "첫 번째로 맞은 뒤 canTakeDamage는 뭐고, 언제 다시 true가 될까요?",
            "options": ["0 - 아직 무적이에요", "첫 번째처럼 1", "2 - 데미지가 쌓여요", "전부 - 죽어요"],
            "explanation": "첫 번째 hit이 damageRecoveryTime(1초) 동안 canTakeDamage = false로 만들어요. 두 번째는 0.5초 뒤라서 TakeDamage가 첫 줄에서 return해요.",
        },
    },
    {
        "id": "combat2d.knockback-steer",
        "type": "MultipleChoice",
        "code": """// PlayerController.cs (FixedUpdate)
private void Move()
{
    if (knockback.GettingKnockedBack || PlayerHealth.Instance.IsDead) { return; }
    rb.MovePosition(rb.position + movement * (moveSpeed * Time.fixedDeltaTime));
}

// Knockback.cs
[SerializeField] private float knockBacktime = .2f;""",
        "highlight": [4, 9],
        "source": ("Assets/Scripts/Player/PlayerController.cs", "private void Move()", "rb.MovePosition(rb.position + movement"),
        "en": {
            "context": "A slime hits you and the knockback starts. You keep holding the stick to run away.",
            "prompt": "What does your input do during the knockback?",
            "hint": "Look at the first line of Move(). What is GettingKnockedBack during the knockback?",
            "options": ["Nothing - for 0.2 s you only slide where the hit pushed you", "You steer the knockback in any direction", "You move twice as fast", "The knockback is cancelled"],
            "explanation": "While GettingKnockedBack is true, Move() returns before MovePosition. After knockBacktime (0.2 s) Knockback zeroes the velocity and your input works again.",
        },
        "sk": {
            "context": "Zasiahne ťa slime a začne knockback. Stále držíš stick, aby si utiekol.",
            "prompt": "Čo robí tvoj input počas knockbacku?",
            "hint": "Pozri prvý riadok Move(). Aké je GettingKnockedBack počas knockbacku?",
            "options": ["Nič - 0,2 s len kĺžeš tam, kam ťa zásah odhodil", "Knockback môžeš riadiť ľubovoľným smerom", "Hýbeš sa dvakrát rýchlejšie", "Knockback sa zruší"],
            "explanation": "Kým je GettingKnockedBack true, Move() skončí pred MovePosition. Po knockBacktime (0,2 s) Knockback vynuluje velocity a input znova funguje.",
        },
        "ko": {
            "context": "slime에게 맞아서 knockback이 시작됐어요. 도망치려고 stick을 계속 누르고 있어요.",
            "prompt": "knockback 동안 입력은 어떻게 될까요?",
            "hint": "Move()의 첫 줄을 보세요. knockback 동안 GettingKnockedBack은 뭘까요?",
            "options": ["아무 효과 없어요 - 0.2초 동안 맞은 방향으로 밀려나기만 해요", "knockback 방향을 마음대로 조종해요", "두 배 빨리 움직여요", "knockback이 취소돼요"],
            "explanation": "GettingKnockedBack이 true인 동안 Move()는 MovePosition 전에 return해요. knockBacktime(0.2초) 뒤 Knockback이 velocity를 0으로 만들고 입력이 다시 동작해요.",
        },
    },
    {
        "id": "combat2d.knockback-direction",
        "type": "MultipleChoice",
        "code": """public void GetKnockedBack(Transform damageSource, float knockbackThrust)
{
    GettingKnockedBack = true;
    Vector2 difference = (transform.position - damageSource.position).normalized * knockbackThrust * rb.mass;
    rb.AddForce(difference, ForceMode2D.Impulse);
    StartCoroutine(KnockRoutine());
}""",
        "highlight": [4, 5],
        "source": ("Assets/Scripts/Misc/Knockback.cs", "public void GetKnockedBack(", "StartCoroutine(KnockRoutine());"),
        "en": {
            "context": "A slime touches you from your left side. PlayerHealth calls GetKnockedBack with the slime's transform.",
            "prompt": "Which way are you pushed?",
            "hint": "transform.position - damageSource.position is an arrow from the slime to you.",
            "options": ["To the right - away from the slime", "To the left - towards the slime", "Up, always", "Towards the mouse cursor"],
            "explanation": "My position minus the source's position points from the slime to me. Normalized and multiplied by the thrust, it pushes me away from whatever hit me.",
        },
        "sk": {
            "context": "Slime sa ťa dotkne z ľavej strany. PlayerHealth zavolá GetKnockedBack s transformom slimu.",
            "prompt": "Ktorým smerom ťa to odhodí?",
            "hint": "transform.position - damageSource.position je šípka od slimu k tebe.",
            "options": ["Doprava - preč od slimu", "Doľava - k slimu", "Vždy hore", "Ku kurzoru myši"],
            "explanation": "Moja pozícia mínus pozícia zdroja ukazuje od slimu ku mne. Normalizované a vynásobené thrustom ma to odtlačí preč od toho, čo ma zasiahlo.",
        },
        "ko": {
            "context": "slime이 왼쪽에서 닿았어요. PlayerHealth가 slime의 transform으로 GetKnockedBack을 호출해요.",
            "prompt": "어느 쪽으로 밀려날까요?",
            "hint": "transform.position - damageSource.position 은 slime에서 나를 향하는 화살표예요.",
            "options": ["오른쪽 - slime에서 멀어지는 쪽", "왼쪽 - slime 쪽", "항상 위쪽", "마우스 커서 쪽"],
            "explanation": "내 위치에서 source의 위치를 빼면 slime에서 나를 향해요. normalize하고 thrust를 곱하면 나를 때린 것에서 멀리 밀어내요.",
        },
    },
    {
        "id": "combat2d.slime-attack-range",
        "type": "MultipleChoice",
        "code": """[SerializeField] private float attackRange = 0f;   // Slime prefab: 0, Ghost: 6

private void Roaming()
{
    enemyPathfinding.MoveTo(roamPosition);

    if (Vector2.Distance(transform.position, PlayerController.Instance.transform.position) < attackRange)
    {
        state = State.Attacking;
    }
}""",
        "highlight": [1, 7, 9],
        "source": ("Assets/Scripts/Enemies/EnemyAI.cs", "private void Roaming()", "state = State.Attacking;"),
        "en": {
            "context": "Every enemy uses EnemyAI. The Slime prefab has attackRange = 0. You walk right up to a slime.",
            "prompt": "Does the slime ever switch to State.Attacking?",
            "hint": "Can a distance ever be smaller than 0?",
            "options": ["No - it keeps Roaming; it only hurts you by touching you", "Yes, as soon as it touches you", "Yes, it is always Attacking", "Yes, every 2 seconds"],
            "explanation": "A distance is never < 0, so the slime stays in Roaming. It still hurts you: PlayerHealth.OnCollisionStay2D calls TakeDamage when an EnemyAI touches the player.",
        },
        "sk": {
            "context": "Každý nepriateľ používa EnemyAI. Slime prefab má attackRange = 0. Prídeš úplne k slimu.",
            "prompt": "Prepne sa slime niekedy do State.Attacking?",
            "hint": "Môže byť vzdialenosť niekedy menšia ako 0?",
            "options": ["Nie - ostane v Roaming; zraní ťa len dotykom", "Áno, hneď ako sa ťa dotkne", "Áno, je stále v Attacking", "Áno, každé 2 sekundy"],
            "explanation": "Vzdialenosť nikdy nie je < 0, takže slime ostane v Roaming. Aj tak ťa zraní: PlayerHealth.OnCollisionStay2D zavolá TakeDamage, keď sa hráča dotkne EnemyAI.",
        },
        "ko": {
            "context": "모든 적은 EnemyAI를 써요. Slime prefab은 attackRange = 0이에요. slime 바로 앞까지 걸어가요.",
            "prompt": "slime이 State.Attacking으로 바뀔 때가 있을까요?",
            "hint": "거리가 0보다 작을 수 있을까요?",
            "options": ["아니요 - 계속 Roaming이고, 닿을 때만 데미지를 줘요", "네, 닿자마자요", "네, 항상 Attacking이에요", "네, 2초마다요"],
            "explanation": "거리는 절대 < 0이 아니라서 slime은 Roaming에 머물러요. 그래도 데미지는 줘요: EnemyAI가 플레이어에 닿으면 PlayerHealth.OnCollisionStay2D가 TakeDamage를 호출해요.",
        },
    },
    {
        "id": "combat2d.ghost-angle-step",
        "type": "MultipleChoice",
        "code": """// Ghost prefab: angleSpread = 165, projectilesPerBurst = 8
if (angleSpread != 0)
{
    angleStep = angleSpread / (projectilesPerBurst - 1);
    halfAngleSpread = angleSpread / 2f;
    startAngle = targetAngle - halfAngleSpread;
    endAngle = targetAngle + halfAngleSpread;
}""",
        "highlight": [1, 4],
        "source": ("Assets/Scripts/Enemies/Shooter.cs", "if (angleSpread != 0)", "currentAngle = startAngle;\n        }"),
        "en": {
            "context": "Before each burst the Ghost's Shooter works out a cone of bullets around you.",
            "prompt": "How many degrees apart are two neighbouring bullets in one burst?",
            "hint": "8 bullets have 7 gaps between them. The code divides by (projectilesPerBurst - 1).",
            "options": ["About 23.6° (165 / 7)", "About 20.6° (165 / 8)", "165°", "82.5°"],
            "explanation": "8 bullets from one edge of the 165° cone to the other leave 7 gaps: 165 / 7 = 23.57°. The first bullet flies at targetAngle - 82.5°, the last at targetAngle + 82.5°.",
        },
        "sk": {
            "context": "Pred každým burstom si Shooter Ghosta vypočíta kužeľ guliek okolo teba.",
            "prompt": "O koľko stupňov sú od seba dve susedné guľky v jednom burste?",
            "hint": "8 guliek má medzi sebou 7 medzier. Kód delí (projectilesPerBurst - 1).",
            "options": ["Asi 23,6° (165 / 7)", "Asi 20,6° (165 / 8)", "165°", "82,5°"],
            "explanation": "8 guliek od jedného okraja 165° kužeľa po druhý necháva 7 medzier: 165 / 7 = 23,57°. Prvá letí na targetAngle - 82,5°, posledná na targetAngle + 82,5°.",
        },
        "ko": {
            "context": "burst마다 Ghost의 Shooter가 나를 중심으로 bullet 원뿔을 계산해요.",
            "prompt": "한 burst에서 이웃한 bullet 두 개는 몇 도 떨어져 있을까요?",
            "hint": "bullet 8개 사이에는 간격이 7개예요. 코드는 (projectilesPerBurst - 1)로 나눠요.",
            "options": ["약 23.6° (165 / 7)", "약 20.6° (165 / 8)", "165°", "82.5°"],
            "explanation": "165° 원뿔의 한쪽 끝에서 다른 쪽 끝까지 bullet 8개면 간격이 7개예요: 165 / 7 = 23.57°. 첫 bullet은 targetAngle - 82.5°, 마지막은 targetAngle + 82.5°로 날아가요.",
        },
    },
    {
        "id": "combat2d.stagger-timing",
        "type": "MultipleChoice",
        "code": """// Ghost prefab: timeBetweenBursts = 1, projectilesPerBurst = 8, stagger = true
if (stagger)
{ timeBetweenProjectiles = timeBetweenBursts / projectilesPerBurst; }

for (int j = 0; j < projectilesPerBurst; j++)
{
    // ... Instantiate one bullet ...
    if (stagger) { yield return new WaitForSeconds(timeBetweenProjectiles); }
}""",
        "highlight": [1, 3, 8],
        "source": ("Assets/Scripts/Enemies/Shooter.cs", "if (stagger)\n        { timeBetweenProjectiles", "if (stagger) { yield return new WaitForSeconds(timeBetweenProjectiles); }"),
        "en": {
            "context": "With stagger on, the Ghost does not fire a whole burst at once - it sweeps the cone bullet by bullet.",
            "prompt": "How often does a new bullet come out?",
            "hint": "timeBetweenProjectiles = timeBetweenBursts / projectilesPerBurst. Put in 1 and 8.",
            "options": ["Every 0.125 s - one burst takes 1 s", "Every 1 s", "Every 8 s", "All 8 at the same moment"],
            "explanation": "1 / 8 = 0.125 s between bullets, so the 8 bullets of a burst are spread over 1 second - the sweeping look of the Ghost.",
        },
        "sk": {
            "context": "So zapnutým stagger Ghost nevystrelí celý burst naraz - prejde kužeľ guľku po guľke.",
            "prompt": "Ako často vyletí nová guľka?",
            "hint": "timeBetweenProjectiles = timeBetweenBursts / projectilesPerBurst. Dosaď 1 a 8.",
            "options": ["Každých 0,125 s - jeden burst trvá 1 s", "Každú 1 s", "Každých 8 s", "Všetkých 8 v tej istej chvíli"],
            "explanation": "1 / 8 = 0,125 s medzi guľkami, takže 8 guliek burstu sa rozloží na 1 sekundu - preto ten zametací pohyb Ghosta.",
        },
        "ko": {
            "context": "stagger가 켜져 있으면 Ghost는 burst를 한 번에 쏘지 않고 bullet 하나씩 원뿔을 훑어요.",
            "prompt": "새 bullet은 얼마나 자주 나올까요?",
            "hint": "timeBetweenProjectiles = timeBetweenBursts / projectilesPerBurst. 1과 8을 넣어 보세요.",
            "options": ["0.125초마다 - 한 burst에 1초", "1초마다", "8초마다", "8개가 동시에"],
            "explanation": "1 / 8 = bullet 사이 0.125초라서, burst의 bullet 8개가 1초에 걸쳐 나와요 - Ghost가 훑듯이 쏘는 이유예요.",
        },
    },
    {
        "id": "combat2d.enemy-bullet-bush",
        "type": "TrueFalse",
        "code": """// Destructible.cs (bushes)
private void OnTriggerEnter2D(Collider2D other)
{
    Projectile projectile = other.gameObject.GetComponent<Projectile>();

    if (other.gameObject.GetComponent<DamageSource>() || (projectile && !projectile.IsEnemyProjectile))
    {
        pickUpSpawner?.DropItems();
        Destroy(gameObject);
    }
}""",
        "highlight": [6],
        "source": ("Assets/Scripts/Misc/Destructible.cs", "private void OnTriggerEnter2D", "Destroy(gameObject);"),
        "en": {
            "context": "A Ghost bullet (isEnemyProjectile = true) flies through a bush.",
            "prompt": "True or false: the bush breaks and drops loot.",
            "hint": "The if needs the player's weapon (DamageSource) or a projectile that is NOT an enemy projectile.",
            "options": ["True", "False"],
            "explanation": "False. The bullet is a Projectile, but !projectile.IsEnemyProjectile is false, so the condition fails and the bush stays. Only your glaive, arrows and laser break bushes.",
        },
        "sk": {
            "context": "Guľka od Ghosta (isEnemyProjectile = true) preletí cez ker.",
            "prompt": "Pravda alebo nepravda: ker sa rozbije a pustí loot.",
            "hint": "if potrebuje zbraň hráča (DamageSource) alebo projektil, ktorý NIE JE nepriateľský.",
            "options": ["Pravda", "Nepravda"],
            "explanation": "Nepravda. Guľka je Projectile, ale !projectile.IsEnemyProjectile je false, takže podmienka neplatí a ker ostane. Kríky rozbije len tvoj glaive, šípy a laser.",
        },
        "ko": {
            "context": "Ghost의 bullet(isEnemyProjectile = true)이 덤불을 통과해요.",
            "prompt": "참일까 거짓일까: 덤불이 부서지고 loot를 떨어뜨려요.",
            "hint": "if에는 플레이어의 무기(DamageSource) 또는 적의 것이 아닌 projectile이 필요해요.",
            "options": ["참", "거짓"],
            "explanation": "거짓이에요. bullet은 Projectile이지만 !projectile.IsEnemyProjectile 이 false라서 조건이 안 맞고 덤불은 그대로예요. 덤불은 내 glaive, 화살, laser만 부숴요.",
        },
        "answerIndex": 1,
    },
    {
        "id": "combat2d.glaive-hits",
        "type": "MultipleChoice",
        "code": """// Glaive.asset: weaponDamage = 1    Staff.asset: weaponDamage = 3
// EnemyHealth.cs
[SerializeField] private int startingHealth = 3;

public void TakeDamage(int damage)
{
    currentHealth -= damage;
    knockback.GetKnockedBack(PlayerController.Instance.transform, knockBackFloat);
    StartCoroutine(CheckDetectDeathRoutine());
}

private void DetectDeath()
{
    if (currentHealth <= 0) { /* death VFX, DropItems, Destroy */ }
}""",
        "highlight": [1, 3, 7, 14],
        "source": ("Assets/Scripts/Enemies/EnemyHealth.cs", "[SerializeField] private int startingHealth", "Destroy(gameObject);"),
        "en": {
            "context": "DamageSource on your glaive calls TakeDamage with the glaive's weaponDamage. A slime starts with startingHealth 3.",
            "prompt": "How many glaive hits does it take to kill a slime?",
            "hint": "Each hit subtracts weaponDamage (1). When does currentHealth reach 0?",
            "options": ["3", "1", "2", "4"],
            "explanation": "3 - 1 - 1 - 1 = 0, so the third hit kills it. The staff (weaponDamage 3) kills a slime in one hit.",
        },
        "sk": {
            "context": "DamageSource na tvojom glaive zavolá TakeDamage s weaponDamage glaivu. Slime začína so startingHealth 3.",
            "prompt": "Koľko zásahov glaivom treba na zabitie slimu?",
            "hint": "Každý zásah odpočíta weaponDamage (1). Kedy currentHealth dosiahne 0?",
            "options": ["3", "1", "2", "4"],
            "explanation": "3 - 1 - 1 - 1 = 0, takže ho zabije tretí zásah. Staff (weaponDamage 3) zabije slime jedným zásahom.",
        },
        "ko": {
            "context": "glaive의 DamageSource가 glaive의 weaponDamage로 TakeDamage를 호출해요. slime은 startingHealth 3으로 시작해요.",
            "prompt": "glaive로 몇 번 때려야 slime이 죽을까요?",
            "hint": "한 번 맞을 때마다 weaponDamage(1)를 빼요. currentHealth는 언제 0이 될까요?",
            "options": ["3", "1", "2", "4"],
            "explanation": "3 - 1 - 1 - 1 = 0이라서 세 번째 hit에 죽어요. staff(weaponDamage 3)는 slime을 한 방에 죽여요.",
        },
    },
    {
        "id": "combat2d.singleton-duplicate",
        "type": "MultipleChoice",
        "code": """public class Singleton<T> : MonoBehaviour where T : Singleton<T>
{
    private static T instance;

    protected virtual void Awake()
    {
        if (instance != null && this.gameObject != null)
        {
            Destroy(this.gameObject);
        }
        else
        {
            instance = (T)this;
        }

        if (!gameObject.transform.parent)
        {
            DontDestroyOnLoad(gameObject);
        }
    }
}""",
        "highlight": [7, 9, 13, 18],
        "source": ("Assets/Scripts/SceneManagement/Singleton.cs", "protected virtual void Awake()", "DontDestroyOnLoad(gameObject);"),
        "en": {
            "context": "You start in Town and walk through a gate into Scene_1. Scene_1 has its own copy of the Player prefab, so it can also be started on its own.",
            "prompt": "What happens to the Player that was placed in Scene_1?",
            "hint": "When Scene_1's Player runs Awake, is instance already set?",
            "options": ["It destroys itself - the Player from Town (DontDestroyOnLoad) carries on", "It replaces the Player from Town", "There are now two Players", "Both Players are destroyed"],
            "explanation": "The Player from Town already set instance and survived the scene load (DontDestroyOnLoad). Scene_1's copy finds instance != null and destroys itself.",
        },
        "sk": {
            "context": "Začneš v Town a prejdeš bránou do Scene_1. Scene_1 má vlastnú kópiu Player prefabu, aby sa dala spustiť aj samostatne.",
            "prompt": "Čo sa stane s Playerom, ktorý bol položený v Scene_1?",
            "hint": "Keď Player zo Scene_1 spustí Awake, je instance už nastavená?",
            "options": ["Zničí sám seba - Player z Town (DontDestroyOnLoad) pokračuje", "Nahradí Playera z Town", "Teraz sú tam dvaja Playeri", "Zničia sa obaja"],
            "explanation": "Player z Town už nastavil instance a prežil načítanie scény (DontDestroyOnLoad). Kópia zo Scene_1 zistí, že instance != null, a zničí sa.",
        },
        "ko": {
            "context": "Town에서 시작해서 문을 지나 Scene_1로 가요. Scene_1은 단독으로도 시작할 수 있게 Player prefab 사본을 갖고 있어요.",
            "prompt": "Scene_1에 놓여 있던 Player는 어떻게 될까요?",
            "hint": "Scene_1의 Player가 Awake를 실행할 때 instance는 이미 설정돼 있을까요?",
            "options": ["스스로 파괴돼요 - Town에서 온 Player(DontDestroyOnLoad)가 계속해요", "Town에서 온 Player를 대체해요", "이제 Player가 두 명이에요", "두 Player 모두 파괴돼요"],
            "explanation": "Town의 Player가 이미 instance를 설정했고 scene 로드에서 살아남았어요(DontDestroyOnLoad). Scene_1의 사본은 instance != null 을 보고 스스로 파괴돼요.",
        },
    },
    {
        "id": "combat2d.area-entrance",
        "type": "TrueFalse",
        "code": """// AreaExit.cs - when the player walks in:
SceneManagement.Instance.SetTransitionName(sceneTransitionName);

// AreaEntrance.cs - in the new scene:
void Start()
{
    if (transitionName == SceneManagement.Instance.sceneTransitionName)
    {
        PlayerController.Instance.transform.position = this.transform.position;
    }
}""",
        "highlight": [2, 7, 9],
        "source": ("Assets/Scripts/SceneManagement/AreaEntrance.cs", "void Start()", "UIFade.Instance.FadeToClear();"),
        "en": {
            "context": "Scene_2 has two entrances. You leave Scene_1 through an exit whose sceneTransitionName is \"Scene1_Exit\".",
            "prompt": "True or false: the player appears at the entrance whose transitionName is \"Scene1_Exit\".",
            "hint": "Each AreaEntrance compares its own transitionName with the name the exit stored.",
            "options": ["True", "False"],
            "explanation": "True. Only the entrance with the matching name moves the player to itself. That is why entrance names must be unique in a scene.",
        },
        "sk": {
            "context": "Scene_2 má dva vstupy. Odídeš zo Scene_1 východom, ktorého sceneTransitionName je \"Scene1_Exit\".",
            "prompt": "Pravda alebo nepravda: hráč sa objaví pri vstupe, ktorého transitionName je \"Scene1_Exit\".",
            "hint": "Každý AreaEntrance porovná svoje transitionName s menom, ktoré uložil východ.",
            "options": ["Pravda", "Nepravda"],
            "explanation": "Pravda. Hráča k sebe presunie len vstup so zhodným menom. Preto musia byť mená vstupov v scéne unikátne.",
        },
        "ko": {
            "context": "Scene_2에는 입구가 두 개 있어요. sceneTransitionName이 \"Scene1_Exit\"인 출구로 Scene_1을 떠나요.",
            "prompt": "참일까 거짓일까: 플레이어는 transitionName이 \"Scene1_Exit\"인 입구에 나타나요.",
            "hint": "각 AreaEntrance는 자기 transitionName과 출구가 저장한 이름을 비교해요.",
            "options": ["참", "거짓"],
            "explanation": "참이에요. 이름이 일치하는 입구만 플레이어를 자기 위치로 옮겨요. 그래서 scene 안의 입구 이름은 고유해야 해요.",
        },
        "answerIndex": 0,
    },
    {
        "id": "combat2d.rage-gain",
        "type": "MultipleChoice",
        "code": """// Rage.cs (Player prefab values)
[SerializeField] private int ragePerEnemyHit = 3;
[SerializeField] private int ragePerKill = 5;
[SerializeField] private int ragePerDamageTaken = 10;

// DamageSource.cs - every glaive hit on an enemy:
enemyHealth.TakeDamage(damageAmount);
Rage.Instance.RegisterEnemyHit();

// EnemyHealth.cs - when the enemy dies:
Rage.Instance.RegisterKill();""",
        "highlight": [2, 3, 8, 11],
        "source": ("Assets/Scripts/Player/Rage.cs", "[SerializeField] private int ragePerEnemyHit", "[SerializeField] private int ragePerDamageTaken"),
        "en": {
            "context": "Your own Rage system. You start with 0 Rage, kill a slime with 3 glaive hits and do not get hit yourself.",
            "prompt": "How much Rage do you have now?",
            "hint": "Each of the 3 hits calls RegisterEnemyHit, and the kill calls RegisterKill once.",
            "options": ["14", "9", "5", "15"],
            "explanation": "3 hits x 3 = 9, plus 5 for the kill = 14. Getting hit yourself would add 10 more.",
        },
        "sk": {
            "context": "Tvoj vlastný Rage systém. Začneš s 0 Rage, zabiješ slime tromi zásahmi glaivom a sám zásah nedostaneš.",
            "prompt": "Koľko Rage máš teraz?",
            "hint": "Každý z 3 zásahov zavolá RegisterEnemyHit a zabitie raz zavolá RegisterKill.",
            "options": ["14", "9", "5", "15"],
            "explanation": "3 zásahy x 3 = 9, plus 5 za zabitie = 14. Keby ťa niečo zasiahlo, pribudlo by ešte 10.",
        },
        "ko": {
            "context": "내가 만든 Rage 시스템이에요. Rage 0에서 시작해서, glaive 3번으로 slime을 죽이고 나는 맞지 않아요.",
            "prompt": "지금 Rage는 얼마일까요?",
            "hint": "hit 3번마다 RegisterEnemyHit을 호출하고, kill은 RegisterKill을 한 번 호출해요.",
            "options": ["14", "9", "5", "15"],
            "explanation": "hit 3번 x 3 = 9, kill 5를 더하면 14예요. 내가 맞으면 10이 더 늘어요.",
        },
    },
]


def find_lines(project, rel_path, first, last):
    path = os.path.join(project, rel_path)
    with open(path, encoding="utf-8-sig") as f:
        text = f.read()
    start = text.find(first)
    if start < 0:
        raise SystemExit(f"{rel_path}: anchor not found: {first!r}")
    end = text.find(last, start)
    if end < 0:
        raise SystemExit(f"{rel_path}: anchor not found after the first: {last!r}")
    line_start = text.count("\n", 0, start) + 1
    line_end = text.count("\n", 0, end + len(last)) + 1
    return line_start, line_end


def main():
    project = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "..", "2DTopDownPixelCombat")
    ids = set()
    english = []
    for q in QUESTIONS:
        assert q["id"] not in ids, q["id"]
        ids.add(q["id"])
        code_lines = q["code"].count("\n") + 1
        assert all(1 <= h <= code_lines for h in q["highlight"]), q["id"]
        for lang in ("en", "sk", "ko"):
            assert len(q[lang]["options"]) == len(q["en"]["options"]), (q["id"], lang)
        file, first, last = q["source"]
        line_start, line_end = find_lines(project, file, first, last)
        en = q["en"]
        english.append({
            "id": q["id"],
            "difficulty": "Easy",
            "type": q["type"],
            "context": en["context"],
            "prompt": en["prompt"],
            "code": q["code"],
            "highlight": q["highlight"],
            "hint": en["hint"],
            "options": en["options"],
            "answerIndex": q.get("answerIndex", 0),
            "explanation": en["explanation"],
            "source": {"project": PROJECT, "file": file, "lineStart": line_start, "lineEnd": line_end},
        })

    title, description = PACK["en"]
    write(f"{PACK_ID}.json", {"id": PACK_ID, "title": title, "description": description, "questions": english})
    for lang in ("sk", "ko"):
        title, description = PACK[lang]
        write(f"{PACK_ID}.{lang}.json", {
            "title": title,
            "description": description,
            "questions": {q["id"]: {key: q[lang][key] for key in ("context", "prompt", "options", "hint", "explanation")} for q in QUESTIONS},
        })
    print(f"{len(QUESTIONS)} questions written")


def write(name, data):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


if __name__ == "__main__":
    main()
