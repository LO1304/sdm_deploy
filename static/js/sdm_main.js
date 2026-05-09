/*
 * SDM Premium - Script Global
 * Centralisation des animations du background étoilé et logique commune
 */

document.addEventListener("DOMContentLoaded", function () {
    // 1. Initialiser AOS (si présent sur la page)
    if (typeof AOS !== 'undefined') {
        AOS.init({
            once: true,
            offset: 10,
            duration: 800,
            easing: 'ease-out-cubic',
        });
    }

    // 2. Initialiser le Canvas Etoilé (Cosmos)
    initCosmos();

    // 3. Gérer les Toast Messages
    initToasts();
});

/* ── CANVAS ÉTOILES ── */
function initCosmos() {
    const c = document.getElementById('sdm-cosmos');
    if (!c) return;
    const ctx = c.getContext('2d');
    let W, H, P = [];
    
    function resize() { 
        W = c.width = window.innerWidth; 
        H = c.height = window.innerHeight; 
    }
    
    function mk() {
        return {
            x: Math.random() * W, 
            y: Math.random() * H,
            r: Math.random() * 1.1 + 0.25,
            a: Math.random() * 0.55 + 0.04,
            da: (Math.random() * 0.004 + 0.001) * (Math.random() > .5 ? 1 : -1),
            vx: (Math.random() - .5) * .07,
            vy: (Math.random() - .5) * .07,
            gold: Math.random() > .82
        };
    }
    
    function init() { 
        resize(); 
        P = Array.from({ length: 200 }, mk); 
    }
    
    function draw() {
        ctx.clearRect(0, 0, W, H);
        P.forEach(p => {
            p.a = Math.max(.04, Math.min(.6, p.a + p.da));
            if (p.a >= .6 || p.a <= .04) p.da *= -1;
            p.x = (p.x + p.vx + W) % W;
            p.y = (p.y + p.vy + H) % H;
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
            ctx.fillStyle = p.gold
                ? `rgba(212,175,55,${p.a * .7})`
                : `rgba(255,255,255,${p.a * .45})`;
            ctx.fill();
        });
        requestAnimationFrame(draw);
    }
    
    init(); 
    draw();
    window.addEventListener('resize', resize);
}

/* ── TOASTS LOGIC ── */
function dismissToast(el) {
    el.classList.add('hiding');
    el.addEventListener('animationend', () => { el.remove(); });
}

window.dismissToast = dismissToast; // Expose to global if inline onclick is used

function initToasts() {
    setTimeout(() => {
        document.querySelectorAll('.toast-msg').forEach((el, i) => {
            setTimeout(() => { dismissToast(el); }, i * 300);
        });
    }, 5000);
}
