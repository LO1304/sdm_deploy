/*
 * SDM Smart Notifications Engine & Offline Indicator
 * Gère :
 *  1. Heures de prière (Fajr, Tisbar, Takussan, Timiss, Guéwé)
 *  2. Verset du Jour à l'heure exacte choisie par l'utilisateur
 *  3. Citation de Cheikh Ahmadou Bamba (318 citations) à l'heure exacte choisie
 *  4. Nouveaux Khassidas ajoutés (avec le nom exact du Khassida + lien direct)
 *  5. Coach Tazawwudu-ç-Çighâr « Mode Duolingo » (relance si cours non fait aujourd'hui ou jour sauté !)
 *  6. Bandeau discret « Mode Hors-Ligne actif » si déconnecté
 */
(function () {
    if (window.__SDM_NOTIFS_INIT__) return;
    window.__SDM_NOTIFS_INIT__ = true;

    const PREFS_KEY = 'sdm_notif_prefs_v2';
    const FIRED_KEY = 'sdm_notif_fired_v2';
    const FEED_KEY = 'sdm_notif_feed_cache_v2';
    const LAST_KH_KEY = 'sdm_last_seen_khassida_id';

    const DEFAULT_PREFS = {
        enabled: true,
        prayerEnabled: true,
        prayerLeadMin: 5,
        verseEnabled: true,
        verseTime: '07:30',
        citationEnabled: true,
        citationTime: '13:30',
        khassidaEnabled: true,
        duolingoEnabled: true,
        duolingoTime: '19:30'
    };

    const FALLBACK_VERSES = [
        { ar: 'أَلَا بِذِكْرِ اللَّهِ تَطْمَئِنُّ الْقُلُوبُ', fr: 'N’est-ce point par l’évocation d’Allah que se tranquillisent les cœurs ?', ref: 'Sourate Ar-Ra\'d (13:28)' },
        { ar: 'فَإِنَّ مَعَ الْعُسْرِ يُسْرًا', fr: 'Certes, à côté de la difficulté est une facilité.', ref: 'Sourate Ash-Sharh (94:5)' },
        { ar: 'وَمَن يَتَوَكَّلْ عَلَى اللَّهِ فَهُوَ حَسْبُهُ', fr: 'Quiconque place sa confiance en Allah, Il lui suffit.', ref: 'Sourate At-Talâq (65:3)' },
        { ar: 'فَاذْكُرُونِي أَذْكُرْكُمْ وَاشْكُرُوا لِي', fr: 'Souvenez-vous de Moi, Je Me souviendrai de vous. Remerciez-Moi.', ref: 'Sourate Al-Baqara (2:152)' },
        { ar: 'رَبِّ زِدْنِي عِلْمًا', fr: 'Ô mon Seigneur, accrois mes connaissances !', ref: 'Sourate Tâ-Hâ (20:114)' },
        { ar: 'إِنَّ اللَّهَ مَعَ الصَّابِرِينَ', fr: 'Certes, Allah est avec les endurants.', ref: 'Sourate Al-Baqara (2:153)' },
        { ar: 'لَا يُكَلِّفُ اللَّهُ نَفْسًا إِلَّا وُسْعَهَا', fr: 'Allah n’impose à aucune âme une charge supérieure à sa capacité.', ref: 'Sourate Al-Baqara (2:286)' }
    ];

    const DUOLINGO_NUDGES_TODAY = [
        '🔥 Ta flamme Tazawwudu-ç-Çighâr attend ! 2 minutes de lecture suffisent pour sauver ta série aujourd\'hui.',
        '🦉 Hey ! Il se fait tard et tu n\'as pas encore fait ta leçon du jour sur Tazawwudu-ç-Çighâr. Ne laisse pas ta série s\'éteindre !',
        '📖 1 petite étape de Tazawwud = +20 XP et ta série préservée ! Cheikh Ahmadou Bamba t\'attend.'
    ];
    const DUOLINGO_NUDGES_MISSED = [
        '🔥 Alerte Série ! Tu as sauté hier sur Tazawwudu-ç-Çighâr… Reviens faire 1 étape rapide pour rallumer ta flamme !',
        '🦉 On ne lâche rien ! Un jour manqué, ça arrive — fais 3 minutes de Tazawwud maintenant et reprends ton élan !',
        '⚡ Ta progression Tazawwud t\'attend ! Ne laisse pas un deuxième jour passer sans apprendre un vers de Serigne Touba.'
    ];

    function getPrefs() {
        try {
            const raw = localStorage.getItem(PREFS_KEY);
            return Object.assign({}, DEFAULT_PREFS, raw ? JSON.parse(raw) : {});
        } catch (e) {
            return Object.assign({}, DEFAULT_PREFS);
        }
    }

    function savePrefs(p) {
        try { localStorage.setItem(PREFS_KEY, JSON.stringify(Object.assign({}, getPrefs(), p))); } catch (e) {}
    }

    function getFired() {
        try { return JSON.parse(localStorage.getItem(FIRED_KEY) || '{}'); } catch (e) { return {}; }
    }

    function markFired(key) {
        const f = getFired();
        f[key] = Date.now();
        // Garder seulement les 60 dernières clés
        const keys = Object.keys(f);
        if (keys.length > 60) {
            keys.sort((a, b) => f[a] - f[b]).slice(0, keys.length - 60).forEach(k => delete f[k]);
        }
        try { localStorage.setItem(FIRED_KEY, JSON.stringify(f)); } catch (e) {}
    }

    function todayIso() {
        const d = new Date();
        return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
    }

    function toMin(hhmm) {
        if (!hhmm || !hhmm.includes(':')) return -1;
        const [h, m] = hhmm.split(':').map(Number);
        return (isNaN(h) || isNaN(m)) ? -1 : h * 60 + m;
    }

    // Afficher une notification système (SW) + toast élégant in-app
    function dispatchNotification(title, body, url, tag) {
        // 1. Toast in-app natif (visible même sans permission OS)
        showInAppBanner(title, body, url);

        // 2. Notification OS Android / Desktop via Service Worker
        if ('Notification' in window && Notification.permission === 'granted') {
            if ('serviceWorker' in navigator) {
                navigator.serviceWorker.ready.then((reg) => {
                    if (reg && reg.showNotification) {
                        reg.showNotification(title, {
                            body: body,
                            icon: '/static/images/icons/icon-192x192.png',
                            badge: '/static/images/icons/icon-192x192.png',
                            tag: tag || 'sdm-notif',
                            renotify: true,
                            vibrate: [160, 80, 160],
                            data: { url: url || '/' }
                        });
                    }
                }).catch(() => {
                    try { new Notification(title, { body, icon: '/static/images/icons/icon-192x192.png' }); } catch (e) {}
                });
            } else {
                try { new Notification(title, { body, icon: '/static/images/icons/icon-192x192.png' }); } catch (e) {}
            }
        }
    }

    function showInAppBanner(title, body, url) {
        if (!document.body) return;
        let box = document.getElementById('sdm-smart-notif-banner');
        if (box) box.remove();
        box = document.createElement('div');
        box.id = 'sdm-smart-notif-banner';
        box.style.cssText = [
            'position:fixed', 'top:max(10px, env(safe-area-inset-top, 10px))', 'left:50%',
            'transform:translateX(-50%) translateY(-16px)', 'width:calc(100% - 24px)', 'max-width:440px',
            'z-index:99998', 'background:rgba(6,22,15,0.97)', 'backdrop-filter:blur(18px)',
            'border:1px solid rgba(212,175,55,0.55)', 'border-radius:18px', 'padding:12px 14px',
            'box-shadow:0 16px 40px rgba(0,0,0,0.65)', 'color:#fff', 'display:flex',
            'align-items:flex-start', 'gap:11px', 'opacity:0', 'transition:all 0.28s ease', 'cursor:pointer'
        ].join(';');
        box.innerHTML =
            `<div style="width:36px;height:36px;border-radius:12px;background:linear-gradient(135deg,#FDE047,#D4AF37);color:#040B08;display:flex;align-items:center;justify-content:center;font-size:16px;flex-shrink:0;">۞</div>` +
            `<div style="flex:1;min-width:0;">` +
                `<div style="font-size:12px;font-weight:900;color:#FDE047;line-height:1.25;">${String(title).replace(/</g,'&lt;')}</div>` +
                `<div style="font-size:11px;color:rgba(255,255,255,0.88);margin-top:3px;line-height:1.35;">${String(body).replace(/</g,'&lt;')}</div>` +
            `</div>` +
            `<button type="button" aria-label="Fermer" style="background:none;border:none;color:rgba(255,255,255,0.5);font-size:14px;padding:2px 4px;cursor:pointer;">✕</button>`;
        box.addEventListener('click', (e) => {
            if (e.target.tagName === 'BUTTON') { box.remove(); return; }
            box.remove();
            if (url) window.location.href = url;
        });
        document.body.appendChild(box);
        requestAnimationFrame(() => {
            box.style.opacity = '1';
            box.style.transform = 'translateX(-50%) translateY(0)';
        });
        setTimeout(() => {
            if (box && box.parentNode) {
                box.style.opacity = '0';
                setTimeout(() => box.remove(), 300);
            }
        }, 7500);
    }

    async function syncFeed() {
        let cached = null;
        try { cached = JSON.parse(localStorage.getItem(FEED_KEY) || 'null'); } catch (e) {}
        if (!navigator.onLine) return cached;
        if (cached && cached._ts && (Date.now() - cached._ts) < 5 * 60 * 1000) return cached;
        try {
            const res = await fetch('/api/notifications/sync-feed/', { credentials: 'same-origin' });
            if (res.ok) {
                const data = await res.json();
                data._ts = Date.now();
                localStorage.setItem(FEED_KEY, JSON.stringify(data));
                return data;
            }
        } catch (e) {}
        return cached;
    }

    async function runNotificationChecks() {
        const prefs = getPrefs();
        if (!prefs.enabled) return;

        const now = new Date();
        const nowMin = now.getHours() * 60 + now.getMinutes();
        const today = todayIso();
        const fired = getFired();
        const feed = await syncFeed();

        // 1. Nouveaux Khassidas ajoutés (avec le NOM EXACT du Khassida !)
        if (prefs.khassidaEnabled && feed && feed.latest_khassida && feed.latest_khassida.id) {
            const latestId = String(feed.latest_khassida.id);
            const seenId = localStorage.getItem(LAST_KH_KEY);
            if (!seenId) {
                localStorage.setItem(LAST_KH_KEY, latestId);
            } else if (seenId !== latestId) {
                localStorage.setItem(LAST_KH_KEY, latestId);
                dispatchNotification(
                    `📚 Nouveau Khassida : ${feed.latest_khassida.titre}`,
                    `« ${feed.latest_khassida.titre} » vient d'être ajouté sur SDM Mouride. Touchez pour lire !`,
                    `/lire/khassida/${latestId}/`,
                    `sdm-kh-${latestId}`
                );
            }
        }

        // 2. Horaires de prière (Dakar / Sénégal par défaut ou horaires du feed)
        if (prefs.prayerEnabled) {
            const prayers = (feed && feed.prayers) || [
                { name: 'Fajr (Subh)', time: '05:45' },
                { name: 'Tisbar (Dhuhr)', time: '13:15' },
                { name: 'Takussan (Asr)', time: '16:35' },
                { name: 'Timiss (Maghrib)', time: '18:55' },
                { name: 'Guéwé (Isha)', time: '20:05' }
            ];
            const lead = parseInt(prefs.prayerLeadMin || 5, 10);
            for (const p of prayers) {
                const pm = toMin(p.time);
                const key = `prayer_${today}_${p.name}`;
                if (pm >= 0 && !fired[key] && nowMin >= (pm - lead) && nowMin <= (pm + 10)) {
                    markFired(key);
                    dispatchNotification(
                        `🕌 Heure de la Prière : ${p.name}`,
                        lead > 0 ? `La prière de ${p.name} est prévue à ${p.time}. Préparez vos ablutions.` : `Il est l'heure de la prière de ${p.name} (${p.time}).`,
                        '/',
                        key
                    );
                    break;
                }
            }
        }

        // 3. Verset du Jour à l'heure exacte choisie par l'utilisateur -> Lien direct vers le Studio Verset !
        if (prefs.verseEnabled) {
            const vm = toMin(prefs.verseTime);
            const vKey = `verse_${today}`;
            if (vm >= 0 && !fired[vKey] && nowMin >= vm && nowMin <= vm + 90) {
                markFired(vKey);
                const v = (feed && feed.verset_du_jour) || FALLBACK_VERSES[now.getDate() % FALLBACK_VERSES.length];
                dispatchNotification(
                    `📖 Verset du Jour · ${v.ref || 'Saint Coran'}`,
                    v.fr || v.ar,
                    '/?tab=spirit&load=verset',
                    vKey
                );
            }
        }

        // 4. Citation de Cheikh Ahmadou Bamba -> Lien DIRECT vers la citation exacte (enregistrer / copier / partager)
        if (prefs.citationEnabled) {
            const cm = toMin(prefs.citationTime);
            const cKey = `citation_${today}`;
            if (cm >= 0 && !fired[cKey] && nowMin >= cm && nowMin <= cm + 90) {
                markFired(cKey);
                const cit = (feed && feed.citation_du_jour) || {
                    id: 'mj_v1089',
                    texte: "La meilleure parure dont l'homme puisse se parer est la bonne conduite (al-adab) partout où il passe.",
                    source: "Masaalikul Jinaan · Cheikh Ahmadou Bamba (RTA)"
                };
                const citUrl = '/?tab=spirit&cid=' + encodeURIComponent(cit.id || 'mj_v1089');
                dispatchNotification(
                    `۞ Parole de Cheikh Ahmadou Bamba`,
                    `« ${cit.texte} » — ${cit.source}`,
                    citUrl,
                    cKey
                );
            }
        }

        // 5. Coach « Mode Duolingo » (Tazawwudu-ç-Çighâr & Masaalikul Jinaan — relance si jour sauté !)
        if (prefs.duolingoEnabled) {
            const dm = toMin(prefs.duolingoTime);
            const dKey = `duolingo_${today}`;
            if (dm >= 0 && !fired[dKey] && nowMin >= dm) {
                // Vérifier progression locale Masaalikul Jinaan
                let mjDoneToday = false, mjMissed = false, mjStreak = 0;
                try {
                    const mj = JSON.parse(localStorage.getItem('sdm_masaalik_progress_v1') || '{}');
                    const days = Array.isArray(mj.active_days) ? mj.active_days : [];
                    mjDoneToday = days.includes(today);
                    const yest = new Date(Date.now() - 86400000);
                    const yIso = `${yest.getFullYear()}-${String(yest.getMonth() + 1).padStart(2, '0')}-${String(yest.getDate()).padStart(2, '0')}`;
                    mjMissed = days.length > 0 && !days.includes(yIso) && !mjDoneToday;
                    mjStreak = mj.streak || 0;
                } catch (e) {}

                const tz = (feed && feed.tazawwud) || { done_today: false, missed_yesterday: false, streak: 0 };
                if (!mjDoneToday && !tz.done_today) {
                    markFired(dKey);
                    const targetMasaalik = (now.getDate() % 2 === 0);
                    if (targetMasaalik) {
                        const title = mjMissed
                            ? '🦉 Jour sauté sur Masaalikul Jinaan !'
                            : '🔥 Ta flamme Masaalikul Jinaan va s\'éteindre !';
                        const body = mjMissed
                            ? 'Tu as sauté hier sur Masaalikul Jinaan ! Reviens faire 1 chapitre rapide pour rallumer ta flamme et monter ta note /20.'
                            : (mjStreak > 0
                                ? `🔥 Série de ${mjStreak} jour(s) en danger ! 3 minutes sur Masaalikul Jinaan suffisent aujourd'hui.`
                                : '📖 3 minutes sur Masaalikul Jinaan aujourd\'hui = une leçon de Cheikh Ahmadou Bamba maîtrisée et ta flamme allumée !');
                        dispatchNotification(title, body, '/masaalik/', dKey);
                    } else {
                        const pool = tz.missed_yesterday ? DUOLINGO_NUDGES_MISSED : DUOLINGO_NUDGES_TODAY;
                        let msg = pool[now.getDate() % pool.length];
                        if (tz.streak > 0 && !tz.missed_yesterday) {
                            msg = `🔥 Série de ${tz.streak} jour(s) en danger ! ` + msg;
                        }
                        dispatchNotification(
                            tz.missed_yesterday ? '🦉 Jour sauté sur Tazawwudu-ç-Çighâr !' : '🔥 Ta flamme Tazawwud va s\'éteindre !',
                            msg,
                            '/tazawwud/',
                            dKey
                        );
                    }
                }
            }
        }
    }

    // 6. Indicateur discret de Mode Hors-Ligne
    function updateOfflinePill() {
        let pill = document.getElementById('sdm-offline-pill');
        if (!navigator.onLine) {
            if (!pill && document.body) {
                pill = document.createElement('div');
                pill.id = 'sdm-offline-pill';
                pill.style.cssText = 'position:fixed;bottom:calc(68px + env(safe-area-inset-bottom,0px));left:50%;transform:translateX(-50%);z-index:950;background:rgba(6,78,59,0.95);border:1px solid #10B981;color:#A7F3D0;font-size:10.5px;font-weight:800;padding:5px 12px;border-radius:99px;box-shadow:0 6px 20px rgba(0,0,0,0.45);display:flex;align-items:center;gap:6px;white-space:nowrap;';
                pill.innerHTML = '<i class="fa-solid fa-plane-up"></i> Mode Hors-Ligne · <a href="/telechargements/" style="color:#FDE047;text-decoration:underline;">Mes fichiers</a>';
                document.body.appendChild(pill);
            }
        } else if (pill) {
            pill.remove();
        }
    }

    window.SDMNotifications = {
        getPrefs,
        savePrefs,
        async requestPermission() {
            if (!('Notification' in window)) return 'unsupported';
            const perm = await Notification.requestPermission();
            if (perm === 'granted') {
                dispatchNotification('۞ Notifications SDM Activées !', 'Vous recevrez vos rappels de prières, versets, citations de Cheikh Ahmadou Bamba et coach Tazawwud.', '/notifications/', 'sdm-welcome');
            }
            return perm;
        },
        testNow(kind) {
            if (kind === 'duolingo') {
                dispatchNotification('🦉 Coach Duolingo · Masaalikul Jinaan', '🔥 Ne brise pas ta série ! 3 minutes sur Masaalikul Jinaan suffisent pour garder ta flamme allumée et améliorer ta note /20 !', '/masaalik/', 'sdm-test-duo');
            } else if (kind === 'khassida') {
                dispatchNotification('📚 Nouveau Khassida : Mawahibou Nâfih', 'Un nouveau manuscrit est disponible dans votre bibliothèque SDM Mouride.', '/collection/khassida/', 'sdm-test-kh');
            } else {
                dispatchNotification('۞ Citation de Cheikh Ahmadou Bamba', '« La meilleure parure dont l\'homme puisse se parer est la bonne conduite (al-adab) partout où il passe. » — Masaalikul Jinaan', '/?tab=spirit&cid=mj_v1089', 'sdm-test-cit');
            }
        },
        checkNow: runNotificationChecks
    };

    window.addEventListener('online', updateOfflinePill);
    window.addEventListener('offline', updateOfflinePill);
    window.addEventListener('DOMContentLoaded', () => {
        updateOfflinePill();
        setTimeout(runNotificationChecks, 2500);
        setInterval(runNotificationChecks, 60000);
    });
    document.addEventListener('visibilitychange', () => {
        if (!document.hidden) runNotificationChecks();
    });
})();
