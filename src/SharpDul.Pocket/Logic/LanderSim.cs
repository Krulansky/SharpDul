namespace SharpDul.Pocket.Logic;

/// <summary>
/// The values from LuaLander's Lander.cs that the Mechanics Lab lets you tune.
/// Defaults are the real values in the game.
/// </summary>
public class LanderTuning
{
    public float Force = 700f;                        // Lander.cs: float force = 700f;
    public float TurnSpeed = 100f;                    // Lander.cs: float turnSpeed = +100f;
    public float GravityNormal = 0.7f;                // Lander.cs: GRAVITY_NORMAL = 0.7f;
    public float FuelAmountMax = 10f;                 // Lander.cs: fuelAmountMax = 10f;
    public float SoftLandingVelocityMagnitude = 4f;   // Lander.cs: softLandingVelocityMagnitude = 4f;
    public float MinDotVector = 0.90f;                // Lander.cs: minDotVector = .90f;
}

public struct LanderInput
{
    public bool Up;
    public bool Left;
    public bool Right;

    public bool Any => Up || Left || Right;
}

/// <summary>
/// A plain C# port of LuaLander's Lander.cs plus the bits of Unity's Rigidbody2D it relies on
/// (mass 1, Linear Damping 1, Angular Damping 5, the BoxCollider2D size). It keeps the same
/// states, events and landing rules, so the Lab behaves like the game. No UI here - the page
/// draws it and reads the events, the same split as Lander / LanderVisuals.
/// The physics is a close approximation of Box2D, not a bit-exact copy.
/// </summary>
public class LanderSim
{
    public const float FixedDeltaTime = 0.02f;   // Unity's default Fixed Timestep
    public const float PadHalfWidth = 1.5f;
    public const float WorldHalfWidth = 10f;
    public const float WorldTop = 16f;

    private const float Gravity = -9.81f;
    private const float Mass = 1f;
    private const float LinearDamping = 1f;
    private const float AngularDamping = 5f;
    private const float ColliderWidth = 0.92f;
    private const float ColliderHeight = 1.47f;
    // Box inertia: m * (w^2 + h^2) / 12
    private const float Inertia = Mass * (ColliderWidth * ColliderWidth + ColliderHeight * ColliderHeight) / 12f;

    private const float StartX = -5f;
    private const float StartY = 11f;

    public enum State
    {
        WaitingToStart,
        Normal,
        GameOver,
    }

    public enum LandingType
    {
        Successful,
        WrongLandingArea,
        TooSteepAngle,
        TooFastLanding,
        LostInSpace,
    }

    public class LandingResult
    {
        public LandingType Type;
        public float LandingSpeed;
        public float DotVector;
        public int Score;
    }

    public event EventHandler? OnBeforeForce;
    public event EventHandler? OnUpForce;
    public event EventHandler? OnLeftForce;
    public event EventHandler? OnRightForce;
    public event EventHandler<LandingResult>? OnLanded;

    public LanderTuning Tuning { get; } = new();

    public State CurrentState { get; private set; }
    public float X { get; private set; }
    public float Y { get; private set; }
    public float VelocityX { get; private set; }
    public float VelocityY { get; private set; }
    /// <summary>Radians, counter-clockwise; 0 = upright.</summary>
    public float Angle { get; private set; }
    public float AngularVelocity { get; private set; }
    public float Fuel { get; private set; }
    public float GravityScale { get; private set; }

    public float Speed => MathF.Sqrt(VelocityX * VelocityX + VelocityY * VelocityY);
    /// <summary>Vector2.Dot(Vector2.up, transform.up)</summary>
    public float DotVector => MathF.Cos(Angle);
    public float FuelNormalized => Tuning.FuelAmountMax <= 0f ? 0f : Fuel / Tuning.FuelAmountMax;

    public LanderSim()
    {
        Reset();
    }

    public void Reset()
    {
        X = StartX;
        Y = StartY;
        VelocityX = 0f;
        VelocityY = 0f;
        Angle = 0f;
        AngularVelocity = 0f;
        Fuel = Tuning.FuelAmountMax;
        GravityScale = 0f;
        CurrentState = State.WaitingToStart;
    }

    /// <summary>One FixedUpdate, the same order as Lander.FixedUpdate, then one physics step.</summary>
    public void FixedUpdate(LanderInput input)
    {
        OnBeforeForce?.Invoke(this, EventArgs.Empty);

        float forceX = 0f;
        float forceY = 0f;
        float torque = 0f;

        switch (CurrentState)
        {
            case State.WaitingToStart:
                if (input.Any)
                {
                    GravityScale = Tuning.GravityNormal;
                    CurrentState = State.Normal;
                }
                break;

            case State.Normal:
                GravityScale = Tuning.GravityNormal;   // so the slider acts mid-flight
                if (Fuel <= 0f)
                {
                    break;
                }

                if (input.Any)
                {
                    Fuel -= 1f * FixedDeltaTime;   // ConsumeFuel()
                }

                if (input.Up)
                {
                    // landerRigidbody2D.AddForce(force * transform.up * Time.deltaTime);
                    float force = Tuning.Force * FixedDeltaTime;
                    forceX += -MathF.Sin(Angle) * force;
                    forceY += MathF.Cos(Angle) * force;
                    OnUpForce?.Invoke(this, EventArgs.Empty);
                }
                if (input.Left)
                {
                    torque += Tuning.TurnSpeed * FixedDeltaTime;
                    OnLeftForce?.Invoke(this, EventArgs.Empty);
                }
                if (input.Right)
                {
                    torque -= Tuning.TurnSpeed * FixedDeltaTime;
                    OnRightForce?.Invoke(this, EventArgs.Empty);
                }
                break;

            case State.GameOver:
                return;
        }

        if (CurrentState == State.WaitingToStart)
        {
            return;
        }

        StepPhysics(forceX, forceY, torque);
        CheckCollision();
    }

    // Semi-implicit Euler with Box2D-style damping.
    private void StepPhysics(float forceX, float forceY, float torque)
    {
        float dt = FixedDeltaTime;

        VelocityX += dt * (forceX / Mass);
        VelocityY += dt * (Gravity * GravityScale + forceY / Mass);
        AngularVelocity += dt * (torque / Inertia);

        float linearDampingFactor = 1f / (1f + dt * LinearDamping);
        VelocityX *= linearDampingFactor;
        VelocityY *= linearDampingFactor;
        AngularVelocity *= 1f / (1f + dt * AngularDamping);

        X += dt * VelocityX;
        Y += dt * VelocityY;
        Angle += dt * AngularVelocity;
    }

    private void CheckCollision()
    {
        if (MathF.Abs(X) > WorldHalfWidth + 2f || Y > WorldTop + 4f)
        {
            Land(new LandingResult { Type = LandingType.LostInSpace });
            return;
        }

        if (LowestPointY() > 0f)
        {
            return;
        }

        float landingSpeed = Speed;   // collision2D.relativeVelocity.magnitude against static ground
        float dotVector = DotVector;

        // if (!collision2D.gameObject.TryGetComponent(out LandingPad landingPad))
        if (MathF.Abs(X) > PadHalfWidth)
        {
            Land(new LandingResult { Type = LandingType.WrongLandingArea });
            return;
        }

        if (landingSpeed > Tuning.SoftLandingVelocityMagnitude)
        {
            Land(new LandingResult { Type = LandingType.TooFastLanding, LandingSpeed = landingSpeed });
            return;
        }

        if (dotVector < Tuning.MinDotVector)
        {
            Land(new LandingResult { Type = LandingType.TooSteepAngle, LandingSpeed = landingSpeed, DotVector = dotVector });
            return;
        }

        // Same score formula as Lander.cs, landing pad multiplier 1.
        float maxScoreAmountLandingAngle = 100;
        float scoreDotVectorMultiplier = 10f;
        float landingAngleScore = maxScoreAmountLandingAngle - MathF.Abs(dotVector - 1f) * scoreDotVectorMultiplier * maxScoreAmountLandingAngle;

        float maxScoreAmountLandingSpeed = 100;
        float landingSpeedScore = (Tuning.SoftLandingVelocityMagnitude - landingSpeed) * maxScoreAmountLandingSpeed;

        int score = (int)MathF.Round(landingAngleScore + landingSpeedScore);
        Land(new LandingResult { Type = LandingType.Successful, LandingSpeed = landingSpeed, DotVector = dotVector, Score = score });
    }

    private float LowestPointY()
    {
        float halfWidth = ColliderWidth / 2f;
        float halfHeight = ColliderHeight / 2f;
        float cos = MathF.Cos(Angle);
        float sin = MathF.Abs(MathF.Sin(Angle));
        return Y - (halfHeight * MathF.Abs(cos) + halfWidth * sin);
    }

    private void Land(LandingResult result)
    {
        if (result.Type == LandingType.Successful)
        {
            Y -= LowestPointY();   // rest on the pad
        }
        VelocityX = 0f;
        VelocityY = 0f;
        AngularVelocity = 0f;
        CurrentState = State.GameOver;
        OnLanded?.Invoke(this, result);
    }

    // Exposed for drawing.
    public static float BodyWidth => ColliderWidth;
    public static float BodyHeight => ColliderHeight;
}
