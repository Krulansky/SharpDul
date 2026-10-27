// Falling Frenzy Lab: drawing and input. The game itself is C# (FallingFrenzySim).
// frame() is called once per tick from C#: it draws the given state and returns the input.
window.sharpDulFrenzy = (function () {
    const held = { left: new Set(), right: new Set() };
    const keys = { KeyA: "left", ArrowLeft: "left", KeyD: "right", ArrowRight: "right" };
    const input = { left: false, right: false };
    let puffs = [];

    function refresh() {
        input.left = held.left.size > 0;
        input.right = held.right.size > 0;
    }

    function bindButton(element, action) {
        element.addEventListener("pointerdown", e => {
            e.preventDefault();
            element.setPointerCapture(e.pointerId);
            held[action].add("p" + e.pointerId);
            element.classList.add("pressed");
            refresh();
        });
        const release = e => { held[action].delete("p" + e.pointerId); element.classList.remove("pressed"); refresh(); };
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

    function draw(canvas, s) {
        const ctx = canvas.getContext("2d");
        const dpr = window.devicePixelRatio || 1;
        const w = canvas.clientWidth, h = canvas.clientHeight;
        if (canvas.width !== Math.round(w * dpr)) { canvas.width = Math.round(w * dpr); canvas.height = Math.round(h * dpr); }
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

        const scale = w / (s.viewHalfWidth * 2);
        const toX = x => (x + s.viewHalfWidth) * scale;
        const toY = y => h - (y - s.viewBottom) * scale;

        // Sky (the URP template's default look, roughly).
        const sky = ctx.createLinearGradient(0, 0, 0, h);
        sky.addColorStop(0, "#9fb7cf");
        sky.addColorStop(1, "#d9e2ea");
        ctx.fillStyle = sky;
        ctx.fillRect(0, 0, w, h);

        // Spawner marker and spawn range.
        if (s.hasSpawner) {
            ctx.strokeStyle = "rgba(0,0,0,0.25)";
            ctx.setLineDash([4, 4]);
            ctx.beginPath();
            const range = s.hasRandomX ? s.spawnRangeX : 0;
            ctx.moveTo(toX(-range), toY(s.spawnerY) + 2);
            ctx.lineTo(toX(range), toY(s.spawnerY) + 2);
            ctx.stroke();
            ctx.setLineDash([]);
            ctx.fillStyle = "rgba(0,0,0,0.35)";
            ctx.fillRect(toX(0) - 4, toY(s.spawnerY), 8, 4);
        }

        // Player (Cube 3 x 0.5).
        if (s.showPlayer) {
            ctx.fillStyle = s.playerIsTrigger ? "rgba(63,63,70,0.75)" : "#3f3f46";
            ctx.fillRect(toX(s.playerX - s.playerHalfWidth), toY(s.playerY + s.playerHalfHeight),
                s.playerHalfWidth * 2 * scale, s.playerHalfHeight * 2 * scale);
            if (s.playerIsTrigger) {
                ctx.strokeStyle = "#16a34a";
                ctx.lineWidth = 1.5;
                ctx.strokeRect(toX(s.playerX - s.playerHalfWidth), toY(s.playerY + s.playerHalfHeight),
                    s.playerHalfWidth * 2 * scale, s.playerHalfHeight * 2 * scale);
            }
        }

        // Sheep (Sphere, radius 0.5).
        for (const sheep of s.sheeps) {
            ctx.fillStyle = "#fafafa";
            ctx.beginPath();
            ctx.arc(toX(sheep.x), toY(sheep.y), s.sheepRadius * scale, 0, Math.PI * 2);
            ctx.fill();
            ctx.strokeStyle = "#71717a";
            ctx.lineWidth = 1;
            ctx.stroke();
        }

        // Catch puffs.
        const now = performance.now();
        for (const p of s.newPuffs) puffs.push({ x: p, born: now });
        puffs = puffs.filter(p => now - p.born < 400);
        for (const p of puffs) {
            const t = (now - p.born) / 400;
            ctx.globalAlpha = 1 - t;
            ctx.strokeStyle = "#16a34a";
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.arc(toX(p.x), toY(s.playerY + s.playerHalfHeight), (0.4 + t * 1.2) * scale, 0, Math.PI * 2);
            ctx.stroke();
        }
        ctx.globalAlpha = 1;

        // Frozen look on Game Over (Time.timeScale = 0).
        if (s.gameOver) {
            ctx.fillStyle = "rgba(0,0,0,0.35)";
            ctx.fillRect(0, 0, w, h);
            ctx.fillStyle = "#ffffff";
            ctx.font = "bold " + Math.round(h * 0.14) + "px system-ui, sans-serif";
            ctx.textAlign = "center";
            ctx.fillText("GAME OVER", w / 2, h / 2);
            ctx.textAlign = "left";
        }

        if (s.hasCounter) {
            ctx.fillStyle = "#18181b";
            ctx.font = "600 " + Math.round(h * 0.06) + "px system-ui, sans-serif";
            ctx.fillText("Sheep Left: " + s.sheepLeft, 10, Math.round(h * 0.08));
        }
    }

    return {
        attach: function (leftButton, rightButton) {
            bindButton(leftButton, "left");
            bindButton(rightButton, "right");
            window.addEventListener("keydown", keyDown);
            window.addEventListener("keyup", keyUp);
        },
        detach: function () {
            window.removeEventListener("keydown", keyDown);
            window.removeEventListener("keyup", keyUp);
            held.left.clear(); held.right.clear();
            refresh();
            puffs = [];
        },
        frame: function (canvas, state) {
            draw(canvas, state);
            return input;
        }
    };
})();
