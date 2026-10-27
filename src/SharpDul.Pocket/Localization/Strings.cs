namespace SharpDul.Pocket.Localization;

/// <summary>
/// UI text in every language: { key, [English, Slovak, Korean] }.
/// Gamedev terms (Daily, Burst, XP, Level, Lab, ...) stay English in every language.
/// </summary>
public static class Strings
{
    private static readonly Dictionary<string, string[]> table = new()
    {
        ["tagline"] = new[] { "#Dul · gamedev coach", "#Dul · gamedev coach", "#Dul · gamedev coach" },
        ["loading"] = new[] { "Loading…", "Načítavam…", "로딩 중…" },
        ["home"] = new[] { "← Home", "← Home", "← Home" },
        ["level"] = new[] { "Level {0}", "Level {0}", "Level {0}" },
        ["activeDays"] = new[] { "Active {0} of the last {1} days", "Aktívny {0} z posledných {1} dní", "최근 {1}일 중 {0}일 활동" },
        ["daily"] = new[] { "Daily", "Daily", "Daily" },
        ["allCaughtUp"] = new[] { "All caught up", "Všetko zopakované", "모두 복습 완료" },
        ["cardsDue"] = new[] { "{0} cards due · up to {1} per session", "{0} kartičiek na zopakovanie · max {1} naraz", "복습할 카드 {0}장 · 한 번에 최대 {1}장" },
        ["projects"] = new[] { "Projects", "Projekty", "프로젝트" },
        ["masteredBurst"] = new[] { "Mastered {0} / {1} · Burst", "Zvládnuté {0} / {1} · Burst", "마스터 {0} / {1} · Burst" },
        ["labs"] = new[] { "Labs", "Labs", "Labs" },
        ["mechanicsLab"] = new[] { "Mechanics Lab", "Mechanics Lab", "Mechanics Lab" },
        ["mechanicsLabDesc"] = new[] { "Fly the LuaLander lander and tune its real code values live.", "Pilotuj LuaLander lander a naživo laď hodnoty z jeho kódu.", "LuaLander 착륙선을 조종하며 실제 코드 값을 실시간으로 조정해 보세요." },
        ["backupLink"] = new[] { "Backup (export / import)", "Záloha (export / import)", "백업 (export / import)" },

        ["nothingDue"] = new[] { "Nothing due right now", "Teraz nie je čo opakovať", "지금은 복습할 카드가 없어요" },
        ["nothingDueText"] = new[] { "Every card is resting until its next review. Pick a project for a Burst instead.", "Všetky kartičky oddychujú do ďalšieho opakovania. Skús Burst pri niektorom projekte.", "모든 카드가 다음 복습까지 쉬는 중이에요. 대신 프로젝트에서 Burst를 해 보세요." },
        ["backHome"] = new[] { "Back home", "Späť na Home", "Home으로" },
        ["sessionDone"] = new[] { "Session done", "Hotovo", "세션 완료" },
        ["sessionResult"] = new[] { "{0} / {1} correct · +{2} XP", "{0} / {1} správne · +{2} XP", "{0} / {1} 정답 · +{2} XP" },
        ["showHint"] = new[] { "Show hint", "Ukáž hint", "힌트 보기" },
        ["correct"] = new[] { "Correct", "Správne", "정답" },
        ["notQuite"] = new[] { "Not quite", "Nie celkom", "아쉬워요" },
        ["next"] = new[] { "Next", "Ďalej", "다음" },
        ["finish"] = new[] { "Finish", "Dokončiť", "완료" },
        ["true"] = new[] { "True", "Pravda", "참" },
        ["false"] = new[] { "False", "Nepravda", "거짓" },

        ["backup"] = new[] { "Backup", "Záloha", "백업" },
        ["export"] = new[] { "Export", "Export", "Export" },
        ["exportText"] = new[] { "Saves all progress (XP, active days, every card) into one file. On iPhone choose Save to Files and keep it in iCloud Drive.", "Uloží celý progres (XP, aktívne dni, všetky kartičky) do jedného súboru. Na iPhone zvoľ Save to Files a ulož ho do iCloud Drive.", "모든 진행 상황(XP, 활동일, 모든 카드)을 파일 하나로 저장해요. iPhone에서는 Save to Files를 눌러 iCloud Drive에 보관하세요." },
        ["exportButton"] = new[] { "Export progress", "Exportovať progres", "진행 상황 Export" },
        ["import"] = new[] { "Import", "Import", "Import" },
        ["importText"] = new[] { "Loads a backup file. It replaces the progress on this device.", "Načíta súbor zálohy. Nahradí progres na tomto zariadení.", "백업 파일을 불러와요. 이 기기의 진행 상황을 덮어써요." },
        ["chooseFile"] = new[] { "Choose backup file", "Vybrať súbor zálohy", "백업 파일 선택" },
        ["imported"] = new[] { "Progress imported.", "Progres importovaný.", "진행 상황을 불러왔어요." },
        ["notBackup"] = new[] { "This file is not a SharpDul backup. Nothing was changed.", "Tento súbor nie je SharpDul záloha. Nič sa nezmenilo.", "SharpDul 백업 파일이 아니에요. 아무것도 바뀌지 않았어요." },
        ["unreadable"] = new[] { "The file could not be read. Nothing was changed.", "Súbor sa nedal prečítať. Nič sa nezmenilo.", "파일을 읽을 수 없어요. 아무것도 바뀌지 않았어요." },
        ["notFound"] = new[] { "Page not found", "Stránka neexistuje", "페이지를 찾을 수 없어요" },

        ["courses"] = new[] { "Courses", "Kurzy", "코스" },
        ["course"] = new[] { "Course", "Kurz", "코스" },
        ["stepsBuilt"] = new[] { "{0} / {1} steps built", "{0} / {1} krokov postavených", "{1}단계 중 {0}단계 완성" },
        ["stepOf"] = new[] { "Step {0} / {1}", "Krok {0} / {1}", "{0} / {1}단계" },
        ["stepN"] = new[] { "Step {0}", "Krok {0}", "{0}단계" },
        ["inUnity"] = new[] { "In Unity", "V Unity", "Unity에서" },
        ["copy"] = new[] { "Copy", "Kopírovať", "복사" },
        ["copied"] = new[] { "Copied ✓", "Skopírované ✓", "복사됨 ✓" },
        ["highlightedIsNew"] = new[] { "Highlighted lines are new in this step.", "Zvýraznené riadky sú v tomto kroku nové.", "강조된 줄은 이번 단계에서 새로 추가됐어요." },
        ["whyItWorks"] = new[] { "Why it works", "Prečo to funguje", "왜 이렇게 동작할까" },
        ["checkInPlay"] = new[] { "Check in Play mode", "Over v Play mode", "Play mode에서 확인" },
        ["previewStep"] = new[] { "Preview this step in the Lab", "Náhľad tohto kroku v Labe", "Lab에서 이 단계 미리보기" },
        ["previewStepDesc"] = new[] { "See how the game behaves after this step - before you build it.", "Pozri sa, ako sa hra po tomto kroku správa - ešte predtým, než ho postavíš.", "만들기 전에, 이 단계 후 게임이 어떻게 동작하는지 보세요." },
        ["markBuilt"] = new[] { "I built it in Unity", "Postavil som to v Unity", "Unity에서 만들었어요" },
        ["builtIt"] = new[] { "Built", "Postavené", "완성" },
        ["previous"] = new[] { "Previous", "Späť", "이전" },
        ["backToCourse"] = new[] { "← Course", "← Kurz", "← 코스" },
        ["previewAfterStep"] = new[] { "The game after", "Hra po", "이 단계 후의 게임:" },
        ["dropAgain"] = new[] { "Drop the sheep again", "Pusti ovcu znova", "양 다시 떨어뜨리기" },
        ["appliesOnRetry"] = new[] { "applies on Retry", "platí po Znova", "다시 시작할 때 적용" },
        ["useForce"] = new[] { "Compare: move with AddForce instead of linearVelocity (LuaLander feel)", "Porovnaj: pohyb cez AddForce namiesto linearVelocity (pocit z LuaLandera)", "비교: linearVelocity 대신 AddForce로 이동 (LuaLander 느낌)" },
        ["noCodeYet"] = new[] { "No game code yet in this step - just the scene.", "V tomto kroku ešte nie je herný kód - len scéna.", "이 단계에는 아직 게임 코드가 없어요 - scene만 있어요." },
        ["ffStage1"] = new[] { "Empty scene - camera at (0, 9, -62), Field of View 20", "Prázdna scéna - kamera na (0, 9, -62), Field of View 20", "빈 scene - 카메라 (0, 9, -62), Field of View 20" },
        ["ffStage2"] = new[] { "The player box is placed - nothing moves yet", "Hráč je položený - zatiaľ sa nič nehýbe", "플레이어 상자 배치 완료 - 아직 아무것도 안 움직여요" },
        ["ffWatch"] = new[] { "Watch the sheep fall and bounce", "Sleduj, ako ovca padá a odráža sa", "양이 떨어지고 튀는 걸 보세요" },
        ["ffMove"] = new[] { "Hold A / D (or the buttons) to move", "Drž A / D (alebo tlačidlá) a hýb sa", "A / D (또는 버튼)를 눌러 움직이세요" },
        ["ffReadOnly"] = new[] { "Keys are read - but nothing moves the player yet", "Klávesy sa čítajú - ale hráčom ešte nič nehýbe", "키는 읽히지만 - 아직 아무것도 플레이어를 움직이지 않아요" },
        ["ffCaught"] = new[] { "Caught: {0}", "Chytené: {0}", "받은 양: {0}" },
        ["ffGameOver"] = new[] { "GAME OVER - caught {0}. Time.timeScale = 0", "GAME OVER - chytené {0}. Time.timeScale = 0", "GAME OVER - 받은 양 {0}. Time.timeScale = 0" },
        ["fallingFrenzyLabDesc"] = new[] { "The Falling Frenzy game at any step of the course.", "Hra Falling Frenzy v ktoromkoľvek kroku kurzu.", "코스의 어느 단계에서든 Falling Frenzy 게임을 볼 수 있어요." },
        ["buildLab"] = new[] { "Build Lab", "Build Lab", "Build Lab" },
        ["buildLabDesc"] = new[] { "Crack the scripts one by one - each one switches its part of the game on.", "Rozlúskni skripty jeden za druhým - každý zapne svoju časť hry.", "script를 하나씩 풀면 게임의 그 부분이 켜져요." },
        ["scriptsCracked"] = new[] { "{0} / {1} scripts cracked", "{0} / {1} skriptov rozlúsknutých", "script {1}개 중 {0}개 해결" },
        ["startOver"] = new[] { "Start over", "Začať odznova", "처음부터" },
        ["startOverConfirm"] = new[] { "Tap again to lock all scripts", "Ťukni znova - všetky skripty sa zamknú", "한 번 더 누르면 모든 script가 잠겨요" },
        ["tapToPlace"] = new[] { "Tap a line below to put it in the next empty slot. Tap a placed line to take it back. Pick the right word in every ____.", "Ťukni na riadok dole a dá sa do ďalšieho prázdneho miesta. Ťuknutím na položený riadok ho vrátiš. V každom ____ vyber správne slovo.", "아래 줄을 누르면 다음 빈칸에 들어가요. 놓인 줄을 누르면 되돌아가요. 모든 ____에서 맞는 단어를 고르세요." },
        ["checkScript"] = new[] { "Check the script", "Skontrolovať skript", "script 확인" },
        ["cracked"] = new[] { "Cracked! ✓", "Rozlúsknuté! ✓", "해결! ✓" },
        ["solvedEarlier"] = new[] { "Solved ✓", "Vyriešené ✓", "해결됨 ✓" },
        ["nextScript"] = new[] { "Next script", "Ďalší skript", "다음 script" },
        ["buildDone"] = new[] { "Every script cracked!", "Všetky skripty rozlúsknuté!", "모든 script 해결!" },
        ["buildDoneText"] = new[] { "The whole game runs on code you assembled. Next: build it for real in Unity with the course.", "Celá hra beží na kóde, ktorý si poskladal. Ďalej: postav ju naozaj v Unity s kurzom.", "게임 전체가 직접 조립한 코드로 돌아가요. 다음: 코스를 따라 Unity에서 진짜로 만들어 보세요." },
        ["toCourse"] = new[] { "Open the Unity course", "Otvoriť Unity kurz", "Unity 코스 열기" },
        ["problemNotAll"] = new[] { "Some slots are still empty.", "Niektoré miesta sú ešte prázdne.", "아직 빈칸이 있어요." },
        ["problemDistractor"] = new[] { "One of the placed lines does not belong in this script - it is marked red.", "Jeden z položených riadkov do tohto skriptu nepatrí - je označený červenou.", "놓인 줄 중 하나는 이 script에 속하지 않아요 - 빨간색으로 표시됐어요." },
        ["problemOrder"] = new[] { "Line {0} of the ones you placed is not right yet - it is marked red.", "Riadok {0} z tých, čo si položil, ešte nesedí - je označený červenou.", "놓은 줄 중 {0}번째가 아직 맞지 않아요 - 빨간색으로 표시됐어요." },
        ["problemBlank"] = new[] { "The order is right! One ____ has the wrong word - it is marked red.", "Poradie sedí! V jednom ____ je zlé slovo - je označené červenou.", "순서는 맞아요! ____ 하나에 틀린 단어가 있어요 - 빨간색으로 표시됐어요." },
        ["labIntro"] = new[] { "This is the physics of your Lander.cs (mass 1, Linear Damping 1, Angular Damping 5). Drag a slider - the matching line of code lights up and the lander changes at once.", "Toto je fyzika z tvojho Lander.cs (mass 1, Linear Damping 1, Angular Damping 5). Potiahni slider - rozsvieti sa príslušný riadok kódu a lander sa hneď zmení.", "내 Lander.cs의 물리 그대로예요 (mass 1, Linear Damping 1, Angular Damping 5). slider를 움직이면 해당 코드 줄이 빛나고 착륙선이 바로 바뀌어요." },
        ["labPress"] = new[] { "Hold a button to start", "Podrž tlačidlo a štartuj", "버튼을 눌러 시작하세요" },
        ["labFlying"] = new[] { "Flying", "Letíš", "비행 중" },
        ["labNoFuel"] = new[] { "Out of fuel!", "Došlo palivo!", "연료가 떨어졌어요!" },
        ["landedOk"] = new[] { "Successful landing! Score {0}", "Úspešné pristátie! Score {0}", "착륙 성공! Score {0}" },
        ["landedFast"] = new[] { "Crash - landed too hard (speed {0} > {1})", "Crash - príliš tvrdé pristátie (speed {0} > {1})", "Crash - 너무 세게 착륙 (speed {0} > {1})" },
        ["landedSteep"] = new[] { "Crash - too steep angle (dot {0} < {1})", "Crash - príliš veľký náklon (dot {0} < {1})", "Crash - 각도가 너무 기울었어요 (dot {0} < {1})" },
        ["landedTerrain"] = new[] { "Crash - you hit the terrain, not the landing pad", "Crash - narazil si do terénu, nie na landing pad", "Crash - landing pad가 아니라 지형에 부딪혔어요" },
        ["lost"] = new[] { "Lost in space - the lander left the screen", "Stratený vo vesmíre - lander uletel z obrazovky", "우주 미아 - 착륙선이 화면을 벗어났어요" },
        ["retry"] = new[] { "Retry", "Znova", "다시" },
        ["resetValues"] = new[] { "Reset values", "Pôvodné hodnoty", "기본값으로" },
        ["speed"] = new[] { "speed", "speed", "speed" },
        ["fuel"] = new[] { "fuel", "fuel", "fuel" },
        ["dot"] = new[] { "dot", "dot", "dot" },
        ["tuning"] = new[] { "Tuning", "Ladenie", "튜닝" },
        ["code"] = new[] { "Code", "Kód", "코드" },
    };

    public static string Get(string key, Language language)
    {
        if (!table.TryGetValue(key, out string[]? texts))
        {
            return key;
        }
        return texts[(int)language];
    }
}
