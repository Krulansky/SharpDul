namespace SharpDul.Pocket.Models;

/// <summary>
/// A build-along course: the director rebuilds a game in Unity step by step, A to Z.
/// wwwroot/content/courses/&lt;course&gt;.json, translations in &lt;course&gt;.&lt;lang&gt;.json.
/// </summary>
public class Course
{
    public string Id { get; set; } = "";
    public string Title { get; set; } = "";
    public string Description { get; set; } = "";
    /// <summary>Where the original comes from (course, repo).</summary>
    public string Source { get; set; } = "";
    /// <summary>Which lab page previews the steps, e.g. "lab/falling-frenzy".</summary>
    public string LabPath { get; set; } = "";
    public List<CourseStep> Steps { get; set; } = new();
}

public class CourseStep
{
    public string Id { get; set; } = "";
    public string Title { get; set; } = "";
    /// <summary>What the game can do after this step, in one sentence.</summary>
    public string Goal { get; set; } = "";
    /// <summary>What to do in Unity, with exact click paths, in order.</summary>
    public List<string> Actions { get; set; } = new();
    public List<CourseCode> Code { get; set; } = new();
    /// <summary>Why it works - the concepts behind the step.</summary>
    public List<string> Why { get; set; } = new();
    /// <summary>What you should see in Play mode when the step is done.</summary>
    public string Check { get; set; } = "";
    /// <summary>Lab preview stage: the game as it behaves after this step. 0 = no preview.</summary>
    public int LabStage { get; set; }
}

public class CourseCode
{
    public string File { get; set; } = "";
    public string Text { get; set; } = "";
    /// <summary>1-based lines that are new or changed in this step.</summary>
    public List<int> Highlight { get; set; } = new();
}

public class CourseIndex
{
    public List<string> Courses { get; set; } = new();
}

public class CourseTranslation
{
    public string? Title { get; set; }
    public string? Description { get; set; }
    public Dictionary<string, CourseStepTranslation> Steps { get; set; } = new();
}

public class CourseStepTranslation
{
    public string? Title { get; set; }
    public string? Goal { get; set; }
    public List<string>? Actions { get; set; }
    public List<string>? Why { get; set; }
    public string? Check { get; set; }
}
