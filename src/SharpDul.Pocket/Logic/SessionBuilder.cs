using SharpDul.Pocket.Models;

namespace SharpDul.Pocket.Logic;

/// <summary>Picks which questions a quiz session asks. Pure logic - no UI, no storage.</summary>
public static class SessionBuilder
{
    public const int DailySessionSize = 10;

    /// <summary>Daily: cards already being learned that are due first, then new cards.</summary>
    public static List<Question> BuildDaily(IEnumerable<Question> allQuestions, ProgressData progress, DateOnly today)
    {
        var due = new List<Question>();
        var fresh = new List<Question>();

        foreach (Question question in allQuestions)
        {
            progress.Cards.TryGetValue(question.Id, out CardProgress? card);
            if (card == null)
            {
                fresh.Add(question);
            }
            else if (LeitnerScheduler.IsDue(card, today))
            {
                due.Add(question);
            }
        }

        Shuffle(due);
        return due.Concat(fresh).Take(DailySessionSize).ToList();
    }

    /// <summary>Burst: every question of one pack, due or not, in random order.</summary>
    public static List<Question> BuildBurst(ContentPack pack)
    {
        var questions = new List<Question>(pack.Questions);
        Shuffle(questions);
        return questions;
    }

    public static int CountDue(IEnumerable<Question> allQuestions, ProgressData progress, DateOnly today)
    {
        return allQuestions.Count(question =>
            LeitnerScheduler.IsDue(progress.Cards.GetValueOrDefault(question.Id), today));
    }

    private static void Shuffle<T>(List<T> list)
    {
        for (int i = list.Count - 1; i > 0; i--)
        {
            int j = Random.Shared.Next(i + 1);
            (list[i], list[j]) = (list[j], list[i]);
        }
    }
}
