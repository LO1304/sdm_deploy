/*
 * SDM Smart Notifications Engine & Offline Indicator
 * Gère :
 *  1. Heures de prière (Fajr, Tisbar, Takussan, Timiss, Guéwé) avec choix Sonore / Vibration / Silencieux
 *  2. Verset du Jour & Citation de Cheikh Ahmadou Bamba (clic direct sur le rappel exact !)
 *  3. Nouveaux Sons & Nouveaux Khassidas publiés (notifications réelles avec titre exact & lien direct)
 *  4. Rappels Wird Quotidien (06h30 après Suba & 17h00 après Takussan) avec suivi des jours
 *  5. Rappels d'Étude (Masaalikul Jinaan & Tazawwudu-ç-Çighâr) si jour sauté
 *  6. Choix du mode sonore (Khassida / Adhan, Vibration seule, ou Silencieux) + prévisualisation audio
 */
(function () {
    if (window.__SDM_NOTIFS_INIT__) return;
    window.__SDM_NOTIFS_INIT__ = true;

    const PREFS_KEY = 'sdm_notif_prefs_v3';
    const FIRED_KEY = 'sdm_notif_fired_v3';
    const FEED_KEY = 'sdm_notif_feed_cache_v3';
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
        { ar: 'أَلَا بِذِكْرِ اللَّهِ تَطْمَئِنُّ الْقُلُوبُ', fr: 'N’est-ce point par l’évocation d’Allah que se tranquillisent les cœurs ?', ref: 'Sourate Ar-Ra\'d (13:28)' },
        { ar: 'فَإِنَّ مَعَ الْعُسْرِ يُسْرًا', fr: 'Certes, à côté de la difficulté est une facilité.', ref: 'Sourate Ash-Sharh (94:5)' },
        { ar: 'وَمَن يَتَوَكَّلْ عَلَى اللَّهِ فَهُوَ حَسْبُهُ', fr: 'Quiconque place sa confiance en Allah, Il lui suffit.', ref: 'Sourate At-Talâq (65:3)' },
        { ar: 'فَاذْكُرُونِي أَذْكُرْكُمْ وَاشْكُرُوا لِي', fr: 'Souvenez-vous de Moi, Je Me souviendrai de vous. Remerciez-Moi.', ref: 'Sourate Al-Baqara (2:152)' },
        { ar: 'رَبِّ زِدْنِي عِلْمًا', fr: 'Ô mon Seigneur, accrois mes connaissances !', ref: 'Sourate Tâ-Hâ (20:114)' },
        { ar: 'إِنَّ اللَّهَ مَعَ الصَّابِرِينَ', fr: 'Certes, Allah est avec les endurants.', ref: 'Sourate Al-Baqara (2:153)' }
    ];

    const STUDY_NUDGES_TODAY = [
        '🔥 Ta série d\'étude t\'attend ! 3 minutes sur Masaalikul Jinaan ou Tazawwudu-ç-Çighâr suffisent aujourd\'hui.',
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

    function savePrefs(p) {
        try { localStorage.setItem(PREFS_KEY, JSON.stringify(Object.assign({}, getPrefs(), p))); } catch (e) {}
    }

    function getFired() {
        try { return JSON.parse(localStorage.getItem(FIRED_KEY) || '{}'); } catch (e) { return {}; }
    }

    function markFired(key) {
        const f = getFired();
        f[key] = Date.now();
        const keys = Object.keys(f);
        if (keys.length > 80) {
            keys.sort((a, b) => f[a] - f[b]).slice(0, keys.length - 80).forEach(k => delete f[k]);
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

    function stopPreviewSound() {
        if (chimeTimer) { clearTimeout(chimeTimer); chimeTimer = null; }
        if (chimeAudio) {
            try { chimeAudio.pause(); chimeAudio.currentTime = 0; } catch (e) {}
        }
    }

    function playNotificationSound(soundUrl, durationMs = 7500) {
        if (!soundUrl) return;
        // Ne pas interrompre un Khassida déjà en lecture dans le lecteur principal
        const mainAud = document.getElementById('sdm-global-audio');
        if (mainAud && !mainAud.paused && mainAud.src) return;
        try {
            stopPreviewSound();
            if (!chimeAudio) {
                chimeAudio = new Audio();
                chimeAudio.preload = 'none';
            }
            chimeAudio.src = soundUrl;
            chimeAudio.volume = 0.85;
            chimeAudio.play().catch(() => {});
            chimeTimer = setTimeout(stopPreviewSound, durationMs);
        } catch (e) {}
    }

    // Afficher notification système + toast in-app respectant le mode Son / Vibration / Silencieux
    function dispatchNotification(title, body, url, tag, opts = {}) {
        const prefs = getPrefs();
        const isPrayer = Boolean(opts.isPrayer);
        const mode = isPrayer ? (prefs.prayerSoundMode || prefs.soundMode || 'sound') : (prefs.soundMode || 'sound');
        const soundUrl = isPrayer ? (prefs.prayerSoundUrl || DEFAULT_KHASSIDA_SOUND) : (prefs.reminderSoundUrl || DEFAULT_KHASSIDA_SOUND);

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
                    if (reg && reg.showNotification) reg.showNotification(title, notifOpts);
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
        }, 8000);
    }

    async function syncFeed(force = false) {
        let cached = null;
        try { cached = JSON.parse(localStorage.getItem(FEED_KEY) || 'null'); } catch (e) {}
        if (!navigator.onLine) return cached;
        if (!force && cached && cached._ts && (Date.now() - cached._ts) < 2 * 60 * 1000) return cached;
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

    async function runNotificationChecks() {
        const prefs = getPrefs();
        if (!prefs.enabled) return;

        const now = new Date();
        const nowMin = now.getHours() * 60 + now.getMinutes();
        const today = todayIso();
        const fired = getFired();
        const feed = await syncFeed();

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
                    `sdm-son-${latestSonId}`
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
                    `sdm-kh-${latestId}`
                );
            }
        }

        // 2. Horaires de prière (avec option sonore dédiée ou silencieux)
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
                        key,
                        { isPrayer: true }
                    );
                    break;
                }
            }
        }

        // 3. Rappels Wird Quotidien (06h30 après Suba & 17h00 après Takussan)
        if (prefs.wirdEnabled) {
            const wUrl = (feed && feed.wird_url) || '/collection/wird/';
            const wStat = getWirdTodayStatus();
            const wm = toMin(prefs.wirdMorningTime || '06:30');
            const we = toMin(prefs.wirdEveningTime || '17:00');

            const wKeyM = `wird_m_${today}`;
            if (wm >= 0 && !wStat.morning && !fired[wKeyM] && nowMin >= wm && nowMin <= wm + 120) {
                markFired(wKeyM);
                dispatchNotification(
                    '📿 Rappel Wird du Matin (après Suba)',
                    'Il est l\'heure de votre Wird du matin (06h30). Touchez pour ouvrir le compteur et enregistrer votre journée.',
                    wUrl,
                    wKeyM
                );
            }

            const wKeyE = `wird_e_${today}`;
            if (we >= 0 && !wStat.evening && !fired[wKeyE] && nowMin >= we && nowMin <= we + 120) {
                markFired(wKeyE);
                dispatchNotification(
                    '📿 Rappel Wird du Soir (après Takussan)',
                    'N\'oubliez pas votre Wird du soir (17h00). Touchez pour accomplir votre séance et maintenir votre série !',
                    wUrl,
                    wKeyE
                );
            }
        }

        // 4. Verset du Jour -> Lien DIRECT vers le Studio Verset !
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

        // 5. Citation de Cheikh Ahmadou Bamba -> Lien DIRECT vers la citation exacte !
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

        // 6. Rappel d'Étude Quotidien (Masaalikul Jinaan & Tazawwudu-ç-Çighâr)
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
                        '/masaalik/',
                        dKey
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
        syncFeed,
        previewSound(url) {
            playNotificationSound(url || getPrefs().reminderSoundUrl, 8000);
        },
        stopPreviewSound,
        async requestPermission() {
            if (!('Notification' in window)) return 'unsupported';
            const perm = await Notification.requestPermission();
            if (perm === 'granted') {
                dispatchNotification('۞ Notifications SDM Activées !', 'Prières, Wird (06h30/17h00), Versets, Citations, Nouveaux Sons & Khassidas actifs.', '/notifications/', 'sdm-welcome');
            }
            return perm;
        },
        testNow(kind) {
            if (kind === 'study') {
                dispatchNotification('🔥 Rappel d\'Étude · Masaalikul Jinaan', 'Ne brise pas ta série ! 3 minutes sur Masaalikul Jinaan suffisent pour garder ta flamme allumée et améliorer ta note /20 !', '/masaalik/', 'sdm-test-study');
            } else if (kind === 'wird') {
                dispatchNotification('📿 Rappel Wird Quotidien (06h30 / 17h00)', 'Pensez à accomplir votre Wird quotidien et à valider votre journée dans le suivi.', '/collection/wird/', 'sdm-test-wird');
            } else if (kind === 'son') {
                dispatchNotification('🎧 Nouveau Son : Wajahtou Wadjhiyaza', 'Kourel National Hizbut Tarqiyyah est disponible dans l\'Audiothèque SDM !', '/collection/son/', 'sdm-test-son');
            } else if (kind === 'prayer') {
                dispatchNotification('🕌 Heure de la Prière : Takussan (Asr)', 'Il est l\'heure de la prière de Takussan. Préparez vos ablutions.', '/', 'sdm-test-prayer', { isPrayer: true });
            } else {
                dispatchNotification('۞ Parole de Cheikh Ahmadou Bamba', '« La meilleure parure dont l\'homme puisse se parer est la bonne conduite (al-adab) partout où il passe. » — Masaalikul Jinaan', '/?tab=spirit&cid=mj_v1089', 'sdm-test-cit');
            }
        },
        checkNow: runNotificationChecks
    };

    window.addEventListener('online', updateOfflinePill);
    window.addEventListener('offline', updateOfflinePill);
    window.addEventListener('DOMContentLoaded', () => {
        updateOfflinePill();
        setTimeout(runNotificationChecks, 2200);
        setInterval(runNotificationChecks, 60000);
    });
    document.addEventListener('visibilitychange', () => {
        if (!document.hidden) runNotificationChecks();
    });
})();
