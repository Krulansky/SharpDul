using System.Text.RegularExpressions;
using SharpDul.Pocket.Models;

namespace SharpDul.Pocket.Logic;

/// <summary>
/// The state of one script puzzle: which lines are placed in which order, which option each
/// blank shows, and whether the script is right. Pure logic - no UI, no storage.
/// </summary>
public class PuzzleBoard
{
    private static readonly Regex blankPattern = new(@"\{\{([^}]*)\}\}");

    /// <summary>Piece of a line: plain text, or a blank with its options.</summary>
    public record Segment(string Text, int BlankIndex);

    /// <summary>A line as shown: indentation plus segments.</summary>
    public class Line
    {
        public int Indent;
        public List<Segment> Segments = new();
        public string Raw = "";
    }

    /// <summary>One blank: its options in display order and which one is right.</summary>
    public class Blank
    {
        public List<string> Options = new();
        public int CorrectOption;
        public int? Chosen;
    }

    public class Chip
    {
        public int Id;
        public Line Line = new();
        public bool IsDistractor;
        /// <summary>Position among the movable lines of the solution; -1 for a distractor.</summary>
        public int SolutionIndex = -1;
    }

    public enum Problem
    {
        None,
        NotAllPlaced,
        DistractorUsed,
        WrongOrder,
        WrongBlank,
    }

    /// <summary>The script template: a locked line, or null where a movable line goes.</summary>
    public List<Line?> Template { get; } = new();
    public List<Chip> Chips { get; } = new();
    public List<Chip> Placed { get; } = new();
    public List<Blank> Blanks { get; } = new();

    public int SlotCount { get; }
    public IEnumerable<Chip> Pool => Chips.Where(chip => !Placed.Contains(chip));

    public Problem LastProblem { get; private set; }
    /// <summary>The slot (0-based among movable slots) or blank that is wrong, after Check.</summary>
    public int? WrongSlot { get; private set; }
    public int? WrongBlankIndex { get; private set; }

    private readonly ScriptPuzzle puzzle;
    private readonly List<string> solution = new();

    public PuzzleBoard(ScriptPuzzle puzzle, Random random)
    {
        this.puzzle = puzzle;
        int nextId = 0;

        foreach (string raw in puzzle.Lines)
        {
            if (raw.StartsWith('#'))
            {
                Template.Add(ParseLine(raw.Substring(1), random));
            }
            else
            {
                Template.Add(null);
                solution.Add(raw);
                Chips.Add(new Chip { Id = nextId++, Line = ParseLine(raw, random), SolutionIndex = solution.Count - 1 });
            }
        }
        foreach (string raw in puzzle.Distractors)
        {
            Chips.Add(new Chip { Id = nextId++, Line = ParseLine(raw, random), IsDistractor = true });
        }

        SlotCount = solution.Count;
        Shuffle(Chips, random);
    }

    /// <summary>A solved board for read-only display: everything in place, blanks right.</summary>
    public static PuzzleBoard Solved(ScriptPuzzle puzzle)
    {
        var board = new PuzzleBoard(puzzle, new Random(0));
        foreach (Chip chip in board.Chips.Where(chip => !chip.IsDistractor).OrderBy(chip => chip.SolutionIndex))
        {
            board.Placed.Add(chip);
        }
        foreach (Blank blank in board.Blanks)
        {
            blank.Chosen = blank.CorrectOption;
        }
        return board;
    }

    public void Place(Chip chip)
    {
        if (!Placed.Contains(chip) && Placed.Count < SlotCount)
        {
            Placed.Add(chip);
            ClearProblem();
        }
    }

    public void Unplace(Chip chip)
    {
        if (Placed.Remove(chip))
        {
            ClearProblem();
        }
    }

    public void Choose(int blankIndex, int option)
    {
        Blanks[blankIndex].Chosen = option;
        ClearProblem();
    }

    public bool Check()
    {
        WrongSlot = null;
        WrongBlankIndex = null;

        Chip? distractor = Placed.FirstOrDefault(chip => chip.IsDistractor);
        if (distractor != null)
        {
            LastProblem = Problem.DistractorUsed;
            WrongSlot = Placed.IndexOf(distractor);
            return false;
        }

        if (Placed.Count < SlotCount)
        {
            LastProblem = Problem.NotAllPlaced;
            return false;
        }

        if (!MatchesAnyOrder(out int firstWrong))
        {
            LastProblem = Problem.WrongOrder;
            WrongSlot = firstWrong;
            return false;
        }

        // Only the blanks that are actually on screen count: placed chips and locked lines.
        foreach (int blankIndex in VisibleBlankIndices())
        {
            Blank blank = Blanks[blankIndex];
            if (blank.Chosen != blank.CorrectOption)
            {
                LastProblem = Problem.WrongBlank;
                WrongBlankIndex = blankIndex;
                return false;
            }
        }

        LastProblem = Problem.None;
        return true;
    }

    private bool MatchesAnyOrder(out int firstWrong)
    {
        List<string> placed = Placed.Select(chip => chip.Line.Raw).ToList();

        var orders = new List<List<string>> { solution };
        foreach (List<int> alternative in puzzle.Alternatives)
        {
            if (alternative.Count == solution.Count)
            {
                orders.Add(alternative.Select(index => solution[index]).ToList());
            }
        }

        firstWrong = int.MaxValue;
        foreach (List<string> order in orders)
        {
            int mismatch = Enumerable.Range(0, order.Count).FirstOrDefault(i => placed[i] != order[i], -1);
            if (mismatch == -1)
            {
                return true;
            }
            firstWrong = Math.Min(firstWrong, mismatch);
        }
        return false;
    }

    private IEnumerable<int> VisibleBlankIndices()
    {
        IEnumerable<Line> lines = Template.Where(line => line != null).Select(line => line!)
            .Concat(Placed.Select(chip => chip.Line));
        return lines.SelectMany(line => line.Segments).Where(segment => segment.BlankIndex >= 0)
            .Select(segment => segment.BlankIndex);
    }

    private void ClearProblem()
    {
        LastProblem = Problem.None;
        WrongSlot = null;
        WrongBlankIndex = null;
    }

    private Line ParseLine(string raw, Random random)
    {
        string trimmed = raw.TrimStart(' ');
        var line = new Line { Indent = raw.Length - trimmed.Length, Raw = raw };

        int position = 0;
        foreach (Match match in blankPattern.Matches(trimmed))
        {
            if (match.Index > position)
            {
                line.Segments.Add(new Segment(trimmed.Substring(position, match.Index - position), -1));
            }

            List<string> options = match.Groups[1].Value.Split('|').ToList();
            string correct = options[0];
            Shuffle(options, random);
            Blanks.Add(new Blank { Options = options, CorrectOption = options.IndexOf(correct) });
            line.Segments.Add(new Segment("", Blanks.Count - 1));

            position = match.Index + match.Length;
        }
        if (position < trimmed.Length)
        {
            line.Segments.Add(new Segment(trimmed.Substring(position), -1));
        }
        return line;
    }

    private static void Shuffle<T>(List<T> list, Random random)
    {
        for (int i = list.Count - 1; i > 0; i--)
        {
            int j = random.Next(i + 1);
            (list[i], list[j]) = (list[j], list[i]);
        }
    }
}
