using System.Text.Json;
using System.Text.Json.Serialization;

namespace SharpDul.Pocket.Services;

public static class Json
{
    public static readonly JsonSerializerOptions Options = new(JsonSerializerDefaults.Web)
    {
        Converters = { new JsonStringEnumConverter() },
        WriteIndented = true,
    };
}
