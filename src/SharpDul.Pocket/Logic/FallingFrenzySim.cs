namespace SharpDul.Pocket.Logic;

public class FallingFrenzyTuning
{
    public float MoveSpeed = 20f;           // PlayerController.moveSpeed (Inspector: 20)
    public float SpawnInterval = 1f;        // SheepSpawner.spawnInterval
    public float SpawnRangeX = 15f;         // SheepSpawner.spawnRangeX (Inspector: 15)
    public int StartingSheepLeft = 5;       // GameManager.startingSheepLeft
    /// <summary>false = rb.linearVelocity (the course), true = AddForce (LuaLander-style) for comparison.</summary>
    public bool UseForce;
}

/// <summary>The parts of the game that exist so far - one per script (or script change).</summary>
[Flags]
public enum FrenzyFeature
{
    None = 0,
    CollisionLog = 1 << 0,    // FallingObject.OnCollisionEnter -> Debug.Log
    ReadInput = 1 << 1,       // PlayerController.Update
    Move = 1 << 2,            // PlayerController.FixedUpdate
    Spawner = 1 << 3,         // SheepSpawner
    Catch = 1 << 4,           // PlayerController.OnTriggerEnter (+ Is Trigger)
    Destroyer = 1 << 5,       // SheepDestroyer
    RandomX = 1 << 6,         // SheepSpawner random position
    Counter = 1 << 7,         // GameManager (text + LostSheep)
    CounterLinked = 1 << 8,   // SheepDestroyer calls LostSheep
    Events = 1 << 9,          // GameManager singleton + events
    EventsUI = 1 << 10,       // GameUI listens
}

/// <summary>
/// Falling Frenzy in plain C#, with only the parts that have been built switched on.
/// Same numbers as the course scene: player box 3 x 0.5 at y -1, sheep radius 0.5 with
/// Bounciness 1 (averaged to 0.5 against the player), spawner at y 20, destroyer at y -10,
/// Unity gravity. A close approximation of PhysX, not a bit-exact copy. No UI here.
/// </summary>
public class FallingFrenzySim
{
    public const float FixedDeltaTime = 0.02f;
    public const float ViewHalfWidth = 18f;
    public const float ViewBottom = -2f;
    public const float ViewTop = 20f;
    public const float PlayerY = -1f;
    public const float PlayerHalfWidth = 1.5f;
    public const float PlayerHalfHeight = 0.25f;
    public const float SheepRadius = 0.5f;
    public const float SpawnerY = 20f;
    public const float DestroyerY = -10f;
    public const float SingleSheepY = 15f;

    private const float Gravity = -9.81f;
    private const float Bounce = 0.5f;
    private const float ForceDamping = 4f;
    private const float PlayerLimitX = ViewHalfWidth + 2f;
    private const float CleanupY = -15f;

    public class Sheep
    {
        public float X;
        public float Y;
        public float VelocityY;
        public bool Resting;
    }

    public event EventHandler? OnSpawned;
    public event EventHandler? OnHitPlayer;
    public event EventHandler? OnCaught;
    public event EventHandler? OnLost;
    public event EventHandler? OnSheepLeftChanged;
    public event EventHandler? OnGameOver;

    public FallingFrenzyTuning Tuning { get; } = new();
    public FrenzyFeature Features { get; private set; }
    /// <summary>1 = empty scene, 2 = player placed, 4 = player + a falling sheep (Rigidbody, no code).</summary>
    public int SceneLevel { get; private set; }
    public float PlayerX { get; private set; }
    public float PlayerVelocityX { get; private set; }
    public List<Sheep> Sheeps { get; } = new();
    public int SheepLeft { get; private set; }
    public int Caught { get; private set; }
    public bool IsGameOver { get; private set; }

    private float timer;
    private readonly Random random = new();

    public bool Has(FrenzyFeature feature) => (Features & feature) == feature;
    public bool ShowPlayer => SceneLevel >= 2;
    public bool HasPhysics => SceneLevel >= 4;

    /// <summary>The course steps as feature sets: the game after step N.</summary>
    public static (int SceneLevel, FrenzyFeature Features) ForStage(int stage)
    {
        FrenzyFeature features = FrenzyFeature.None;
        if (stage >= 4) features |= FrenzyFeature.CollisionLog;
        if (stage >= 5) features |= FrenzyFeature.ReadInput | FrenzyFeature.Move;
        if (stage >= 6) features |= FrenzyFeature.Spawner;
        if (stage >= 7) features |= FrenzyFeature.Catch | FrenzyFeature.Destroyer;
        if (stage >= 8) features |= FrenzyFeature.RandomX;
        if (stage >= 9) features |= FrenzyFeature.Counter | FrenzyFeature.CounterLinked;
        if (stage >= 10) features |= FrenzyFeature.Events | FrenzyFeature.EventsUI;
        int sceneLevel = stage >= 4 ? 4 : stage >= 2 ? 2 : 1;
        return (sceneLevel, features);
    }

    public FallingFrenzySim(int sceneLevel, FrenzyFeature features)
    {
        Configure(sceneLevel, features);
    }

    public void Configure(int sceneLevel, FrenzyFeature features)
    {
        bool changed = sceneLevel != SceneLevel || features != Features;
        SceneLevel = sceneLevel;
        Features = features;
        if (changed)
        {
            Reset();
        }
    }

    public void Reset()
    {
        PlayerX = 0f;
        PlayerVelocityX = 0f;
        Sheeps.Clear();
        SheepLeft = Tuning.StartingSheepLeft;
        Caught = 0;
        IsGameOver = false;
        timer = 0f;

        if (HasPhysics && !Has(FrenzyFeature.Spawner))
        {
            DropSingleSheep();
        }
    }

    /// <summary>Before the spawner exists: one sheep placed in the scene at (0, 15).</summary>
    public void DropSingleSheep()
    {
        Sheeps.Clear();
        Sheeps.Add(new Sheep { X = 0f, Y = SingleSheepY });
    }

    /// <param name="moveInput">-1, 0 or 1, as PlayerController.moveInput.</param>
    public void FixedUpdate(float moveInput)
    {
        // Time.timeScale = 0: physics and timers stop.
        if (IsGameOver || !HasPhysics)
        {
            return;
        }

        if (Has(FrenzyFeature.Move))
        {
            MovePlayer(Has(FrenzyFeature.ReadInput) ? moveInput : 0f);
        }

        if (Has(FrenzyFeature.Spawner))
        {
            // SheepSpawner.Update
            timer += FixedDeltaTime;
            if (timer > Tuning.SpawnInterval)
            {
                float x = Has(FrenzyFeature.RandomX) ? (float)(random.NextDouble() * 2 - 1) * Tuning.SpawnRangeX : 0f;
                Sheeps.Add(new Sheep { X = x, Y = SpawnerY });
                timer = 0f;
                OnSpawned?.Invoke(this, EventArgs.Empty);
            }
        }

        for (int i = Sheeps.Count - 1; i >= 0; i--)
        {
            StepSheep(Sheeps[i], out bool remove);
            if (remove)
            {
                Sheeps.RemoveAt(i);
            }
            if (IsGameOver)
            {
                return;
            }
        }
    }

    private void MovePlayer(float moveInput)
    {
        if (Tuning.UseForce)
        {
            // rb.AddForce(moveInput * moveSpeed * k) with damping k: same top speed, but momentum.
            PlayerVelocityX += FixedDeltaTime * (moveInput * Tuning.MoveSpeed * ForceDamping);
            PlayerVelocityX *= 1f / (1f + FixedDeltaTime * ForceDamping);
        }
        else
        {
            // playerRigidbody.linearVelocity = new Vector3(moveInput * moveSpeed, 0f, 0f);
            PlayerVelocityX = moveInput * Tuning.MoveSpeed;
        }

        PlayerX += FixedDeltaTime * PlayerVelocityX;
        if (MathF.Abs(PlayerX) > PlayerLimitX)
        {
            PlayerX = MathF.Sign(PlayerX) * PlayerLimitX;
            PlayerVelocityX = 0f;
        }
    }

    private void StepSheep(Sheep sheep, out bool remove)
    {
        remove = false;
        float playerTop = PlayerY + PlayerHalfHeight;
        bool overPlayer = MathF.Abs(sheep.X - PlayerX) <= PlayerHalfWidth;
        bool playerIsTrigger = Has(FrenzyFeature.Catch);

        if (sheep.Resting && (!overPlayer || playerIsTrigger))
        {
            sheep.Resting = false;   // the player slid away - it falls again
        }

        if (!sheep.Resting)
        {
            float previousBottom = sheep.Y - SheepRadius;
            sheep.VelocityY += FixedDeltaTime * Gravity;
            sheep.Y += FixedDeltaTime * sheep.VelocityY;
            float bottom = sheep.Y - SheepRadius;

            if (playerIsTrigger)
            {
                // PlayerController.OnTriggerEnter: overlap with the catcher box.
                bool overlapsY = bottom <= playerTop && sheep.Y + SheepRadius >= PlayerY - PlayerHalfHeight;
                if (overPlayer && overlapsY)
                {
                    Caught++;
                    remove = true;
                    OnCaught?.Invoke(this, EventArgs.Empty);
                    return;
                }
            }
            else if (overPlayer && previousBottom >= playerTop && bottom < playerTop && sheep.VelocityY < 0f)
            {
                // Solid collision: bounce (Bounciness 1 and 0, Average = 0.5). Every bounce is a new OnCollisionEnter.
                sheep.Y = playerTop + SheepRadius;
                OnHitPlayer?.Invoke(this, EventArgs.Empty);
                sheep.VelocityY = -sheep.VelocityY * Bounce;
                if (sheep.VelocityY < 1f)
                {
                    sheep.VelocityY = 0f;
                    sheep.Resting = true;
                }
            }
        }

        if (Has(FrenzyFeature.Destroyer) && sheep.Y <= DestroyerY)
        {
            // SheepDestroyer.OnTriggerEnter
            remove = true;
            OnLost?.Invoke(this, EventArgs.Empty);
            if (Has(FrenzyFeature.Counter | FrenzyFeature.CounterLinked))
            {
                LostSheep();
            }
            return;
        }

        if (sheep.Y < CleanupY)
        {
            remove = true;   // Lab-only cleanup; in Unity, without a destroyer it would fall for ever.
        }
    }

    // GameManager.LostSheep
    private void LostSheep()
    {
        if (SheepLeft <= 0)
        {
            return;
        }

        SheepLeft--;
        OnSheepLeftChanged?.Invoke(this, EventArgs.Empty);
        if (SheepLeft <= 0)
        {
            IsGameOver = true;
            OnGameOver?.Invoke(this, EventArgs.Empty);
        }
    }
}
