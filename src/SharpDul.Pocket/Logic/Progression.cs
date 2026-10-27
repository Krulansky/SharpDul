using SharpDul.Pocket.Models;

namespace SharpDul.Pocket.Logic;

/// <summary>XP, levels and active days. Pure logic - no UI, no storage.</summary>
public static class Progression
{
    public const int ActiveDaysWindow = 7;
    public const int XpForCourseStep = 25;
    private const int XpForWrongAnswer = 2;

    public static int XpForAnswer(Difficulty difficulty, bool correct)
    {
        if (!correct)
        {
            return XpForWrongAnswer;
        }

        return difficulty switch
        {
            Difficulty.Medium => 20,
            Difficulty.Hard => 30,
            _ => 10,
        };
    }

    // Total XP needed to reach a level: 1 -> 0, 2 -> 100, 3 -> 300, 4 -> 600, ...
    public static int TotalXpForLevel(int level)
    {
        return 50 * level * (level - 1);
    }

    public static int GetLevel(int xp)
    {
        int level = 1;
        while (xp >= TotalXpForLevel(level + 1))
        {
            level++;
        }
        return level;
    }

    /// <summary>0..1 progress from the current level to the next.</summary>
    public static float GetLevelProgress(int xp)
    {
        int level = GetLevel(xp);
        int from = TotalXpForLevel(level);
        int to = TotalXpForLevel(level + 1);
        return (float)(xp - from) / (to - from);
    }

    /// <summary>Which of the last 7 days (oldest first, today last) had activity. A missed day never resets anything.</summary>
    public static bool[] GetActiveDays(ProgressData progress, DateOnly today)
    {
        bool[] days = new bool[ActiveDaysWindow];
        for (int i = 0; i < ActiveDaysWindow; i++)
        {
            DateOnly day = today.AddDays(i - (ActiveDaysWindow - 1));
            days[i] = progress.ActiveDays.Contains(day);
        }
        return days;
    }
}
