namespace SharpDul.Pocket.Models;

public enum Difficulty
{
    Easy,
    Medium,
    Hard,
}

public enum QuestionType
{
    MultipleChoice,
    WhatDoesItDo,
    TrueFalse,
}

/// <summary>Where in a real project a question comes from.</summary>
public class SourceRef
{
    public string Project { get; set; } = "";
    public string File { get; set; } = "";
    public int LineStart { get; set; }
    public int LineEnd { get; set; }

    public string Label => LineStart == LineEnd
        ? $"{Project} · {File}:{LineStart}"
        : $"{Project} · {File}:{LineStart}–{LineEnd}";
}

public class Question
{
    public string Id { get; set; } = "";
    public Difficulty Difficulty { get; set; }
    public QuestionType Type { get; set; }
    /// <summary>Plain-language setup: where this code lives and when it runs in the game.</summary>
    public string Context { get; set; } = "";
    public string Prompt { get; set; } = "";
    /// <summary>A trimmed snippet in which the answer can be found.</summary>
    public string? Code { get; set; }
    /// <summary>1-based lines of Code that hold the answer; shown highlighted.</summary>
    public List<int> Highlight { get; set; } = new();
    /// <summary>Points at what to look for in the code without giving the answer away.</summary>
    public string Hint { get; set; } = "";
    public List<string> Options { get; set; } = new();
    public int AnswerIndex { get; set; }
    public string Explanation { get; set; } = "";
    public SourceRef Source { get; set; } = new();
}

/// <summary>One JSON file in wwwroot/content: the questions for one project or topic.</summary>
public class ContentPack
{
    public string Id { get; set; } = "";
    public string Title { get; set; } = "";
    public string Description { get; set; } = "";
    public List<Question> Questions { get; set; } = new();
}

/// <summary>wwwroot/content/index.json: the list of pack files to load.</summary>
public class ContentIndex
{
    public List<string> Packs { get; set; } = new();
}
