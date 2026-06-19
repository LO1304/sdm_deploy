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

/* ── THEMES LOGIC ── */
window.setTheme = function(themeName) {
    // Save to localStorage
    if (themeName) {
        localStorage.setItem('sdm_theme', themeName);
        document.documentElement.setAttribute('data-theme', themeName);
    } else {
        localStorage.removeItem('sdm_theme');
        document.documentElement.removeAttribute('data-theme');
    }
    
    // Update active state on buttons if they exist
    updateThemeUI(themeName);
};

function updateThemeUI(themeName) {
    const currentTheme = themeName !== undefined ? themeName : (localStorage.getItem('sdm_theme') || '');
    const buttons = document.querySelectorAll('.theme-btn');
    
    buttons.forEach(btn => {
        if (btn.getAttribute('data-theme-id') === currentTheme) {
            btn.classList.add('ring-2', 'ring-white');
            btn.classList.remove('opacity-70');
        } else {
            btn.classList.remove('ring-2', 'ring-white');
            btn.classList.add('opacity-70');
        }
    });
}

// Initialize Theme UI on load
document.addEventListener("DOMContentLoaded", function () {
    updateThemeUI();
    
    // Check Notification Permission on load if logged in (or we could trigger this via button)
    if ("Notification" in window && Notification.permission !== "granted" && Notification.permission !== "denied") {
        // Optionnel : On peut afficher un custom toast demandant d'activer les notifications
        console.log("Notifications can be enabled.");
    }
});

// ── WEB PUSH NOTIFICATIONS ──
window.requestNotificationPermission = function() {
    if (!("Notification" in window)) {
        alert("Ce navigateur ne supporte pas les notifications desktop.");
        return;
    }
    
    Notification.requestPermission().then(function (permission) {
        if (permission === "granted") {
            console.log("Notification permission granted.");
            // Si on utilise Firebase JS SDK pour le front-end, on génère le token ici
            // Pour l'instant on utilise le Service Worker Standard Web Push
            // On peut s'abonner au pushManager
            navigator.serviceWorker.ready.then(function(registration) {
                // Nécessite une clé VAPID publique pour le Web Push standard
                // Registration pushManager logic here
            });
        }
    });
};

// ── AJAX FAVORIS ──
window.toggleFavoriAjax = function(event, element, removeCard = false) {
    event.preventDefault();
    if(event.stopPropagation) event.stopPropagation();

    const url = element.getAttribute('href');
    if (!url) return;
    
    // Feedback visuel immédiat (animation du bouton)
    const icon = element.querySelector('i');
    element.style.transform = 'scale(0.8)';
    setTimeout(() => { element.style.transform = ''; }, 200);

    fetch(url, {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === 'added') {
            if (icon) {
                icon.classList.remove('fa-regular');
                icon.classList.add('fa-solid');
                icon.style.color = 'var(--gold)';
            }
        } else if (data.status === 'removed') {
            if (removeCard) {
                // Sur la page Favoris, on retire la carte
                const card = element.closest('.fav-card');
                if (card) {
                    card.style.transition = 'all 0.4s ease';
                    card.style.opacity = '0';
                    card.style.transform = 'scale(0.9)';
                    setTimeout(() => card.remove(), 400);
                }
            } else {
                // Sur les autres pages, on grise l'icône
                if (icon) {
                    icon.classList.remove('fa-solid');
                    icon.classList.add('fa-regular');
                    icon.style.color = ''; // Remet la couleur par défaut
                }
            }
        }
    })
    .catch(err => console.error('Erreur AJAX favoris:', err));
};
