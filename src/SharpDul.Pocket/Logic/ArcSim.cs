namespace SharpDul.Pocket.Logic;

/// <summary>
/// Fake height along an AnimationCurve, from 2DTopDownPixelCombat: the Grape's lobbed
/// projectile (GrapeProjectile + shadow + GrapeLandSplatter) and the loot pop of PickUp
/// (pop, then the magnet pull). The ground position is a straight Lerp; the curve only adds
/// height on Y. One tick = 0.02 s (Update, FixedUpdate and coroutines together). No UI here.
/// </summary>
public class ArcSim
{
    public const float FixedDeltaTime = 0.02f;
    public const float ViewMinX = -6f, ViewMaxX = 6f, ViewMinY = -4f, ViewMaxY = 6f;
    public const float GrapeX = -2.5f, GrapeY = 0f;
    public const float BushX = 2.5f, BushY = 2f;
    public const float ShadowOffsetY = -0.3f;           // GrapeProjectile.Start
    public const float ColliderOffTime = 0.2f;          // GrapeLandSplatter: Invoke("DisableCollider", 0.2f)
    public const float SplatterFadeTime = 0.6f;         // Splatter prefab SpriteFade.fadeTime
    public const float SplatterHalfX = 0.67f;           // CapsuleCollider2D 1.35 x 0.63
    public const float SplatterHalfY = 0.32f;
    public const float GlobeRadius = 0.25f;             // CapsuleCollider2D 0.49 x 0.5
    public const float PlayerSpeed = 4f;                // Player prefab moveSpeed
    public const float PlayerHalfX = 0.25f, PlayerHalfY = 0.1f;
    public const float AttackRange = 5f;                // Grape prefab EnemyAI
    public const float AttackCooldown = 2f;
    public const float DamageRecoveryTime = 1f;

    public class Lob
    {
        public float StartX, StartY, EndX, EndY, ShadowStartX, ShadowStartY;
        public float X, Y, ShadowX, ShadowY, TimePassed, LinearT, HeightT, Height;
        public List<(float X, float Y)> Path { get; } = new();
    }

    public class Splatter
    {
        public float X, Y, Age;
        public bool ColliderOn => Age < ColliderOffTime;
        public bool Hit;
    }

    public class Globe
    {
        public float StartX, StartY, EndX, EndY;
        public float X, Y, TimePassed, LinearT, HeightT, Height;
        public bool Popping = true;
        public float MoveSpeed;
        public float DirX, DirY;
    }

    /// <summary>A code line just ran (key = the line in the Lab's code list).</summary>
    public event Action<string>? OnLine;

    // GrapeProjectile (Grape Projectile.prefab)
    public AnimCurve GrapeCurve { get; set; } = AnimCurve.Grape();
    public float Duration = 2f;
    public float GrapeHeightY = 5.5f;
    public bool AutoThrow = true;

    // PickUp (Stamina / Health Globe prefab)
    public AnimCurve PickUpCurve { get; set; } = AnimCurve.Grape();
    public float PopDuration = 0.5f;
    public float PickUpHeightY = 1.5f;
    public float PickUpDistance = 4f;
    public float AccelerationRate = 0.08f;
    public float StartMoveSpeed = 0.04f;

    public float PlayerX { get; private set; } = 2f;
    public float PlayerY { get; private set; } = -2f;
    public float TargetX => targetX;
    public float TargetY => targetY;
    public bool PlayerFlashing => flashLeft > 0f;
    public int Hits { get; private set; }
    public int Collected { get; private set; }
    public List<Lob> Lobs { get; } = new();
    public List<Splatter> Splatters { get; } = new();
    public List<Globe> Globes { get; } = new();
    public Lob? LastLob { get; private set; }
    public Globe? LastGlobe { get; private set; }

    private float targetX = 2f, targetY = -2f;
    private float cooldownLeft;
    private float recoveryLeft;
    private float flashLeft;
    private readonly Random random = new();

    public float DistanceToGrape => Distance(PlayerX, PlayerY, GrapeX, GrapeY);

    public void SetTarget(float x, float y)
    {
        targetX = Math.Clamp(x, ViewMinX + 0.5f, ViewMaxX - 0.5f);
        targetY = Math.Clamp(y, ViewMinY + 0.5f, ViewMaxY - 0.5f);
    }

    public void Reset()
    {
        Lobs.Clear();
        Splatters.Clear();
        Globes.Clear();
        LastLob = null;
        LastGlobe = null;
        Hits = Collected = 0;
        cooldownLeft = recoveryLeft = flashLeft = 0f;
    }

    public void Tick()
    {
        float dt = FixedDeltaTime;
        MovePlayer(dt);
        recoveryLeft = MathF.Max(0f, recoveryLeft - dt);
        flashLeft = MathF.Max(0f, flashLeft - dt);

        // EnemyAI.Attacking on the Grape: attack when the player is in range and the cooldown is over.
        cooldownLeft = MathF.Max(0f, cooldownLeft - dt);
        if (AutoThrow && cooldownLeft <= 0f && DistanceToGrape < AttackRange)
        {
            Throw();
        }

        foreach (Lob lob in Lobs.ToArray())
        {
            StepLob(lob, dt);
        }
        StepSplatters(dt);
        foreach (Globe globe in Globes.ToArray())
        {
            StepGlobe(globe, dt);
        }
    }

    private void MovePlayer(float dt)
    {
        float dx = targetX - PlayerX, dy = targetY - PlayerY;
        float distance = MathF.Sqrt(dx * dx + dy * dy);
        float step = PlayerSpeed * dt;
        if (distance <= step)
        {
            PlayerX = targetX;
            PlayerY = targetY;
        }
        else
        {
            PlayerX += dx / distance * step;
            PlayerY += dy / distance * step;
        }
    }

    // ---------- Grape ----------

    /// <summary>Grape.SpawnProjectileAnimEvent -> GrapeProjectile.Start.</summary>
    public void Throw()
    {
        cooldownLeft = AttackCooldown;
        OnLine?.Invoke("throw");
        Lob lob = new()
        {
            StartX = GrapeX, StartY = GrapeY, X = GrapeX, Y = GrapeY,
            // Vector3 playerPos = PlayerController.Instance.transform.position; - read once.
            EndX = PlayerX, EndY = PlayerY,
            ShadowStartX = GrapeX, ShadowStartY = GrapeY + ShadowOffsetY,
        };
        lob.ShadowX = lob.ShadowStartX;
        lob.ShadowY = lob.ShadowStartY;
        lob.Path.Add((lob.X, lob.Y));
        Lobs.Add(lob);
        LastLob = lob;
    }

    private void StepLob(Lob lob, float dt)
    {
        if (lob.TimePassed < Duration)
        {
            lob.TimePassed += dt;
            lob.LinearT = lob.TimePassed / Duration;
            lob.HeightT = GrapeCurve.Evaluate(lob.LinearT);
            lob.Height = Lerp(0f, GrapeHeightY, lob.HeightT);
            float t = Clamp01(lob.LinearT);   // Vector2.Lerp clamps t too
            lob.X = Lerp(lob.StartX, lob.EndX, t);
            lob.Y = Lerp(lob.StartY, lob.EndY, t) + lob.Height;
            lob.ShadowX = Lerp(lob.ShadowStartX, lob.EndX, t);
            lob.ShadowY = Lerp(lob.ShadowStartY, lob.EndY, t);
            lob.Path.Add((lob.X, lob.Y));
            OnLine?.Invoke("lobStep");
            if (lob.TimePassed < Duration)
            {
                return;   // yield return null;
            }
        }

        // The while loop ended: Instantiate(splatterPrefab, transform.position, ...); Destroy(gameObject);
        Lobs.Remove(lob);
        Splatters.Add(new Splatter { X = lob.X, Y = lob.Y });
        OnLine?.Invoke("land");
    }

    private void StepSplatters(float dt)
    {
        foreach (Splatter splatter in Splatters.ToArray())
        {
            bool wasOn = splatter.ColliderOn;
            // OnTriggerEnter2D: once, while the collider is still enabled.
            if (splatter.ColliderOn && !splatter.Hit && PlayerOverlapsBox(splatter.X, splatter.Y, SplatterHalfX, SplatterHalfY))
            {
                splatter.Hit = true;
                OnLine?.Invoke("splatHit");
                TakeDamage();
            }
            splatter.Age += dt;
            if (wasOn && !splatter.ColliderOn)
            {
                OnLine?.Invoke("colliderOff");
            }
            if (splatter.Age >= SplatterFadeTime)
            {
                Splatters.Remove(splatter);
            }
        }
    }

    private void TakeDamage()
    {
        if (recoveryLeft > 0f)
        {
            OnLine?.Invoke("blocked");
            return;
        }
        Hits++;
        recoveryLeft = DamageRecoveryTime;
        flashLeft = 0.2f;
    }

    private bool PlayerOverlapsBox(float x, float y, float halfX, float halfY) =>
        MathF.Abs(PlayerX - x) < PlayerHalfX + halfX && MathF.Abs(PlayerY - y) < PlayerHalfY + halfY;

    // ---------- PickUp ----------

    /// <summary>PickUpSpawner.DropItems: a few globes from the bush.</summary>
    public void DropLoot(int count)
    {
        for (int i = 0; i < count; i++)
        {
            float randomX = BushX + (float)(random.NextDouble() * 4 - 2);
            float randomY = BushY + (float)(random.NextDouble() * 2 - 1);
            Globe globe = new()
            {
                StartX = BushX, StartY = BushY, X = BushX, Y = BushY,
                EndX = randomX, EndY = randomY, MoveSpeed = StartMoveSpeed,
            };
            Globes.Add(globe);
            LastGlobe = globe;
        }
        OnLine?.Invoke("drop");
    }

    private void StepGlobe(Globe globe, float dt)
    {
        // FixedUpdate: speed builds up while moveDir is set - even during the pop.
        if (globe.DirX != 0f || globe.DirY != 0f)
        {
            globe.MoveSpeed += AccelerationRate;
            OnLine?.Invoke("accelerate");
        }
        // rb.velocity = moveDir * moveSpeed; the physics step moves it.
        globe.X += globe.DirX * globe.MoveSpeed * dt;
        globe.Y += globe.DirY * globe.MoveSpeed * dt;

        // Update: the magnet.
        float distance = Distance(globe.X, globe.Y, PlayerX, PlayerY);
        if (distance < PickUpDistance)
        {
            globe.DirX = (PlayerX - globe.X) / MathF.Max(distance, 1e-5f);
            globe.DirY = (PlayerY - globe.Y) / MathF.Max(distance, 1e-5f);
        }
        else
        {
            globe.DirX = globe.DirY = 0f;
            if (globe.MoveSpeed != 0f)
            {
                OnLine?.Invoke("outOfRange");
            }
            globe.MoveSpeed = 0f;
        }

        // AnimCurveSpawnRoutine (resumes after Update) overwrites the position while it runs.
        if (globe.Popping)
        {
            if (globe.TimePassed < PopDuration)
            {
                globe.TimePassed += dt;
                globe.LinearT = globe.TimePassed / PopDuration;
                globe.HeightT = PickUpCurve.Evaluate(globe.LinearT);
                globe.Height = Lerp(0f, PickUpHeightY, globe.HeightT);
                float t = Clamp01(globe.LinearT);
                globe.X = Lerp(globe.StartX, globe.EndX, t);
                globe.Y = Lerp(globe.StartY, globe.EndY, t) + globe.Height;
                OnLine?.Invoke("popStep");
            }
            else
            {
                globe.Popping = false;
                OnLine?.Invoke("popDone");
            }
        }

        // OnTriggerEnter2D with the player: DetectPickupType(); Destroy(gameObject);
        float nearestX = Math.Clamp(globe.X, PlayerX - PlayerHalfX, PlayerX + PlayerHalfX);
        float nearestY = Math.Clamp(globe.Y, PlayerY - PlayerHalfY, PlayerY + PlayerHalfY);
        float ox = globe.X - nearestX, oy = globe.Y - nearestY;
        if (ox * ox + oy * oy < GlobeRadius * GlobeRadius)
        {
            Globes.Remove(globe);
            Collected++;
            OnLine?.Invoke("collect");
        }
    }

    // Mathf.Lerp clamps t to 0..1.
    private static float Lerp(float a, float b, float t) => a + (b - a) * Clamp01(t);

    private static float Clamp01(float t) => Math.Clamp(t, 0f, 1f);

    private static float Distance(float ax, float ay, float bx, float by)
    {
        float dx = ax - bx, dy = ay - by;
        return MathF.Sqrt(dx * dx + dy * dy);
    }
}
