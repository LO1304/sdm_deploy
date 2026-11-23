/*
 * SDM Smart Notifications Engine v4 — Fiabilité Maximale (OS + Arrière-Plan SW + Historique + Son Khassida)
 * Gère :
 *  1. Heures de prière LIVE (Fajr, Tisbar, Takussan, Timiss, Guéwé) avec choix Sonore / Vibration / Silencieux
 *  2. Rappels Wird Mahuz (06h30 après Suba & 17h00 après Takussan) avec suivi des jours
 *  3. Verset du Jour & Citation de Cheikh Ahmadou Bamba (clic direct sur le rappel exact !)
 *  4. Nouveaux Sons & Nouveaux Khassidas publiés (alertes réelles avec titre exact & lien direct)
 *  5. Rappels d'Étude (Masaalik-ul Jinaan & Tazawwudu-ç-Çighâr) si jour sauté
 *  6. Synchronisation des préférences dans le Service Worker (Periodic Background Sync Android PWA)
 *  7. Historique local consultable sur /notifications/ (même en mode invité)
 */
(function () {
    if (window.__SDM_NOTIFS_INIT__) return;
    window.__SDM_NOTIFS_INIT__ = true;

    const PREFS_KEY = 'sdm_notif_prefs_v3';
    const FIRED_KEY = 'sdm_notif_fired_v3';
    const FEED_KEY = 'sdm_notif_feed_cache_v3';
    const HISTORY_KEY = 'sdm_notif_history_v1';
    const LIVE_PRAYERS_KEY = 'sdm_live_prayers_v1';
    const LAST_KH_KEY = 'sdm_last_seen_khassida_id';
    const LAST_SON_KEY = 'sdm_last_seen_son_id';
    const WIRD_TRACK_KEY = 'sdm_wird_tracker_v1';

    const DEFAULT_KHASSIDA_SOUND = 'https://res.cloudinary.com/dcajqzg2h/video/upload/v1795376309/media/audios/telegram/khassida/KURELSQACIDAS_8012_Wajahtou_Wadjhiyaza.mp3';

    const DEFAULT_PREFS = {
        enabled: true,
        prayerEnabled: true,
        prayerLeadMin: 5,
        verseEnabled: true,
        verseTime: '07:30',
        citationEnabled: true,
        citationTime: '13:30',
        khassidaEnabled: true,
        sonEnabled: true,
        wirdEnabled: true,
        wirdMorningTime: '06:30',
        wirdEveningTime: '17:00',
        studyEnabled: true,
        studyTime: '19:30',
        soundMode: 'sound',         // 'sound' | 'vibrate' | 'silent'
        prayerSoundMode: 'sound',   // 'sound' | 'vibrate' | 'silent'
        reminderSoundUrl: DEFAULT_KHASSIDA_SOUND,
        prayerSoundUrl: DEFAULT_KHASSIDA_SOUND
    };

    const FALLBACK_VERSES = [
        { ar: 'أَلَا بِذِكْرِ اللَّهِ تَطْمَئِنُّ الْقُلُوبُ', fr: 'N’est-ce point par l’évocation d’Allah que se tranquillisent les cœurs ?', ref: "Sourate Ar-Ra'd (13:28)" },
        { ar: 'فَإِنَّ مَعَ الْعُسْرِ يُسْرًا', fr: 'Certes, à côté de la difficulté est une facilité.', ref: 'Sourate Ash-Sharh (94:5)' },
        { ar: 'وَمَن يَتَوَكَّلْ عَلَى اللَّهِ فَهُوَ حَسْبُهُ', fr: 'Quiconque place sa confiance en Allah, Il lui suffit.', ref: 'Sourate At-Talâq (65:3)' },
        { ar: 'فَاذْكُرُونِي أَذْكُرْكُمْ وَاشْكُرُوا لِي', fr: 'Souvenez-vous de Moi, Je Me souviendrai de vous. Remerciez-Moi.', ref: 'Sourate Al-Baqara (2:152)' },
        { ar: 'رَبِّ زِدْنِي عِلْمًا', fr: 'Ô mon Seigneur, accrois mes connaissances !', ref: 'Sourate Tâ-Hâ (20:114)' },
        { ar: 'إِنَّ اللَّهَ مَعَ الصَّابِرِينَ', fr: 'Certes, Allah est avec les endurants.', ref: 'Sourate Al-Baqara (2:153)' }
    ];

    const STUDY_NUDGES_TODAY = [
        '🔥 Ta série d\'étude t\'attend ! 3 minutes sur Masaalik-ul Jinaan ou Tazawwudu-ç-Çighâr suffisent aujourd\'hui.',
        '📖 1 petite étape aujourd\'hui = ta flamme préservée et ta moyenne /20 en hausse !'
    ];
    const STUDY_NUDGES_MISSED = [
        '🔥 Tu as sauté hier ! Reviens faire 1 leçon rapide pour rallumer ta flamme et continuer ton chemin.',
        '⚡ On ne lâche rien ! 3 minutes maintenant suffisent pour reprendre ta progression quotidienne.'
    ];

    let chimeAudio = null;
    let chimeTimer = null;

    function getPrefs() {
        try {
            const raw = localStorage.getItem(PREFS_KEY);
            return Object.assign({}, DEFAULT_PREFS, raw ? JSON.parse(raw) : {});
        } catch (e) {
            return Object.assign({}, DEFAULT_PREFS);
        }
    }

    function syncPrefsToSwCache(prefsObj) {
        if (!('caches' in window)) return;
        try {
            const payload = {
                prefs: prefsObj || getPrefs(),
                prayers: getLivePrayers(),
                wirdToday: getWirdTodayStatus(),
                today: todayIso(),
                updatedAt: Date.now()
            };
            caches.open('sdm-notif-state-v1').then((c) => {
                c.put('/__sdm_notif_state__', new Response(JSON.stringify(payload), {
                    headers: { 'Content-Type': 'application/json' }
                }));
            }).catch(() => {});
        } catch (e) {}
    }

    function savePrefs(p) {
        const merged = Object.assign({}, getPrefs(), p);
        try { localStorage.setItem(PREFS_KEY, JSON.stringify(merged)); } catch (e) {}
        syncPrefsToSwCache(merged);
    }

    function getLivePrayers() {
        try {
            const raw = JSON.parse(localStorage.getItem(LIVE_PRAYERS_KEY) || 'null');
            if (raw && Array.isArray(raw.prayers) && raw.prayers.length >= 5) return raw.prayers;
        } catch (e) {}
        return null;
    }

    function saveLivePrayers(ptObj) {
        if (!ptObj) return;
        const map = [
            { name: 'Fajr (Subh)', time: ptObj.Fajr },
            { name: 'Tisbar (Dhuhr)', time: ptObj.Dhuhr },
            { name: 'Takussan (Asr)', time: ptObj.Asr },
            { name: 'Timiss (Maghrib)', time: ptObj.Maghrib },
            { name: 'Guéwé (Isha)', time: ptObj.Isha }
        ].filter(x => x.time && /^\d{1,2}:\d{2}/.test(String(x.time)));
        if (map.length === 5) {
            try {
                localStorage.setItem(LIVE_PRAYERS_KEY, JSON.stringify({ date: todayIso(), prayers: map }));
            } catch (e) {}
            syncPrefsToSwCache(getPrefs());
        }
    }

    function getHistory() {
        try {
            const arr = JSON.parse(localStorage.getItem(HISTORY_KEY) || '[]');
            return Array.isArray(arr) ? arr : [];
        } catch (e) {
            return [];
        }
    }

    function addHistoryEntry(title, body, url, kind) {
        try {
            const hist = getHistory();
            hist.unshift({
                title: String(title || 'Notification SDM'),
                body: String(body || ''),
                url: url || '/',
                kind: kind || 'general',
                ts: Date.now()
            });
            localStorage.setItem(HISTORY_KEY, JSON.stringify(hist.slice(0, 30)));
            window.dispatchEvent(new CustomEvent('sdm-notif-history-updated'));
        } catch (e) {}
    }

    function getFired() {
        try { return JSON.parse(localStorage.getItem(FIRED_KEY) || '{}'); } catch (e) { return {}; }
    }

    function markFired(key) {
        const f = getFired();
        f[key] = Date.now();
        const keys = Object.keys(f);
        if (keys.length > 100) {
            keys.sort((a, b) => f[a] - f[b]).slice(0, keys.length - 100).forEach(k => delete f[k]);
        }
        try { localStorage.setItem(FIRED_KEY, JSON.stringify(f)); } catch (e) {}
    }

    function todayIso() {
        const d = new Date();
        return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
    }

    function toMin(hhmm) {
        if (!hhmm || !String(hhmm).includes(':')) return -1;
        const [h, m] = String(hhmm).slice(0, 5).split(':').map(Number);
        return (isNaN(h) || isNaN(m)) ? -1 : h * 60 + m;
    }

    function stopPreviewSound() {
        if (chimeTimer) { clearTimeout(chimeTimer); chimeTimer = null; }
        if (chimeAudio) {
            try { chimeAudio.pause(); chimeAudio.currentTime = 0; } catch (e) {}
        }
    }

    function playSoftWebAudioChime() {
        try {
            const Ctx = window.AudioContext || window.webkitAudioContext;
            if (!Ctx) return;
            const ctx = new Ctx();
            const now = ctx.currentTime;
            [523.25, 659.25, 783.99].forEach((freq, i) => {
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.type = 'sine';
                osc.frequency.setValueAtTime(freq, now + i * 0.14);
                gain.gain.setValueAtTime(0.001, now + i * 0.14);
                gain.gain.exponentialRampToValueAtTime(0.14, now + i * 0.14 + 0.03);
                gain.gain.exponentialRampToValueAtTime(0.001, now + i * 0.14 + 0.42);
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start(now + i * 0.14);
                osc.stop(now + i * 0.14 + 0.45);
            });
        } catch (e) {}
    }

    function playNotificationSound(soundUrl, durationMs = 7500) {
        // Ne pas interrompre un Khassida déjà en lecture dans le lecteur principal
        const mainAud = document.getElementById('sdm-global-audio');
        if (mainAud && !mainAud.paused && mainAud.src) return;
        if (!soundUrl) { playSoftWebAudioChime(); return; }
        try {
            stopPreviewSound();
            if (!chimeAudio) {
                chimeAudio = new Audio();
                chimeAudio.preload = 'none';
            }
            chimeAudio.src = soundUrl;
            chimeAudio.volume = 0.85;
            const p = chimeAudio.play();
            if (p && typeof p.catch === 'function') {
                p.catch(() => playSoftWebAudioChime());
            }
            chimeTimer = setTimeout(stopPreviewSound, durationMs);
        } catch (e) {
            playSoftWebAudioChime();
        }
    }

    function dispatchNotification(title, body, url, tag, opts = {}) {
        const prefs = getPrefs();
        const isPrayer = Boolean(opts.isPrayer);
        const mode = isPrayer ? (prefs.prayerSoundMode || prefs.soundMode || 'sound') : (prefs.soundMode || 'sound');
        const soundUrl = isPrayer ? (prefs.prayerSoundUrl || DEFAULT_KHASSIDA_SOUND) : (prefs.reminderSoundUrl || DEFAULT_KHASSIDA_SOUND);

        addHistoryEntry(title, body, url, opts.kind || (isPrayer ? 'prayer' : 'general'));
        showInAppBanner(title, body, url);

        if (mode === 'sound') {
            playNotificationSound(soundUrl, isPrayer ? 10000 : 7000);
            try { if (navigator.vibrate) navigator.vibrate([160, 80, 160]); } catch (e) {}
        } else if (mode === 'vibrate') {
            try { if (navigator.vibrate) navigator.vibrate([180, 90, 180]); } catch (e) {}
        }

        if ('Notification' in window && Notification.permission === 'granted') {
            const notifOpts = {
                body: body,
                icon: '/static/images/icons/icon-192x192.png',
                badge: '/static/images/icons/icon-192x192.png',
                tag: tag || 'sdm-notif',
                renotify: true,
                silent: (mode === 'silent'),
                vibrate: (mode === 'silent') ? undefined : [160, 80, 160],
                data: { url: url || '/' }
            };
            if ('serviceWorker' in navigator) {
                navigator.serviceWorker.ready.then((reg) => {
                    if (reg && reg.showNotification) {
                        return reg.showNotification(title, notifOpts);
                    }
                    if (reg && reg.active) {
                        reg.active.postMessage({ type: 'SHOW_NOTIFICATION', title, body, url, tag, silent: mode === 'silent' });
                    }
                }).catch(() => {
                    try { new Notification(title, { body, icon: '/static/images/icons/icon-192x192.png', silent: mode === 'silent' }); } catch (e) {}
                });
            } else {
                try { new Notification(title, { body, icon: '/static/images/icons/icon-192x192.png', silent: mode === 'silent' }); } catch (e) {}
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
            stopPreviewSound();
            if (e.target.tagName === 'BUTTON') { box.remove(); return; }
            box.remove();
            if (url) {
                if (typeof window.sdmSoftNavigate === 'function' && url.startsWith('/')) {
                    window.sdmSoftNavigate(url, true);
                } else {
                    window.location.href = url;
                }
            }
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
        }, 9000);
    }

    async function syncFeed(force = false) {
        let cached = null;
        try { cached = JSON.parse(localStorage.getItem(FEED_KEY) || 'null'); } catch (e) {}
        if (!navigator.onLine) return cached;
        if (!force && cached && cached._ts && (Date.now() - cached._ts) < 60 * 1000) return cached;
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

    function getWirdTodayStatus() {
        const today = todayIso();
        try {
            const tr = JSON.parse(localStorage.getItem(WIRD_TRACK_KEY) || '{}');
            const rec = (tr.days && tr.days[today]) || {};
            return { morning: !!rec.morning, evening: !!rec.evening };
        } catch (e) {
            return { morning: false, evening: false };
        }
    }

    async function registerPeriodicBgSync() {
        try {
            if (!('serviceWorker' in navigator)) return false;
            const reg = await navigator.serviceWorker.ready;
            if ('periodicSync' in reg) {
                const status = await navigator.permissions.query({ name: 'periodic-background-sync' });
                if (status.state === 'granted') {
                    await reg.periodicSync.register('sdm-smart-notifs', { minInterval: 15 * 60 * 1000 });
                    return true;
                }
            }
        } catch (e) {}
        return false;
    }

    async function runNotificationChecks(forceFeed = false) {
        const prefs = getPrefs();
        syncPrefsToSwCache(prefs);
        if (!prefs.enabled) return;

        const now = new Date();
        const nowMin = now.getHours() * 60 + now.getMinutes();
        const today = todayIso();
        const fired = getFired();
        const feed = await syncFeed(forceFeed);

        // 1A. Nouveaux Sons publiés (alerte RÉELLE avec nom exact du son et lecture directe !)
        if (prefs.sonEnabled && feed && feed.latest_son && feed.latest_son.id) {
            const latestSonId = String(feed.latest_son.id);
            const seenSonId = localStorage.getItem(LAST_SON_KEY);
            if (!seenSonId) {
                localStorage.setItem(LAST_SON_KEY, latestSonId);
            } else if (seenSonId !== latestSonId) {
                localStorage.setItem(LAST_SON_KEY, latestSonId);
                dispatchNotification(
                    `🎧 Nouveau Son : ${feed.latest_son.titre}`,
                    `${feed.latest_son.auteur || 'Kourel Mouride'} vient d'être ajouté dans l'Audiothèque SDM. Touchez pour écouter !`,
                    `/collection/son/?autoplay=${latestSonId}`,
                    `sdm-son-${latestSonId}`,
                    { kind: 'son' }
                );
            }
        }

        // 1B. Nouveaux Khassidas PDF ajoutés
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
                    `sdm-kh-${latestId}`,
                    { kind: 'khassida' }
                );
            }
        }

        // 2. Horaires de prière LIVE (avec fenêtre de rattrapage 25 min)
        if (prefs.prayerEnabled) {
            const prayers = getLivePrayers() || (feed && feed.prayers) || [
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
                if (pm >= 0 && !fired[key] && nowMin >= (pm - lead) && nowMin <= (pm + 25)) {
                    markFired(key);
                    dispatchNotification(
                        `🕌 Heure de la Prière : ${p.name}`,
                        lead > 0 ? `La prière de ${p.name} est prévue à ${p.time}. Préparez vos ablutions.` : `Il est l'heure de la prière de ${p.name} (${p.time}).`,
                        '/',
                        key,
                        { isPrayer: true, kind: 'prayer' }
                    );
                    break;
                }
            }
        }

        // 3. Rappels Wird Mahuz Quotidien (06h30 après Suba & 17h00 après Takussan — fenêtre 3h si non validé)
        if (prefs.wirdEnabled) {
            const wUrl = (feed && feed.wird_url) || '/wird/mahuz-al-khafif/';
            const wStat = getWirdTodayStatus();
            const wm = toMin(prefs.wirdMorningTime || '06:30');
            const we = toMin(prefs.wirdEveningTime || '17:00');

            const wKeyM = `wird_m_${today}`;
            if (wm >= 0 && !wStat.morning && !fired[wKeyM] && nowMin >= wm && nowMin <= wm + 180) {
                markFired(wKeyM);
                dispatchNotification(
                    '📿 Rappel Wird Mahuz du Matin (après Suba)',
                    'Il est l\'heure de votre Wird Mahuz du matin. Touchez pour ouvrir le compteur sacré et valider votre journée.',
                    wUrl,
                    wKeyM,
                    { kind: 'wird' }
                );
            }

            const wKeyE = `wird_e_${today}`;
            if (we >= 0 && !wStat.evening && !fired[wKeyE] && nowMin >= we && nowMin <= we + 180) {
                markFired(wKeyE);
                dispatchNotification(
                    '📿 Rappel Wird Mahuz du Soir (après Takussan)',
                    'N\'oubliez pas votre Wird Mahuz du soir. Touchez pour ouvrir le compteur et préserver votre série !',
                    wUrl,
                    wKeyE,
                    { kind: 'wird' }
                );
            }
        }

        // 4. Verset du Jour -> Lien DIRECT vers le Studio Verset !
        if (prefs.verseEnabled) {
            const vm = toMin(prefs.verseTime);
            const vKey = `verse_${today}`;
            if (vm >= 0 && !fired[vKey] && nowMin >= vm && nowMin <= vm + 180) {
                markFired(vKey);
                const v = (feed && feed.verset_du_jour) || FALLBACK_VERSES[now.getDate() % FALLBACK_VERSES.length];
                dispatchNotification(
                    `📖 Verset du Jour · ${v.ref || 'Saint Coran'}`,
                    v.fr || v.ar,
                    '/?tab=spirit&load=verset',
                    vKey,
                    { kind: 'verse' }
                );
            }
        }

        // 5. Citation de Cheikh Ahmadou Bamba -> Lien DIRECT vers la citation exacte !
        if (prefs.citationEnabled) {
            const cm = toMin(prefs.citationTime);
            const cKey = `citation_${today}`;
            if (cm >= 0 && !fired[cKey] && nowMin >= cm && nowMin <= cm + 180) {
                markFired(cKey);
                const cit = (feed && feed.citation_du_jour) || {
                    id: 'mj_v1089',
                    texte: "La meilleure parure dont l'homme puisse se parer est la bonne conduite (al-adab) partout où il passe.",
                    source: "Masaalik-ul Jinaan · Cheikh Ahmadou Bamba (RTA)"
                };
                const citUrl = '/?tab=spirit&cid=' + encodeURIComponent(cit.id || 'mj_v1089');
                dispatchNotification(
                    '۞ Parole de Cheikh Ahmadou Bamba',
                    `« ${cit.texte} » — ${cit.source}`,
                    citUrl,
                    cKey,
                    { kind: 'citation' }
                );
            }
        }

        // 6. Rappel d'Étude Quotidien (Masaalik-ul Jinaan & Tazawwudu-ç-Çighâr)
        if (prefs.studyEnabled) {
            const dm = toMin(prefs.studyTime);
            const dKey = `study_${today}`;
            if (dm >= 0 && !fired[dKey] && nowMin >= dm) {
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
                    const pool = (mjMissed || tz.missed_yesterday) ? STUDY_NUDGES_MISSED : STUDY_NUDGES_TODAY;
                    let msg = pool[now.getDate() % pool.length];
                    if ((mjStreak || tz.streak) > 0 && !mjMissed && !tz.missed_yesterday) {
                        msg = `🔥 Série de ${Math.max(mjStreak, tz.streak)} jour(s) en jeu ! ` + msg;
                    }
                    dispatchNotification(
                        (mjMissed || tz.missed_yesterday) ? '🔥 Rappel d\'Étude · Jour sauté !' : '📖 Votre leçon du jour vous attend !',
                        msg,
                        '/apprentissage/',
                        dKey,
                        { kind: 'study' }
                    );
                }
            }
        }
    }

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
        saveLivePrayers,
        getLivePrayers,
        getHistory,
        syncFeed,
        previewSound(url) {
            playNotificationSound(url || getPrefs().reminderSoundUrl, 8000);
        },
        stopPreviewSound,
        async requestPermission() {
            if (!('Notification' in window)) return 'unsupported';
            const perm = await Notification.requestPermission();
            if (perm === 'granted') {
                syncPrefsToSwCache(getPrefs());
                await registerPeriodicBgSync();
                dispatchNotification(
                    '۞ Notifications SDM Activées !',
                    'Prières, Wird Mahuz (06h30/17h00), Versets, Citations, Nouveaux Sons & Khassidas actifs.',
                    '/notifications/',
                    'sdm-welcome',
                    { kind: 'system' }
                );
            }
            return perm;
        },
        testNow(kind) {
            if (kind === 'study') {
                dispatchNotification('🔥 Rappel d\'Étude · Masaalik-ul Jinaan', 'Ne brise pas ta série ! 3 minutes sur Masaalik-ul Jinaan suffisent pour garder ta flamme allumée et améliorer ta note /20 !', '/apprentissage/', 'sdm-test-study', { kind: 'study' });
            } else if (kind === 'wird') {
                dispatchNotification('📿 Rappel Wird Mahuz (06h30 / 17h00)', 'Pensez à accomplir votre Wird Mahuz et à valider votre séance dans le compteur sacré.', '/wird/mahuz-al-khafif/', 'sdm-test-wird', { kind: 'wird' });
            } else if (kind === 'son') {
                dispatchNotification('🎧 Nouveau Son : Serigne Bassirou Mbacké Khelcom', 'De nouveaux enseignements sont disponibles dans l\'Audiothèque SDM !', '/collection/son/?cat=BASSIROU_KHELCOM', 'sdm-test-son', { kind: 'son' });
            } else if (kind === 'prayer') {
                dispatchNotification('🕌 Heure de la Prière : Takussan (Asr)', 'Il est l\'heure de la prière de Takussan. Préparez vos ablutions.', '/', 'sdm-test-prayer', { isPrayer: true, kind: 'prayer' });
            } else {
                dispatchNotification('۞ Parole de Cheikh Ahmadou Bamba', '« La meilleure parure dont l\'homme puisse se parer est la bonne conduite (al-adab) partout où il passe. » — Masaalik-ul Jinaan (v.1089)', '/?tab=spirit&cid=mj_v1089', 'sdm-test-cit', { kind: 'citation' });
            }
        },
        checkNow: () => runNotificationChecks(true)
    };

    window.addEventListener('online', () => { updateOfflinePill(); runNotificationChecks(true); });
    window.addEventListener('offline', updateOfflinePill);
    window.addEventListener('DOMContentLoaded', () => {
        updateOfflinePill();
        syncPrefsToSwCache(getPrefs());
        if ('Notification' in window && Notification.permission === 'granted') {
            registerPeriodicBgSync();
        }
        setTimeout(() => runNotificationChecks(false), 1800);
        setInterval(() => runNotificationChecks(false), 45000);
    });
    document.addEventListener('visibilitychange', () => {
        if (!document.hidden) runNotificationChecks(true);
    });
})();
