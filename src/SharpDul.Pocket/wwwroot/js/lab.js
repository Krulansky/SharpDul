// Mechanics Lab: drawing, thruster particles and input. The simulation itself is C# (LanderSim).
// frame() is called once per tick from C#: it draws the given state and returns the input.
window.sharpDulLab = (function () {
    const input = { up: false, left: false, right: false };
    const held = { up: new Set(), left: new Set(), right: new Set() };
    const keys = { ArrowUp: "up", KeyW: "up", Space: "up", ArrowLeft: "left", KeyA: "left", ArrowRight: "right", KeyD: "right" };
    let particles = [];
    let stars = null;
    let lastTime = 0;

    function refresh() {
        input.up = held.up.size > 0;
        input.left = held.left.size > 0;
        input.right = held.right.size > 0;
    }

    function bindButton(element, action) {
        const press = e => { e.preventDefault(); element.setPointerCapture(e.pointerId); held[action].add("p" + e.pointerId); element.classList.add("pressed"); refresh(); };
        const release = e => { held[action].delete("p" + e.pointerId); element.classList.remove("pressed"); refresh(); };
        element.addEventListener("pointerdown", press);
        element.addEventListener("pointerup", release);
        element.addEventListener("pointercancel", release);
        element.addEventListener("lostpointercapture", release);
        element.addEventListener("contextmenu", e => e.preventDefault());
    }

    function onKey(e, down) {
        const action = keys[e.code];
        if (!action) return;
        e.preventDefault();
        if (down) held[action].add(e.code); else held[action].delete(e.code);
        refresh();
    }
    const keyDown = e => onKey(e, true);
    const keyUp = e => onKey(e, false);

    // Emission: while a thruster is on, spawn particles. Turning it off only stops spawning -
    // particles already alive live out their lifetime (the same lesson as LanderVisuals).
    function emit(s, localX, localY, dirX, dirY, count) {
        const cos = Math.cos(s.angle), sin = Math.sin(s.angle);
        const wx = s.x + localX * cos - localY * sin;
        const wy = s.y + localX * sin + localY * cos;
        const wdx = dirX * cos - dirY * sin;
        const wdy = dirX * sin + dirY * cos;
        for (let i = 0; i < count; i++) {
            const spread = (Math.random() - 0.5) * 0.6;
            const speed = 3 + Math.random() * 2;
            particles.push({
                x: wx, y: wy,
                vx: (wdx + spread * wdy) * speed + s.vx,
                vy: (wdy - spread * wdx) * speed + s.vy,
                life: 0.35 + Math.random() * 0.2, age: 0
            });
        }
    }

    function draw(canvas, s) {
        const ctx = canvas.getContext("2d");
        const dpr = window.devicePixelRatio || 1;
        const w = canvas.clientWidth, h = canvas.clientHeight;
        if (canvas.width !== Math.round(w * dpr)) { canvas.width = Math.round(w * dpr); canvas.height = Math.round(h * dpr); }
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

        const scale = w / (s.worldHalfWidth * 2);
        const toX = x => (x + s.worldHalfWidth) * scale;
        const toY = y => h - (y + 1) * scale;

        ctx.fillStyle = "#0b0b10";
        ctx.fillRect(0, 0, w, h);
        if (!stars) { stars = Array.from({ length: 60 }, () => [Math.random(), Math.random(), Math.random()]); }
        ctx.fillStyle = "#ffffff";
        for (const [sx, sy, sb] of stars) { ctx.globalAlpha = 0.2 + sb * 0.6; ctx.fillRect(sx * w, sy * (h - scale), 1.5, 1.5); }
        ctx.globalAlpha = 1;

        // Ground and landing pad.
        ctx.fillStyle = "#3f3f46";
        ctx.fillRect(0, toY(0), w, h - toY(0));
        ctx.fillStyle = "#a1a1aa";
        ctx.fillRect(toX(-s.padHalfWidth), toY(0) - 3, s.padHalfWidth * 2 * scale, 6);

        // Particles.
        const now = performance.now() / 1000;
        const dt = lastTime ? Math.min(now - lastTime, 0.1) : 0;
        lastTime = now;
        if (s.upForce) { emit(s, -0.3, -0.75, 0, -1, 2); emit(s, 0, -0.75, 0, -1, 3); emit(s, 0.3, -0.75, 0, -1, 2); }
        if (s.leftForce) emit(s, -0.3, -0.75, 0, -1, 2);
        if (s.rightForce) emit(s, 0.3, -0.75, 0, -1, 2);
        particles = particles.filter(p => (p.age += dt) < p.life);
        for (const p of particles) {
            p.x += p.vx * dt; p.y += p.vy * dt;
            const t = p.age / p.life;
            ctx.globalAlpha = 1 - t;
            ctx.fillStyle = t < 0.4 ? "#fde68a" : "#f97316";
            const size = (1 - t) * 0.22 * scale + 1;
            ctx.fillRect(toX(p.x) - size / 2, toY(p.y) - size / 2, size, size);
        }
        ctx.globalAlpha = 1;

        // Lander body (BoxCollider2D size) with two legs.
        if (!s.crashed) {
            ctx.save();
            ctx.translate(toX(s.x), toY(s.y));
            ctx.rotate(-s.angle);
            const bw = s.bodyWidth * scale, bh = s.bodyHeight * scale;
            ctx.fillStyle = "#e4e4e7";
            ctx.fillRect(-bw / 2, -bh / 2, bw, bh * 0.75);
            ctx.strokeStyle = "#e4e4e7";
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(-bw * 0.3, bh * 0.25); ctx.lineTo(-bw / 2, bh / 2);
            ctx.moveTo(bw * 0.3, bh * 0.25); ctx.lineTo(bw / 2, bh / 2);
            ctx.stroke();
            ctx.fillStyle = "#0b0b10";
            ctx.fillRect(-bw * 0.2, -bh * 0.3, bw * 0.4, bh * 0.2);
            ctx.restore();
        } else {
            ctx.fillStyle = "#f97316";
            for (let i = 0; i < 8; i++) {
                const a = i / 8 * Math.PI * 2;
                ctx.fillRect(toX(s.x + Math.cos(a) * 0.5) - 3, toY(s.y + Math.sin(a) * 0.5) - 3, 6, 6);
            }
        }
    }

    return {
        attach: function (upButton, leftButton, rightButton) {
            bindButton(upButton, "up");
            bindButton(leftButton, "left");
            bindButton(rightButton, "right");
            window.addEventListener("keydown", keyDown);
            window.addEventListener("keyup", keyUp);
        },
        detach: function () {
            window.removeEventListener("keydown", keyDown);
            window.removeEventListener("keyup", keyUp);
            held.up.clear(); held.left.clear(); held.right.clear();
            refresh();
            particles = [];
        },
        frame: function (canvas, state) {
            draw(canvas, state);
            return input;
        }
    };
})();
