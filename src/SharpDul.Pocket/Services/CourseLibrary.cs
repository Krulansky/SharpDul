using System.Net.Http.Json;
using SharpDul.Pocket.Localization;
using SharpDul.Pocket.Models;

namespace SharpDul.Pocket.Services;

/// <summary>
/// Loads the build-along courses listed in wwwroot/content/courses/index.json, translated into
/// the chosen language where a translation exists. Code is never translated.
/// </summary>
public class CourseLibrary
{
    private readonly HttpClient http;
    private readonly Localizer localizer;
    private readonly Dictionary<Language, List<Course>> coursesByLanguage = new();

    public CourseLibrary(HttpClient http, Localizer localizer)
    {
        this.http = http;
        this.localizer = localizer;
    }

    public async Task<IReadOnlyList<Course>> GetCoursesAsync()
    {
        Language language = localizer.Current;
        if (coursesByLanguage.TryGetValue(language, out List<Course>? cached))
        {
            return cached;
        }

        CourseIndex index = await http.GetFromJsonAsync<CourseIndex>("content/courses/index.json", Json.Options)
            ?? new CourseIndex();

        var loaded = new List<Course>();
        foreach (string file in index.Courses)
        {
            Course? course = await http.GetFromJsonAsync<Course>($"content/courses/{file}", Json.Options);
            if (course == null)
            {
                continue;
            }

            if (language != Language.En)
            {
                CourseTranslation? translation = await TryLoadTranslationAsync(file, language);
                if (translation != null)
                {
                    ApplyTranslation(course, translation);
                }
            }
            loaded.Add(course);
        }

        coursesByLanguage[language] = loaded;
        return loaded;
    }

    public async Task<Course?> GetCourseAsync(string id)
    {
        return (await GetCoursesAsync()).FirstOrDefault(course => course.Id == id);
    }

    private async Task<CourseTranslation?> TryLoadTranslationAsync(string courseFile, Language language)
    {
        string translationFile = Path.ChangeExtension(courseFile, $"{LanguageInfo.Code(language)}.json");
        try
        {
            return await http.GetFromJsonAsync<CourseTranslation>($"content/courses/{translationFile}", Json.Options);
        }
        catch (HttpRequestException)
        {
            return null;
        }
    }

    private static void ApplyTranslation(Course course, CourseTranslation translation)
    {
        course.Title = translation.Title ?? course.Title;
        course.Description = translation.Description ?? course.Description;

        foreach (CourseStep step in course.Steps)
        {
            if (!translation.Steps.TryGetValue(step.Id, out CourseStepTranslation? text))
            {
                continue;
            }

            step.Title = text.Title ?? step.Title;
            step.Goal = text.Goal ?? step.Goal;
            step.Check = text.Check ?? step.Check;
            // Lists are replaced only when complete, so a half-done translation never drops a step.
            if (text.Actions != null && text.Actions.Count == step.Actions.Count)
            {
                step.Actions = text.Actions;
            }
            if (text.Why != null && text.Why.Count == step.Why.Count)
            {
                step.Why = text.Why;
            }
        }
    }
}
