namespace SharpDul.Pocket.Localization;

public enum Language
{
    En,
    Sk,
    Ko,
}

public static class LanguageInfo
{
    public static readonly Language[] All = { Language.En, Language.Sk, Language.Ko };

    /// <summary>Short label on the language switch.</summary>
    public static string Label(Language language) => language switch
    {
        Language.Sk => "SK",
        Language.Ko => "KR",
        _ => "EN",
    };

    /// <summary>File suffix of a content translation, e.g. lualander-easy.sk.json.</summary>
    public static string Code(Language language) => language switch
    {
        Language.Sk => "sk",
        Language.Ko => "ko",
        _ => "en",
    };

    public static Language Parse(string? code) => code switch
    {
        "sk" => Language.Sk,
        "ko" => Language.Ko,
        _ => Language.En,
    };
}
