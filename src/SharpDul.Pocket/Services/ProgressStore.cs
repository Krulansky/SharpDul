using System.Text.Json;
using Microsoft.JSInterop;
using SharpDul.Pocket.Logic;
using SharpDul.Pocket.Models;

namespace SharpDul.Pocket.Services;

/// <summary>
/// Owns the player's progress: keeps it in browser localStorage and exports/imports it as a
/// backup file. Pages read progress from here and report answers to it.
/// </summary>
public class ProgressStore
{
    private const string StorageKey = "sharpdul.progress";

    private readonly IJSRuntime js;
    private ProgressData? progress;

    public event EventHandler? OnProgressChanged;

    public ProgressStore(IJSRuntime js)
    {
        this.js = js;
    }

    public static DateOnly Today => DateOnly.FromDateTime(DateTime.Now);

    public async Task<ProgressData> GetAsync()
    {
        if (progress != null)
        {
            return progress;
        }

        string? json = await js.InvokeAsync<string?>("localStorage.getItem", StorageKey);
        progress = TryParse(json) ?? new ProgressData();
        return progress;
    }

    /// <summary>Records one answer: moves the card between boxes, adds XP, marks today active.</summary>
    public async Task<int> RecordAnswerAsync(Question question, bool correct)
    {
        ProgressData data = await GetAsync();
        DateOnly today = Today;

        data.Cards.TryGetValue(question.Id, out CardProgress? card);
        data.Cards[question.Id] = LeitnerScheduler.Answer(card, correct, today);

        int xp = Progression.XpForAnswer(question.Difficulty, correct);
        data.Xp += xp;
        data.ActiveDays.Add(today);

        await SaveAsync();
        return xp;
    }

    public async Task SetLanguageAsync(string languageCode)
    {
        ProgressData data = await GetAsync();
        data.Language = languageCode;
        await SaveAsync();
    }

    public async Task ExportAsync()
    {
        ProgressData data = await GetAsync();
        string json = JsonSerializer.Serialize(data, Json.Options);
        string fileName = $"sharpdul-backup-{Today:yyyy-MM-dd}.json";
        await js.InvokeVoidAsync("sharpDul.saveTextFile", fileName, json);
    }

    /// <summary>Replaces all progress with a backup file. Returns false if the file is not a SharpDul backup.</summary>
    public async Task<bool> ImportAsync(string json)
    {
        ProgressData? imported = TryParse(json);
        if (imported == null)
        {
            return false;
        }

        progress = imported;
        await SaveAsync();
        return true;
    }

    private async Task SaveAsync()
    {
        string json = JsonSerializer.Serialize(progress, Json.Options);
        await js.InvokeVoidAsync("localStorage.setItem", StorageKey, json);
        OnProgressChanged?.Invoke(this, EventArgs.Empty);
    }

    private static ProgressData? TryParse(string? json)
    {
        if (string.IsNullOrWhiteSpace(json))
        {
            return null;
        }

        try
        {
            ProgressData? data = JsonSerializer.Deserialize<ProgressData>(json, Json.Options);
            if (data == null || data.Version < 1 || data.Version > ProgressData.CurrentVersion)
            {
                return null;
            }
            return data;
        }
        catch (JsonException)
        {
            return null;
        }
    }
}
