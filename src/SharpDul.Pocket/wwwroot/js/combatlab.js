// Combat Lab: drawing and input. The fight itself is C# (CombatSim).
// frame() is called once per tick from C#: it draws the given state and returns the input.
window.sharpDulCombat = (function () {
    const keys = new Set();
    const stick = { x: 0, y: 0, pointer: null };
    let dashes = 0;
    let trail = [];
    let stickElement = null, knobElement = null, dashElement = null;

    const keyMap = {
        KeyW: "up", ArrowUp: "up", KeyS: "down", ArrowDown: "down",
        KeyA: "left", ArrowLeft: "left", KeyD: "right", ArrowRight: "right"
    };

    function onKeyDown(e) {
        if (e.code === "Space" || e.code === "ShiftLeft") {
            e.preventDefault();
            if (!e.repeat) dashes++;
            return;
        }
        const k = keyMap[e.code];
        if (!k) return;
        e.preventDefault();
        keys.add(k);
    }
    function onKeyUp(e) {
        const k = keyMap[e.code];
        if (k) keys.delete(k);
    }

    function moveStick(e) {
        const r = stickElement.getBoundingClientRect();
        const radius = r.width / 2;
        let dx = (e.clientX - (r.left + radius)) / radius;
        let dy = -(e.clientY - (r.top + radius)) / radius;
        const len = Math.hypot(dx, dy);
        if (len > 1) { dx /= len; dy /= len; }
        stick.x = dx; stick.y = dy;
        knobElement.style.transform = "translate(" + (dx * radius * 0.6) + "px," + (-dy * radius * 0.6) + "px)";
    }
    function releaseStick(e) {
        if (stick.pointer !== e.pointerId) return;
        stick.pointer = null; stick.x = 0; stick.y = 0;
        knobElement.style.transform = "";
        stickElement.classList.remove("pressed");
    }
    const stickDown = e => {
        e.preventDefault();
        stickElement.setPointerCapture(e.pointerId);
        stick.pointer = e.pointerId;
        stickElement.classList.add("pressed");
        moveStick(e);
    };
    const stickMove = e => { if (stick.pointer === e.pointerId) moveStick(e); };
    const dashDown = e => {
        e.preventDefault();
        dashes++;
        dashElement.classList.add("pressed");
        setTimeout(() => dashElement && dashElement.classList.remove("pressed"), 120);
    };
    const noMenu = e => e.preventDefault();

    function readInput() {
        // Keyboard: the Input System's 2D Vector composite (normalized diagonals).
        let x = (keys.has("right") ? 1 : 0) - (keys.has("left") ? 1 : 0);
        let y = (keys.has("up") ? 1 : 0) - (keys.has("down") ? 1 : 0);
        if (x !== 0 && y !== 0) { x *= Math.SQRT1_2; y *= Math.SQRT1_2; }
        if (x === 0 && y === 0) { x = stick.x; y = stick.y; }
        return { x: x, y: y, dashes: dashes };
    }

    function draw(canvas, s) {
        const ctx = canvas.getContext("2d");
        const dpr = window.devicePixelRatio || 1;
        const w = canvas.clientWidth, h = canvas.clientHeight;
        if (canvas.width !== Math.round(w * dpr)) { canvas.width = Math.round(w * dpr); canvas.height = Math.round(h * dpr); }
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

        const scale = w / (s.viewHalf * 2);
        const toX = x => (x + s.viewHalf) * scale;
        const toY = y => (s.viewHalf - y) * scale;

        // Ground.
        ctx.fillStyle = "#3b4a3a";
        ctx.fillRect(0, 0, w, h);
        ctx.strokeStyle = "rgba(255,255,255,0.05)";
        ctx.lineWidth = 1;
        for (let i = -6; i <= 6; i++) {
            ctx.beginPath(); ctx.moveTo(toX(i), 0); ctx.lineTo(toX(i), h); ctx.stroke();
            ctx.beginPath(); ctx.moveTo(0, toY(i)); ctx.lineTo(w, toY(i)); ctx.stroke();
        }
        ctx.strokeStyle = "rgba(0,0,0,0.45)";
        ctx.lineWidth = 2;
        ctx.strokeRect(toX(-s.arenaHalf), toY(s.arenaHalf), s.arenaHalf * 2 * scale, s.arenaHalf * 2 * scale);

        // attackRange around the Ghost.
        if (s.attackRange > 0) {
            ctx.setLineDash([5, 5]);
            ctx.strokeStyle = s.attacking ? "rgba(248,113,113,0.8)" : "rgba(255,255,255,0.35)";
            ctx.lineWidth = 1.5;
            ctx.beginPath();
            ctx.arc(toX(s.ghostX), toY(s.ghostY), s.attackRange * scale, 0, Math.PI * 2);
            ctx.stroke();
            ctx.setLineDash([]);
        }

        // The cone of the current burst (canvas angles turn the other way: y is down).
        if (s.shooting) {
            const a0 = -s.coneStart * Math.PI / 180, a1 = -s.coneEnd * Math.PI / 180;
            ctx.fillStyle = "rgba(196,181,253,0.12)";
            ctx.beginPath();
            ctx.moveTo(toX(s.ghostX), toY(s.ghostY));
            ctx.arc(toX(s.ghostX), toY(s.ghostY), 3 * scale, Math.min(a0, a1), Math.max(a0, a1));
            ctx.closePath();
            ctx.fill();
            // Where the burst starts.
            ctx.strokeStyle = "rgba(196,181,253,0.7)";
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(toX(s.ghostX), toY(s.ghostY));
            ctx.lineTo(toX(s.ghostX + Math.cos(-a0) * 3), toY(s.ghostY + Math.sin(-a0) * 3));
            ctx.stroke();
        }

        // Ghost (sprite 1 x 1, collider 1.0 x 0.8).
        const gx = toX(s.ghostX), gy = toY(s.ghostY);
        ctx.fillStyle = "rgba(226,232,240,0.9)";
        ctx.beginPath();
        ctx.arc(gx, gy - 0.1 * scale, 0.45 * scale, Math.PI, 0);
        ctx.lineTo(gx + 0.45 * scale, gy + 0.4 * scale);
        for (let i = 0; i < 3; i++) {
            const x0 = gx + 0.45 * scale - (i + 0.5) * 0.3 * scale;
            ctx.lineTo(x0, gy + 0.25 * scale);
            ctx.lineTo(x0 - 0.15 * scale, gy + 0.4 * scale);
        }
        ctx.closePath();
        ctx.fill();
        ctx.fillStyle = "#1e1b4b";
        ctx.fillRect(gx - 0.2 * scale, gy - 0.15 * scale, 0.1 * scale, 0.14 * scale);
        ctx.fillRect(gx + 0.1 * scale, gy - 0.15 * scale, 0.1 * scale, 0.14 * scale);

        // Dash trail.
        const now = performance.now();
        if (s.dashing && !s.dead) trail.push({ x: s.playerX, y: s.playerY, born: now });
        trail = trail.filter(p => now - p.born < 250);
        for (const p of trail) {
            ctx.globalAlpha = 0.5 * (1 - (now - p.born) / 250);
            ctx.fillStyle = "#4ade80";
            ctx.beginPath();
            ctx.arc(toX(p.x), toY(p.y), 0.3 * scale, 0, Math.PI * 2);
            ctx.fill();
        }
        ctx.globalAlpha = 1;

        // Player (sprite 1 x 1; the collider is the small box at the feet).
        const px = toX(s.playerX), py = toY(s.playerY);
        const blink = !s.canTakeDamage && !s.dead && Math.floor(now / 80) % 2 === 0;
        ctx.globalAlpha = blink ? 0.45 : 1;
        if (s.dead) {
            ctx.fillStyle = "#52525b";
            ctx.fillRect(px - 0.4 * scale, py - 0.12 * scale, 0.8 * scale, 0.24 * scale);
        } else {
            ctx.fillStyle = s.flashing ? "#ffffff" : "#166534";
            ctx.fillRect(px - 0.22 * scale, py - 0.45 * scale, 0.44 * scale, 0.75 * scale);
            ctx.fillStyle = s.flashing ? "#ffffff" : "#4ade80";
            const eyeX = s.facingLeft ? -0.14 : 0.04;
            ctx.fillRect(px + eyeX * scale, py - 0.35 * scale, 0.1 * scale, 0.06 * scale);
        }
        ctx.globalAlpha = 1;
        ctx.strokeStyle = "rgba(250,204,21,0.9)";
        ctx.lineWidth = 1;
        ctx.strokeRect(toX(s.playerX + s.boxOffsetX - s.boxHalfX), toY(s.playerY + s.boxOffsetY + s.boxHalfY),
            s.boxHalfX * 2 * scale, s.boxHalfY * 2 * scale);

        // Bullets: the collider (radius 0.5) and the sprite.
        for (const b of s.bullets) {
            ctx.strokeStyle = "rgba(244,114,182,0.35)";
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.arc(toX(b.x), toY(b.y), s.bulletRadius * scale, 0, Math.PI * 2);
            ctx.stroke();
            ctx.fillStyle = "#f472b6";
            ctx.beginPath();
            ctx.arc(toX(b.x), toY(b.y), 0.14 * scale, 0, Math.PI * 2);
            ctx.fill();
        }

        // HUD: health and stamina orbs.
        const unit = Math.max(10, Math.round(h * 0.035));
        for (let i = 0; i < s.maxHealth; i++) {
            ctx.fillStyle = i < s.health ? "#ef4444" : "rgba(0,0,0,0.4)";
            ctx.fillRect(10 + i * (unit + 4), 10, unit, unit);
        }
        for (let i = 0; i < s.maxStamina; i++) {
            ctx.fillStyle = i < s.stamina ? "#4ade80" : "rgba(0,0,0,0.4)";
            ctx.beginPath();
            ctx.arc(10 + unit / 2 + i * (unit + 4), 14 + unit * 1.5, unit / 2, 0, Math.PI * 2);
            ctx.fill();
        }
        ctx.fillStyle = "#fafafa";
        ctx.font = "600 " + Math.round(unit * 1.1) + "px system-ui, sans-serif";
        ctx.textAlign = "right";
        ctx.fillText(s.stateLabel, w - 10, 10 + unit);
        ctx.textAlign = "left";

        if (s.dead) {
            ctx.fillStyle = "rgba(0,0,0,0.35)";
            ctx.fillRect(0, 0, w, h);
            ctx.fillStyle = "#ffffff";
            ctx.font = "bold " + Math.round(h * 0.09) + "px system-ui, sans-serif";
            ctx.textAlign = "center";
            ctx.fillText("Death → Town", w / 2, h / 2);
            ctx.textAlign = "left";
        }
    }

    return {
        attach: function (stickEl, knobEl, dashEl) {
            stickElement = stickEl; knobElement = knobEl; dashElement = dashEl;
            stickEl.addEventListener("pointerdown", stickDown);
            stickEl.addEventListener("pointermove", stickMove);
            stickEl.addEventListener("pointerup", releaseStick);
            stickEl.addEventListener("pointercancel", releaseStick);
            stickEl.addEventListener("lostpointercapture", releaseStick);
            stickEl.addEventListener("contextmenu", noMenu);
            dashEl.addEventListener("pointerdown", dashDown);
            dashEl.addEventListener("contextmenu", noMenu);
            window.addEventListener("keydown", onKeyDown);
            window.addEventListener("keyup", onKeyUp);
        },
        detach: function () {
            window.removeEventListener("keydown", onKeyDown);
            window.removeEventListener("keyup", onKeyUp);
            keys.clear();
            stick.x = 0; stick.y = 0; stick.pointer = null;
            stickElement = knobElement = dashElement = null;
            trail = [];
        },
        frame: function (canvas, state) {
            draw(canvas, state);
            return readInput();
        }
    };
})();
