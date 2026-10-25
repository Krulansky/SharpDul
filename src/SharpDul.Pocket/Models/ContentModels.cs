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
    public string Prompt { get; set; } = "";
    public string? Code { get; set; }
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
