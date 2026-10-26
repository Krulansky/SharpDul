using SharpDul.Pocket.Services;

namespace SharpDul.Pocket.Localization;

/// <summary>Holds the chosen language (saved with the progress, so it is part of the backup).</summary>
public class Localizer
{
    private readonly ProgressStore progressStore;

    public Language Current { get; private set; } = Language.En;

    public event EventHandler? OnLanguageChanged;

    public Localizer(ProgressStore progressStore)
    {
        this.progressStore = progressStore;
    }

    public async Task InitAsync()
    {
        Language saved = LanguageInfo.Parse((await progressStore.GetAsync()).Language);
        if (saved != Current)
        {
            Current = saved;
            OnLanguageChanged?.Invoke(this, EventArgs.Empty);
        }
    }

    public async Task SetLanguageAsync(Language language)
    {
        if (language == Current)
        {
            return;
        }

        Current = language;
        await progressStore.SetLanguageAsync(LanguageInfo.Code(language));
        OnLanguageChanged?.Invoke(this, EventArgs.Empty);
    }

    public string this[string key] => Strings.Get(key, Current);

    public string Format(string key, params object[] args) => string.Format(Strings.Get(key, Current), args);
}
