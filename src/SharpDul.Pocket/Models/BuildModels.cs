namespace SharpDul.Pocket.Models;

/// <summary>
/// A Build Lab project: the game is assembled inside the app, one script puzzle at a time,
/// and each solved puzzle switches its part of the game on in the Lab.
/// wwwroot/content/builds/&lt;build&gt;.json, translations in &lt;build&gt;.&lt;lang&gt;.json.
/// </summary>
public class BuildProject
{
    public string Id { get; set; } = "";
    public string Title { get; set; } = "";
    public string Description { get; set; } = "";
    /// <summary>The Unity build-along course for the same game, if there is one.</summary>
    public string? CourseId { get; set; }
    public List<ScriptPuzzle> Puzzles { get; set; } = new();
}

/// <summary>
/// One script to assemble. Lines starting with "#" are given (locked); the others are shuffled
/// and must be tapped into order. "{{right|wrong|wrong}}" is a blank - the first option is right.
/// </summary>
public class ScriptPuzzle
{
    public string Id { get; set; } = "";
    public string Title { get; set; } = "";
    public string File { get; set; } = "";
    /// <summary>Which object the script sits on and what it does in the game.</summary>
    public string Context { get; set; } = "";
    public string Hint { get; set; } = "";
    /// <summary>Shown when solved: what just came alive in the game.</summary>
    public string Success { get; set; } = "";
    public List<string> Lines { get; set; } = new();
    /// <summary>Wrong lines mixed into the pool. They must stay unused.</summary>
    public List<string> Distractors { get; set; } = new();
    /// <summary>Other correct orders, as indices into the movable lines (0-based).</summary>
    public List<List<int>> Alternatives { get; set; } = new();
    /// <summary>FrenzyFeature names this puzzle switches on, e.g. "Spawner".</summary>
    public List<string> Unlocks { get; set; } = new();
}

public class BuildIndex
{
    public List<string> Builds { get; set; } = new();
}

public class BuildTranslation
{
    public string? Title { get; set; }
    public string? Description { get; set; }
    public Dictionary<string, PuzzleTranslation> Puzzles { get; set; } = new();
}

public class PuzzleTranslation
{
    public string? Title { get; set; }
    public string? Context { get; set; }
    public string? Hint { get; set; }
    public string? Success { get; set; }
}
