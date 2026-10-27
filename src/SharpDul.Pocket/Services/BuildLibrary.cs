using System.Net.Http.Json;
using SharpDul.Pocket.Localization;
using SharpDul.Pocket.Models;

namespace SharpDul.Pocket.Services;

/// <summary>
/// Loads the Build Lab projects listed in wwwroot/content/builds/index.json, translated into
/// the chosen language where a translation exists. Code lines are never translated.
/// </summary>
public class BuildLibrary
{
    private readonly HttpClient http;
    private readonly Localizer localizer;
    private readonly Dictionary<Language, List<BuildProject>> buildsByLanguage = new();

    public BuildLibrary(HttpClient http, Localizer localizer)
    {
        this.http = http;
        this.localizer = localizer;
    }

    public async Task<IReadOnlyList<BuildProject>> GetBuildsAsync()
    {
        Language language = localizer.Current;
        if (buildsByLanguage.TryGetValue(language, out List<BuildProject>? cached))
        {
            return cached;
        }

        BuildIndex index = await http.GetFromJsonAsync<BuildIndex>("content/builds/index.json", Json.Options)
            ?? new BuildIndex();

        var loaded = new List<BuildProject>();
        foreach (string file in index.Builds)
        {
            BuildProject? build = await http.GetFromJsonAsync<BuildProject>($"content/builds/{file}", Json.Options);
            if (build == null)
            {
                continue;
            }

            if (language != Language.En)
            {
                BuildTranslation? translation = await TryLoadTranslationAsync(file, language);
                if (translation != null)
                {
                    ApplyTranslation(build, translation);
                }
            }
            loaded.Add(build);
        }

        buildsByLanguage[language] = loaded;
        return loaded;
    }

    public async Task<BuildProject?> GetBuildAsync(string id)
    {
        return (await GetBuildsAsync()).FirstOrDefault(build => build.Id == id);
    }

    private async Task<BuildTranslation?> TryLoadTranslationAsync(string buildFile, Language language)
    {
        string translationFile = Path.ChangeExtension(buildFile, $"{LanguageInfo.Code(language)}.json");
        try
        {
            return await http.GetFromJsonAsync<BuildTranslation>($"content/builds/{translationFile}", Json.Options);
        }
        catch (HttpRequestException)
        {
            return null;
        }
    }

    private static void ApplyTranslation(BuildProject build, BuildTranslation translation)
    {
        build.Title = translation.Title ?? build.Title;
        build.Description = translation.Description ?? build.Description;

        foreach (ScriptPuzzle puzzle in build.Puzzles)
        {
            if (!translation.Puzzles.TryGetValue(puzzle.Id, out PuzzleTranslation? text))
            {
                continue;
            }

            puzzle.Title = text.Title ?? puzzle.Title;
            puzzle.Context = text.Context ?? puzzle.Context;
            puzzle.Hint = text.Hint ?? puzzle.Hint;
            puzzle.Success = text.Success ?? puzzle.Success;
        }
    }
}
