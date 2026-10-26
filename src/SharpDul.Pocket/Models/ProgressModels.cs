namespace SharpDul.Pocket.Models;

/// <summary>Spaced-repetition state of one question.</summary>
public class CardProgress
{
    public int Box { get; set; }
    public DateOnly Due { get; set; }
    public int TimesSeen { get; set; }
    public int TimesCorrect { get; set; }
}

/// <summary>Everything the app remembers. This is exactly what Export writes to the backup file.</summary>
public class ProgressData
{
    public const int CurrentVersion = 1;

    public int Version { get; set; } = CurrentVersion;
    public string Language { get; set; } = "en";
    public int Xp { get; set; }
    public HashSet<DateOnly> ActiveDays { get; set; } = new();
    public Dictionary<string, CardProgress> Cards { get; set; } = new();
}
