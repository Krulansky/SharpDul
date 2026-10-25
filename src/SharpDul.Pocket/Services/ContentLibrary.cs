using System.Net.Http.Json;
using SharpDul.Pocket.Models;

namespace SharpDul.Pocket.Services;

/// <summary>Loads the content packs listed in wwwroot/content/index.json, once.</summary>
public class ContentLibrary
{
    private readonly HttpClient http;
    private List<ContentPack>? packs;

    public ContentLibrary(HttpClient http)
    {
        this.http = http;
    }

    public async Task<IReadOnlyList<ContentPack>> GetPacksAsync()
    {
        if (packs != null)
        {
            return packs;
        }

        ContentIndex index = await http.GetFromJsonAsync<ContentIndex>("content/index.json", Json.Options)
            ?? new ContentIndex();

        var loaded = new List<ContentPack>();
        foreach (string file in index.Packs)
        {
            ContentPack? pack = await http.GetFromJsonAsync<ContentPack>($"content/{file}", Json.Options);
            if (pack != null)
            {
                loaded.Add(pack);
            }
        }

        packs = loaded;
        return packs;
    }

    public async Task<IEnumerable<Question>> GetAllQuestionsAsync()
    {
        return (await GetPacksAsync()).SelectMany(pack => pack.Questions);
    }
}
