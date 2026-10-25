using SharpDul.Pocket.Models;

namespace SharpDul.Pocket.Logic;

/// <summary>
/// Leitner boxes: a correct answer moves a card one box up and pushes it further into the
/// future, a wrong answer sends it back to box 1. Pure logic - no UI, no storage.
/// </summary>
public static class LeitnerScheduler
{
    public const int MaxBox = 5;
    public const int MasteredBox = 4;

    // Days until a card in box N comes back. Index 0 = a card never answered.
    private static readonly int[] intervalDaysByBox = { 0, 1, 2, 4, 8, 16 };

    public static bool IsDue(CardProgress? card, DateOnly today)
    {
        return card == null || card.Due <= today;
    }

    public static CardProgress Answer(CardProgress? card, bool correct, DateOnly today)
    {
        card ??= new CardProgress();

        card.TimesSeen++;
        if (correct)
        {
            card.TimesCorrect++;
            card.Box = Math.Min(card.Box + 1, MaxBox);
        }
        else
        {
            card.Box = 1;
        }

        card.Due = today.AddDays(intervalDaysByBox[card.Box]);
        return card;
    }
}
