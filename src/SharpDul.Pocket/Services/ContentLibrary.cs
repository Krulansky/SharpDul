using System.Net.Http.Json;
using SharpDul.Pocket.Localization;
using SharpDul.Pocket.Models;

namespace SharpDul.Pocket.Services;

/// <summary>
/// Loads the content packs listed in wwwroot/content/index.json, translated into the chosen
/// language where a translation file exists. Each language is loaded once.
/// </summary>
public class ContentLibrary
{
    private readonly HttpClient http;
    private readonly Localizer localizer;
    private readonly Dictionary<Language, List<ContentPack>> packsByLanguage = new();

    public ContentLibrary(HttpClient http, Localizer localizer)
    {
        this.http = http;
        this.localizer = localizer;
    }

    public async Task<IReadOnlyList<ContentPack>> GetPacksAsync()
    {
        Language language = localizer.Current;
        if (packsByLanguage.TryGetValue(language, out List<ContentPack>? cached))
        {
            return cached;
        }

        ContentIndex index = await http.GetFromJsonAsync<ContentIndex>("content/index.json", Json.Options)
            ?? new ContentIndex();

        var loaded = new List<ContentPack>();
        foreach (string file in index.Packs)
        {
            ContentPack? pack = await http.GetFromJsonAsync<ContentPack>($"content/{file}", Json.Options);
            if (pack == null)
            {
                continue;
            }

            if (language != Language.En)
            {
                PackTranslation? translation = await TryLoadTranslationAsync(file, language);
                if (translation != null)
                {
                    ApplyTranslation(pack, translation);
                }
            }
            loaded.Add(pack);
        }

        packsByLanguage[language] = loaded;
        return loaded;
    }

    private async Task<PackTranslation?> TryLoadTranslationAsync(string packFile, Language language)
    {
        string translationFile = Path.ChangeExtension(packFile, $"{LanguageInfo.Code(language)}.json");
        try
        {
            return await http.GetFromJsonAsync<PackTranslation>($"content/{translationFile}", Json.Options);
        }
        catch (HttpRequestException)
        {
            // No translation for this pack yet - English it is.
            return null;
        }
    }

    private static void ApplyTranslation(ContentPack pack, PackTranslation translation)
    {
        pack.Title = translation.Title ?? pack.Title;
        pack.Description = translation.Description ?? pack.Description;

        foreach (Question question in pack.Questions)
        {
            if (!translation.Questions.TryGetValue(question.Id, out QuestionTranslation? text))
            {
                continue;
            }

            question.Context = text.Context ?? question.Context;
            question.Prompt = text.Prompt ?? question.Prompt;
            question.Hint = text.Hint ?? question.Hint;
            question.Explanation = text.Explanation ?? question.Explanation;
            if (text.Options != null && text.Options.Count == question.Options.Count)
            {
                question.Options = text.Options;
            }
        }
    }
}
