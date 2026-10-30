namespace SharpDul.Pocket.Logic;

/// <summary>
/// The Inspector values from 2DTopDownPixelCombat (Ghost.prefab, Player.prefab, Bullet.prefab).
/// </summary>
public class CombatTuning
{
    // Shooter (Ghost.prefab)
    public float BulletMoveSpeed = 6f;
    public int BurstCount = 6;
    public int ProjectilesPerBurst = 8;
    public float AngleSpread = 165f;
    public float StartingDistance = 0.3f;
    public float TimeBetweenBursts = 1f;
    public float RestTime = 0.1f;
    public bool Stagger = true;
    public bool Oscillate = true;

    // EnemyAI (Ghost.prefab)
    public float AttackRange = 6f;
    public float AttackCooldown = 2f;
    public bool StopMovingWhileAttacking = true;

    // Player.prefab
    public float MoveSpeed = 4f;
    public float DashSpeed = 4f;
    public float KnockBackThrustAmount = 10f;
    public float KnockBackTime = 0.2f;
    public float DamageRecoveryTime = 1f;
    public int TimeBetweenStaminaRefresh = 2;

    /// <summary>
    /// Shooter.OnValidate. With <paramref name="asInProject"/> it is the director's version,
    /// where both oscillate lines set stagger = true.
    /// </summary>
    public void OnValidate(bool asInProject)
    {
        if (asInProject)
        {
            if (Oscillate) { Stagger = true; }
            if (!Oscillate) { Stagger = true; }
        }
        if (ProjectilesPerBurst < 1) { ProjectilesPerBurst = 1; }
        if (BurstCount < 1) { BurstCount = 1; }
        if (TimeBetweenBursts < 0.1f) { TimeBetweenBursts = 0.1f; }
        if (RestTime < 0.1f) { RestTime = 0.1f; }
        if (StartingDistance < 0.1f) { StartingDistance = 0.1f; }
        if (AngleSpread == 0) { ProjectilesPerBurst = 1; }
        if (BulletMoveSpeed <= 0) { BulletMoveSpeed = 0.1f; }
    }
}

/// <summary>
/// The Ghost fight from 2DTopDownPixelCombat in plain C#: EnemyAI + Shooter + Projectile on one
/// side, PlayerController + PlayerHealth + Knockback + Flash + Stamina on the other.
/// Coroutines are C# iterators that yield the seconds of each WaitForSeconds, so the routines
/// read like the Unity code. One tick = 0.02 s (Update and FixedUpdate together).
/// No UI here: the Lab listens to OnLine and reads the state.
/// </summary>
public class CombatSim
{
    public const float FixedDeltaTime = 0.02f;
    public const float ViewHalf = 6.5f;
    public const float ArenaHalf = 6f;
    public const float BulletRadius = 0.5f;          // Bullet.prefab CircleCollider2D
    public const float ProjectileRange = 15f;        // Bullet.prefab Projectile.projectileRange
    public const float GhostMoveSpeed = 2f;          // EnemyPathfinding.moveSpeed
    public const float RoamChangeDirFloat = 2f;      // EnemyAI.roamChangeDirFloat
    public const float FlashTime = 0.2f;             // Player Flash.restoreDefaultMatTime
    public const int MaxHealth = 3;
    public const int StartingStamina = 3;
    public const float DashTime = 0.2f;
    public const float DashCooldown = 0.25f;
    public const float DeathLoadTime = 2f;
    // Colliders as boxes: Player CapsuleCollider2D 0.5 x 0.2 at the feet, Ghost 1.0 x 0.8.
    public const float PlayerBoxHalfX = 0.25f;
    public const float PlayerBoxHalfY = 0.1f;
    public const float PlayerBoxOffsetX = 0.063f;
    public const float PlayerBoxOffsetY = -0.036f;
    public const float GhostBoxHalfX = 0.5f;
    public const float GhostBoxHalfY = 0.4f;

    private const float PlayerStartX = 0f, PlayerStartY = -3f;
    private const float GhostStartX = 0f, GhostStartY = 2f;

    public enum State { Roaming, Attacking }

    public class Bullet
    {
        public float X, Y, DirX, DirY, StartX, StartY, Speed;
    }

    private sealed class Routine
    {
        public required IEnumerator<float> Body;
        public required string Owner;
        public float Wait;
    }

    /// <summary>A code line just ran (key = the line in the Lab's code list).</summary>
    public event Action<string>? OnLine;

    public CombatTuning Tuning { get; } = new();
    /// <summary>Lab-only switch: bullets fly through the player, to watch a pattern.</summary>
    public bool WatchOnly { get; set; }
    public float Time { get; private set; }

    // Player
    public float PlayerX { get; private set; }
    public float PlayerY { get; private set; }
    public int Health { get; private set; }
    public int CurrentStamina { get; private set; }
    public bool IsDead { get; private set; }
    public bool IsDashing { get; private set; }
    public bool IsFlashing { get; private set; }
    public bool CanTakeDamage { get; private set; }
    public bool GettingKnockedBack { get; private set; }
    public bool IsMoving { get; private set; }
    public float MovementX { get; private set; }
    public int Deaths { get; private set; }
    private float moveSpeed;
    private float startingMoveSpeed;
    private float velocityX, velocityY;

    // Ghost
    public float GhostX { get; private set; }
    public float GhostY { get; private set; }
    public State GhostState { get; private set; }
    public bool IsShooting { get; private set; }
    public int CurrentBurst { get; private set; }
    public float ConeStart { get; private set; }
    public float ConeEnd { get; private set; }
    private bool canAttack;
    private float roamX, roamY, moveDirX, moveDirY, timeRoaming;

    public List<Bullet> Bullets { get; } = new();
    public int BulletsFired { get; private set; }

    private readonly List<Routine> routines = new();
    private readonly Random random = new();

    public CombatSim()
    {
        Reset();
    }

    /// <summary>Like loading the scene again: everything back to its start, routines stopped.</summary>
    public void Reset()
    {
        routines.Clear();
        Bullets.Clear();
        PlayerX = PlayerStartX;
        PlayerY = PlayerStartY;
        velocityX = velocityY = 0f;
        Health = MaxHealth;
        CurrentStamina = StartingStamina;
        IsDead = IsDashing = IsFlashing = GettingKnockedBack = false;
        CanTakeDamage = true;
        startingMoveSpeed = moveSpeed = Tuning.MoveSpeed;

        GhostX = GhostStartX;
        GhostY = GhostStartY;
        GhostState = State.Roaming;
        IsShooting = false;
        CurrentBurst = 0;
        canAttack = true;
        (roamX, roamY) = GetRoamingPosition();
    }

    /// <summary>The Inspector moveSpeed changed (PlayerController keeps it in startingMoveSpeed).</summary>
    public void SetMoveSpeed(float value)
    {
        bool dashBoosted = moveSpeed != startingMoveSpeed;
        Tuning.MoveSpeed = value;
        startingMoveSpeed = value;
        moveSpeed = dashBoosted ? value * Tuning.DashSpeed : value;
    }

    /// <param name="moveX">Movement.Move (-1..1), already normalized like the Input System's composite.</param>
    /// <param name="dashPressed">Combat.Dash performed this tick.</param>
    public void Tick(float moveX, float moveY, bool dashPressed)
    {
        Time += FixedDeltaTime;
        if (dashPressed)
        {
            Dash();
        }

        EnemyAIUpdate();
        RunRoutines();
        GhostFixedUpdate();
        PlayerFixedUpdate(moveX, moveY);
        ProjectilesUpdate();
        GhostContact();
    }

    // ---------- coroutines ----------

    private void StartCoroutine(IEnumerator<float> body, string owner)
    {
        Routine routine = new() { Body = body, Owner = owner };
        // Unity runs a coroutine straight away until its first yield.
        if (body.MoveNext())
        {
            routine.Wait = body.Current;
            routines.Add(routine);
        }
    }

    private void StopAllCoroutines(string owner) => routines.RemoveAll(routine => routine.Owner == owner);

    private void RunRoutines()
    {
        foreach (Routine routine in routines.ToArray())
        {
            if (!routines.Contains(routine))
            {
                continue;
            }
            routine.Wait -= FixedDeltaTime;
            while (routine.Wait <= 1e-4f)
            {
                if (!routine.Body.MoveNext())
                {
                    routines.Remove(routine);
                    break;
                }
                routine.Wait += routine.Body.Current;
            }
        }
    }

    // ---------- EnemyAI + EnemyPathfinding ----------

    private float DistanceToPlayer()
    {
        float dx = PlayerX - GhostX, dy = PlayerY - GhostY;
        return MathF.Sqrt(dx * dx + dy * dy);
    }

    private void EnemyAIUpdate()
    {
        switch (GhostState)
        {
            default:
            case State.Roaming:
                Roaming();
                break;
            case State.Attacking:
                Attacking();
                break;
        }
    }

    private void Roaming()
    {
        timeRoaming += FixedDeltaTime;
        (moveDirX, moveDirY) = (roamX, roamY);

        if (DistanceToPlayer() < Tuning.AttackRange)
        {
            GhostState = State.Attacking;
            OnLine?.Invoke("toAttacking");
        }

        if (timeRoaming > RoamChangeDirFloat)
        {
            (roamX, roamY) = GetRoamingPosition();
            OnLine?.Invoke("newRoam");
        }
    }

    private void Attacking()
    {
        if (DistanceToPlayer() > Tuning.AttackRange)
        {
            GhostState = State.Roaming;
            OnLine?.Invoke("toRoaming");
        }

        if (Tuning.AttackRange != 0 && canAttack)
        {
            canAttack = false;
            OnLine?.Invoke("attack");
            ShooterAttack();

            if (Tuning.StopMovingWhileAttacking)
            {
                moveDirX = moveDirY = 0f;
            }
            else
            {
                (moveDirX, moveDirY) = (roamX, roamY);
            }
            StartCoroutine(AttackCooldownRoutine(), "EnemyAI");
        }
    }

    private IEnumerator<float> AttackCooldownRoutine()
    {
        yield return Tuning.AttackCooldown;
        canAttack = true;
        OnLine?.Invoke("canAttack");
    }

    private (float, float) GetRoamingPosition()
    {
        timeRoaming = 0f;
        float x = (float)(random.NextDouble() * 2 - 1), y = (float)(random.NextDouble() * 2 - 1);
        float length = MathF.Sqrt(x * x + y * y);
        return length < 1e-5f ? (0f, 0f) : (x / length, y / length);
    }

    private void GhostFixedUpdate()
    {
        GhostX = Math.Clamp(GhostX + moveDirX * GhostMoveSpeed * FixedDeltaTime, -ArenaHalf, ArenaHalf);
        GhostY = Math.Clamp(GhostY + moveDirY * GhostMoveSpeed * FixedDeltaTime, -ArenaHalf, ArenaHalf);
    }

    // ---------- Shooter ----------

    private void ShooterAttack()
    {
        if (!IsShooting)
        {
            StartCoroutine(ShootRoutine(), "Shooter");
        }
        else
        {
            OnLine?.Invoke("stillShooting");
        }
    }

    private IEnumerator<float> ShootRoutine()
    {
        CombatTuning t = Tuning;
        IsShooting = true;

        float startAngle, currentAngle, angleStep, endAngle;
        float timeBetweenProjectiles = 0f;

        TargetConeOfInfluence(out startAngle, out currentAngle, out angleStep, out endAngle);

        if (t.Stagger)
        {
            timeBetweenProjectiles = t.TimeBetweenBursts / t.ProjectilesPerBurst;
        }

        for (int i = 0; i < t.BurstCount; i++)
        {
            CurrentBurst = i + 1;
            if (!t.Oscillate)
            {
                TargetConeOfInfluence(out startAngle, out currentAngle, out angleStep, out endAngle);
            }

            if (t.Oscillate && i % 2 != 1)
            {
                TargetConeOfInfluence(out startAngle, out currentAngle, out angleStep, out endAngle);
            }
            else if (t.Oscillate)
            {
                currentAngle = endAngle;
                endAngle = startAngle;
                startAngle = currentAngle;
                angleStep *= -1;
                OnLine?.Invoke("swap");
            }
            ConeStart = startAngle;
            ConeEnd = endAngle;

            for (int j = 0; j < t.ProjectilesPerBurst; j++)
            {
                SpawnBullet(currentAngle, t.BulletMoveSpeed, t.StartingDistance);
                currentAngle += angleStep;

                if (t.Stagger)
                {
                    OnLine?.Invoke("waitProjectile");
                    yield return timeBetweenProjectiles;
                }
            }

            currentAngle = startAngle;

            if (!t.Stagger)
            {
                OnLine?.Invoke("waitBurst");
                yield return t.TimeBetweenBursts;
            }
        }

        OnLine?.Invoke("rest");
        yield return t.RestTime;
        IsShooting = false;
        CurrentBurst = 0;
        OnLine?.Invoke("doneShooting");
    }

    private void TargetConeOfInfluence(out float startAngle, out float currentAngle, out float angleStep, out float endAngle)
    {
        float targetAngle = MathF.Atan2(PlayerY - GhostY, PlayerX - GhostX) * (180f / MathF.PI);
        startAngle = targetAngle;
        endAngle = targetAngle;
        currentAngle = targetAngle;
        float halfAngleSpread = 0f;
        angleStep = 0;
        if (Tuning.AngleSpread != 0)
        {
            angleStep = Tuning.AngleSpread / (Tuning.ProjectilesPerBurst - 1);
            halfAngleSpread = Tuning.AngleSpread / 2f;
            startAngle = targetAngle - halfAngleSpread;
            endAngle = targetAngle + halfAngleSpread;
            currentAngle = startAngle;
        }
        OnLine?.Invoke("cone");
    }

    private void SpawnBullet(float angle, float speed, float startingDistance)
    {
        float radians = angle * (MathF.PI / 180f);
        float x = GhostX + startingDistance * MathF.Cos(radians);
        float y = GhostY + startingDistance * MathF.Sin(radians);
        // newBullet.transform.right = newBullet.transform.position - transform.position;
        float dx = x - GhostX, dy = y - GhostY;
        float length = MathF.Sqrt(dx * dx + dy * dy);
        Bullets.Add(new Bullet
        {
            X = x, Y = y, StartX = x, StartY = y, Speed = speed,
            DirX = length > 0 ? dx / length : 1f, DirY = length > 0 ? dy / length : 0f,
        });
        BulletsFired++;
        OnLine?.Invoke("spawn");
    }

    // ---------- Projectile ----------

    private void ProjectilesUpdate()
    {
        for (int i = Bullets.Count - 1; i >= 0; i--)
        {
            Bullet bullet = Bullets[i];
            bullet.X += bullet.DirX * bullet.Speed * FixedDeltaTime;
            bullet.Y += bullet.DirY * bullet.Speed * FixedDeltaTime;

            if (!WatchOnly && !IsDead && CircleHitsPlayer(bullet.X, bullet.Y))
            {
                OnLine?.Invoke("bulletHit");
                TakeDamage(1, bullet.X, bullet.Y);
                Bullets.RemoveAt(i);
                continue;
            }

            float fx = bullet.X - bullet.StartX, fy = bullet.Y - bullet.StartY;
            if (MathF.Sqrt(fx * fx + fy * fy) > ProjectileRange)
            {
                Bullets.RemoveAt(i);
            }
        }
    }

    private bool CircleHitsPlayer(float x, float y)
    {
        float cx = PlayerX + PlayerBoxOffsetX, cy = PlayerY + PlayerBoxOffsetY;
        float nearestX = Math.Clamp(x, cx - PlayerBoxHalfX, cx + PlayerBoxHalfX);
        float nearestY = Math.Clamp(y, cy - PlayerBoxHalfY, cy + PlayerBoxHalfY);
        float dx = x - nearestX, dy = y - nearestY;
        return dx * dx + dy * dy < BulletRadius * BulletRadius;
    }

    // ---------- PlayerController ----------

    private void PlayerFixedUpdate(float moveX, float moveY)
    {
        MovementX = moveX;
        IsMoving = false;

        // Knockback: the impulse set a velocity; Rigidbody2D (Linear Drag 0) keeps it.
        if (velocityX != 0f || velocityY != 0f)
        {
            PlayerX += velocityX * FixedDeltaTime;
            PlayerY += velocityY * FixedDeltaTime;
        }

        if (!GettingKnockedBack && !IsDead && (moveX != 0f || moveY != 0f))
        {
            PlayerX += moveX * moveSpeed * FixedDeltaTime;
            PlayerY += moveY * moveSpeed * FixedDeltaTime;
            IsMoving = true;
        }

        PlayerX = Math.Clamp(PlayerX, -ArenaHalf, ArenaHalf);
        PlayerY = Math.Clamp(PlayerY, -ArenaHalf, ArenaHalf);
    }

    private void Dash()
    {
        if (!IsDashing && CurrentStamina > 0)
        {
            UseStamina();
            IsDashing = true;
            moveSpeed *= Tuning.DashSpeed;
            OnLine?.Invoke("dash");
            StartCoroutine(EndDashRoutine(), "PlayerController");
        }
        else
        {
            OnLine?.Invoke("dashRefused");
        }
    }

    private IEnumerator<float> EndDashRoutine()
    {
        yield return DashTime;
        moveSpeed = startingMoveSpeed;
        OnLine?.Invoke("dashEnd");
        yield return DashCooldown;
        IsDashing = false;
    }

    // ---------- Stamina ----------

    private void UseStamina()
    {
        CurrentStamina--;
        StopAllCoroutines("Stamina");
        StartCoroutine(RefreshStaminaRoutine(), "Stamina");
    }

    private IEnumerator<float> RefreshStaminaRoutine()
    {
        while (true)
        {
            yield return Tuning.TimeBetweenStaminaRefresh;
            if (CurrentStamina < StartingStamina && !IsDead)
            {
                CurrentStamina++;
                OnLine?.Invoke("staminaRefresh");
            }
        }
    }

    // ---------- PlayerHealth + Knockback + Flash ----------

    /// <summary>PlayerHealth.OnCollisionStay2D: touching the Ghost hurts too.</summary>
    private void GhostContact()
    {
        if (IsDead)
        {
            return;
        }
        float cx = PlayerX + PlayerBoxOffsetX, cy = PlayerY + PlayerBoxOffsetY;
        float overlapX = PlayerBoxHalfX + GhostBoxHalfX - MathF.Abs(cx - GhostX);
        float overlapY = PlayerBoxHalfY + GhostBoxHalfY - MathF.Abs(cy - GhostY);
        if (overlapX <= 0f || overlapY <= 0f)
        {
            return;
        }

        // The two colliders push apart (along the smaller overlap).
        if (overlapX < overlapY)
        {
            PlayerX += cx < GhostX ? -overlapX : overlapX;
        }
        else
        {
            PlayerY += cy < GhostY ? -overlapY : overlapY;
        }
        OnLine?.Invoke("ghostTouch");
        TakeDamage(1, GhostX, GhostY);
    }

    private void TakeDamage(int damageAmount, float hitX, float hitY)
    {
        if (!CanTakeDamage)
        {
            OnLine?.Invoke("blocked");
            return;
        }

        OnLine?.Invoke("hurt");
        GetKnockedBack(hitX, hitY, Tuning.KnockBackThrustAmount);
        StartCoroutine(FlashRoutine(), "Flash");
        CanTakeDamage = false;
        Health -= damageAmount;
        StartCoroutine(DamageRecoveryRoutine(), "PlayerHealth");
        CheckIfPlayerDeath();
    }

    private void GetKnockedBack(float sourceX, float sourceY, float knockbackThrust)
    {
        GettingKnockedBack = true;
        float dx = PlayerX - sourceX, dy = PlayerY - sourceY;
        float length = MathF.Sqrt(dx * dx + dy * dy);
        if (length > 1e-5f)
        {
            // AddForce(direction * thrust * mass, Impulse): velocity += impulse / mass = direction * thrust.
            velocityX += dx / length * knockbackThrust;
            velocityY += dy / length * knockbackThrust;
        }
        StartCoroutine(KnockRoutine(), "Knockback");
    }

    private IEnumerator<float> KnockRoutine()
    {
        yield return Tuning.KnockBackTime;
        velocityX = velocityY = 0f;
        GettingKnockedBack = false;
        OnLine?.Invoke("knockEnd");
    }

    private IEnumerator<float> FlashRoutine()
    {
        IsFlashing = true;
        yield return FlashTime;
        IsFlashing = false;
    }

    private IEnumerator<float> DamageRecoveryRoutine()
    {
        yield return Tuning.DamageRecoveryTime;
        CanTakeDamage = true;
        OnLine?.Invoke("recovered");
    }

    private void CheckIfPlayerDeath()
    {
        if (Health <= 0 && !IsDead)
        {
            IsDead = true;
            Health = 0;
            Deaths++;
            OnLine?.Invoke("death");
            StartCoroutine(DeathLoadSceneRoutine(), "PlayerHealth");
        }
    }

    private IEnumerator<float> DeathLoadSceneRoutine()
    {
        yield return DeathLoadTime;
        // Destroy(gameObject); Stamina.ReplenishStaminaOnDeath(); SceneManager.LoadScene("Town");
        OnLine?.Invoke("loadTown");
        Reset();
    }
}
