namespace SharpDul.Pocket.Logic;

/// <summary>One key of an AnimationCurve, as the .prefab file stores it.</summary>
public record CurveKey(float Time, float Value, float InSlope, float OutSlope);

/// <summary>
/// Unity's AnimationCurve for non-weighted keys: cubic Hermite between keys, using each key's
/// tangent slopes; outside the keys it clamps (m_PreInfinity / m_PostInfinity = 2).
/// </summary>
public class AnimCurve
{
    public List<CurveKey> Keys { get; } = new();

    public AnimCurve(IEnumerable<CurveKey> keys)
    {
        Keys.AddRange(keys);
    }

    public AnimCurve Clone() => new(Keys);

    public float Evaluate(float time)
    {
        if (Keys.Count == 0)
        {
            return 0f;
        }
        if (time <= Keys[0].Time)
        {
            return Keys[0].Value;
        }
        if (time >= Keys[^1].Time)
        {
            return Keys[^1].Value;
        }

        int i = 1;
        while (Keys[i].Time < time)
        {
            i++;
        }
        CurveKey a = Keys[i - 1], b = Keys[i];
        float dt = b.Time - a.Time;
        if (dt <= 0f)
        {
            return b.Value;
        }
        float s = (time - a.Time) / dt;
        float s2 = s * s, s3 = s2 * s;
        return (2 * s3 - 3 * s2 + 1) * a.Value
             + (s3 - 2 * s2 + s) * a.OutSlope * dt
             + (-2 * s3 + 3 * s2) * b.Value
             + (s3 - s2) * b.InSlope * dt;
    }

    /// <summary>Moves one key, kept between its neighbours so the keys stay in time order.</summary>
    public void MoveKey(int index, float time, float value)
    {
        if (index < 0 || index >= Keys.Count)
        {
            return;
        }
        float min = index > 0 ? Keys[index - 1].Time + 0.02f : 0f;
        float max = index < Keys.Count - 1 ? Keys[index + 1].Time - 0.02f : 1.1f;
        Keys[index] = Keys[index] with { Time = Math.Clamp(time, min, max), Value = Math.Clamp(value, -0.5f, 1.5f) };
    }

    // The curves stored in the director's prefabs (2DTopDownPixelCombat).
    public static AnimCurve Grape() => new(new[]
    {
        new CurveKey(0f, 0f, 2f, 2f),
        new CurveKey(0.49841797f, 0.4995572f, -0.007457613f, -0.007457613f),
        new CurveKey(1.0124857f, -0.0023566913f, -1.9679554f, -1.9679554f),
    });

    public static AnimCurve FelFireGlobe() => new(new[]
    {
        new CurveKey(0.003376007f, 0f, 0.3972145f, 0.3972145f),
        new CurveKey(0.49841797f, 0.20342225f, -0.007457613f, -0.007457613f),
        new CurveKey(1.0327356f, 0.0014277454f, -0.2261788f, -0.2261788f),
    });

    public static AnimCurve Flat() => new(new[]
    {
        new CurveKey(0f, 0f, 0f, 0f),
        new CurveKey(0.5f, 0f, 0f, 0f),
        new CurveKey(1f, 0f, 0f, 0f),
    });

    public static AnimCurve FullHeight() => new(new[]
    {
        new CurveKey(0f, 0f, 4f, 4f),
        new CurveKey(0.5f, 1f, 0f, 0f),
        new CurveKey(1f, 0f, -4f, -4f),
    });

    public static AnimCurve LateDrop() => new(new[]
    {
        new CurveKey(0f, 0f, 2.5f, 2.5f),
        new CurveKey(0.8f, 0.9f, 0f, 0f),
        new CurveKey(1f, 0f, -9f, -9f),
    });
}
