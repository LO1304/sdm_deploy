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

    // 2. Initialiser le Canvas Etoilé (allégé mobile & en pause en arrière-plan)
    initCosmos();

    // 3. Gérer les Toast Messages
    initToasts();

    // 4. Micro-retour haptique natif Android sur la barre de navigation
    document.querySelectorAll('.nav-island .nav-item, .m-icon-pill').forEach(el => {
        el.addEventListener('click', () => {
            try { if (navigator.vibrate) navigator.vibrate(6); } catch (e) {}
        });
    });
});

/* ── CANVAS ÉTOILES (DÉSACTIVÉ SUR MOBILE POUR 60FPS BATTERIE & FLUIDITÉ NATIVE) ── */
function initCosmos() {
    const c = document.getElementById('sdm-cosmos');
    if (!c) return;
    if (window.innerWidth < 768 || (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches)) {
        c.style.display = 'none';
        return;
    }
    const ctx = c.getContext('2d');
    let W, H, P = [];
    let rafId = null;

    function resize() {
        W = c.width = window.innerWidth;
        H = c.height = window.innerHeight;
    }

    function mk() {
        return {
            x: Math.random() * W,
            y: Math.random() * H,
            r: Math.random() * 1.05 + 0.25,
            a: Math.random() * 0.45 + 0.04,
            da: (Math.random() * 0.003 + 0.001) * (Math.random() > 0.5 ? 1 : -1),
            vx: (Math.random() - 0.5) * 0.05,
            vy: (Math.random() - 0.5) * 0.05,
            gold: Math.random() > 0.8
        };
    }

    function init() {
        resize();
        const count = window.innerWidth < 768 ? 36 : 90;
        P = Array.from({ length: count }, mk);
    }

    function draw() {
        if (document.hidden) {
            rafId = null;
            return;
        }
        ctx.clearRect(0, 0, W, H);
        for (let i = 0; i < P.length; i++) {
            const p = P[i];
            p.a = Math.max(0.04, Math.min(0.55, p.a + p.da));
            if (p.a >= 0.55 || p.a <= 0.04) p.da *= -1;
            p.x = (p.x + p.vx + W) % W;
            p.y = (p.y + p.vy + H) % H;
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
            ctx.fillStyle = p.gold
                ? `rgba(212,175,55,${p.a * 0.65})`
                : `rgba(255,255,255,${p.a * 0.4})`;
            ctx.fill();
        }
        rafId = requestAnimationFrame(draw);
    }

    document.addEventListener('visibilitychange', () => {
        if (!document.hidden && !rafId) {
            rafId = requestAnimationFrame(draw);
        }
    });

    init();
    rafId = requestAnimationFrame(draw);
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
            // Demander la localisation pour les prières
            updateUserLocation();
            
            navigator.serviceWorker.ready.then(function(registration) {
                // Initialiser FCM ou Web Push ici
            });
        }
    });
};

window.updateUserLocation = function() {
    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(function(position) {
            const lat = position.coords.latitude;
            const lng = position.coords.longitude;
            const tz = Intl.DateTimeFormat().resolvedOptions().timeZone;
            
            // Récupérer CSRF token
            const csrfMatch = document.cookie.match(/csrftoken=([^;]+)/);
            const csrf = csrfMatch ? csrfMatch[1] : '';
            
            fetch('/api/profil/update-location/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrf
                },
                body: JSON.stringify({ latitude: lat, longitude: lng, timezone: tz })
            }).then(res => res.json()).then(data => console.log('Location updated'))
              .catch(err => console.error('Erreur loc:', err));
        }, function(err) {
            console.log("Geolocation error:", err);
        });
    }
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
