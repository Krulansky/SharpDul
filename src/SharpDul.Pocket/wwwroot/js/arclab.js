// Arc Lab: drawing and input. The lobs and pops themselves are C# (ArcSim, AnimCurve).
// frame() is called once per tick from C#: it draws the given state and returns the input.
window.sharpDulArc = (function () {
    const input = { tapX: 0, tapY: 0, taps: 0, dragKey: -1, dragTime: 0, dragValue: 0 };
    let scene = null, curve = null, lastState = null;

    // The curve graph: time 0..1.1 across, value -0.3..1.55 up.
    const graph = { tMin: 0, tMax: 1.1, vMin: -0.3, vMax: 1.55, pad: 14 };

    function sceneToWorld(e) {
        const r = scene.getBoundingClientRect();
        const s = lastState;
        const x = s.viewMinX + (e.clientX - r.left) / r.width * (s.viewMaxX - s.viewMinX);
        const y = s.viewMaxY - (e.clientY - r.top) / r.height * (s.viewMaxY - s.viewMinY);
        return { x, y };
    }
    const sceneDown = e => {
        if (!lastState) return;
        e.preventDefault();
        const p = sceneToWorld(e);
        input.tapX = p.x; input.tapY = p.y; input.taps++;
    };

    function graphToCurve(e) {
        const r = curve.getBoundingClientRect();
        const w = r.width - graph.pad * 2, h = r.height - graph.pad * 2;
        return {
            t: graph.tMin + (e.clientX - r.left - graph.pad) / w * (graph.tMax - graph.tMin),
            v: graph.vMax - (e.clientY - r.top - graph.pad) / h * (graph.vMax - graph.vMin)
        };
    }
    const curveDown = e => {
        if (!lastState) return;
        e.preventDefault();
        const p = graphToCurve(e);
        let best = -1, bestD = 0.12;
        lastState.keys.forEach((k, i) => {
            const d = Math.hypot((k.t - p.t) / (graph.tMax - graph.tMin), (k.v - p.v) / (graph.vMax - graph.vMin));
            if (d < bestD) { best = i; bestD = d; }
        });
        if (best < 0) return;
        curve.setPointerCapture(e.pointerId);
        input.dragKey = best; input.dragTime = lastState.keys[best].t; input.dragValue = lastState.keys[best].v;
    };
    const curveMove = e => {
        if (input.dragKey < 0) return;
        const p = graphToCurve(e);
        input.dragTime = p.t; input.dragValue = p.v;
    };
    const curveUp = () => { input.dragKey = -1; };
    const noMenu = e => e.preventDefault();

    function fit(canvas) {
        const ctx = canvas.getContext("2d");
        const dpr = window.devicePixelRatio || 1;
        const w = canvas.clientWidth, h = canvas.clientHeight;
        if (canvas.width !== Math.round(w * dpr)) { canvas.width = Math.round(w * dpr); canvas.height = Math.round(h * dpr); }
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
        return { ctx, w, h };
    }

    function drawScene(s) {
        const { ctx, w, h } = fit(scene);
        const scale = w / (s.viewMaxX - s.viewMinX);
        const X = x => (x - s.viewMinX) * scale;
        const Y = y => (s.viewMaxY - y) * scale;

        ctx.fillStyle = "#3b4a3a";
        ctx.fillRect(0, 0, w, h);
        ctx.strokeStyle = "rgba(255,255,255,0.05)";
        for (let i = Math.ceil(s.viewMinX); i <= s.viewMaxX; i++) { ctx.beginPath(); ctx.moveTo(X(i), 0); ctx.lineTo(X(i), h); ctx.stroke(); }
        for (let i = Math.ceil(s.viewMinY); i <= s.viewMaxY; i++) { ctx.beginPath(); ctx.moveTo(0, Y(i)); ctx.lineTo(w, Y(i)); ctx.stroke(); }

        if (s.grapeMode) {
            // attackRange
            ctx.setLineDash([5, 5]);
            ctx.strokeStyle = s.inRange ? "rgba(248,113,113,0.8)" : "rgba(255,255,255,0.3)";
            ctx.beginPath(); ctx.arc(X(s.grapeX), Y(s.grapeY), s.attackRange * scale, 0, Math.PI * 2); ctx.stroke();
            ctx.setLineDash([]);
            // Grape (purple bunch).
            ctx.fillStyle = "#7c3aed";
            for (const [dx, dy] of [[0, 0.25], [-0.2, 0], [0.2, 0], [0, -0.22]]) {
                ctx.beginPath(); ctx.arc(X(s.grapeX + dx), Y(s.grapeY + dy), 0.2 * scale, 0, Math.PI * 2); ctx.fill();
            }
        } else {
            // Bush and pickUpDistance around the player.
            ctx.fillStyle = "#166534";
            ctx.beginPath(); ctx.arc(X(s.bushX), Y(s.bushY), 0.45 * scale, 0, Math.PI * 2); ctx.fill();
            ctx.setLineDash([5, 5]);
            ctx.strokeStyle = "rgba(250,204,21,0.6)";
            ctx.beginPath(); ctx.arc(X(s.playerX), Y(s.playerY), s.pickUpDistance * scale, 0, Math.PI * 2); ctx.stroke();
            ctx.setLineDash([]);
        }

        // Splatters: the collider is red while it is enabled (0.2 s), then the sprite fades.
        for (const sp of s.splatters) {
            ctx.globalAlpha = Math.max(0, 1 - sp.age / s.fadeTime);
            ctx.fillStyle = "#a855f7";
            ctx.beginPath(); ctx.ellipse(X(sp.x), Y(sp.y), s.splatHalfX * scale, s.splatHalfY * scale, 0, 0, Math.PI * 2); ctx.fill();
            ctx.globalAlpha = 1;
            if (sp.on) {
                ctx.strokeStyle = "#ef4444"; ctx.lineWidth = 2;
                ctx.beginPath(); ctx.ellipse(X(sp.x), Y(sp.y), s.splatHalfX * scale, s.splatHalfY * scale, 0, 0, Math.PI * 2); ctx.stroke();
                ctx.lineWidth = 1;
            }
        }

        // Lobs: path, shadow on the ground, the grape above it, and the height line between.
        for (const l of s.lobs) {
            ctx.strokeStyle = "rgba(196,181,253,0.5)";
            ctx.setLineDash([3, 4]);
            ctx.beginPath();
            l.path.forEach((p, i) => i ? ctx.lineTo(X(p[0]), Y(p[1])) : ctx.moveTo(X(p[0]), Y(p[1])));
            ctx.stroke();
            ctx.setLineDash([]);
            ctx.fillStyle = "rgba(255,255,255,0.35)";
            ctx.beginPath(); ctx.arc(X(l.endX), Y(l.endY), 0.12 * scale, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = "rgba(0,0,0,0.4)";
            ctx.beginPath(); ctx.ellipse(X(l.shadowX), Y(l.shadowY), 0.3 * scale, 0.12 * scale, 0, 0, Math.PI * 2); ctx.fill();
            ctx.strokeStyle = "rgba(250,204,21,0.7)";
            ctx.beginPath(); ctx.moveTo(X(l.x), Y(l.y)); ctx.lineTo(X(l.x), Y(l.y - l.height)); ctx.stroke();
            ctx.fillStyle = "#a855f7";
            ctx.beginPath(); ctx.arc(X(l.x), Y(l.y), 0.22 * scale, 0, Math.PI * 2); ctx.fill();
        }

        // Globes.
        for (const g of s.globes) {
            ctx.fillStyle = "rgba(0,0,0,0.35)";
            ctx.beginPath(); ctx.ellipse(X(g.x), Y(g.y - g.height), 0.2 * scale, 0.08 * scale, 0, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = g.popping ? "#86efac" : "#4ade80";
            ctx.beginPath(); ctx.arc(X(g.x), Y(g.y), s.globeRadius * scale, 0, Math.PI * 2); ctx.fill();
        }

        // Player and where they walk to.
        ctx.strokeStyle = "rgba(255,255,255,0.4)";
        ctx.beginPath(); ctx.arc(X(s.targetX), Y(s.targetY), 0.15 * scale, 0, Math.PI * 2); ctx.stroke();
        ctx.fillStyle = s.flashing ? "#ffffff" : "#15803d";
        ctx.fillRect(X(s.playerX) - 0.22 * scale, Y(s.playerY) - 0.75 * scale, 0.44 * scale, 0.75 * scale);
        ctx.strokeStyle = "rgba(250,204,21,0.9)";
        ctx.strokeRect(X(s.playerX - s.playerHalfX), Y(s.playerY + s.playerHalfY), s.playerHalfX * 2 * scale, s.playerHalfY * 2 * scale);

        ctx.fillStyle = "#fafafa";
        ctx.font = "600 13px system-ui, sans-serif";
        ctx.fillText(s.label, 10, 20);
    }

    function drawCurve(s) {
        const { ctx, w, h } = fit(curve);
        const gw = w - graph.pad * 2, gh = h - graph.pad * 2;
        const X = t => graph.pad + (t - graph.tMin) / (graph.tMax - graph.tMin) * gw;
        const Y = v => graph.pad + (graph.vMax - v) / (graph.vMax - graph.vMin) * gh;
        const dark = matchMedia("(prefers-color-scheme: dark)").matches;
        ctx.fillStyle = dark ? "#18181b" : "#ffffff";
        ctx.fillRect(0, 0, w, h);
        ctx.strokeStyle = dark ? "#3f3f46" : "#e4e4e7";
        ctx.font = "11px ui-monospace, monospace";
        ctx.fillStyle = dark ? "#a1a1aa" : "#71717a";
        for (const v of [0, 0.5, 1]) {
            ctx.beginPath(); ctx.moveTo(X(0), Y(v)); ctx.lineTo(X(graph.tMax), Y(v)); ctx.stroke();
            ctx.fillText(v.toString(), X(0) + 2, Y(v) - 3);
        }
        for (const t of [0.5, 1]) {
            ctx.beginPath(); ctx.moveTo(X(t), Y(graph.vMin)); ctx.lineTo(X(t), Y(graph.vMax)); ctx.stroke();
            ctx.fillText("t " + t, X(t) + 2, Y(graph.vMin) - 3);
        }
        ctx.strokeStyle = "#a855f7";
        ctx.lineWidth = 2.5;
        ctx.beginPath();
        s.samples.forEach((v, i) => {
            const t = i / (s.samples.length - 1) * graph.tMax;
            i ? ctx.lineTo(X(t), Y(v)) : ctx.moveTo(X(t), Y(v));
        });
        ctx.stroke();
        ctx.lineWidth = 1;
        s.keys.forEach((k, i) => {
            ctx.fillStyle = i === input.dragKey ? "#f59e0b" : (dark ? "#e4e4e7" : "#3f3f46");
            ctx.beginPath(); ctx.arc(X(k.t), Y(k.v), 8, 0, Math.PI * 2); ctx.fill();
        });
        if (s.liveT !== null) {
            ctx.fillStyle = "#f59e0b";
            ctx.beginPath(); ctx.arc(X(s.liveT), Y(s.liveV), 5, 0, Math.PI * 2); ctx.fill();
        }
    }

    return {
        attach: function (sceneCanvas, curveCanvas) {
            scene = sceneCanvas; curve = curveCanvas;
            scene.addEventListener("pointerdown", sceneDown);
            scene.addEventListener("contextmenu", noMenu);
            curve.addEventListener("pointerdown", curveDown);
            curve.addEventListener("pointermove", curveMove);
            curve.addEventListener("pointerup", curveUp);
            curve.addEventListener("pointercancel", curveUp);
            curve.addEventListener("lostpointercapture", curveUp);
            curve.addEventListener("contextmenu", noMenu);
        },
        detach: function () {
            scene = curve = lastState = null;
            input.dragKey = -1;
        },
        frame: function (sceneCanvas, curveCanvas, state) {
            lastState = state;
            drawScene(state);
            drawCurve(state);
            return input;
        }
    };
})();
