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
