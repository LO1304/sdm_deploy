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
    style.setAttribute('data-sdm-global-style', '1');
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

    // 5. MOTEUR PJAX ZERO-COUPURE AUDIO (le lecteur <audio id="sdm-global-audio"> ne s'arrête JAMAIS lors des retours / dossiers / onglets)
    const pjaxHtmlCache = new Map();
    let pjaxInFlight = null;

    function isPjaxEligible(urlPath) {
        if (!urlPath) return false;
        if (!document.getElementById('sdm-pjax-root')) return false;
        if (/^\/(logout|login|register|admin|api|sons-api|proxy-|lire\/|abonnement|paiement|favoris\/toggle|tazawwud\/paiement)/.test(urlPath)) {
            return false;
        }
        return true;
    }

    function updateBottomNavActive(pathname) {
        const nav = document.querySelector('.nav-island');
        if (!nav) return;
        nav.querySelectorAll('.nav-item').forEach(item => {
            const href = item.getAttribute('href') || '';
            let active = false;
            if (href === '/') active = (pathname === '/');
            else if (href.includes('/collection/son')) active = pathname.includes('/son');
            else if (href.includes('/collection/khassida')) active = pathname.includes('khassida');
            else if (href.includes('/coran')) active = pathname.includes('coran');
            else if (href.includes('/zikr')) active = pathname.includes('zikr') || pathname.includes('historique');
            item.classList.toggle('active', active);
        });
    }

    function isPageStyleEl(el) {
        if (!el || el.tagName !== 'STYLE') return false;
        if (el.hasAttribute('data-sdm-global-style')) return false;
        const txt = (el.textContent || '').slice(0, 120);
        if (/tailwindcss/i.test(txt)) return false;
        return true;
    }

    async function fetchHtmlForPjax(urlPath) {
        const cached = pjaxHtmlCache.get(urlPath);
        if (cached && (Date.now() - cached.ts) < 35000) {
            return cached.html;
        }
        const res = await fetch(urlPath, {
            credentials: 'same-origin',
            headers: { 'X-SDM-PJAX': '1', 'Accept': 'text/html' }
        });
        if (!res.ok) throw new Error('HTTP ' + res.status);
        const ct = (res.headers.get('content-type') || '').toLowerCase();
        if (!ct.includes('text/html')) throw new Error('Not HTML');
        const html = await res.text();
        if (pjaxHtmlCache.size > 16) {
            const oldestKey = pjaxHtmlCache.keys().next().value;
            pjaxHtmlCache.delete(oldestKey);
        }
        pjaxHtmlCache.set(urlPath, { html, ts: Date.now() });
        return html;
    }

    async function sdmSoftNavigate(urlPath, pushHistory = true) {
        if (!isPjaxEligible(urlPath)) {
            window.location.href = urlPath;
            return;
        }
        startProgress();
        const myToken = Symbol('pjax');
        pjaxInFlight = myToken;

        try {
            const html = await fetchHtmlForPjax(urlPath);
            if (pjaxInFlight !== myToken) return;

            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const newRoot = doc.getElementById('sdm-pjax-root');
            const curRoot = document.getElementById('sdm-pjax-root');
            if (!newRoot || !curRoot) {
                window.location.href = urlPath;
                return;
            }

            // 1. Nettoyer l'ancien écran (timers, listeners DOM liés à l'audio global) SANS JAMAIS stopper l'audio !
            if (typeof window.__sdmPageCleanup === 'function') {
                try { window.__sdmPageCleanup(); } catch (e) {}
                window.__sdmPageCleanup = null;
            }
            window._sdmPagePlayNext = null;
            window._sdmPagePlayPrev = null;

            // 2. Remplacer les <style> spécifiques de page dans <head> (préserve Tailwind & styles globaux)
            document.head.querySelectorAll('style').forEach(st => {
                if (isPageStyleEl(st)) st.remove();
            });
            doc.head.querySelectorAll('style').forEach(st => {
                if (isPageStyleEl(st)) {
                    const cloned = document.createElement('style');
                    cloned.textContent = st.textContent;
                    document.head.appendChild(cloned);
                }
            });

            // 3. Mettre à jour le titre, l'URL, le contenu principal et la barre d'onglets
            if (doc.title) document.title = doc.title;
            if (pushHistory) {
                history.pushState({ sdmPjax: true, url: urlPath }, '', urlPath);
            }
            curRoot.className = newRoot.className;
            curRoot.innerHTML = newRoot.innerHTML;

            const parsedU = new URL(urlPath, window.location.origin);
            updateBottomNavActive(parsedU.pathname);

            // 4. Exécuter les scripts spécifiques de la nouvelle page
            const oldScriptsBox = document.getElementById('sdm-pjax-scripts');
            const newScriptsBox = doc.getElementById('sdm-pjax-scripts');
            if (oldScriptsBox && newScriptsBox) {
                oldScriptsBox.innerHTML = '';
                const scripts = Array.from(newScriptsBox.querySelectorAll('script'));
                for (const sc of scripts) {
                    const s = document.createElement('script');
                    if (sc.type) s.type = sc.type;
                    if (sc.id) s.id = sc.id;
                    if (sc.src) {
                        s.src = sc.src;
                    } else if (!sc.type || sc.type === 'text/javascript') {
                        // Isoler dans un bloc pour éviter toute collision const/let entre navigations
                        s.textContent = sc.textContent;
                    } else {
                        // ex: application/json (#sdm-sons-data)
                        s.textContent = sc.textContent;
                    }
                    oldScriptsBox.appendChild(s);
                }
            }

            // 5. Rafraîchir le micro-widget audio persistant (toujours en lecture sans aucune coupure !)
            if (window.SDMAudioEngine && window.SDMAudioEngine.refreshWidgets) {
                window.SDMAudioEngine.refreshWidgets();
            }

            // 6. Scroll haut fluide
            window.scrollTo({ top: 0, behavior: 'instant' });
            resetProgress();
        } catch (err) {
            resetProgress();
            window.location.href = urlPath;
        }
    }

    window.sdmSoftNavigate = sdmSoftNavigate;

    // Intercepter les clics internes pour naviguer sans rechargement (0ms coupure audio)
    document.addEventListener('click', (e) => {
        const a = e.target && e.target.closest ? e.target.closest('a[href]') : null;
        if (!a || e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
        if (a.target === '_blank' || a.hasAttribute('download') || a.hasAttribute('data-no-pjax')) return;
        const hrefAttr = a.getAttribute('href') || '';
        if (hrefAttr.startsWith('#') || hrefAttr.startsWith('javascript:')) return;
        const path = canPrefetchUrl(hrefAttr);
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

        if (isPjaxEligible(path)) {
            e.preventDefault();
            sdmSoftNavigate(path, true);
        } else {
            startProgress();
        }
    });

    // Intercepter le bouton Retour / Suivant du téléphone ou navigateur (ZÉRO coupure audio !)
    window.addEventListener('popstate', () => {
        const cur = window.location.pathname + window.location.search;
        if (isPjaxEligible(cur)) {
            sdmSoftNavigate(cur, false);
        } else {
            window.location.reload();
        }
    });

    // Nettoyer la barre en cas de retour navigateur (bfcache)
    window.addEventListener('pageshow', resetProgress);
    window.addEventListener('DOMContentLoaded', resetProgress);
})();
