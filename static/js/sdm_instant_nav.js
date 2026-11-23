/*
 * SDM Mobile App Engine — Navigation Instantanée (Zéro Latence, Zéro "Superposition de liens")
 * - Native View Transitions (@view-transition)
 * - Speculation Rules API (Prerender / Prefetch instantané sur Android Chrome / Edge / Samsung)
 * - Prefetch prédictif au toucher (touchstart / pointerdown)
 * - Feedback haptique + onglet actif immédiat (0ms) + barre de progression dorée ultra-fine
 */
(function () {
    if (window.__SDM_INSTANT_NAV_INIT__) return;
    window.__SDM_INSTANT_NAV_INIT__ = true;

    const CORE_TABS = [
        '/',
        '/collection/son/',
        '/collection/khassida/',
        '/coran/',
        '/zikr-compteur/'
    ];

    // 1. Injecter les styles natifs (View Transitions + Barre de progression dorée)
    const style = document.createElement('style');
    style.textContent = `
        @view-transition { navigation: auto; }
        ::view-transition-old(root) { animation: sdmFadeOut 130ms ease-out both; }
        ::view-transition-new(root) { animation: sdmFadeIn 160ms ease-out both; }
        @keyframes sdmFadeOut { from { opacity: 1; } to { opacity: 0.72; } }
        @keyframes sdmFadeIn { from { opacity: 0.72; } to { opacity: 1; } }
        #sdm-nav-progress {
            position: fixed; top: 0; left: 0; right: 0; height: 2.5px; z-index: 99999;
            background: linear-gradient(90deg, #D4AF37, #FDE047, #10B981);
            transform-origin: left center; transform: scaleX(0); opacity: 0;
            pointer-events: none; transition: transform 0.28s cubic-bezier(.22,1,.36,1), opacity 0.18s ease;
        }
        #sdm-nav-progress.active { opacity: 1; transform: scaleX(0.78); }
        #sdm-nav-progress.done { opacity: 0; transform: scaleX(1); }
    `;
    document.head.appendChild(style);

    // 2. Speculation Rules API léger (Prefetch au toucher uniquement — ne sature jamais le CPU mobile ni Render)
    try {
        if (HTMLScriptElement.supports && HTMLScriptElement.supports('speculationrules')) {
            const rules = {
                prefetch: [
                    {
                        source: 'document',
                        where: {
                            and: [
                                { href_matches: '/*' },
                                { not: { href_matches: '/logout*' } },
                                { not: { href_matches: '/admin*' } },
                                { not: { href_matches: '/api/*' } },
                                { not: { selector_matches: '[data-no-prefetch], [target="_blank"]' } }
                            ]
                        },
                        eagerness: 'conservative'
                    }
                ]
            };
            const s = document.createElement('script');
            s.type = 'speculationrules';
            s.textContent = JSON.stringify(rules);
            document.head.appendChild(s);
        }
    } catch (e) {}

    // 3. Barre de progression ultra-fine
    function ensureProgressBar() {
        let bar = document.getElementById('sdm-nav-progress');
        if (!bar && document.body) {
            bar = document.createElement('div');
            bar.id = 'sdm-nav-progress';
            document.body.appendChild(bar);
        }
        return bar;
    }

    function startProgress() {
        const bar = ensureProgressBar();
        if (!bar) return;
        bar.classList.remove('done');
        void bar.offsetWidth;
        bar.classList.add('active');
    }

    function resetProgress() {
        const bar = document.getElementById('sdm-nav-progress');
        if (bar) bar.classList.remove('active', 'done');
    }

    // 4. Prefetch intelligent au toucher (gagne 120-250ms avant que le doigt ne se lève)
    const prefetched = new Set();
    function canPrefetchUrl(href) {
        if (!href || href.startsWith('#') || href.startsWith('javascript:') || href.startsWith('mailto:') || href.startsWith('tel:')) return false;
        try {
            const u = new URL(href, window.location.origin);
            if (u.origin !== window.location.origin) return false;
            if (u.pathname === window.location.pathname && u.search === window.location.search) return false;
            if (/^\/(logout|admin|api|sons-api|proxy-|favoris\/toggle)/.test(u.pathname)) return false;
            return u.pathname + u.search;
        } catch (e) {
            return false;
        }
    }

    function prefetchUrl(urlPath) {
        if (!urlPath || prefetched.has(urlPath)) return;
        if (navigator.connection && navigator.connection.saveData) return;
        prefetched.add(urlPath);
        try {
            fetch(urlPath, { credentials: 'same-origin', priority: 'low' }).catch(() => {});
        } catch (e) {
            fetch(urlPath, { credentials: 'same-origin' }).catch(() => {});
        }
    }

    function warmCoreTabs() {
        const conn = navigator.connection;
        if (conn && (conn.saveData || conn.effectiveType === '2g' || conn.effectiveType === 'slow-2g')) return;
        const cur = window.location.pathname;
        // Précharger doucement 1 onglet à la fois après 3.5s pour ne jamais ralentir l'écran actif
        const queue = CORE_TABS.filter(t => t !== cur);
        queue.forEach((tab, idx) => {
            setTimeout(() => {
                if (!document.hidden) prefetchUrl(tab);
            }, 3500 + idx * 1400);
        });
    }

    if (document.readyState === 'complete') {
        warmCoreTabs();
    } else {
        window.addEventListener('load', warmCoreTabs, { once: true });
    }

    // Prefetch dès que le doigt touche un lien ou une carte
    document.addEventListener('pointerdown', (e) => {
        const a = e.target && e.target.closest ? e.target.closest('a[href]') : null;
        if (!a || a.target === '_blank' || a.hasAttribute('download')) return;
        const path = canPrefetchUrl(a.getAttribute('href'));
        if (path) prefetchUrl(path);
    }, { passive: true, capture: true });

    // Feedback instantané (0ms) lors du clic sur la barre de navigation ou un lien interne
    document.addEventListener('click', (e) => {
        const a = e.target && e.target.closest ? e.target.closest('a[href]') : null;
        if (!a || e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
        if (a.target === '_blank' || a.hasAttribute('download')) return;
        const path = canPrefetchUrl(a.getAttribute('href'));
        if (!path) return;

        // Mise en surbrillance immédiate de l'onglet touché (sensation app native 0ms)
        if (a.classList.contains('nav-item')) {
            const nav = a.closest('.nav-island, nav');
            if (nav) {
                nav.querySelectorAll('.nav-item.active').forEach(el => el.classList.remove('active'));
                a.classList.add('active');
            }
            try { if (navigator.vibrate) navigator.vibrate(6); } catch (err) {}
        }
        startProgress();
    }, { passive: true });

    // Nettoyer la barre en cas de retour navigateur (bfcache)
    window.addEventListener('pageshow', resetProgress);
    window.addEventListener('DOMContentLoaded', resetProgress);
})();
